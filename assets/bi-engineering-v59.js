/* v5.9 BI engineering learning view */
(()=>{
"use strict";
const host=document.getElementById("biEngineeringV59"); if(!host)return;
const tasks=[
"State the fact-table grain and explain why it prevents double counting.",
"Create one-to-many, single-direction relationships from Date and Department dimensions.",
"Mark the date dimension as the model date table.",
"Create explicit measures for encounter count, unique patients and IPD share.",
"Validate monthly totals against the SQL semantic view.",
"Test blank periods and zero denominators with DIVIDE.",
"Create and test department-level row-level security roles.",
"Use Performance Analyzer to identify expensive visuals.",
"Publish metric definitions, refresh cadence and data limitations."
];
host.innerHTML=`<article class="panel"><h3>BI engineering workbench</h3><p>Design a governed Power BI semantic model from a synthetic encounter dataset. This page is a learning guide; it does not execute DAX, Power Query M or create PBIX files.</p><div class="metric-grid"><div class="metric"><b>20</b><span>Synthetic encounters</span></div><div class="metric"><b>3</b><span>Dashboard blueprints</span></div><div class="metric"><b>10+</b><span>DAX measures</span></div></div></article>
<article class="panel"><h3>1 · Data model contract</h3><p><b>Fact grain:</b> one row per encounter. Dimensions: Date and Department. Use one-to-many relationships, dimension-to-fact single-direction filtering and explicit measures.</p><p class="muted">Unique patient counts are non-additive across departments. Charges are not necessarily revenue or collected cash.</p></article>
<article class="panel"><h3>2 · Build sequence</h3><ol><li>Import <code>data/encounters.csv</code>.</li><li>Apply type and quality transformations from <code>powerquery/transform_encounters.m</code>.</li><li>Build Date and Department dimensions.</li><li>Create relationships and mark the Date table.</li><li>Add measures from <code>powerbi/measures.dax</code>.</li><li>Build audience-specific dashboards and validate totals.</li><li>Configure RLS and test each role before publishing.</li></ol></article>
<article class="panel"><h3>3 · Learning checkpoints</h3><div id="bi59Tasks">${tasks.map((t,i)=>`<label style="display:block;margin:10px 0"><input type="checkbox" data-bi59="${i}"> ${t}</label>`).join("")}</div><p id="bi59Progress" class="muted">0 of ${tasks.length} completed.</p></article>
<article class="panel"><h3>4 · Execute local semantic validation</h3><pre><code>python scripts/run_semantic_validation.py</code></pre><p>Expected: PASS, 20 fixture rows and 20 semantic rows. This validates the SQLite equivalent only; it does not validate Power BI DAX or M.</p></article>
<article class="panel"><h3>5 · Deliverable acceptance criteria</h3><ul><li>Fact grain and relationships documented.</li><li>All dashboard totals reconcile to SQL.</li><li>Metric definitions include numerator, denominator and exclusions.</li><li>RLS tested using representative identities.</li><li>Refresh timestamp, data lineage and limitations disclosed.</li><li>Dashboard labels distinguish charges from revenue and encounters from admissions.</li></ul></article>`;
const checks=[...host.querySelectorAll("[data-bi59]")];
checks.forEach(x=>x.addEventListener("change",()=>{const n=checks.filter(c=>c.checked).length;host.querySelector("#bi59Progress").textContent=`${n} of ${tasks.length} completed.`;}));
})();