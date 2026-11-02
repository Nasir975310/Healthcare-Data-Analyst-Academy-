/* v5.13 data dictionary and validation engine interface */
(()=>{
"use strict";
const host=document.getElementById("dataValidationV513");if(!host)return;
const terms=[
{name:"participant_id",label:"Participant identifier",role:"identifier",type:"string",unit:"—",definition:"Study-specific pseudonymous participant key.",rule:"Required where configured; avoid direct identifiers in analytical extracts."},
{name:"encounter_id",label:"Encounter identifier",role:"identifier",type:"string",unit:"—",definition:"Unique key for an encounter-level record.",rule:"Configured as a unique key; duplicate values are errors."},
{name:"age_years",label:"Age",role:"covariate",type:"integer",unit:"years",definition:"Age at the prespecified index date.",rule:"Example range 0–120 is a broad technical plausibility screen."},
{name:"encounter_date",label:"Encounter date",role:"process",type:"date",unit:"YYYY-MM-DD",definition:"Calendar date on which the encounter occurred.",rule:"Must parse as an ISO 8601 date."},
{name:"systolic_bp_mmhg",label:"Systolic blood pressure",role:"outcome",type:"decimal",unit:"mmHg",definition:"Systolic blood pressure measured using the protocol-defined method.",rule:"Example range 40–300 is not a clinical reference interval."},
{name:"diastolic_bp_mmhg",label:"Diastolic blood pressure",role:"outcome",type:"decimal",unit:"mmHg",definition:"Diastolic blood pressure measured using the protocol-defined method.",rule:"Cross-field warning if diastolic exceeds systolic."},
{name:"exposure_group",label:"Exposure group",role:"exposure",type:"category",unit:"—",definition:"Prespecified exposure classification at the defined time origin.",rule:"Allowed values in the example: exposed, unexposed."},
{name:"primary_outcome",label:"Primary outcome",role:"outcome",type:"boolean",unit:"—",definition:"Whether the protocol-defined primary outcome occurred in its specified window.",rule:"Allowed values configured explicitly; no automatic endpoint derivation."}
];
const rules=[
["Completeness","Required fields and blank-cell profile","Missing required values are errors; overall blank-cell percentage is descriptive."],
["Uniqueness","Duplicate key detection","Configured unique columns are checked across the file."],
["Type and format","Numeric, date and category validation","Checks parseability and configured allowed values."],
["Range plausibility","Configurable numeric minimum and maximum","Warnings by default; thresholds are not clinical reference intervals."],
["Temporal logic","Index date and follow-up ordering","Configured end date cannot precede start date."],
["Cross-field logic","Relationships between multiple variables","Example: diastolic pressure should not exceed systolic pressure; flagged for review."]
];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
host.innerHTML=`<style>
.dv513{display:grid;gap:14px}.dv513 .panel{padding:14px;border:1px solid var(--border);border-radius:14px;background:var(--panel,rgba(127,127,127,.06))}.dv513 .stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.dv513 .stat{padding:12px;border:1px solid var(--border);border-radius:11px}.dv513 .stat b{display:block;font-size:1.25rem}.dv513 .muted{opacity:.72;font-size:.86rem}.dv513 input,.dv513 select{padding:9px;border:1px solid var(--border);border-radius:9px;background:var(--bg,transparent);color:inherit;font:inherit;min-width:0}.dv513 button{padding:8px 11px;border:1px solid var(--border);border-radius:9px;background:var(--panel);color:inherit;cursor:pointer}.dv513 .controls{display:flex;gap:8px;flex-wrap:wrap}.dv513 .list{display:grid;gap:8px}.dv513 .entry{padding:12px;border:1px solid var(--border);border-radius:11px}.dv513 .entry summary{cursor:pointer;font-weight:650}.dv513 .table{width:100%;border-collapse:collapse}.dv513 .table td,.dv513 .table th{padding:9px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}.dv513 code{overflow-wrap:anywhere}.dv513 .callout{padding:12px;border-radius:10px;background:rgba(37,99,235,.09)}@media(max-width:600px){.dv513 .stats{grid-template-columns:1fr}.dv513 .table{font-size:.82rem}}
</style><div class="dv513">
<section class="panel"><div class="muted">DATA QUALITY ENGINEERING · v5.13.0</div><h2 style="margin:5px 0">Universal data dictionary & validation engine</h2><p class="muted">Configurable rules for different diseases, domains, datasets and study designs. The Python engine performs deterministic CSV validation; this page explores the dictionary and rule framework.</p><div class="stats"><div class="stat"><b>8</b><span class="muted">Starter variables</span></div><div class="stat"><b>6</b><span class="muted">Rule families</span></div><div class="stat"><b>3</b><span class="muted">Report formats</span></div></div></section>
<section class="panel"><h3>1 · Explore the variable dictionary</h3><div class="controls"><input id="dvSearch" type="search" placeholder="Search variable, role or definition" aria-label="Search variable dictionary" style="flex:1"><select id="dvRole"><option value="all">All roles</option>${[...new Set(terms.map(t=>t.role))].map(x=>`<option>${x}</option>`).join("")}</select></div><div id="dvTerms" class="list" style="margin-top:10px"></div></section>
<section class="panel"><h3>2 · Validation rule library</h3><div class="list">${rules.map(r=>`<details class="entry"><summary>${esc(r[0])} — ${esc(r[1])}</summary><p class="muted">${esc(r[2])}</p></details>`).join("")}</div></section>
<section class="panel"><h3>3 · Run the executable validator</h3><p>From the <code>data_validation_v513</code> folder:</p><pre><code>python scripts/validate_dataset.py</code></pre><p>Windows PowerShell:</p><pre><code>py scripts\\validate_dataset.py</code></pre><p class="muted">Custom input: <code>python scripts/validate_dataset.py --input path/to/data.csv --output-dir output</code></p><div class="callout"><b>Generated outputs</b><ul><li><code>output/validation_report.json</code> — machine-readable results</li><li><code>output/issues.csv</code> — row-level findings</li><li><code>output/quality_report.html</code> — review report</li></ul></div></section>
<section class="panel"><h3>4 · Interpretation safeguards</h3><ul><li>Configured errors block a PASS result; warnings require review.</li><li>A range rule is a technical plausibility screen, not a clinical reference interval.</li><li>Completeness is not the same as data accuracy.</li><li>A clean report does not establish absence of bias or scientific validity.</li><li>No imputation, statistical inference or clinical decision is performed.</li></ul></section>
</div>`;
const list=host.querySelector("#dvTerms");
function render(){
 const q=host.querySelector("#dvSearch").value.toLowerCase(),role=host.querySelector("#dvRole").value;
 const rows=terms.filter(t=>(role==="all"||t.role===role)&&[t.name,t.label,t.role,t.definition,t.rule].join(" ").toLowerCase().includes(q));
 list.innerHTML=rows.length?rows.map(t=>`<details class="entry"><summary>${esc(t.label)} <span class="muted">· ${esc(t.name)}</span></summary><p><b>Role:</b> ${esc(t.role)} · <b>Type:</b> ${esc(t.type)} · <b>Unit:</b> ${esc(t.unit)}</p><p class="muted">${esc(t.definition)}</p><p class="muted"><b>Validation:</b> ${esc(t.rule)}</p></details>`).join(""):'<p class="muted">No matching variables.</p>';
}
host.querySelector("#dvSearch").addEventListener("input",render);
host.querySelector("#dvRole").addEventListener("change",render);
render();
})();