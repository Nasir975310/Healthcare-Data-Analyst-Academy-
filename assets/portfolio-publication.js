/* HDA Academy v4.0.0 — Portfolio publication suite */
(()=>{
"use strict";
const KEY="hda_portfolio_publication_v40";
const $=s=>document.querySelector(s);
const items=[
["PUBLISH-01","Confirm project question, audience and decision are explicit"],
["PUBLISH-02","Confirm dataset provenance, synthetic/public/authorised status"],
["PUBLISH-03","Document row grain, keys, joins and deduplication"],
["PUBLISH-04","Approve numerator, denominator, time window and null rules"],
["PUBLISH-05","Run project scripts from a clean environment"],
["PUBLISH-06","Run automated tests and retain test output"],
["PUBLISH-07","Reconcile dashboard metrics to source outputs"],
["PUBLISH-08","Review clinical, statistical and operational interpretation"],
["PUBLISH-09","Inspect every staged Git file for PHI, secrets and restricted data"],
["PUBLISH-10","Include README, data dictionary, metric contracts and limitations"],
["PUBLISH-11","Capture current screenshots with no sensitive information"],
["PUBLISH-12","Record reviewer, version, date and release decision"]
];
let state={checked:{},notes:"",updatedAt:null};
try{state={...state,...JSON.parse(localStorage.getItem(KEY)||"{}")}}catch(e){}
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function save(){state.updatedAt=new Date().toISOString();try{localStorage.setItem(KEY,JSON.stringify(state));const x=$("#pubSaved");if(x)x.textContent="Saved locally · "+new Date(state.updatedAt).toLocaleString()}catch(e){alert("Storage unavailable. Export the checklist backup.")}}
function exportBackup(){const blob=new Blob([JSON.stringify({module:"HDA Portfolio Publication Suite",version:"4.0.0",state},null,2)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="hda-portfolio-publication-v40-backup.json";a.click();URL.revokeObjectURL(a.href)}
function render(){
 const host=$("#portfolioPublicationApp");if(!host)return;
 const n=items.filter(x=>state.checked[x[0]]).length;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>3</b><span>Standalone dashboards</span></div><div class="upgrade-stat"><b>3</b><span>Portfolio case studies</span></div><div class="upgrade-stat"><b>${n}/${items.length}</b><span>Publication gates checked</span></div></div>
 <article class="panel module-note"><b>Dashboard previews — offline HTML</b><p>These dashboards are generated from the synthetic v3.9 reference outputs. They are static review artifacts, not live-connected Power BI reports.</p><ul>
 <li><a href="real_world_project_studio/portfolio_publication/dashboards/hospital_operations_dashboard.html" target="_blank" rel="noopener">Hospital operations dashboard</a></li>
 <li><a href="real_world_project_studio/portfolio_publication/dashboards/antihypertensive_due_dashboard.html" target="_blank" rel="noopener">Antihypertensive DUE dashboard</a></li>
 <li><a href="real_world_project_studio/portfolio_publication/dashboards/pharmacovigilance_quality_dashboard.html" target="_blank" rel="noopener">Pharmacovigilance quality dashboard</a></li></ul></article>
 <article class="panel"><h3>Portfolio case studies</h3><ul>
 <li><a href="real_world_project_studio/portfolio_publication/case_studies/01-hospital-operations.md" download>Hospital operations case study</a></li>
 <li><a href="real_world_project_studio/portfolio_publication/case_studies/02-antihypertensive-due.md" download>Antihypertensive DUE case study</a></li>
 <li><a href="real_world_project_studio/portfolio_publication/case_studies/03-pharmacovigilance-quality.md" download>Pharmacovigilance case study</a></li>
 </ul></article>
 <article class="panel"><h3>Reproducibility and automated tests</h3><pre><code>cd real_world_project_studio
python scripts/run_all.py
python portfolio_publication/scripts_dashboard_build.py
python -m unittest discover -s portfolio_publication/tests -v</code></pre><p>Expected: three reference analyses complete and six automated tests pass. Review the generated output files before publishing.</p><p><a href="real_world_project_studio/portfolio_publication/README.md" download>Publication suite README</a> · <a href="real_world_project_studio/portfolio_publication/repository_scaffold/GIT_WORKFLOW.md" download>Git workflow guide</a> · <a href="real_world_project_studio/portfolio_publication/repository_scaffold/README_TEMPLATE.md" download>Repository README template</a> · <a href="real_world_project_studio/portfolio_publication/repository_scaffold/.gitignore" download>.gitignore template</a></p></article>
 <article class="panel"><h3>Portfolio release gate</h3><p>Mark a gate only after you have retained evidence. A checked box is a self-attestation, not independent verification.</p><div class="progress-track"><i style="width:${Math.round(n/items.length*100)}%"></i></div><p class="small muted">${n} of ${items.length} checks complete</p>${items.map(([id,label])=>`<label class="check-row"><input type="checkbox" data-pub="${id}" ${state.checked[id]?"checked":""}> ${esc(label)}</label>`).join("")}<label>Reviewer notes / unresolved release risks</label><textarea id="pubNotes" rows="5" placeholder="Document exceptions, reviewer feedback and release decision">${esc(state.notes)}</textarea><p><button class="secondary-btn" id="pubExport">Export checklist backup</button> <button class="secondary-btn" id="pubImportBtn">Import checklist backup</button> <input id="pubImport" type="file" accept="application/json" hidden></p><small id="pubSaved">Progress is stored locally in this browser.</small></article>
 <article class="panel"><h3>Publishing boundary</h3><p>Use synthetic, public, or explicitly authorised data only. Do not publish patient-level data, PHI, credentials, API tokens, confidential employer extracts, or screenshots containing sensitive information. A public GitHub repository is not an approved clinical-data environment.</p><p>For Power BI Desktop work, use Windows. On Linux, use the supplied static HTML/Streamlit alternatives; they are not feature-equivalent to Power BI Desktop.</p></article>`;
 host.querySelectorAll("[data-pub]").forEach(x=>x.addEventListener("change",()=>{state.checked[x.dataset.pub]=x.checked;save();render()}));
 $("#pubNotes").addEventListener("change",e=>{state.notes=e.target.value;save()});
 $("#pubExport").addEventListener("click",exportBackup);
 $("#pubImportBtn").addEventListener("click",()=>$("#pubImport").click());
 $("#pubImport").addEventListener("change",async e=>{const f=e.target.files[0];if(!f)return;try{const d=JSON.parse(await f.text());if(d.module!=="HDA Portfolio Publication Suite"||d.version!=="4.0.0"||!d.state)throw Error("Not a v4.0 publication-suite backup");state={...state,...d.state};save();render()}catch(err){alert("Import failed: "+err.message)}e.target.value=""});
}
document.querySelector('.nav-item[data-view="portfolio-publication"]')?.addEventListener("click",()=>setTimeout(render,30));
if(document.getElementById("view-portfolio-publication"))render();
})();
