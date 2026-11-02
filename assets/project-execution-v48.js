/* v4.8 Practical Project Execution Engine */
(()=>{
"use strict";
const host=document.getElementById("projectV48App");if(!host)return;
const KEY="hda_project_execution_v48";
const steps=[
["Inspect the source dataset","Confirm row count, columns, grain, primary key and synthetic-data status.","data/raw/synthetic_hospital_encounters.csv"],
["Profile the raw data","Run the pipeline and inspect missingness, duplicates and distributions.","data/processed/quality_report.json"],
["Review quarantined records","Inspect every issue flag and confirm invalid records are excluded transparently.","data/quarantine/quarantined_encounters.csv"],
["Validate cleaning and reconciliation","Check raw = accepted + quarantined and verify unique encounter IDs.","data/processed/clean_encounters.csv"],
["Load and inspect SQLite","Open the database in DBeaver and confirm row count and schema.","data/processed/hospital_analytics.sqlite"],
["Perform SQL analysis","Run department, disposition, age-band and reconciliation queries.","sql/analysis_queries.sql"],
["Interpret statistics responsibly","Explain denominators, missingness and descriptive-only limitations.","reports/project_report.md"],
["Review visual output","Check labels, units, ordering and whether chart matches SQL output.","reports/department_encounters.png"],
["Run automated tests","Execute pytest and resolve failures before packaging.","tests/test_pipeline.py"],
["Build portfolio case study","Complete the case-study template with reproducible commands and limitations.","templates/case_study_template.md"]
];
let state={completed:{},evidence:{},notes:"",started:false};
try{state={...state,...JSON.parse(localStorage.getItem(KEY)||"{}")}}catch(e){}
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const save=()=>localStorage.setItem(KEY,JSON.stringify(state));
function render(){
const count=steps.filter((x,i)=>state.completed[i]).length;
host.innerHTML=`<div class="metric-grid"><div class="metric"><b>${count}/10</b><span>Project stages completed</span></div><div class="metric"><b>${Math.round(count*10)}%</b><span>Self-reported workflow progress</span></div><div class="metric"><b>241</b><span>Raw synthetic rows</span></div></div>
<article class="panel"><h3>Project brief: Hospital Encounter Data Quality and Operations</h3><p><b>Business question:</b> Can we create a defensible descriptive summary of encounter volume and length of stay after identifying and isolating data-quality defects?</p><p><b>Dataset grain:</b> one row per encounter. Primary key: <code>encounter_id</code>. The dataset contains deliberately planted errors.</p><p><b>Expected outcome:</b> reproducible Python pipeline, quarantine file, SQLite database, SQL summaries, report, chart and portfolio case study.</p><p class="muted">All data is synthetic. This is not a real hospital performance assessment or clinical evidence.</p><p><a href="project_execution_v48/README.md" target="_blank">Project README</a> · <a href="project_execution_v48/guides/project_workflow.md" target="_blank">Workflow guide</a> · <a href="project_execution_v48/data/raw/synthetic_hospital_encounters.csv" target="_blank">Raw dataset</a></p></article>
<article class="panel"><h3>Ten-stage execution checklist</h3>${steps.map((x,i)=>`<div class="er-service"><label><input type="checkbox" data-step="${i}" ${state.completed[i]?"checked":""}><b>${i+1}. ${esc(x[0])}</b></label><p>${esc(x[1])}</p><p><a href="project_execution_v48/${x[2]}" target="_blank">Open expected artefact / instruction</a></p><label>Evidence path or result<input data-evidence="${i}" value="${esc(state.evidence[i]||"")}" placeholder="Record file path, test result or observation"></label></div>`).join("")}</article>
<article class="panel"><h3>Run the project on your computer</h3><p>From the <code>project_execution_v48</code> directory, activate your v4.7 Python environment (or install the requirements) and run:</p><pre><code>python -m pip install -r requirements.txt
python run_project.py
python -m pytest -q</code></pre><p>Open <code>data/processed/hospital_analytics.sqlite</code> in DBeaver and execute <a href="project_execution_v48/sql/analysis_queries.sql" target="_blank">analysis_queries.sql</a>.</p><p class="muted">The browser does not run these commands or verify local files. Record results only after you execute them.</p></article>
<article class="panel"><h3>Analysis notes and evidence review</h3><label>Interpretation, issues found, validation results and limitations<textarea id="p48Notes" rows="5">${esc(state.notes)}</textarea></label><div class="button-row"><button id="p48Report">Export project progress report</button><button id="p48Backup" class="secondary-small">Export JSON backup</button><label class="secondary-small file-button">Import backup<input type="file" id="p48Import" accept="application/json"></label></div><p class="muted">Progress and notes are saved in this browser only. The report is a record of your entries, not independent validation.</p></article>`;
host.querySelectorAll("[data-step]").forEach(el=>el.onchange=()=>{state.completed[el.dataset.step]=el.checked;save();render()});
host.querySelectorAll("[data-evidence]").forEach(el=>el.onchange=()=>{state.evidence[el.dataset.evidence]=el.value;save()});
host.querySelector("#p48Notes").onchange=e=>{state.notes=e.target.value;save()};
host.querySelector("#p48Report").onclick=()=>{const body=["# Project Execution Record","",`Exported: ${new Date().toISOString()}`,"",...steps.map((x,i)=>`## ${i+1}. ${x[0]}\nStatus: ${state.completed[i]?"Completed (self-reported)":"Not completed"}\nEvidence: ${state.evidence[i]||"Not recorded"}\nExpected artefact: ${x[2]}`),"## Notes",state.notes,"","All data is synthetic. Completion is self-reported and not independently verified."].join("\n");download("healthcare-project-execution-record.md",body,"text/markdown")};
host.querySelector("#p48Backup").onclick=()=>download("hda-project-v48-backup.json",JSON.stringify({product:"HDA Project Execution v48",state},null,2),"application/json");
host.querySelector("#p48Import").onchange=async e=>{try{const f=e.target.files[0];if(!f)return;const x=JSON.parse(await f.text());if(x.product!=="HDA Project Execution v48")throw Error("Unsupported backup");state={...state,...x.state};save();render()}catch(err){alert("Import failed: "+err.message)}};
}
function download(name,content,type){const a=document.createElement("a"),u=URL.createObjectURL(new Blob([content],{type}));a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)}
document.addEventListener("click",e=>{if(e.target.closest('[data-view="project-v48"]'))setTimeout(render,0)});
render();
})();