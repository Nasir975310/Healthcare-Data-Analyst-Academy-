/* HDA Academy v4.1.0 — Interactive Healthcare Analytics Workbench */
(()=>{
"use strict";
const KEY="hda_interactive_workbench_v41";
const host=document.getElementById("interactiveWorkbenchApp");
if(!host)return;
const datasets=[
{id:"ops",name:"Hospital operations",file:"real_world_project_studio/interactive_workbench/data/operations_encounters.csv",description:"Encounter-level operations dataset",fields:["encounter_id","patient_id","department","admission_date","discharge_date","length_of_stay_days","age_years","readmission_flag"]},
{id:"due",name:"Antihypertensive DUE",file:"real_world_project_studio/interactive_workbench/data/antihypertensive_due_cohort.csv",description:"Synthetic patient-level DUE cohort",fields:["patient_id","age_years","sex","diabetes","baseline_sbp_mmhg","followup_sbp_mmhg","antihypertensive_class","prescribed_any_antihypertensive","followup_days"]},
{id:"pv",name:"Pharmacovigilance",file:"real_world_project_studio/interactive_workbench/data/pharmacovigilance_cases.csv",description:"Synthetic case-quality register",fields:["case_id","patient_age_years","suspect_drug","event_term","event_onset_day","report_received_day","serious_flag","outcome","duplicate_candidate_flag"]}
];
let state={dataset:"ops",search:"",category:"",group:"department",metric:"count",limit:25,quality:false,loaded:{},notes:""};
try{state={...state,...JSON.parse(localStorage.getItem(KEY)||"{}")}}catch(e){}
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const num=v=>v!==""&&v!==null&&Number.isFinite(Number(v));
function parseCSV(text){
 const rows=[];let row=[],field="",quoted=false;
 for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];
  if(quoted){if(c==='"'&&n==='"'){field+='"';i++}else if(c==='"')quoted=false;else field+=c;}
  else if(c==='"')quoted=true;else if(c===","){row.push(field);field=""}else if(c==="\n"){row.push(field);rows.push(row);row=[];field=""}else if(c!=="\r")field+=c;
 }
 if(field.length||row.length){row.push(field);rows.push(row)}
 const headers=rows.shift()||[];
 return rows.filter(r=>r.length===headers.length).map(r=>Object.fromEntries(headers.map((h,i)=>[h,r[i]])));
}
function filteredRows(){
 const d=state.loaded[state.dataset]||[];
 return d.filter(r=>{
  const q=state.search.toLowerCase();
  const searchOk=!q||Object.values(r).some(v=>String(v).toLowerCase().includes(q));
  const catOk=!state.category||String(r[categoryField()])===state.category;
  return searchOk&&catOk;
 });
}
function categoryField(){
 return state.dataset==="ops"?"department":state.dataset==="due"?"antihypertensive_class":"suspect_drug";
}
function metricValue(rows){
 const avg=(field)=>{const a=rows.map(r=>Number(r[field])).filter(Number.isFinite);return a.length?a.reduce((x,y)=>x+y,0)/a.length:null};
 if(state.dataset==="ops"){
  if(state.metric==="patients")return new Set(rows.map(r=>r.patient_id).filter(Boolean)).size;
  if(state.metric==="los")return avg("length_of_stay_days");
  if(state.metric==="flag") {const a=rows.filter(r=>num(r.readmission_flag));return a.length?a.reduce((s,r)=>s+Number(r.readmission_flag),0)/a.length*100:null}
 }
 if(state.dataset==="due"){
  if(state.metric==="sbpbase")return avg("baseline_sbp_mmhg");
  if(state.metric==="sbpfollow")return avg("followup_sbp_mmhg");
  if(state.metric==="change")return avg("followup_sbp_mmhg")-avg("baseline_sbp_mmhg");
  if(state.metric==="treated")return rows.length?rows.filter(r=>r.prescribed_any_antihypertensive==="1").length/rows.length*100:null;
 }
 if(state.dataset==="pv"){
  if(state.metric==="serious") {const a=rows.filter(r=>num(r.serious_flag));return a.length?a.filter(r=>r.serious_flag==="1").length/a.length*100:null}
  if(state.metric==="duplicates")return rows.filter(r=>r.duplicate_candidate_flag==="1").length;
 }
 return rows.length;
}
function metricLabel(){
 return ({count:"Filtered row count",patients:"Unique patients",los:"Mean length of stay (days)",flag:"Supplied flag proportion (%)",sbpbase:"Mean baseline SBP (mmHg)",sbpfollow:"Mean follow-up SBP (mmHg)",change:"Mean follow-up minus baseline SBP (mmHg)",treated:"Recorded prescribed proportion (%)",serious:"Serious case proportion (%)",duplicates:"Duplicate candidates (manual review)"})[state.metric]||"Filtered row count";
}
function groups(rows){
 const g={};rows.forEach(r=>{const k=r[state.group]||"(missing)";(g[k]??=[]).push(r)});
 return Object.entries(g).map(([label,rs])=>({label,n:rs.length,value:metricValue(rs)})).sort((a,b)=>(b.value??-Infinity)-(a.value??-Infinity));
}
function quality(rows){
 const d=state.dataset;let checks=[];
 const missing=(field)=>rows.filter(r=>!String(r[field]??"").trim()).length;
 if(d==="ops"){
  checks=[["Missing encounter IDs",missing("encounter_id")],["Duplicate encounter IDs",rows.length-new Set(rows.map(r=>r.encounter_id)).size],["Missing patient IDs",missing("patient_id")],["Discharge before admission",rows.filter(r=>r.discharge_date<r.admission_date).length],["Negative length of stay",rows.filter(r=>Number(r.length_of_stay_days)<0).length]];
 }else if(d==="due"){
  checks=[["Missing patient IDs",missing("patient_id")],["Duplicate patient IDs",rows.length-new Set(rows.map(r=>r.patient_id)).size],["Age outside 18–110",rows.filter(r=>Number(r.age_years)<18||Number(r.age_years)>110).length],["Baseline SBP outside 60–260",rows.filter(r=>Number(r.baseline_sbp_mmhg)<60||Number(r.baseline_sbp_mmhg)>260).length],["Follow-up SBP outside 60–260",rows.filter(r=>Number(r.followup_sbp_mmhg)<60||Number(r.followup_sbp_mmhg)>260).length]];
 }else{
  checks=[["Missing case IDs",missing("case_id")],["Duplicate case IDs",rows.length-new Set(rows.map(r=>r.case_id)).size],["Event after report receipt",rows.filter(r=>Number(r.event_onset_day)>Number(r.report_received_day)).length],["Duplicate candidates (manual review)",rows.filter(r=>r.duplicate_candidate_flag==="1").length],["Missing event terms",missing("event_term")]];
 }
 return checks;
}
function save(){try{localStorage.setItem(KEY,JSON.stringify({...state,loaded:{}}))}catch(e){}}
function download(name,text,type="text/csv"){const b=new Blob([text],{type});const a=document.createElement("a");a.href=URL.createObjectURL(b);a.download=name;a.click();URL.revokeObjectURL(a.href)}
function csv(rows){if(!rows.length)return "";const h=Object.keys(rows[0]);const q=v=>'"'+String(v??"").replace(/"/g,'""')+'"';return [h.map(q).join(","),...rows.map(r=>h.map(k=>q(r[k])).join(","))].join("\n")}
function render(){
 const rows=filteredRows(),summary=metricValue(rows),gs=groups(rows),qs=quality(rows);
 const d=datasets.find(x=>x.id===state.dataset);
 const metricOptions=state.dataset==="ops"?[["count","Row count"],["patients","Unique patients"],["los","Mean LOS"],["flag","Supplied flag %"]]:state.dataset==="due"?[["count","Row count"],["sbpbase","Mean baseline SBP"],["sbpfollow","Mean follow-up SBP"],["change","Mean SBP change"],["treated","Recorded prescribed %"]]:[["count","Case rows"],["serious","Serious proportion %"],["duplicates","Duplicate candidates"]];
 const groupsList=[...new Set((state.loaded[state.dataset]||[]).map(r=>r[categoryField()]).filter(Boolean))].sort();
 const fields=d.fields;
 host.innerHTML=`<div class="upgrade-stat-grid"><div class="upgrade-stat"><b>${(state.loaded[state.dataset]||[]).length.toLocaleString()}</b><span>Source rows loaded</span></div><div class="upgrade-stat"><b>${rows.length.toLocaleString()}</b><span>Rows after filters</span></div><div class="upgrade-stat"><b>${summary===null||!Number.isFinite(summary)?"—":Number(summary).toFixed(2)}</b><span>${esc(metricLabel())}</span></div><div class="upgrade-stat"><b>${qs.reduce((s,x)=>s+x[1],0)}</b><span>Findings in selected quality checks</span></div></div>
 <article class="panel module-note"><b>Browser-side exploration</b><p>${esc(d.description)}. The CSV is read locally by this browser; no upload or external service is used. Filters and metrics are exploratory and must be validated independently before reporting.</p><div class="workbench-controls"><label>Dataset <select id="wbDataset">${datasets.map(x=>`<option value="${x.id}" ${x.id===state.dataset?"selected":""}>${x.name}</option>`).join("")}</select></label><label>Search all fields <input id="wbSearch" value="${esc(state.search)}" placeholder="Search value or ID"></label><label>Filter ${esc(categoryField())}<select id="wbCategory"><option value="">All categories</option>${groupsList.map(x=>`<option ${state.category===x?"selected":""}>${esc(x)}</option>`).join("")}</select></label><label>KPI <select id="wbMetric">${metricOptions.map(([v,l])=>`<option value="${v}" ${state.metric===v?"selected":""}>${l}</option>`).join("")}</select></label></div><p class="small muted">Fields: ${fields.map(esc).join(" · ")}</p></article>
 <div class="grid-2"><article class="panel"><h3>Group comparison</h3><label>Group by <select id="wbGroup">${fields.filter(x=>!["encounter_id","patient_id","case_id"].includes(x)).map(x=>`<option ${state.group===x?"selected":""}>${x}</option>`).join("")}</select></label><div class="wb-bars">${gs.map(g=>`<div class="wb-bar-row"><span>${esc(g.label)}</span><div class="wb-bar-track"><i style="width:${Math.max(0,Math.min(100,(Number(g.value)||0)/(Math.max(1,...gs.map(x=>Number(x.value)||0)))*100))}%"></i></div><b>${g.value===null?"—":Number(g.value).toFixed(2)}</b><small>n=${g.n}</small></div>`).join("")}</div><button class="secondary-btn" id="wbExportGroups">Export grouped summary</button></article>
 <article class="panel"><h3>Data-quality checks</h3><p class="small muted">Checks apply to the filtered rows, not automatically to the full source.</p>${qs.map(([l,n])=>`<div class="wb-quality-row"><span>${esc(l)}</span><b>${n}</b></div>`).join("")}<button class="secondary-btn" id="wbExportQuality">Export quality results</button></article></div>
 <article class="panel"><h3>Filtered row preview</h3><p class="small muted">Showing first ${Math.min(25,rows.length)} of ${rows.length} filtered rows.</p><div class="table-scroll"><table><thead><tr>${fields.map(x=>`<th>${esc(x)}</th>`).join("")}</tr></thead><tbody>${rows.slice(0,25).map(r=>`<tr>${fields.map(x=>`<td>${esc(r[x])}</td>`).join("")}</tr>`).join("")}</tbody></table></div><button class="secondary-btn" id="wbExportRows">Export filtered rows</button></article>
 <article class="panel"><h3>Interpretation checkpoint</h3><ul><li>State the unit of analysis and denominator.</li><li>Explain how filters change the cohort and the metric.</li><li>Check missingness, duplicates and join cardinality before trusting totals.</li><li>Separate descriptive association from causal inference.</li><li>Document data provenance, limitations and intended audience.</li></ul><p><b>Dataset-specific caution:</b> ${state.dataset==="ops"?"The supplied flag is not a validated readmission measure.":state.dataset==="due"?"Prescription does not establish dispensing, administration or adherence; group differences are not causal.":"Duplicate candidates require manual review; case counts are not incidence or comparative risk."}</p><label>My interpretation / questions</label><textarea id="wbNotes" rows="4" placeholder="Write a concise interpretation with denominator and limitations">${esc(state.notes)}</textarea><button class="secondary-btn" id="wbSaveNotes">Save notes locally</button></article>`;
 $("#wbDataset").addEventListener("change",e=>{state.dataset=e.target.value;state.search="";state.category="";state.group=state.dataset==="ops"?"department":state.dataset==="due"?"antihypertensive_class":"suspect_drug";state.metric="count";render()});
 $("#wbSearch").addEventListener("change",e=>{state.search=e.target.value;render()});
 $("#wbCategory").addEventListener("change",e=>{state.category=e.target.value;render()});
 $("#wbMetric").addEventListener("change",e=>{state.metric=e.target.value;render()});
 $("#wbGroup").addEventListener("change",e=>{state.group=e.target.value;render()});
 $("#wbExportRows").addEventListener("click",()=>download(state.dataset+"_filtered_rows.csv",csv(rows)));
 $("#wbExportGroups").addEventListener("click",()=>download(state.dataset+"_group_summary.csv",csv(gs.map(x=>({group:x.label,row_count:x.n,metric:metricLabel(),value:x.value})))));
 $("#wbExportQuality").addEventListener("click",()=>download(state.dataset+"_quality_checks.csv",csv(qs.map(x=>({check:x[0],finding_count:x[1]})))));
 $("#wbSaveNotes").addEventListener("click",()=>{state.notes=$("#wbNotes").value;save();alert("Notes saved locally in this browser.")});
}
async function loadAll(){
 for(const d of datasets){
  try{const r=await fetch(d.file);if(!r.ok)throw Error("HTTP "+r.status);state.loaded[d.id]=parseCSV(await r.text())}
  catch(e){host.innerHTML=`<article class="panel"><b>Could not load ${esc(d.file)}</b><p>${esc(e.message)}. Start the academy with <code>python -m http.server 8000</code> from its root folder, then reload.</p></article>`;return}
 }
 render();
}
loadAll();
})();
