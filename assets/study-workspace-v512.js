/* v5.12 universal study workspace — client-side protocol builder */
(()=>{
"use strict";
const host=document.getElementById("studyWorkspaceV512"); if(!host)return;
const designs={
 observational_cohort:{label:"Observational cohort",required:["index_date","exposure","comparator","outcome","follow_up","confounders"],steps:["Define population and eligibility","Set index date and exposure window","Define comparator strategy","Specify baseline look-back and covariates","Define outcome and follow-up","Specify censoring and analysis"]},
 case_control:{label:"Case-control",required:["case_definition","control_selection","index_date","exposure_window","matching_or_adjustment"],steps:["Define case rule","Specify control source and sampling","Set index date","Define exposure window","Specify matching and adjustment"]},
 cross_sectional:{label:"Cross-sectional",required:["sampling_frame","measurement_period","outcome_definition","sampling_method"],steps:["Define target population and sampling frame","Specify measurement period","Define outcome and instrument","Specify sampling and non-response","Plan prevalence estimates"]},
 randomized_trial:{label:"Randomized controlled trial",required:["intervention","comparator","randomization","primary_outcome","follow_up","analysis_population"],steps:["Specify eligibility","Define intervention and comparator","Specify randomisation and concealment","Define primary endpoint and time point","Prespecify analysis population","Specify safety monitoring"]},
 diagnostic_accuracy:{label:"Diagnostic accuracy",required:["target_condition","index_test","reference_standard","threshold","blinding"],steps:["Define target condition","Specify index test and threshold","Specify reference standard","Define participant spectrum","Plan diagnostic metrics","Address indeterminate results"]},
 case_series:{label:"Case series",required:["case_definition","case_ascertainment","observation_period","descriptive_plan"],steps:["Define case and inclusion criteria","Specify ascertainment and setting","Set observation period","Define variables and missingness","Prespecify descriptive summaries"]},
 registry_longitudinal:{label:"Registry / longitudinal",required:["enrolment_rule","time_origin","visit_schedule","outcome","loss_to_follow_up"],steps:["Define registry population","Specify time origin and repeated measures","Define visit schedule","Specify outcome and event capture","Plan missing visits and loss-to-follow-up"]}
};
const roles=["exposure","comparator","outcome","covariate","demographic","process","safety","identifier","other"];
const types=["integer","decimal","string","date","datetime","boolean","category"];
let variables=[{name:"exposure_group",role:"exposure",data_type:"category",unit:"",definition:"Define the baseline exposure classification",allowed_values:"exposed, unexposed"},{name:"primary_outcome",role:"outcome",data_type:"boolean",unit:"",definition:"Define the primary outcome and ascertainment rule",allowed_values:""}];
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
host.innerHTML=`<style>
.sw512{display:grid;gap:14px}.sw512 .panel{border:1px solid var(--border);border-radius:14px;padding:14px;background:var(--panel,rgba(127,127,127,.06))}.sw512 .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.sw512 label{display:grid;gap:5px;font-size:.9rem}.sw512 input,.sw512 select,.sw512 textarea{width:100%;min-width:0;padding:9px;border:1px solid var(--border);border-radius:9px;background:var(--bg,transparent);color:inherit;font:inherit}.sw512 textarea{min-height:72px}.sw512 button{padding:9px 12px;border:1px solid var(--border);border-radius:9px;background:var(--panel);color:inherit;cursor:pointer}.sw512 .primary{background:rgba(37,99,235,.18);border-color:#3b82f6}.sw512 .var{border:1px solid var(--border);border-radius:12px;padding:12px;display:grid;gap:9px}.sw512 .muted{opacity:.72;font-size:.85rem}.sw512 .actions{display:flex;gap:8px;flex-wrap:wrap}.sw512 .check{display:flex;gap:8px;align-items:flex-start}.sw512 .check input{width:auto;margin-top:4px}
@media(max-width:640px){.sw512 .grid{grid-template-columns:1fr}}
</style>
<div class="sw512">
 <section class="panel"><div class="muted">UNIVERSAL RESEARCH DESIGN · v5.12.0</div><h2 style="margin:5px 0">Study specification builder</h2><p class="muted">Create a reusable study plan for different diseases, healthcare domains and study designs. This tool stores no patient-level records.</p><div class="grid">
  <label>Study title<input id="sTitle" value="New study specification"></label>
  <label>Study design<select id="sDesign">${Object.entries(designs).map(([k,v])=>`<option value="${k}">${v.label}</option>`).join("")}</select></label>
  <label>Domain / disease area<input id="sDomain" placeholder="e.g. diabetes, oncology, service evaluation"></label>
  <label>Setting<input id="sSetting" placeholder="e.g. tertiary hospital, registry, community"></label>
 </div><label style="margin-top:10px">Research question<textarea id="sQuestion" placeholder="State population, exposure/intervention, comparator and outcome where relevant"></textarea></label></section>
 <section class="panel"><h3>1 · Population and time</h3><div class="grid">
  <label>Target population<input id="sPopulation" placeholder="Who is eligible for this study?"></label>
  <label>Index date / time origin<input id="sIndex" placeholder="e.g. first eligible encounter"></label>
  <label>Baseline look-back<input id="sLookback" placeholder="e.g. 12 months before index"></label>
  <label>Follow-up / measurement period<input id="sFollowup" placeholder="e.g. 180 days after index"></label>
 </div><label style="margin-top:10px">Inclusion criteria<textarea id="sInclusion" placeholder="One criterion per line"></textarea></label><label style="margin-top:10px">Exclusion criteria<textarea id="sExclusion" placeholder="One criterion per line"></textarea></label></section>
 <section class="panel"><h3>2 · Design-specific planning</h3><p class="muted">Use this as a prompt list. Required topics differ by design and must be completed in the formal protocol.</p><div id="sWorkflow"></div><div id="sRequired" class="muted" style="margin-top:8px"></div></section>
 <section class="panel"><div style="display:flex;justify-content:space-between;gap:10px;align-items:center;flex-wrap:wrap"><h3 style="margin:0">3 · Variable dictionary</h3><button id="sAdd">+ Add variable</button></div><p class="muted">Define each variable's role, type, unit and operational meaning. Avoid patient identifiers in analytical extracts.</p><div id="sVariables" style="display:grid;gap:9px;margin-top:10px"></div></section>
 <section class="panel"><h3>4 · Review and export</h3><div class="actions"><button class="primary" id="sValidate">Validate specification</button><button id="sExport">Export JSON</button><button id="sLoadExample">Load generic example</button><button id="sReset">Reset</button></div><div id="sResult" class="muted" style="margin-top:12px" aria-live="polite">Complete the required fields, then validate. Validation checks structure and common omissions, not scientific validity.</div></section>
</div>`;
const $=id=>host.querySelector("#"+id);
function renderWorkflow(){
 const d=designs[$("sDesign").value];
 $("sWorkflow").innerHTML="<ol>"+d.steps.map(x=>`<li>${esc(x)}</li>`).join("")+"</ol>";
 $("sRequired").textContent="Design-specific topics to confirm: "+d.required.join(", ");
}
function renderVars(){
 $("sVariables").innerHTML=variables.map((v,i)=>`<div class="var" data-var="${i}">
 <div class="actions" style="justify-content:space-between"><b>Variable ${i+1}</b><button data-remove="${i}" ${variables.length===1?"disabled":""}>Remove</button></div>
 <div class="grid">
 <label>Machine name<input data-field="name" value="${esc(v.name)}" placeholder="e.g. systolic_bp"></label>
 <label>Role<select data-field="role">${roles.map(x=>`<option ${v.role===x?"selected":""}>${x}</option>`).join("")}</select></label>
 <label>Data type<select data-field="data_type">${types.map(x=>`<option ${v.data_type===x?"selected":""}>${x}</option>`).join("")}</select></label>
 <label>Unit<input data-field="unit" value="${esc(v.unit)}" placeholder="e.g. mmHg, years, days"></label>
 </div>
 <label>Operational definition<textarea data-field="definition">${esc(v.definition)}</textarea></label>
 <label>Allowed values (comma separated for categories)<input data-field="allowed_values" value="${esc(v.allowed_values)}" placeholder="e.g. mild, moderate, severe"></label>
 </div>`).join("");
 $("sVariables").querySelectorAll("[data-field]").forEach(el=>el.addEventListener("input",e=>{
  const card=e.target.closest("[data-var]"),i=Number(card.dataset.var);variables[i][e.target.dataset.field]=e.target.value;
 }));
 $("sVariables").querySelectorAll("[data-remove]").forEach(b=>b.addEventListener("click",()=>{variables.splice(Number(b.dataset.remove),1);renderVars();}));
}
function lines(id){return $(id).value.split(/\r?\n/).map(x=>x.trim()).filter(Boolean)}
function build(){
 return {schema_version:"1.0",study_title:$("sTitle").value.trim(),study_design:$("sDesign").value,research_question:$("sQuestion").value.trim(),disease_or_domain:$("sDomain").value.trim(),setting:$("sSetting").value.trim(),population:{target_population:$("sPopulation").value.trim(),inclusion_criteria:lines("sInclusion"),exclusion_criteria:lines("sExclusion")},time:{index_date:$("sIndex").value.trim(),lookback:$("sLookback").value.trim(),follow_up:$("sFollowup").value.trim()},variables:variables.map(v=>({name:v.name.trim(),role:v.role,data_type:v.data_type,unit:v.unit.trim(),definition:v.definition.trim(),allowed_values:v.allowed_values.split(",").map(x=>x.trim()).filter(Boolean)}))};
}
function validate(){
 const s=build(),errors=[],warnings=[];
 if(s.study_title.length<3)errors.push("Study title must contain at least 3 characters.");
 if(s.research_question.length<10)errors.push("Research question must be at least 10 characters.");
 if(s.population.target_population.length<3)errors.push("Define the target population.");
 if(!s.population.inclusion_criteria.length)errors.push("Add at least one inclusion criterion.");
 if(!s.variables.length)errors.push("Add at least one variable.");
 const names=new Set();
 s.variables.forEach((v,i)=>{
  if(!/^[A-Za-z][A-Za-z0-9_]*$/.test(v.name))errors.push(`Variable ${i+1}: use a valid machine name (letters, numbers, underscore).`);
  if(names.has(v.name.toLowerCase()))errors.push(`Duplicate variable name: ${v.name}`);names.add(v.name.toLowerCase());
  if(v.definition.length<5)errors.push(`Variable ${i+1}: add a meaningful operational definition.`);
  if(v.role==="identifier")warnings.push(`Variable ${v.name}: privacy review required for identifier-like data.`);
  if(v.data_type==="category"&&!v.allowed_values.length)warnings.push(`Variable ${v.name}: define permissible category values.`);
 });
 if(s.study_design==="observational_cohort"&&!s.variables.some(v=>v.role==="exposure"))warnings.push("Cohort design: explicitly define an exposure variable.");
 if(s.study_design==="observational_cohort"&&!s.variables.some(v=>v.role==="outcome"))warnings.push("Cohort design: explicitly define an outcome variable.");
 const d=designs[s.study_design];
 if(!s.time.index_date)warnings.push("Confirm the design-specific time origin or index date.");
 if(!s.time.follow_up)warnings.push("Specify follow-up or measurement period where applicable.");
 $("sResult").innerHTML=`<b>${errors.length?"Needs correction":"Structural checks passed"}</b><p>${errors.length?errors.map(esc).join("<br>"):"No blocking structural errors detected."}</p>${warnings.length?`<b>Review warnings</b><p>${warnings.map(esc).join("<br>")}</p>`:"<p>No automated warnings.</p>"}<p class="muted">This does not assess bias, sample size, ethics, statistical assumptions or clinical correctness.</p>`;
 return {s,errors,warnings};
}
$("sDesign").addEventListener("change",renderWorkflow);
$("sAdd").addEventListener("click",()=>{variables.push({name:"new_variable_"+(variables.length+1),role:"covariate",data_type:"string",unit:"",definition:"",allowed_values:""});renderVars();});
$("sValidate").addEventListener("click",validate);
$("sExport").addEventListener("click",()=>{
 const r=validate();if(r.errors.length){$("sResult").scrollIntoView({behavior:"smooth",block:"center"});return;}
 const blob=new Blob([JSON.stringify(r.s,null,2)],{type:"application/json"});
 const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="study_specification.json";a.click();URL.revokeObjectURL(url);
});
$("sLoadExample").addEventListener("click",()=>{
 $("sTitle").value="Example: longitudinal service outcome evaluation";$("sDesign").value="observational_cohort";
 $("sDomain").value="Generic service evaluation";$("sSetting").value="Synthetic teaching example";
 $("sQuestion").value="Among eligible service users, is baseline programme exposure associated with a later service outcome?";
 $("sPopulation").value="Eligible service users";$("sIndex").value="First eligible encounter";$("sLookback").value="365 days before index";$("sFollowup").value="180 days after index";
 $("sInclusion").value="Meets prespecified criteria\nHas a valid index date";$("sExclusion").value="Outside observation period";
 variables=[{name:"participant_key",role:"identifier",data_type:"string",unit:"",definition:"Pseudonymous teaching identifier",allowed_values:""},{name:"exposure_group",role:"exposure",data_type:"category",unit:"",definition:"Baseline exposure classification",allowed_values:"exposed, unexposed"},{name:"outcome_event",role:"outcome",data_type:"boolean",unit:"",definition:"Whether the prespecified event occurred",allowed_values:""},{name:"age_years",role:"covariate",data_type:"integer",unit:"years",definition:"Age at index date",allowed_values:""}];
 renderWorkflow();renderVars();$("sResult").textContent="Generic synthetic example loaded. Review and edit before exporting.";
});
$("sReset").addEventListener("click",()=>{host.querySelectorAll("input,textarea").forEach(x=>x.value="");$("sTitle").value="New study specification";$("sDesign").value="observational_cohort";variables=[{name:"exposure_group",role:"exposure",data_type:"category",unit:"",definition:"Define the baseline exposure classification",allowed_values:"exposed, unexposed"},{name:"primary_outcome",role:"outcome",data_type:"boolean",unit:"",definition:"Define the primary outcome and ascertainment rule",allowed_values:""}];renderWorkflow();renderVars();$("sResult").textContent="Draft reset. No patient-level data was stored."});
renderWorkflow();renderVars();
})();