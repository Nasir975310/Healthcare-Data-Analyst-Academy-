/* HDA Academy v2.4.0 — ETL mastery */
(()=>{
"use strict";
const STORE="hda-etl-mastery-v240";
const host=document.getElementById("etlMasteryApp");
if(!host)return;
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let challenges=[],state={done:[],query:""};
const read=()=>{try{state={...state,...JSON.parse(localStorage.getItem(STORE)||"{}")}}catch(e){}};
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(state));}catch(e){}};
function render(){
 const done=new Set(state.done||[]);
 const filtered=challenges.filter(c=>(c.id+" "+c.title+" "+c.scenario+" "+c.level).toLowerCase().includes((state.query||"").toLowerCase()));
 host.innerHTML=`
 <div class="etl-mastery-summary">
  <div><b>${challenges.length}</b><span>Progressive challenges</span></div>
  <div><b>${done.size}/${challenges.length}</b><span>Completed on this device</span></div>
  <div><b>${Math.round(done.size/Math.max(1,challenges.length)*100)}%</b><span>Completion progress</span></div>
  <div><b>90 min</b><span>Timed end-to-end assignment</span></div>
 </div>
 <div class="etl-note"><b>Practical assets</b><div class="etl-links">
 <a href="scripts/healthcare_etl_pipeline.py" download>ETL pipeline</a>
 <a href="scripts/healthcare_api_extractor_template.py" download>REST API extractor template</a>
 <a href="requirements-etl.txt" download>Python requirements</a>
 <a href="etl/DATA_CONTRACTS.md" download>Data contracts</a>
 <a href="etl/PIPELINE_ARCHITECTURE.md" download>Pipeline architecture</a>
 <a href="sql/healthcare_etl/etl_audit_queries.sql" download>SQL audit queries</a>\n <a href="assignments/outputs/healthcare_etl_training.db" download>Sample SQLite ETL database</a>\n <a href="assignments/outputs/etl_runs/" download>Run outputs folder (browse locally)</a>
 <a href="etl/PLATFORM_GUIDE.md" download>Platform and scheduling guide</a>
 </div>
 <p><b>What it does:</b> reads local CSV or paginated mock-API fixtures, preserves raw payloads, validates records, quarantines orphan references, loads SQLite marts, and writes run logs, quality reports and source-hash manifests.</p>
 <p><b>Scope:</b> a local batch training pipeline. It is not a production clinical integration, streaming, CDC or high-availability system. The mock API makes no network requests.</p></div>
 <div class="etl-toolbar"><input id="etlChallengeSearch" type="search" placeholder="Search ETL challenges…" value="${esc(state.query)}"><button class="secondary-small" id="etlResetProgress">Reset ETL progress</button></div>
 <div id="etlChallengeList">${filtered.map(c=>`
 <article class="etl-challenge">
  <div class="challenge-top"><span class="level">${esc(c.id)} · ${esc(c.level)} · ${esc(c.time)}</span><label><input type="checkbox" data-etl-done="${esc(c.id)}" ${done.has(c.id)?"checked":""}> Completed</label></div>
  <h3>${esc(c.title)}</h3><p>${esc(c.scenario)}</p>
  <details><summary>View tasks and acceptance criteria</summary><div class="lab-detail"><h4>Tasks</h4><ul>${c.tasks.map(x=>`<li>${esc(x)}</li>`).join("")}</ul><h4>Acceptance criteria</h4><ul>${c.acceptance.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div></details>
  <details><summary>Show starter commands / patterns</summary><pre>${esc(c.starter)}</pre></details>
  <details><summary>Show hint</summary><p>${esc(c.hint)}</p></details>
  <details><summary>Show worked solution and expected result</summary><p>${esc(c.solution)}</p><p><b>Expected result:</b> ${esc(c.expected)}</p></details>
 </article>`).join("")||'<div class="empty-state">No matching challenges.</div>'}</div>
 <div class="etl-note"><b>Safety and data interpretation</b><p>All supplied datasets are synthetic. Do not use real patient-identifiable data in these exercises. The source does not contain unit costs; the pipeline reports that the field was not supplied. Medication orders are not dispensing, administration or adherence evidence.</p></div>`;
 bind();
}
function bind(){
 document.getElementById("etlChallengeSearch")?.addEventListener("input",e=>{state.query=e.target.value;const p=e.target.selectionStart;save();render();const n=document.getElementById("etlChallengeSearch");n?.focus();n?.setSelectionRange(p,p);});
 host.querySelectorAll("[data-etl-done]").forEach(x=>x.addEventListener("change",()=>{state.done=state.done||[];state.done=x.checked?[...new Set([...state.done,x.dataset.etlDone])]:state.done.filter(id=>id!==x.dataset.etlDone);save();render();}));
 document.getElementById("etlResetProgress")?.addEventListener("click",()=>{if(confirm("Reset all ETL challenge completion marks on this device?")){state.done=[];save();render();}});
}
read();
fetch("content/etl-mastery.json").then(r=>{if(!r.ok)throw Error("ETL challenge content unavailable");return r.json();}).then(x=>{challenges=x.challenges||[];render();}).catch(e=>{host.innerHTML='<div class="empty-state">ETL content failed to load. Start the Academy through its local HTTP server, not file://.</div>';console.error(e);});
document.querySelectorAll('.nav-item[data-view="etl-mastery"]').forEach(btn=>btn.addEventListener("click",()=>{document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active",v.id==="view-etl-mastery"));document.querySelectorAll(".nav-item[data-view]").forEach(v=>v.classList.toggle("active",v===btn));const crumb=document.getElementById("crumb");if(crumb)crumb.textContent="Data engineering";document.getElementById("sidebar")?.classList.remove("open");window.scrollTo({top:0,behavior:"smooth"});}));
})();