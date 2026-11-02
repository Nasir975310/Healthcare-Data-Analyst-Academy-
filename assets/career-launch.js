/* HDA Academy v3.0.0 — Career launch */
(()=>{
"use strict";
const STORE="hda-career-launch-v1", $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let roles=[],challenges=[],assessments=[],done={};
try{done=JSON.parse(localStorage.getItem(STORE)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(done))}catch(e){alert("Browser storage unavailable. Export your Academy backup.")}};
function render(){
 const host=$("#careerLaunchApp");if(!host)return;
 const n=challenges.filter(x=>done[x.id]).length;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>${roles.length}</b><span>Role families</span></div><div class="upgrade-stat"><b>${assessments.length}</b><span>Hiring simulations</span></div><div class="upgrade-stat"><b>${n}/${challenges.length}</b><span>Career challenges</span></div></div>
 <article class="panel module-note"><b>Market reality — India, snapshot dated 2 November 2026</b><p>Remote-only fresher healthcare analytics vacancies appear more constrained than general healthcare data roles. Target adjacent entry routes as well: clinical data coordination, drug-safety data operations, hospital reporting, healthcare vendor analytics and trainee roles. Check current eligibility on the employer's official careers site; third-party listings may be stale.</p><p>Pharm.D is relevant domain training, but does not replace SQL, Excel/BI, data-quality and communication evidence.</p></article>
 <div class="module-toolbar"><input id="clSearch" type="search" placeholder="Search role families, assessments or job-readiness tasks"></div>
 <h2>Role-family map</h2><div class="upgrade-card-grid" id="clRoles"></div>
 <h2>Timed hiring simulations</h2><div class="upgrade-card-grid" id="clAssess"></div>
 <h2>Career launch challenges</h2><div class="upgrade-card-grid" id="clChallenges"></div>
 <article class="panel module-note"><b>Career templates and execution plan</b><ul><li><code>career_launch/templates/cv_master_template.md</code> — role-specific CV structure.</li><li><code>career_launch/templates/linkedin_profile_template.md</code> — headline, About and Featured sections.</li><li><code>career_launch/templates/cover_letter_template.md</code> — concise application note.</li><li><code>career_launch/templates/application_tracker.csv</code> and <code>job_description_scorecard.csv</code> — application pipeline.</li><li><code>career_launch/application_system/30_day_execution_plan.md</code> — build evidence while applying.</li></ul></article>
 <article class="panel module-note"><b>Safety and honesty</b><p>Never pay for a job offer or interview slot. Verify the employer and vacancy. Do not claim production EDC, licensed MedDRA, CDISC conformance, Power BI or claims/EHR experience unless actually obtained. Do not publish patient data or confidential employer information.</p></article>`;
 const draw=()=>{
  const q=$("#clSearch").value.toLowerCase();
  $("#clRoles").innerHTML=roles.filter(x=>(x.role+" "+x.fit+" "+x.core.join(" ")).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><div class="card-kicker">${esc(x.fit)}</div><h3>${esc(x.role)}</h3><h4>Core skills</h4><ul>${x.core.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><h4>Evidence to show</h4><ul>${x.proof.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><h4>Likely gaps</h4><ul>${x.gaps.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><p><b>Search terms:</b> ${esc(x.search_terms.join(" · "))}</p></article>`).join("");
  $("#clAssess").innerHTML=assessments.filter(x=>(x.id+" "+x.title+" "+x.task).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><div class="card-kicker">${esc(x.id)} · ${x.duration_minutes} minutes</div><h3>${esc(x.title)}</h3><p>${esc(x.task)}</p><details><summary>Deliverable and scoring rubric</summary><p>${esc(x.deliverable)}</p><ul>${Object.entries(x.rubric).map(([k,v])=>`<li>${esc(k.replaceAll("_"," "))}: ${v} points</li>`).join("")}</ul></details></article>`).join("");
  $("#clChallenges").innerHTML=challenges.filter(x=>(x.id+" "+x.title+" "+x.scenario).toLowerCase().includes(q)).map(x=>`<article class="upgrade-card"><div class="card-kicker">${esc(x.id)} · ${done[x.id]?"Completed":"Not completed"}</div><h3>${esc(x.title)}</h3><p>${esc(x.scenario)}</p><details><summary>Task and acceptance criteria</summary><p>${esc(x.task)}</p><ul>${x.acceptance.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><h4>Reference approach</h4><p>${esc(x.solution)}</p></details><label class="check-row"><input type="checkbox" data-cl-done="${esc(x.id)}" ${done[x.id]?"checked":""}> Mark complete</label></article>`).join("");
  $("#clChallenges").querySelectorAll("[data-cl-done]").forEach(el=>el.addEventListener("change",()=>{done[el.dataset.clDone]=el.checked;if(!el.checked)delete done[el.dataset.clDone];save();render();}));
 };
 $("#clSearch").addEventListener("input",draw);draw();
}
Promise.all(["career_launch/role_maps/role_matrix.json","career_launch/challenges.json","career_launch/assessments/hiring_assessments.json"].map(p=>fetch(p).then(r=>{if(!r.ok)throw Error(p);return r.json()}))).then(([a,b,c])=>{roles=a;challenges=b;assessments=c;render()}).catch(()=>{const h=$("#careerLaunchApp");if(h)h.innerHTML='<div class="notice">Career launch resources could not load. Start the Academy from its local HTTP server.</div>';});
})();
