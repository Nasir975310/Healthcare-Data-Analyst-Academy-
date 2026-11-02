#!/usr/bin/env python3
"""Generate a descriptive healthcare analytics report from a CSV file."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True); ap.add_argument("--output-dir",default="output")
    ap.add_argument("--title",default="Healthcare analytics descriptive report")
    ap.add_argument("--report-type",default="Operational analytics")
    ap.add_argument("--analyst",default=""); ap.add_argument("--period",default="Not specified")
    ap.add_argument("--purpose",default="Descriptive review of the supplied dataset.")
    a=ap.parse_args(); src=Path(a.input); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(src); df.columns=[str(c).strip() for c in df.columns]
    missing=df.isna().sum()+df.astype(str).apply(lambda s:s.str.strip().eq("").sum())
    numeric=df.select_dtypes(include="number")
    digest=hashlib.sha256(src.read_bytes()).hexdigest()
    profile=[("Rows",len(df)),("Columns",len(df.columns)),("Duplicate rows",int(df.duplicated().sum())),
             ("Distinct patient tokens",int(df["patient_id"].nunique()) if "patient_id" in df else "Not available")]
    stats=[]
    for c in numeric.columns:
        s=pd.to_numeric(df[c],errors="coerce").dropna()
        stats.append((c,len(s),round(float(s.mean()),3) if len(s) else "NA",
                      round(float(s.median()),3) if len(s) else "NA"))
    quality=[(c,int(missing[c]),round(float(missing[c]/max(len(df),1)*100),2)) for c in df.columns]
    doc=Document(); sec=doc.sections[0]; sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.65)
    doc.add_heading(a.title,0); doc.add_paragraph(f"{a.report_type} | Reporting period: {a.period}")
    doc.add_paragraph(f"Analyst: {a.analyst or 'Not specified'}")
    doc.add_heading("Executive summary",1)
    doc.add_paragraph(f"The supplied file contains {len(df):,} parsed records across {len(df.columns)} fields. "
                      f"There are {int(df.duplicated().sum()):,} fully duplicated rows. "
                      "Findings below are descriptive and depend on the supplied extract.")
    doc.add_paragraph(a.purpose)
    doc.add_heading("Methods and dataset profile",1)
    doc.add_paragraph("Unit of analysis: one CSV row; confirm this matches the intended encounter/patient/event grain.")
    doc.add_paragraph("Method: CSV ingestion with pandas; column-level missingness, duplicate-row count and numeric descriptive statistics.")
    t=doc.add_table(rows=1,cols=2); t.style="Light Shading Accent 1"
    t.rows[0].cells[0].text="Profile measure"; t.rows[0].cells[1].text="Value"
    for k,v in profile:
        cells=t.add_row().cells; cells[0].text=str(k); cells[1].text=str(v)
    doc.add_heading("Numeric descriptive statistics",1)
    t=doc.add_table(rows=1,cols=4); t.style="Light Shading Accent 1"
    for cell,val in zip(t.rows[0].cells,["Field","Valid n","Mean","Median"]): cell.text=val
    for row in stats:
        for cell,val in zip(t.add_row().cells,map(str,row)): cell.text=val
    doc.add_heading("Data quality",1)
    t=doc.add_table(rows=1,cols=3); t.style="Light Shading Accent 1"
    for cell,val in zip(t.rows[0].cells,["Field","Missing","Missing %"]): cell.text=val
    for row in quality:
        for cell,val in zip(t.add_row().cells,map(str,row)): cell.text=val
    doc.add_heading("Limitations and interpretation",1)
    limitations=["No causal inference or clinical validation is performed.",
      "Missingness and invalid values may bias summaries; numeric means use parseable values only.",
      "The row grain, inclusion criteria, data provenance and reporting period require owner confirmation.",
      "Small-cell disclosure risk and local privacy requirements must be assessed before sharing.",
      "Synthetic example data must never be represented as actual hospital performance."]
    for x in limitations: doc.add_paragraph(x,style="List Bullet")
    doc.add_heading("Reproducibility",1)
    doc.add_paragraph(f"Source file: {src.name}\nSHA-256: {digest}\nPandas: {pd.__version__}")
    docx=out/"healthcare_analytics_report.docx"; doc.save(docx)
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name="Small",parent=styles["BodyText"],fontSize=8,leading=10))
    story=[Paragraph(a.title,styles["Title"]),Paragraph(f"{a.report_type} | Period: {a.period}",styles["Heading2"]),
           Paragraph(f"Analyst: {a.analyst or 'Not specified'}",styles["BodyText"]),Spacer(1,5*mm),
           Paragraph("Executive summary",styles["Heading1"]),
           Paragraph(f"The supplied file contains {len(df):,} parsed records across {len(df.columns)} fields, with {int(df.duplicated().sum()):,} fully duplicated rows. Findings are descriptive and depend on the supplied extract.",styles["BodyText"]),
           Paragraph(a.purpose,styles["BodyText"]),Paragraph("Methods and dataset profile",styles["Heading1"]),
           Paragraph("Unit of analysis: one CSV row; confirm it matches the intended grain. Method: pandas CSV ingestion, duplicate-row count, column missingness and numeric descriptive statistics.",styles["BodyText"])]
    def pdf_table(data,widths=None):
        tb=Table(data,colWidths=widths,repeatRows=1); tb.setStyle(TableStyle([
          ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#dce8f2")),("GRID",(0,0),(-1,-1),.35,colors.grey),
          ("FONTSIZE",(0,0),(-1,-1),7),("VALIGN",(0,0),(-1,-1),"TOP"),("PADDING",(0,0),(-1,-1),4)])); return tb
    story += [pdf_table([["Measure","Value"]]+[[str(k),str(v)] for k,v in profile]),Paragraph("Numeric descriptive statistics",styles["Heading1"]),
      pdf_table([["Field","Valid n","Mean","Median"]]+[[str(x) for x in r] for r in stats]),
      Paragraph("Data quality — missingness",styles["Heading1"]),
      pdf_table([["Field","Missing","Missing %"]]+[[str(x) for x in r] for r in quality]),
      Paragraph("Limitations and interpretation",styles["Heading1"])]
    story += [Paragraph("• "+x,styles["Small"]) for x in limitations]
    story += [Paragraph("Reproducibility",styles["Heading1"]),Paragraph(f"Source: {src.name}<br/>SHA-256: {digest}<br/>Pandas: {pd.__version__}",styles["Small"])]
    pdf=out/"healthcare_analytics_report.pdf"; SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=15*mm,leftMargin=15*mm).build(story)
    manifest={"input":str(src),"sha256":digest,"rows":len(df),"columns":len(df.columns),"duplicate_rows":int(df.duplicated().sum()),
              "docx":str(docx),"pdf":str(pdf),"numeric_fields":list(numeric.columns)}
    (out/"report_manifest.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
