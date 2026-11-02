/* HDA Academy v2.3.0 — Power BI mastery */
(()=>{
"use strict";
const STORE="hda-powerbi-mastery-v230";
const host=document.getElementById("powerbiMasteryApp");
if(!host)return;
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let challenges=[],state={done:[],query:""};
const read=()=>{try{state={...state,...JSON.parse(localStorage.getItem(STORE)||"{}")}}catch(e){}};
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(state));}catch(e){}};
function render(){
 const done=new Set(state.done||[]);
 const filtered=challenges.filter(c=>(c.id+" "+c.title+" "+c.scenario+" "+c.level).toLowerCase().includes((state.query||"").toLowerCase()));
 host.innerHTML=`
 <div class="pbi-mastery-summary">
  <div><b>${challenges.length}</b><span>Progressive challenges</span></div>
  <div><b>${done.size}/${challenges.length}</b><span>Completed on this device</span></div>
  <div><b>${Math.round(done.size/Math.max(1,challenges.length)*100)}%</b><span>Completion progress</span></div>
  <div><b>90 min</b><span>Professional client simulation</span></div>
 </div>
 <div class="pbi-note"><b>Required practical files</b><div class="pbi-links">
 <a href="assignments/data/pbi_dim_date.csv" download>Admission date dimension</a>\n <a href="assignments/data/pbi_dim_order_date.csv" download>Order date dimension</a>
 <a href="assignments/data/pbi_dim_encounter.csv" download>Encounter dimension</a>
 <a href="assignments/data/pbi_dim_department.csv" download>Department dimension</a>
 <a href="assignments/data/pbi_dim_payer.csv" download>Payer dimension</a>
 <a href="assignments/data/pbi_dim_drug.csv" download>Drug dimension</a>
 <a href="assignments/data/pbi_fact_encounter_metrics.csv" download>Encounter metrics fact</a>
 <a href="assignments/data/pbi_fact_medication_orders.csv" download>Medication orders fact</a>
 <a href="powerbi/measures.dax" download>DAX measure library</a>
 <a href="powerbi/MODEL_RELATIONSHIPS.md" download>Model relationships</a>
 <a href="powerbi/REPORT_BLUEPRINT.md" download>Report blueprint</a>
 <a href="powerbi/hda_powerbi_theme.json" download>Power BI theme JSON</a>
 <a href="powerbi/import_fact_medication_orders.m" download>Power Query M example</a>
 <a href="powerbi/model_reference_checks.json" download>Reference checks</a>
 <a href="powerbi/PLATFORM_GUIDE.md" download>Platform guide</a>
 </div>
 <p><b>Platform:</b> Power BI Desktop is the primary Windows route. Linux users can use Metabase or Python-based reporting for related skills, but these do not reproduce Power BI Desktop, DAX or PBIX workflows exactly.</p></div>
 <div class="pbi-toolbar"><input id="pbiChallengeSearch" type="search" placeholder="Search Power BI challenges…" value="${esc(state.query)}"><button class="secondary-small" id="pbiResetProgress">Reset Power BI progress</button></div>
 <div id="pbiChallengeList">${filtered.map(c=>`
 <article class="pbi-challenge">
  <div class="challenge-top"><span class="level">${esc(c.id)} · ${esc(c.level)} · ${esc(c.time)}</span><label><input type="checkbox" data-pbi-done="${esc(c.id)}" ${done.has(c.id)?"checked":""}> Completed</label></div>
  <h3>${esc(c.title)}</h3><p>${esc(c.scenario)}</p>
  <details><summary>View tasks and acceptance criteria</summary><div class="lab-detail"><h4>Tasks</h4><ul>${c.tasks.map(x=>`<li>${esc(x)}</li>`).join("")}</ul><h4>Acceptance criteria</h4><ul>${c.acceptance.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div></details>
  <details><summary>Show starter model / DAX</summary><pre>${esc(c.starter)}</pre></details>
  <details><summary>Show hint</summary><p>${esc(c.hint)}</p></details>
  <details><summary>Show worked solution and expected result</summary><p>${esc(c.solution)}</p><p><b>Expected result:</b> ${esc(c.expected)}</p></details>
 </article>`).join("")||'<div class="empty-state">No matching challenges.</div>'}</div>
 <div class="pbi-note"><b>Unfiltered reference controls</b><p>80 encounters · 151 medication-order rows · mean LOS 3.875 days · supplied readmission flag 7/80 = 8.75% · ordered quantity 3,038 · synthetic order value INR 100,279.75. One order has a missing unit cost, one has a blank therapeutic class and one references a nonexistent encounter key.</p><p>All records are synthetic. The readmission flag is supplied and not independently validated; medication orders do not prove dispensing, administration, adherence or appropriateness; costs are synthetic.</p></div>`;
 bind();
}
function bind(){
 document.getElementById("pbiChallengeSearch")?.addEventListener("input",e=>{state.query=e.target.value;const p=e.target.selectionStart;save();render();const n=document.getElementById("pbiChallengeSearch");n?.focus();n?.setSelectionRange(p,p);});
 host.querySelectorAll("[data-pbi-done]").forEach(x=>x.addEventListener("change",()=>{state.done=state.done||[];state.done=x.checked?[...new Set([...state.done,x.dataset.pbiDone])]:state.done.filter(id=>id!==x.dataset.pbiDone);save();render();}));
 document.getElementById("pbiResetProgress")?.addEventListener("click",()=>{if(confirm("Reset all Power BI challenge completion marks on this device?")){state.done=[];save();render();}});
}
read();
fetch("content/powerbi-mastery.json").then(r=>{if(!r.ok)throw Error("Power BI challenge content unavailable");return r.json();}).then(x=>{challenges=x.challenges||[];render();}).catch(e=>{host.innerHTML='<div class="empty-state">Power BI content failed to load. Start the Academy using its local HTTP server, not file://.</div>';console.error(e);});
document.querySelectorAll('.nav-item[data-view="powerbi-mastery"]').forEach(btn=>btn.addEventListener("click",()=>{document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active",v.id==="view-powerbi-mastery"));document.querySelectorAll(".nav-item[data-view]").forEach(v=>v.classList.toggle("active",v===btn));const crumb=document.getElementById("crumb");if(crumb)crumb.textContent="Power BI mastery";document.getElementById("sidebar")?.classList.remove("open");window.scrollTo({top:0,behavior:"smooth"});}));
})();