#!/usr/bin/env python3
"""Configurable, deterministic CSV data-quality validator. Standard library only."""
from pathlib import Path
import argparse, csv, json, html, hashlib, datetime as dt, re, sys
ROOT=Path(__file__).resolve().parents[1]
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(65536),b''): h.update(chunk)
    return h.hexdigest()
def validate(input_path, rules_path, output_dir, dictionary_path=None):
    rules=json.loads(rules_path.read_text(encoding='utf-8'))
    dictionary=json.loads(dictionary_path.read_text(encoding='utf-8')) if dictionary_path else {"variables":[]}
    output_dir.mkdir(parents=True,exist_ok=True)
    issues=[]; row_count=0; missing_cells=0; checked_cells=0
    def add(row, column, code, severity, message, value=""):
        issues.append({"source_row":row,"column":column,"rule_id":code,"severity":severity,"message":message,"observed_value":value})
    with input_path.open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        headers=reader.fieldnames or []
        if not headers: raise ValueError("Input CSV has no header row.")
        for col in rules.get('required_columns',[]):
            if col not in headers: add(1,col,"missing_column","error",f"Required column '{col}' is absent.")
        for col in rules.get('unique_columns',[]):
            if col not in headers: add(1,col,"missing_unique_column","error",f"Unique-key column '{col}' is absent.")
        seen={c:set() for c in rules.get('unique_columns',[]) if c in headers}
        for row_num,row in enumerate(reader,2):
            row_count+=1
            for col in headers:
                value=(row.get(col) or "").strip(); checked_cells+=1
                if value=="": missing_cells+=1
            for col in rules.get('required_columns',[]):
                if col in headers and not (row.get(col) or "").strip():
                    add(row_num,col,"missing_required","error","Required value is blank.")
            for col,values in seen.items():
                value=(row.get(col) or "").strip()
                if value:
                    if value in values: add(row_num,col,"duplicate_key","error","Duplicate value in configured unique column.",value)
                    values.add(value)
            for col,bounds in rules.get('numeric_ranges',{}).items():
                if col not in headers: continue
                raw=(row.get(col) or "").strip()
                if not raw: continue
                try: number=float(raw)
                except ValueError: add(row_num,col,"invalid_type","error","Expected a numeric value.",raw); continue
                if bounds.get('min') is not None and number<float(bounds['min']):
                    add(row_num,col,"out_of_range","warning",f"Value is below configured minimum {bounds['min']}.",raw)
                if bounds.get('max') is not None and number>float(bounds['max']):
                    add(row_num,col,"out_of_range","warning",f"Value is above configured maximum {bounds['max']}.",raw)
            for col,allowed in rules.get('categorical_values',{}).items():
                if col not in headers: continue
                raw=(row.get(col) or "").strip()
                if raw and raw not in [str(x) for x in allowed]:
                    add(row_num,col,"unknown_category","error","Value is not in configured allowed-values list.",raw)
            for col in rules.get('date_columns',[]):
                if col not in headers: continue
                raw=(row.get(col) or "").strip()
                if raw:
                    try: dt.date.fromisoformat(raw)
                    except ValueError: add(row_num,col,"invalid_date","error","Expected an ISO 8601 date (YYYY-MM-DD).",raw)
            for rule in rules.get('temporal_rules',[]):
                a,b=rule['start_column'],rule['end_column']
                if a in headers and b in headers and row.get(a) and row.get(b):
                    try:
                        start=dt.date.fromisoformat(row[a]); end=dt.date.fromisoformat(row[b])
                        if rule['rule']=='end_on_or_after_start' and end<start:
                            add(row_num,b,rule['id'],rule.get('severity','error'),rule['message'],row[b])
                    except ValueError: pass
            for rule in rules.get('cross_field_rules',[]):
                cols=rule.get('when_columns',[])
                if all(c in headers and (row.get(c) or '').strip() for c in cols):
                    if rule['rule']=='diastolic_lte_systolic':
                        try:
                            if float(row['diastolic_bp_mmhg'])>float(row['systolic_bp_mmhg']):
                                add(row_num,','.join(cols),rule['id'],rule.get('severity','warning'),rule['message'],f"{row['systolic_bp_mmhg']}/{row['diastolic_bp_mmhg']}")
                        except ValueError: pass
    # Aggregate completeness and severity.
    error_count=sum(i['severity']=='error' for i in issues)
    warning_count=sum(i['severity']=='warning' for i in issues)
    report={"status":"PASS" if error_count==0 else "FAIL","input_file":input_path.name,
      "input_sha256":digest(input_path),"rules_file":rules_path.name,
      "dictionary_version":dictionary.get('version'),"rows_checked":row_count,
      "columns_checked":len(headers),"cells_checked":checked_cells,"blank_cells":missing_cells,
      "completeness_pct":round(100*(checked_cells-missing_cells)/checked_cells,2) if checked_cells else 100.0,
      "error_count":error_count,"warning_count":warning_count,"issue_count":len(issues),
      "issues_by_rule":{},"issues_by_severity":{},"issues":issues}
    for issue in issues:
        report['issues_by_rule'][issue['rule_id']]=report['issues_by_rule'].get(issue['rule_id'],0)+1
        report['issues_by_severity'][issue['severity']]=report['issues_by_severity'].get(issue['severity'],0)+1
    (output_dir/'validation_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    with (output_dir/'issues.csv').open('w',newline='',encoding='utf-8') as f:
        fields=['source_row','column','rule_id','severity','message','observed_value']
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(issues)
    rows=''.join(f"<tr><td>{html.escape(str(i['source_row']))}</td><td>{html.escape(i['column'])}</td><td>{html.escape(i['rule_id'])}</td><td>{html.escape(i['severity'])}</td><td>{html.escape(i['message'])}</td></tr>" for i in issues)
    page=f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Data validation report</title><body><h1>Dataset validation report</h1><p>Status: <b>{report['status']}</b></p><p>Rows: {row_count} · Completeness: {report['completeness_pct']}% · Errors: {error_count} · Warnings: {warning_count}</p><p>Source SHA-256: <code>{report['input_sha256']}</code></p><table border="1" cellpadding="6"><thead><tr><th>Row</th><th>Column</th><th>Rule</th><th>Severity</th><th>Finding</th></tr></thead><tbody>{rows}</tbody></table></body></html>"""
    (output_dir/'quality_report.html').write_text(page,encoding='utf-8')
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,default=ROOT/'data/synthetic_study.csv')
    p.add_argument('--rules',type=Path,default=ROOT/'config/validation_rules.json')
    p.add_argument('--dictionary',type=Path,default=ROOT/'dictionary/core_variables.json')
    p.add_argument('--output-dir',type=Path,default=ROOT/'output')
    a=p.parse_args(); result=validate(a.input,a.rules,a.output_dir,a.dictionary)
    print(json.dumps({k:v for k,v in result.items() if k!='issues'},indent=2))
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__': sys.exit(main())
