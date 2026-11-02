/* v3.8 Advanced Professional Mastery */
(() => {
"use strict";
const KEY="hda_advanced_mastery_v38";
const challenges=[
["SQL-ADV-01","Table grain and key audit","Profile row counts, distinct keys and duplicate keys across the three tables.","Compare COUNT(*) with COUNT(DISTINCT key)."],
["SQL-ADV-02","Orphan anti-join","Find medication orders whose encounter key is absent.","LEFT JOIN ... IS NULL or NOT EXISTS."],
["SQL-ADV-03","Safe fact aggregation","Produce department encounter and order metrics without fan-out.","Aggregate facts independently before joining."],
["SQL-ADV-04","Window ranking","Rank departments by encounter volume and explain ties.","DENSE_RANK() OVER."],
["SQL-ADV-05","First encounter cohort","Select first encounter per patient and calculate supplied flag proportion.","ROW_NUMBER() with deterministic tie-break."],
["SQL-ADV-06","Monthly utilisation","Produce monthly orders, distinct encounters with orders and quantity totals.","Use month grain and COUNT(DISTINCT encounter_id)."],
["SQL-ADV-07","Latest clinical observation","Find latest SBP per encounter and summarise it.","ROW_NUMBER() by encounter, date and stable ID."],
["SQL-ADV-08","Data-quality audit","Count non-positive quantity, missing cost and missing class.","CASE expressions and explicit null handling."],
["SQL-ADV-09","Index and query plan","Inspect lookup plan before/after a composite index.","EXPLAIN QUERY PLAN; describe actual plan output."],
["SQL-ADV-10","Cross-domain cohort","Count encounters with both SBP observation and medication order.","Use distinct encounter-key sets."],
["SQL-ADV-11","Pre-aggregated join","Join encounter-level mean SBP and order count safely.","Aggregate each source to encounter grain first."],
["SQL-ADV-12","Metric contract","Define numerator, denominator, grain, exclusions and caveats for supplied flag.","Flag is synthetic and unvalidated."]
];
const assignments=[
["STAT-ADV-01","Statistical Validation","120 min","Crude vs adjusted observational comparison, missingness, robust confidence intervals and confounding."],
["DASH-ADV-01","Dashboard Review","75 min","Reconcile four KPI cards; diagnose one-to-many join fan-out and orphan handling."],
["ADV-EXAM-01","Advanced Mastery Examination","180 min","Integrated SQL, statistical validation, dashboard QA, reproducibility and executive communication."]
];
const $=s=>document.querySelector(s),esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let state={};try{state=JSON.parse(localStorage.getItem(KEY)||"{}")}catch{}
const entry=id=>state[id]||{done:false,notes:"",score:"",minutes:""};
function save(id,v){state[id]=v;localStorage.setItem(KEY,JSON.stringify(state));}
function render(){
 const done=challenges.filter(x=>entry(x[0]).done).length, adone=assignments.filter(x=>entry(x[0]).done).length;
 $("#advancedMasteryApp").innerHTML=`<div class="stats-grid"><article class="stat-card"><span>SQL investigations</span><strong>${done}/12</strong></article><article class="stat-card"><span>Advanced practicals</span><strong>${adone}/3</strong></article><article class="stat-card"><span>Overall tracked items</span><strong>${done+adone}/15</strong></article></div>
 <div class="notice"><b>Mastery standard:</b> solve from raw inputs, explain the grain, preserve denominators, validate outputs and disclose limitations. Reference outputs are for checking after your first attempt. Synthetic analyses are not clinical evidence.</div>
 <section class="panel"><h2>1. Advanced SQL investigation bank</h2><p>Use <code>advanced_professional_mastery/data/advanced_healthcare_analytics.db</code> and <code>sql/advanced_investigation.sql</code>. Track each investigation when you can explain and reproduce it.</p>
 <div class="mastery-list">${challenges.map((c,i)=>{let s=entry(c[0]);return `<article class="mastery-item"><label><input type="checkbox" data-check="${c[0]}" ${s.done?"checked":""}><b>${c[0]} — ${c[1]}</b></label><p>${esc(c[2])}</p><details><summary>Hint</summary><p>${esc(c[3])}</p></details><textarea data-notes="${c[0]}" rows="2" placeholder="Query approach, result, validation and lesson…">${esc(s.notes)}</textarea></article>`}).join("")}</div></section>
 <section class="panel"><h2>2. Advanced practical assignments</h2><div class="sim-grid">${assignments.map(a=>{let s=entry(a[0]);return `<article class="sim-card"><div class="eyebrow">${a[0]} · ${a[2]}</div><h3>${a[1]}</h3><p>${esc(a[3])}</p><label><input type="checkbox" data-check="${a[0]}" ${s.done?"checked":""}> Mark submitted after evidence review</label><label>Score (%)<input type="number" min="0" max="100" data-score="${a[0]}" value="${esc(s.score)}"></label><label>Time spent (minutes)<input type="number" min="0" data-minutes="${a[0]}" value="${esc(s.minutes)}"></label><textarea data-notes="${a[0]}" rows="3" placeholder="Evidence, assumptions, key finding, limitations…">${esc(s.notes)}</textarea></article>`}).join("")}</div></section>
 <section class="panel"><h2>3. Statistical validation reference</h2><p>Run from Academy root:</p><pre><code>python advanced_professional_mastery/solutions/statistical_validation.py</code></pre><p>Reference result from the synthetic cohort:</p><table><tbody><tr><th>Raw cohort</th><td>1,200</td></tr><tr><th>Complete cases</th><td>1,181</td></tr><tr><th>Crude treated-minus-untreated difference</th><td>+6.66 mmHg (95% CI 4.14 to 9.18)</td></tr><tr><th>Adjusted treatment coefficient</th><td>−3.62 mmHg (95% CI −4.96 to −2.29)</td></tr></tbody></table><p>The reversal illustrates confounding by indication in this generated example. Adjustment does not eliminate unmeasured confounding or prove causality.</p></section>
 <section class="panel"><h2>4. Dashboard review</h2><p>Open <code>assignments/dashboard_review.md</code> and <code>data/dashboard_cards_flawed.csv</code>. Recompute all cards from raw data. The key trap is calculating encounter-level metrics after joining to multiple medication orders.</p><p>Reference values are in <code>outputs/metric_reference.json</code>; do not inspect until you have produced your own reconciliation.</p></section>
 <section class="panel"><h2>5. Progress backup</h2><div class="button-row"><button class="primary-btn" id="advExport">Export v3.8 progress</button><label class="secondary-btn file-button">Import v3.8 progress<input id="advImport" type="file" accept="application/json"></label></div><p class="muted">Progress is stored locally in this browser. Keep a separate full Academy backup.</p></section>`;
 $$("[data-check]").forEach(el=>el.onchange=()=>{let v=entry(el.dataset.check);v.done=el.checked;save(el.dataset.check,v);render();});
 $$("[data-notes]").forEach(el=>el.onchange=()=>{let v=entry(el.dataset.notes);v.notes=el.value;save(el.dataset.notes,v);});
 $$("[data-score]").forEach(el=>el.onchange=()=>{let v=entry(el.dataset.score);v.score=el.value;save(el.dataset.score,v);});
 $$("[data-minutes]").forEach(el=>el.onchange=()=>{let v=entry(el.dataset.minutes);v.minutes=el.value;save(el.dataset.minutes,v);});
 $("#advExport").onclick=()=>download("hda-v3.8-advanced-mastery-progress.json",JSON.stringify({module:"advanced-professional-mastery",version:"3.8.0",exportedAt:new Date().toISOString(),state},null,2),"application/json");
 $("#advImport").onchange=async e=>{let f=e.target.files[0];if(!f)return;try{let x=JSON.parse(await f.text());if(x.module!=="advanced-professional-mastery"||!x.state||typeof x.state!=="object")throw Error();state=x.state;localStorage.setItem(KEY,JSON.stringify(state));render();alert("v3.8 progress imported.");}catch{alert("Invalid v3.8 backup.");}e.target.value="";};
}
function download(n,c,t){let u=URL.createObjectURL(new Blob([c],{type:t})),a=document.createElement("a");a.href=u;a.download=n;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
const $$=s=>[...document.querySelectorAll(s)];
document.addEventListener("DOMContentLoaded",()=>{let b=document.querySelector('[data-view="advanced-mastery"]');if(b)b.addEventListener("click",()=>{if(!$("#advancedMasteryApp").dataset.ready){render();$("#advancedMasteryApp").dataset.ready="1";}});});
})();