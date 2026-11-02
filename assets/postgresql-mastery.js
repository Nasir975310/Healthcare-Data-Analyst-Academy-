/* HDA Academy v2.5.0 — PostgreSQL mastery module */
(()=>{
"use strict";
const STORE="hda-postgresql-mastery-v1";
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let challenges=[],completed={};
try{completed=JSON.parse(localStorage.getItem(STORE)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(completed))}catch(e){alert("Browser storage is unavailable. Export your main Academy backup regularly.")}};
function render(){
 const host=$("#postgresqlMasteryApp"); if(!host)return;
 const done=challenges.filter(x=>completed[x.id]).length;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>${challenges.length}</b><span>Challenges</span></div><div class="upgrade-stat"><b>${done}/${challenges.length}</b><span>Marked complete on this device</span></div><div class="upgrade-stat"><b>${Math.round(done/Math.max(1,challenges.length)*100)}%</b><span>Module progress</span></div></div>
 <article class="panel module-note"><b>Execution requirement</b><p>These challenges require a local PostgreSQL server for execution. The browser displays instructions; it does not execute SQL. Use DBeaver or psql and retain your query files and result evidence. SQLite is not a substitute for PostgreSQL-specific syntax.</p></article>
 <div class="module-toolbar"><input id="pgSearch" type="search" placeholder="Search PostgreSQL challenges, concepts or SQL features"><select id="pgFilter"><option value="all">All challenges</option><option value="open">Not completed</option><option value="done">Completed</option></select></div>
 <div id="pgCards" class="upgrade-card-grid"></div>
 <article class="panel module-note"><b>Safety and interpretation</b><p>Use synthetic data only. An order record does not establish administration, dispensing or adherence. The supplied 30-day flag is a synthetic field, not a validated clinical outcome. Never expose database ports, commit credentials or upload PHI to a personal repository.</p></article>`;
 const draw=()=>{
  const q=$("#pgSearch").value.toLowerCase(),f=$("#pgFilter").value;
  const rows=challenges.filter(c=>(f==="all"||(f==="done"&&completed[c.id])||(f==="open"&&!completed[c.id]))&&[c.id,c.title,c.scenario,c.tasks,c.starter].join(" ").toLowerCase().includes(q));
  $("#pgCards").innerHTML=rows.map(c=>`<article class="upgrade-card"><div class="card-kicker">${esc(c.id)} · ${completed[c.id]?"Completed":"Challenge"}</div><h3>${esc(c.title)}</h3><p>${esc(c.scenario)}</p><details class="project-files"><summary>Open task, starter SQL and acceptance criteria</summary><h4>Tasks</h4><p>${esc(c.tasks)}</p><h4>Starter SQL / reference pattern</h4><pre><code>${esc(c.starter)}</code></pre><h4>Acceptance criteria</h4><p>${esc(c.acceptance)}</p><h4>Safety / limitation</h4><p>${esc(c.safety)}</p></details><label class="field-label"><input type="checkbox" data-pg-done="${esc(c.id)}" ${completed[c.id]?"checked":""}> I executed or completed this challenge and saved evidence</label></article>`).join("")||`<div class="empty-state">No challenges match this search.</div>`;
 };
 $("#pgSearch").addEventListener("input",draw);$("#pgFilter").addEventListener("change",draw);
 host.onchange=e=>{const id=e.target.dataset.pgDone;if(!id)return;if(e.target.checked)completed[id]=true;else delete completed[id];save();render();};
 draw();
}
async function init(){
 const nav=document.querySelector('[data-view="postgresql-mastery"]');
 const main=$("#view-postgresql-mastery");
 if(!nav||!main)return;
 nav.addEventListener("click",e=>{e.stopImmediatePropagation();e.preventDefault();document.querySelectorAll(".view").forEach(x=>x.classList.toggle("active",x===main));document.querySelectorAll(".nav-item[data-view]").forEach(x=>x.classList.toggle("active",x===nav));const crumb=$("#crumb");if(crumb)crumb.textContent="PostgreSQL engineering";$("#sidebar")?.classList.remove("open");window.scrollTo({top:0,behavior:"smooth"});render();},true);
 try{const r=await fetch("content/postgresql-mastery.json");if(!r.ok)throw Error("HTTP "+r.status);const d=await r.json();challenges=d.challenges||[];render();}
 catch(e){$("#postgresqlMasteryApp").innerHTML='<div class="empty-state">Could not load PostgreSQL challenge content. Start the Academy through its local HTTP server and confirm the content folder is present.</div>';console.error(e);}
}
document.addEventListener("DOMContentLoaded",init);
})();