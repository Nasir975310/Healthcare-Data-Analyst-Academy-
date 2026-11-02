/* v5.1 Interactive client project simulator */
(()=>{
"use strict";
const host=document.getElementById("projectSimulatorV51");if(!host)return;
const KEY="hda_project_simulator_v51";
const steps=[
{id:"scope",title:"1 · Clarify the request",client:"Operations Manager: “Can you rank departments by encounter volume and average LOS?”",question:"What do you clarify before analysis?",choices:[
["grain","Confirm encounter grain, period, LOS definition, and whether Emergency is included.",10,"Correct: establish grain, period, numerator/denominator and metric definition before querying."],
["chart","Start building a bar chart from the raw CSV.",0,"Premature: the metric contract and data quality are not yet understood."],
["guess","Assume one row per patient and use average date difference.",0,"Incorrect: the stated grain is encounter; patients may have multiple encounters."]
]},
{id:"quality",title:"2 · Respond to quality escalation",client:"Data steward: “There are duplicate encounter IDs, missing departments, missing patient IDs, invalid dates and implausible SBP values.”",question:"What is the safest response?",choices:[
["quarantine","Preserve raw data; profile row-level overlap; quarantine invalid records with reason codes; reconcile totals.",10,"Correct: preserve lineage, avoid silent repairs, and make exclusions auditable."],
["drop","Drop duplicates and rows with missing values without an audit trail.",0,"Unsafe: silently changes denominators and destroys traceability."],
["impute","Fill missing departments from the most common department.",0,"Unsupported imputation: a department cannot be inferred from its mode."]
]},
{id:"metric",title:"3 · Apply the revised metric contract",client:"Operations Manager: “Exclude Emergency from the department comparison, but keep it in the hospital total. Average LOS should use discharged encounters only.”",question:"How do you implement this?",choices:[
["separate","Keep Emergency in overall totals; filter it only from department comparison; calculate LOS among discharged encounters.",10,"Correct: apply the exclusion only to the metric/view it governs and use the stated LOS cohort."],
["global","Remove Emergency from the entire dataset and all metrics.",0,"Incorrect: the client explicitly retains Emergency in the overall hospital total."],
["alllos","Calculate LOS for every disposition.",0,"Incorrect: the revised contract specifies discharged encounters only."]
]},
{id:"sbp",title:"4 · Interpret SBP completeness",client:"Clinical lead: “Can we call the department with the highest SBP completeness the best-performing department?”",question:"What do you tell the client?",choices:[
["caution","No. Completeness measures recordedness, not BP control, treatment appropriateness or quality; show denominator and missingness.",10,"Correct: distinguish data completeness from clinical performance."],
["yes","Yes. Higher completeness means better hypertension care.",0,"Unsupported: completeness is not a clinical outcome or quality measure."],
["omit","Remove SBP completeness because it may be misunderstood.",2,"Partly cautious, but a clearly defined completeness metric can still be useful."]
]},
{id:"handoff",title:"5 · Prepare the handoff",client:"The client requests reproducible scripts, SQL summaries, a QA log, limitations and a concise note.",question:"Which delivery is complete?",choices:[
["repro","Versioned raw/accepted/quarantine files, executable script, SQL, QA reconciliation, metric definitions, limitations and client summary.",10,"Correct: reproducibility, lineage, metric contract and communication are all present."],
["pdf","Send only a PDF with charts and no code or QA evidence.",1,"Incomplete: not reproducible and no audit trail."],
["numbers","Send headline numbers without denominators or exclusions.",0,"Not acceptable: conclusions cannot be interpreted or reproduced."]
]}
];
let state={answers:{},notes:"",evidence:"",revealed:false};
try{state={...state,...JSON.parse(localStorage.getItem(KEY)||"{}")}}catch(e){}
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const score=steps.reduce((n,s)=>n+(s.choices.find(c=>c[0]===state.answers[s.id])?.[1]||0),0);
const save=()=>localStorage.setItem(KEY,JSON.stringify(state));
function render(){
host.innerHTML=`<div class="metric-grid"><div class="metric"><b>${score}/50</b><span>Decision score</span></div><div class="metric"><b>${Object.keys(state.answers).length}/5</b><span>Decisions recorded</span></div><div class="metric"><b>${Math.round(score/50*100)}%</b><span>Current attainment</span></div></div>
<article class="panel"><h3>Client engagement brief</h3><p>Act as the analyst for a simulated hospital operations team. The project begins with an ambiguous request and evolves through client messages. Your choices are scored against safe analytical practice.</p><p><a href="project_simulator_v51/project_brief.md" target="_blank">Open full project brief</a> · <a href="project_simulator_v51/guides/client_communications.md" target="_blank">Client communication guide</a></p><p><b>Execution files:</b> <code>project_simulator_v51/data/encounters_raw.csv</code>, <code>project_simulator_v51/scripts/run_engagement.py</code>, <code>project_simulator_v51/sql/engagement_queries.sql</code>.</p></article>
${steps.map(s=>{const chosen=s.choices.find(c=>c[0]===state.answers[s.id]);return `<article class="panel"><div class="eyebrow">CLIENT MESSAGE</div><h3>${s.title}</h3><blockquote>${esc(s.client)}</blockquote><p><b>${s.question}</b></p>${s.choices.map(c=>`<label class="er-service"><input type="radio" name="${s.id}" value="${c[0]}" ${state.answers[s.id]===c[0]?"checked":""}><span>${esc(c[0]==="scope"?"":c[0])}</span> ${esc(c[0]=== "grain"?"Confirm encounter grain, period, LOS definition, and Emergency handling.":c[0]==="chart"?"Build a chart immediately from raw counts.":c[0]==="guess"?"Assume one row per patient.":c[0]==="quarantine"?"Preserve raw data, profile issues and quarantine invalid records with reason codes.":c[0]==="drop"?"Drop duplicates and missing values silently.":c[0]==="impute"?"Fill missing departments with the most common department.":c[0]==="separate"?"Keep Emergency in overall totals; exclude it only from department comparison; use discharged-only LOS.":c[0]==="global"?"Remove Emergency from all metrics.":c[0]==="alllos"?"Calculate LOS for every disposition.":c[0]==="caution"?"Explain completeness is not clinical quality; show denominator and missingness.":c[0]==="yes"?"Treat higher completeness as better hypertension care.":c[0]==="omit"?"Remove the metric entirely.":c[0]==="repro"?"Deliver versioned data, executable code, SQL, QA, definitions, limitations and client summary.":c[0]==="pdf"?"Send only a PDF with charts.":"Send headline numbers without denominators.")}</label>`).join("")}
${chosen?`<p><b>Score:</b> ${chosen[1]}/10 ${state.revealed?`— ${esc(chosen[2])}`:"— feedback available after reveal"}</p>`:"<p class='muted'>Select one decision.</p>"}</article>`}).join("")}
<article class="panel"><h3>Run the real project locally</h3><p>Run the script to create accepted and quarantined data, a row-level QA audit, KPI CSVs and a JSON summary. Browser decisions do not execute the Python/SQL files.</p><pre><code>python -m pip install pandas
python project_simulator_v51/scripts/run_engagement.py</code></pre><p>Windows PowerShell: use the same commands with <code>py</code> instead of <code>python</code> if required. SQL instructions are in the project README.</p><label>Evidence path and actual run results</label><textarea id="v51Evidence" rows="3">${esc(state.evidence)}</textarea><label>Client note / reflection</label><textarea id="v51Notes" rows="4">${esc(state.notes)}</textarea><button id="v51Reveal">Reveal decision feedback</button> <button class="secondary-small" id="v51Export">Export project report</button> <button class="secondary-small" id="v51Backup">Export JSON backup</button></article>
<article class="panel"><h3>Final delivery checklist</h3><ul><li>Raw data preserved and row-level QA reasons supplied.</li><li>Raw = accepted + quarantined reconciliation verified.</li><li>Department comparison excludes Emergency, overall totals retain it.</li><li>Average LOS uses discharged encounters only.</li><li>SBP completeness is not represented as clinical quality.</li><li>SQL/Python execution evidence and limitations are documented.</li></ul><p class="muted">This is synthetic project practice, not an employer credential or clinical decision-support system.</p></article>`;
steps.forEach(s=>host.querySelectorAll(`input[name="${s.id}"]`).forEach(el=>el.addEventListener("change",()=>{state.answers[s.id]=el.value;state.revealed=false;save();render()})));
host.querySelector("#v51Evidence").addEventListener("input",e=>{state.evidence=e.target.value;save()});
host.querySelector("#v51Notes").addEventListener("input",e=>{state.notes=e.target.value;save()});
host.querySelector("#v51Reveal").addEventListener("click",()=>{state.revealed=true;save();render()});
host.querySelector("#v51Export").addEventListener("click",()=>{let md="# Hospital Operations Project Simulation\\n\\nDecision score: "+score+"/50\\n\\n";steps.forEach(s=>{const c=s.choices.find(x=>x[0]===state.answers[s.id]);md+="## "+s.title+"\\nChoice: "+(c?c[0]:"Not answered")+"\\nScore: "+(c?c[1]:0)+"/10\\nFeedback: "+(c?c[2]:"Not attempted")+"\\n\\n"});md+="## Evidence\\n"+state.evidence+"\\n\\n## Client note\\n"+state.notes;download("hda_v51_project_report.md",md,"text/markdown")});
host.querySelector("#v51Backup").addEventListener("click",()=>download("hda_v51_backup.json",JSON.stringify(state,null,2),"application/json"));
}
function download(n,d,t){const u=URL.createObjectURL(new Blob([d],{type:t})),a=document.createElement("a");a.href=u;a.download=n;a.click();URL.revokeObjectURL(u)}
render();
})();