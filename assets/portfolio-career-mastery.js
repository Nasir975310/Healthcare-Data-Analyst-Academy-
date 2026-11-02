/* HDA Academy v2.9.0 — Portfolio capstones and job readiness */
(()=>{
"use strict";
const STORE="hda-portfolio-career-mastery-v1", $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let challenges=[],caps=[],interviews=[],done={};
try{done=JSON.parse(localStorage.getItem(STORE)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(done))}catch(e){alert("Browser storage unavailable. Export your Academy backup.")}};
function render(){
 const host=$("#portfolioCareerMasteryApp");if(!host)return;
 const n=challenges.filter(x=>done[x.id]).length;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>${caps.length}</b><span>End-to-end capstones</span></div><div class="upgrade-stat"><b>${challenges.length}</b><span>Professional challenges</span></div><div class="upgrade-stat"><b>${n}/${challenges.length}</b><span>Completed locally</span></div></div>
 <article class="panel module-note"><b>Portfolio standard</b><p>Do not present a project as validated merely because the code runs. Retain definitions, provenance, QA evidence, limitations and a reproducible handoff. Synthetic data only; no patient-identifiable or confidential employer data.</p></article>
 <div class="module-toolbar"><input id="pcSearch" type="search" placeholder="Search capstones, portfolio, interview or client delivery"></div>
 <h2>End-to-end capstones</h2><div class="upgrade-card-grid" id="pcCaps"></div>
 <h2>Professional execution challenges</h2><div class="upgrade-card-grid" id="pcChallenges"></div>
 <h2>Interview preparation</h2><div class="upgrade-card-grid" id="pcInterviews"></div>
 <article class="panel module-note"><b>Included assets</b><p><code>portfolio_career/data/</code> contains three synthetic client datasets. Run <code>python portfolio_career/scripts/run_portfolio_capstone.py</code> from the Academy root. Outputs are written to <code>portfolio_career/outputs/</code>. SQL reference queries, README and client handoff templates are included.</p><p>The capstone dataset deliberately contains 36 orphan medication-order rows for reconciliation practice. The reference script retains and reports them rather than silently dropping them.</p></article>`;
 const draw=()=>{
  const q=$("#pcSearch").value.toLowerCase();
  $("#pcCaps").innerHTML=caps.filter(x=>(x.id+" "+x.title+" "+x.question).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><div class="card-kicker">${esc(x.id)} · ${esc(x.audience)}</div><h3>${esc(x.title)}</h3><p>${esc(x.question)}</p><details><summary>Deliverables and critical cautions</summary><h4>Deliverables</h4><ul>${x.deliverables.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><h4>Critical cautions</h4><ul>${x.critical_cautions.map(v=>`<li>${esc(v)}</li>`).join("")}</ul></details></article>`).join("");
  $("#pcChallenges").innerHTML=challenges.filter(x=>(x.id+" "+x.title+" "+x.scenario).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><div class="card-kicker">${esc(x.id)} · ${done[x.id]?"Completed":"Not completed"}</div><h3>${esc(x.title)}</h3><p>${esc(x.scenario)}</p><details><summary>Task and acceptance criteria</summary><p>${esc(x.task)}</p><ul>${x.acceptance.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><h4>Reference approach</h4><p>${esc(x.solution)}</p><h4>Portfolio evidence</h4><p>${esc(x.portfolio)}</p></details><label class="check-row"><input type="checkbox" data-pc-done="${esc(x.id)}" ${done[x.id]?"checked":""}> Mark complete</label></article>`).join("");
  $("#pcInterviews").innerHTML=interviews.filter(x=>(x.question+" "+x.strong_answer).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><h3>${esc(x.question)}</h3><details><summary>What a strong answer should cover</summary><p>${esc(x.strong_answer)}</p><h4>Avoid</h4><p>${esc(x.avoid)}</p></details></article>`).join("");
  $("#pcChallenges").querySelectorAll("[data-pc-done]").forEach(el=>el.addEventListener("change",()=>{done[el.dataset.pcDone]=el.checked;if(!el.checked)delete done[el.dataset.pcDone];save();render();}));
 };
 $("#pcSearch").addEventListener("input",draw);draw();
}
Promise.all(["portfolio_career/challenges.json","portfolio_career/capstones/capstone_briefs.json","portfolio_career/templates/interview_bank.json"].map(p=>fetch(p).then(r=>{if(!r.ok)throw Error(p);return r.json()}))).then(([a,b,c])=>{challenges=a;caps=b;interviews=c;render()}).catch(()=>{const h=$("#portfolioCareerMasteryApp");if(h)h.innerHTML='<div class="notice">Portfolio resources could not load. Run the Academy from its local HTTP server.</div>';});
})();
