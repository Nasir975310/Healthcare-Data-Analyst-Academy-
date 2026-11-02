/* HDA Academy v2.7.0 — Healthcare Warehousing and Interoperability */
(()=>{
"use strict";
const STORE="hda-interoperability-mastery-v1", $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let challenges=[],completed={};
try{completed=JSON.parse(localStorage.getItem(STORE)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(completed))}catch(e){alert("Browser storage unavailable. Export your Academy backup.")}};
function render(){
 const host=$("#interoperabilityMasteryApp");if(!host)return;
 const done=challenges.filter(x=>completed[x.id]).length;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>${challenges.length}</b><span>Challenges</span></div><div class="upgrade-stat"><b>${done}/${challenges.length}</b><span>Completed on this device</span></div><div class="upgrade-stat"><b>${Math.round(done/Math.max(1,challenges.length)*100)}%</b><span>Module progress</span></div></div>
 <article class="panel module-note"><b>Interoperability execution requirement</b><p>The browser presents the challenge instructions but does not run an HL7 interface engine or FHIR server. Use the supplied synthetic fixtures and local Python/SQLite tools. These examples are not production conformance tests.</p></article>
 <div class="module-toolbar"><input id="intSearch" type="search" placeholder="Search HL7, FHIR, terminology, warehouse or governance"><select id="intFilter"><option value="all">All challenges</option><option value="open">Not completed</option><option value="done">Completed</option></select></div><div id="intCards" class="upgrade-card-grid"></div>
 <article class="panel module-note"><b>Clinical data safeguards</b><p>Preserve source identifiers, code systems, terminology versions, units and provenance. Keep unmapped concepts visible. A medication request is not an administration or adherence record. Do not use real patient data or commit PHI or credentials.</p></article>`;
 const draw=()=>{
  const q=$("#intSearch").value.toLowerCase(),f=$("#intFilter").value;
  const list=challenges.filter(c=>(f==="all"||(f==="done"&&completed[c.id])||(f==="open"&&!completed[c.id]))&&[c.id,c.title,c.scenario,c.tasks,c.method].join(" ").toLowerCase().includes(q));
  $("#intCards").innerHTML=list.map(c=>`<article class="upgrade-card"><div class="card-kicker">${esc(c.id)} · ${completed[c.id]?"Completed":"Challenge"}</div><h3>${esc(c.title)}</h3><p>${esc(c.scenario)}</p><details class="project-files"><summary>Open tasks, method and acceptance criteria</summary><h4>Tasks</h4><p>${esc(c.tasks)}</p><h4>Suggested method</h4><p>${esc(c.method)}</p><h4>Acceptance criteria</h4><p>${esc(c.acceptance)}</p><h4>Safety / limitation</h4><p>${esc(c.safety)}</p></details><label class="field-label"><input type="checkbox" data-int-done="${esc(c.id)}" ${completed[c.id]?"checked":""}> I completed the challenge and saved evidence</label></article>`).join("")||'<div class="empty-state">No challenges match this search.</div>';
 };
 $("#intSearch").addEventListener("input",draw);$("#intFilter").addEventListener("change",draw);
 host.onchange=e=>{const id=e.target.dataset.intDone;if(!id)return;if(e.target.checked)completed[id]=true;else delete completed[id];save();render();};
 draw();
}
async function init(){
 const nav=document.querySelector('[data-view="interoperability-mastery"]'),main=$("#view-interoperability-mastery");
 if(!nav||!main)return;
 nav.addEventListener("click",e=>{e.stopImmediatePropagation();e.preventDefault();document.querySelectorAll(".view").forEach(x=>x.classList.toggle("active",x===main));document.querySelectorAll(".nav-item[data-view]").forEach(x=>x.classList.toggle("active",x===nav));const crumb=$("#crumb");if(crumb)crumb.textContent="Healthcare interoperability";$("#sidebar")?.classList.remove("open");window.scrollTo({top:0,behavior:"smooth"});render();},true);
 try{const r=await fetch("interoperability/interoperability-mastery.json");if(!r.ok)throw Error("HTTP "+r.status);const d=await r.json();challenges=d.challenges||[];render();}catch(e){$("#interoperabilityMasteryApp").innerHTML='<div class="empty-state">Could not load interoperability challenges. Start the Academy with its local HTTP server.</div>';console.error(e);}
}
document.addEventListener("DOMContentLoaded",init);
})();