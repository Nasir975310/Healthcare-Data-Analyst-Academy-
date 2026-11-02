/* v4.9 Portfolio Builder and Publication Quality Gate */
(()=>{
"use strict";
const host=document.getElementById("portfolioV49App");if(!host)return;
const KEY="hda_portfolio_builder_v49";
const gates=[
"Dataset is synthetic or explicitly authorised for public release",
"No PHI, credentials, .env files or confidential client notes",
"README describes the actual work and limitations",
"Data dictionary and metric contract reviewed",
"Raw = accepted + quarantined reconciliation checked",
"Primary-key uniqueness tested",
"SQL totals reconcile to cleaned data",
"Project runs from a clean environment",
"Automated tests pass and actual results recorded",
"Charts have labels, units and denominators",
"No unsupported causal, clinical, financial or compliance claims",
"CV statements link to inspectable evidence",
"Git staged diff reviewed before publishing",
"Public repository visibility deliberately approved"
];
let state={checks:{},role:"Healthcare Data Analyst",action:"Built",tool:"Python, pandas and SQLite",scale:"241 synthetic encounter rows",method:"rule-based validation, quarantine and SQL reconciliation",output:"reproducible report, database and visualisation",evidence:"project_execution_v48/",notes:""};
try{state={...state,...JSON.parse(localStorage.getItem(KEY)||"{}")}}catch(e){}
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const save=()=>localStorage.setItem(KEY,JSON.stringify(state));
function render(){
const n=gates.filter((x,i)=>state.checks[i]).length;
const bullet=`${state.action} a healthcare analytics project using ${state.tool} on ${state.scale}, applying ${state.method}; produced ${state.output}. Evidence: ${state.evidence}`;
host.innerHTML=`<div class="metric-grid"><div class="metric"><b>${n}/14</b><span>Publication quality checks</span></div><div class="metric"><b>${Math.round(n/14*100)}%</b><span>Self-reported readiness</span></div><div class="metric"><b>7</b><span>Data dictionary fields</span></div></div>
<article class="panel"><h3>1. Generate the portfolio pack</h3><p>Run this from <code>portfolio_builder_v49</code> after running the v4.8 project:</p><pre><code>python scripts/build_portfolio_pack.py --project ../project_execution_v48 --output output</code></pre><p>The generator creates a README draft, data dictionary, metric contract, QA/reproducibility summary, evidence inventory, evidence manifest with SHA-256 hashes, CV worksheet, interview questions and publication checklist.</p><p><a href="portfolio_builder_v49/README.md" target="_blank">Portfolio builder guide</a> · <a href="portfolio_builder_v49/guides/github_publication.md" target="_blank">GitHub publication workflow</a> · <a href="portfolio_builder_v49/output/README_draft.md" target="_blank">Generated README draft</a> · <a href="portfolio_builder_v49/output/qa_reproducibility.md" target="_blank">Generated QA summary</a></p><p class="muted">Generated drafts require human review. The generator reads project evidence; it does not prove employer impact or publish a repository.</p></article>
<article class="panel"><h3>2. Portfolio publication quality gate</h3>${gates.map((x,i)=>`<div class="er-service"><label><input type="checkbox" data-gate="${i}" ${state.checks[i]?"checked":""}><b>${esc(x)}</b></label></div>`).join("")}<p class="muted">A checked item is your attestation, not an automated audit. Do not publish until all relevant checks are genuinely complete.</p></article>
<article class="panel"><h3>3. Evidence-backed CV bullet builder</h3><div class="grid-2"><label>Target role<input id="p49Role" value="${esc(state.role)}"></label><label>Action verb<input id="p49Action" value="${esc(state.action)}"></label><label>Verified tools<input id="p49Tool" value="${esc(state.tool)}"></label><label>Dataset scale<input id="p49Scale" value="${esc(state.scale)}"></label><label>Methods<input id="p49Method" value="${esc(state.method)}"></label><label>Deliverable<input id="p49Output" value="${esc(state.output)}"></label></div><label>Evidence path / commit<input id="p49Evidence" value="${esc(state.evidence)}"></label><p><b>Draft bullet — verify every phrase before using:</b></p><blockquote>${esc(bullet)}</blockquote><button id="p49Copy">Copy draft bullet</button><p class="muted">Do not claim paid client work, production deployment, savings, clinical improvement or compliance unless separately verified.</p></article>
<article class="panel"><h3>4. Interview preparation</h3><p><a href="portfolio_builder_v49/output/interview_questions.md" target="_blank">Open project-based interview questions</a> · <a href="portfolio_builder_v49/templates/case_study_template.md" target="_blank">Case study template</a> · <a href="portfolio_builder_v49/templates/cv_evidence_worksheet.md" target="_blank">CV evidence worksheet</a></p><label>Practice notes<textarea id="p49Notes" rows="4">${esc(state.notes)}</textarea></label><div class="button-row"><button id="p49Report">Export portfolio readiness report</button><button id="p49Backup" class="secondary-small">Export JSON backup</button><label class="secondary-small file-button">Import backup<input type="file" id="p49Import" accept="application/json"></label></div></article>`;
host.querySelectorAll("[data-gate]").forEach(el=>el.onchange=()=>{state.checks[el.dataset.gate]=el.checked;save();render()});
const fields={p49Role:"role",p49Action:"action",p49Tool:"tool",p49Scale:"scale",p49Method:"method",p49Output:"output",p49Evidence:"evidence",p49Notes:"notes"};
Object.entries(fields).forEach(([id,key])=>host.querySelector("#"+id).onchange=e=>{state[key]=e.target.value;save()});
host.querySelector("#p49Copy").onclick=()=>{const t=`${state.action} a healthcare analytics project using ${state.tool} on ${state.scale}, applying ${state.method}; produced ${state.output}. Evidence: ${state.evidence}`;if(navigator.clipboard?.writeText)navigator.clipboard.writeText(t);else alert(t)};
host.querySelector("#p49Report").onclick=()=>{const lines=["# Portfolio Publication Readiness",`Target role: ${state.role}`,`Self-reported gate: ${n}/14`,"",...gates.map((x,i)=>`- [${state.checks[i]?"x":" "}] ${x}`),"","## Draft CV bullet",bullet,"","## Notes",state.notes,"","This report is self-reported and does not certify skills, employment or publication safety."].join("\n");download("portfolio-readiness-v49.md",lines,"text/markdown")};
host.querySelector("#p49Backup").onclick=()=>download("hda-portfolio-v49-backup.json",JSON.stringify({product:"HDA Portfolio Builder v49",state},null,2),"application/json");
host.querySelector("#p49Import").onchange=async e=>{try{const f=e.target.files[0];if(!f)return;const x=JSON.parse(await f.text());if(x.product!=="HDA Portfolio Builder v49")throw Error("Unsupported backup");state={...state,...x.state};save();render()}catch(err){alert("Import failed: "+err.message)}};
}
function download(name,content,type){const a=document.createElement("a"),u=URL.createObjectURL(new Blob([content],{type}));a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)}
document.addEventListener("click",e=>{if(e.target.closest('[data-view="portfolio-v49"]'))setTimeout(render,0)});
render();
})();