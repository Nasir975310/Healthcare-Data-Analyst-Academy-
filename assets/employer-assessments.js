/* HDA Academy v3.1.0 — Employer-style technical assessments */
(()=>{
"use strict";
const STORE="hda-employer-assessments-v1", $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let sims=[],challenges=[],done={};
try{done=JSON.parse(localStorage.getItem(STORE)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(done))}catch(e){alert("Browser storage unavailable. Export your Academy backup.")}};
function render(){
 const host=$("#employerAssessmentsApp");if(!host)return;
 const n=challenges.filter(x=>done[x.id]).length;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>${sims.length}</b><span>Employer simulations</span></div><div class="upgrade-stat"><b>${challenges.length}</b><span>Review challenges</span></div><div class="upgrade-stat"><b>${n}/${challenges.length}</b><span>Completed locally</span></div></div>
 <article class="panel module-note"><b>Assessment rules</b><p>Attempt each task within its time limit before opening reference solutions. Record assumptions and what you could not validate. The module does not execute Excel, SQL or Python in the browser; use your local tools. All supplied data are synthetic.</p></article>
 <div class="module-toolbar"><input id="eaSearch" type="search" placeholder="Search SQL, Python, Excel, dashboard, client or review"></div>
 <h2>Employer-style simulations</h2><div class="upgrade-card-grid" id="eaSims"></div>
 <h2>Portfolio review and interview practice</h2><div class="upgrade-card-grid" id="eaChallenges"></div>
 <article class="panel module-note"><b>Reference assets</b><ul><li><code>employer_assessments/solutions/reference_queries.sql</code></li><li><code>employer_assessments/solutions/qa_assessment.py</code></li><li><code>employer_assessments/review_tools/portfolio_review_scorecard.md</code></li><li><code>employer_assessments/review_tools/mock_interview_rubric.md</code></li></ul><p>The QA reference run finds 41 orphan order references. This is intentional and should be reported, not silently removed.</p></article>`;
 const draw=()=>{
  const q=$("#eaSearch").value.toLowerCase();
  $("#eaSims").innerHTML=sims.filter(x=>(x.id+" "+x.title+" "+x.scenario).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><div class="card-kicker">${esc(x.id)} · ${x.time_limit_minutes} minutes</div><h3>${esc(x.title)}</h3><p>${esc(x.scenario)}</p><details><summary>Tasks, deliverables and scoring</summary><h4>Tasks</h4><ul>${x.tasks.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><h4>Deliverables</h4><ul>${x.deliverables.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><h4>Scoring</h4><ul>${Object.entries(x.scoring).map(([k,v])=>`<li>${esc(k.replaceAll("_"," "))}: ${v} points</li>`).join("")}</ul><h4>Critical failures</h4><ul>${x.critical_failures.map(v=>`<li>${esc(v)}</li>`).join("")}</ul></details></article>`).join("");
  $("#eaChallenges").innerHTML=challenges.filter(x=>(x.id+" "+x.title+" "+x.scenario).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><div class="card-kicker">${esc(x.id)} · ${done[x.id]?"Completed":"Not completed"}</div><h3>${esc(x.title)}</h3><p>${esc(x.scenario)}</p><details><summary>Acceptance criteria and reference</summary><p>${esc(x.task)}</p><ul>${x.acceptance.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><p>${esc(x.solution)}</p></details><label class="check-row"><input type="checkbox" data-ea-done="${esc(x.id)}" ${done[x.id]?"checked":""}> Mark complete</label></article>`).join("");
  $("#eaChallenges").querySelectorAll("[data-ea-done]").forEach(el=>el.addEventListener("change",()=>{done[el.dataset.eaDone]=el.checked;if(!el.checked)delete done[el.dataset.eaDone];save();render();}));
 };
 $("#eaSearch").addEventListener("input",draw);draw();
}
Promise.all(["employer_assessments/simulations/employer_simulations.json","employer_assessments/challenges.json"].map(p=>fetch(p).then(r=>{if(!r.ok)throw Error(p);return r.json()}))).then(([a,b])=>{sims=a;challenges=b;render()}).catch(()=>{const h=$("#employerAssessmentsApp");if(h)h.innerHTML='<div class="notice">Assessment resources could not load. Start the Academy from its local HTTP server.</div>';});
})();
