/* HDA Academy v2.6.0 — Statistics, Epidemiology and Clinical Research */
(()=>{
"use strict";
const STORE="hda-statistics-mastery-v1", $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let challenges=[],completed={};
try{completed=JSON.parse(localStorage.getItem(STORE)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(completed))}catch(e){alert("Browser storage unavailable. Export your Academy backup.")}};
function render(){
 const host=$("#statisticsMasteryApp");if(!host)return;
 const done=challenges.filter(x=>completed[x.id]).length;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>${challenges.length}</b><span>Challenges</span></div><div class="upgrade-stat"><b>${done}/${challenges.length}</b><span>Completed on this device</span></div><div class="upgrade-stat"><b>${Math.round(done/Math.max(1,challenges.length)*100)}%</b><span>Module progress</span></div></div>
 <article class="panel module-note"><b>Reproducible analysis requirement</b><p>The Academy presents the task and reference method; it does not execute Python or R in the browser. Run the supplied scripts locally, inspect generated tables and figures, and retain your code and validation evidence. Never interpret synthetic data as clinical evidence.</p></article>
 <div class="module-toolbar"><input id="statSearch" type="search" placeholder="Search statistics, epidemiology, models or methods"><select id="statFilter"><option value="all">All challenges</option><option value="open">Not completed</option><option value="done">Completed</option></select></div><div id="statCards" class="upgrade-card-grid"></div>
 <article class="panel module-note"><b>Interpretation safeguards</b><p>Report effect estimates and confidence intervals, not p-values alone. Distinguish association from causation; risk from odds; risk ratio from hazard ratio; prevalence from incidence; and discrimination from calibration. State the population, denominator, time horizon, missingness and limitations.</p></article>`;
 const draw=()=>{
  const q=$("#statSearch").value.toLowerCase(),f=$("#statFilter").value;
  const list=challenges.filter(c=>(f==="all"||(f==="done"&&completed[c.id])||(f==="open"&&!completed[c.id]))&&[c.id,c.title,c.scenario,c.tasks,c.method].join(" ").toLowerCase().includes(q));
  $("#statCards").innerHTML=list.map(c=>`<article class="upgrade-card"><div class="card-kicker">${esc(c.id)} · ${completed[c.id]?"Completed":"Challenge"}</div><h3>${esc(c.title)}</h3><p>${esc(c.scenario)}</p><details class="project-files"><summary>Open task, method and acceptance criteria</summary><h4>Tasks</h4><p>${esc(c.tasks)}</p><h4>Suggested method</h4><p>${esc(c.method)}</p><h4>Acceptance criteria</h4><p>${esc(c.acceptance)}</p><h4>Interpretation safeguard</h4><p>${esc(c.safety)}</p></details><label class="field-label"><input type="checkbox" data-stat-done="${esc(c.id)}" ${completed[c.id]?"checked":""}> I completed the practical and saved reproducible evidence</label></article>`).join("")||'<div class="empty-state">No challenges match this search.</div>';
 };
 $("#statSearch").addEventListener("input",draw);$("#statFilter").addEventListener("change",draw);
 host.onchange=e=>{const id=e.target.dataset.statDone;if(!id)return;if(e.target.checked)completed[id]=true;else delete completed[id];save();render();};
 draw();
}
async function init(){
 const nav=document.querySelector('[data-view="statistics-mastery"]'),main=$("#view-statistics-mastery");
 if(!nav||!main)return;
 nav.addEventListener("click",e=>{e.stopImmediatePropagation();e.preventDefault();document.querySelectorAll(".view").forEach(x=>x.classList.toggle("active",x===main));document.querySelectorAll(".nav-item[data-view]").forEach(x=>x.classList.toggle("active",x===nav));const crumb=$("#crumb");if(crumb)crumb.textContent="Statistics & epidemiology";$("#sidebar")?.classList.remove("open");window.scrollTo({top:0,behavior:"smooth"});render();},true);
 try{const r=await fetch("statistics/statistics-mastery.json");if(!r.ok)throw Error("HTTP "+r.status);const d=await r.json();challenges=d.challenges||[];render();}catch(e){$("#statisticsMasteryApp").innerHTML='<div class="empty-state">Could not load statistics challenge content. Start the Academy using its local HTTP server.</div>';console.error(e);}
}
document.addEventListener("DOMContentLoaded",init);
})();