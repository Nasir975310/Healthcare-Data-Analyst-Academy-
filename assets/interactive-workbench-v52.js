/* v5.2 Interactive Healthcare Analytics Workbench — browser-local CSV analysis */
(()=>{
"use strict";
const host=document.getElementById("interactiveWorkbenchV52");if(!host)return;
let headers=[],rows=[],sourceName="",cleanRows=[],profile=[],required=[];
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function parseCSV(text){
 const out=[];let row=[],field="",quoted=false;
 for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];
  if(quoted){if(c==='"'&&n==='"'){field+='"';i++}else if(c==='"')quoted=false;else field+=c}
  else if(c==='"')quoted=true;
  else if(c===","){row.push(field);field=""}
  else if(c==="\n"){row.push(field);out.push(row);row=[];field=""}
  else if(c!=="\r")field+=c;
 }
 if(field.length||row.length){row.push(field);out.push(row)}
 if(out.length<2)throw Error("CSV needs a header and at least one data row.");
 const h=out.shift().map(x=>x.trim());
 if(h.some(x=>!x))throw Error("Blank column header detected.");
 if(new Set(h).size!==h.length)throw Error("Duplicate column names detected.");
 return {headers:h,rows:out.filter(r=>r.some(x=>x!=="")).map(r=>Object.fromEntries(h.map((k,i)=>[k,(r[i]??"").trim()])))};
}
function profileData(){
 profile=headers.map(k=>{const vals=rows.map(r=>r[k]??""),non=vals.filter(x=>x!==""),nums=non.map(Number).filter(Number.isFinite),numeric=non.length>0&&nums.length>=Math.max(3,Math.ceil(non.length*.7));
 return {name:k,missing:vals.length-non.length,distinct:new Set(non).size,numeric,nums: numeric?nums:[],min:numeric?Math.min(...nums):null,max:numeric?Math.max(...nums):null,mean:numeric?nums.reduce((a,b)=>a+b,0)/nums.length:null};});
}
function keyDuplicateRows(data,key){if(!key)return 0;const counts={};data.forEach(r=>{const x=(r[key]||"").trim();if(x)counts[x]=(counts[x]||0)+1});return data.filter(r=>r[key]&&counts[r[key]]>1).length}
function makeClean(){
 const key=document.getElementById("wbKey")?.value||"";
 const exact=document.getElementById("wbExact")?.checked||false;
 const dropMissing=document.getElementById("wbMissing")?.checked||false;
 const req=[...host.querySelectorAll("[data-required]:checked")].map(x=>x.dataset.required);
 let data=rows.map(r=>({...r}));
 let before=data.length,exactRemoved=0,missingRemoved=0;
 if(exact){const seen=new Set();data=data.filter(r=>{const sig=headers.map(h=>r[h]).join("\u001f");if(seen.has(sig)){exactRemoved++;return false}seen.add(sig);return true})}
 if(dropMissing&&req.length){const prior=data.length;data=data.filter(r=>req.every(k=>(r[k]||"").trim()!==""));missingRemoved=prior-data.length}
 if(key){const counts={};data.forEach(r=>{const x=(r[key]||"").trim();if(x)counts[x]=(counts[x]||0)+1});const prior=data.length;data=data.filter(r=>!(r[key]&&counts[r[key]]>1));missingRemoved+=prior-data.length}
 cleanRows=data;
 return {before,after:data.length,exactRemoved,missingRemoved,duplicateRows:keyDuplicateRows(rows,key),required:req};
}
function table(data,cols){return `<div class="table-wrap"><table><thead><tr>${cols.map(c=>`<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${data.slice(0,12).map(r=>`<tr>${cols.map(c=>`<td>${esc(r[c])}</td>`).join("")}</tr>`).join("")}</tbody></table></div><p class="muted">Showing ${Math.min(12,data.length)} of ${data.length} rows.</p>`}
function render(){
 host.innerHTML=`<article class="panel"><h3>1 · Load a CSV file</h3><p>Select a local CSV file. Processing occurs in this browser tab; the file is not sent to a server by this module. Start with the included synthetic sample.</p><input id="wbFile" type="file" accept=".csv,text/csv"><button class="secondary-small" id="wbSample">Load included sample</button><span id="wbStatus" class="muted">${rows.length?esc(sourceName):"No dataset loaded."}</span></article>
 <div id="wbResults">${rows.length?renderResults():"<article class='panel'><p>Load a CSV to begin profiling, cleaning and analysis.</p></article>"}</div>`;
 host.querySelector("#wbFile").addEventListener("change",async e=>{const f=e.target.files?.[0];if(!f)return;try{loadText(await f.text(),f.name)}catch(err){status(err.message)}});
 host.querySelector("#wbSample").addEventListener("click",async()=>{try{const r=await fetch("interactive_workbench_v52/data/workbench_sample.csv");if(!r.ok)throw Error("Sample file could not be loaded. Start the Academy from its local HTTP server.");loadText(await r.text(),"workbench_sample.csv")}catch(e){status(e.message)}});
}
function status(s){const el=host.querySelector("#wbStatus");if(el)el.textContent=s}
function loadText(text,name){const x=parseCSV(text);headers=x.headers;rows=x.rows;sourceName=name;profileData();render()}
function renderResults(){
 const dupCol=headers.includes("encounter_id")?"encounter_id":headers[0];
 const miss=profile.map(p=>({column:p.name,missing:p.missing,missing_pct:(p.missing/rows.length*100).toFixed(1)+"%",distinct:p.distinct}));
 const numeric=profile.filter(p=>p.numeric);
 const opts=headers.map(h=>`<option value="${esc(h)}">${esc(h)}</option>`).join("");
 return `<article class="panel"><h3>2 · Dataset overview</h3><div class="metric-grid"><div class="metric"><b>${rows.length}</b><span>Rows</span></div><div class="metric"><b>${headers.length}</b><span>Columns</span></div><div class="metric"><b>${keyDuplicateRows(rows,dupCol)}</b><span>Rows with duplicate ${esc(dupCol)}</span></div></div><h4>Column profile</h4>${table(miss,["column","missing","missing_pct","distinct"])}<details><summary>Numeric profile</summary>${numeric.length?`<div class="table-wrap"><table><thead><tr><th>Column</th><th>Min</th><th>Mean</th><th>Max</th></tr></thead><tbody>${numeric.map(p=>`<tr><td>${esc(p.name)}</td><td>${p.min.toFixed(2)}</td><td>${p.mean.toFixed(2)}</td><td>${p.max.toFixed(2)}</td></tr>`).join("")}</tbody></table></div>`:"No numeric columns detected."}</details></article>
 <article class="panel"><h3>3 · Cleaning preview</h3><p>Cleaning rules create a separate preview; the uploaded source remains unchanged. Duplicate-key handling removes all rows sharing a nonblank duplicate key, so investigate before accepting that rule.</p><label>Key column for duplicate detection</label><select id="wbKey">${opts}</select><div class="er-service"><label><input id="wbExact" type="checkbox"> Remove exact duplicate rows</label></div><div class="er-service"><label><input id="wbMissing" type="checkbox"> Exclude rows missing selected required fields</label></div><p><b>Required fields</b></p>${headers.map(h=>`<label class="er-service"><input type="checkbox" data-required="${esc(h)}"> ${esc(h)}</label>`).join("")}<button id="wbApply">Apply preview rules</button><div id="wbCleanSummary" class="muted">No cleaning rules applied.</div><div id="wbCleanTable"></div><button class="secondary-small" id="wbExportClean" disabled>Export cleaned CSV</button> <button class="secondary-small" id="wbExportQA">Export profile report</button></article>
 <article class="panel"><h3>4 · KPI calculator</h3><p>Enter a numerator and denominator. Define what each represents before interpreting the percentage.</p><label>Numerator</label><input id="wbNum" type="number" value="68"><label>Denominator</label><input id="wbDen" type="number" value="103"><label>Metric label</label><input id="wbMetric" value="SBP completeness"><div id="wbKpi" class="metric"><b>66.02%</b><span>Calculated percentage</span></div></article>
 <article class="panel"><h3>5 · Descriptive statistics</h3><label>Numeric column</label><select id="wbStatCol">${numeric.map(p=>`<option value="${esc(p.name)}">${esc(p.name)}</option>`).join("")}</select><div id="wbStats">Select a numeric column.</div><p class="muted">Mean, median and sample standard deviation are descriptive only. They do not establish clinical effects or causality.</p></article>
 <article class="panel"><h3>6 · SQL query starter</h3><p>Choose a query template to copy into DBeaver/SQLite. This workbench does not execute SQL.</p><select id="wbSql"><option value="dept">Encounter volume by department</option><option value="patients">Unique patients by department</option><option value="los">Discharged-only average LOS</option><option value="missing">SBP completeness</option></select><pre id="wbSqlText"></pre><button class="secondary-small" id="wbCopySql">Copy SQL</button><p class="muted">Templates: <code>interactive_workbench_v52/sql/query_templates.sql</code></p></article>
 <article class="panel"><h3>7 · Dashboard review checklist</h3>${["Metric has a written numerator, denominator and grain","Date range and inclusion/exclusion rules are visible","Missingness and data freshness are disclosed","Counts are not compared across unequal populations without normalization","Units, labels and chart scales are clear","Clinical interpretation does not exceed the evidence"].map((x,i)=>`<label class="er-service"><input type="checkbox" data-dash="${i}"> ${x}</label>`).join("")}<p class="muted">Checklist completion is self-attested, not an automated dashboard audit.</p></article>`;
}
function updateStats(){
 const col=host.querySelector("#wbStatCol")?.value;const p=profile.find(x=>x.name===col);if(!p||!p.numeric){host.querySelector("#wbStats").textContent="No numeric values detected.";return}
 const a=p.nums.slice().sort((x,y)=>x-y),n=a.length,mean=a.reduce((s,x)=>s+x,0)/n,med=n%2?a[(n-1)/2]:(a[n/2-1]+a[n/2])/2,sd=n>1?Math.sqrt(a.reduce((s,x)=>s+(x-mean)**2,0)/(n-1)):null;
 host.querySelector("#wbStats").innerHTML=`<div class="metric-grid"><div class="metric"><b>${mean.toFixed(2)}</b><span>Mean</span></div><div class="metric"><b>${med.toFixed(2)}</b><span>Median</span></div><div class="metric"><b>${sd===null?"—":sd.toFixed(2)}</b><span>Sample SD</span></div></div><p>Valid numeric observations: ${n}. Missing/non-numeric: ${rows.length-n}.</p>`;
}
const sqls={
dept:"SELECT department, COUNT(*) AS encounters FROM encounters GROUP BY department ORDER BY encounters DESC;",
patients:"SELECT department, COUNT(DISTINCT patient_id) AS unique_patients FROM encounters WHERE patient_id IS NOT NULL AND TRIM(patient_id) <> '' GROUP BY department;",
los:"SELECT AVG(julianday(discharge_date)-julianday(admit_date)) AS mean_los_days FROM encounters WHERE disposition='Discharged';",
missing:"SELECT COUNT(*) AS total_encounters, SUM(CASE WHEN sbp IS NOT NULL AND TRIM(CAST(sbp AS TEXT))<>'' THEN 1 ELSE 0 END) AS sbp_recorded FROM encounters;"
};
function wireResults(){
 const key=host.querySelector("#wbKey");
 host.querySelector("#wbApply").addEventListener("click",()=>{const r=makeClean();host.querySelector("#wbCleanSummary").textContent=`${r.before} raw rows → ${r.after} preview rows. Exact duplicates removed: ${r.exactRemoved}. Duplicate-key/missing-required exclusions: ${r.missingRemoved}. Key duplicate rows detected in raw data: ${r.duplicateRows}.`;host.querySelector("#wbCleanTable").innerHTML=table(cleanRows,headers);host.querySelector("#wbExportClean").disabled=false});
 host.querySelector("#wbExportClean").addEventListener("click",()=>{if(!cleanRows.length)return;download("cleaned_preview.csv",toCSV(headers,cleanRows),"text/csv")});
 host.querySelector("#wbExportQA").addEventListener("click",()=>{const report={source:sourceName,rows:rows.length,columns:headers,profile,duplicate_key_rows:keyDuplicateRows(rows,dupColName()),limitations:["Heuristic profiling; inspect data types and domain validity","Cleaning preview does not infer or repair values","No clinical or causal validation"]};download("csv_profile_report.json",JSON.stringify(report,null,2),"application/json")});
 const calc=()=>{const n=Number(host.querySelector("#wbNum").value),d=Number(host.querySelector("#wbDen").value),label=host.querySelector("#wbMetric").value;host.querySelector("#wbKpi").innerHTML=`<b>${Number.isFinite(n)&&Number.isFinite(d)&&d>0?(n/d*100).toFixed(2)+"%":"—"}</b><span>${esc(label)} · numerator ${n}, denominator ${d}</span>`};
 ["wbNum","wbDen","wbMetric"].forEach(id=>host.querySelector("#"+id).addEventListener("input",calc));
 host.querySelector("#wbStatCol").addEventListener("change",updateStats);updateStats();calc();
 const sql=host.querySelector("#wbSql"),show=()=>host.querySelector("#wbSqlText").textContent=sqls[sql.value];sql.addEventListener("change",show);show();
 host.querySelector("#wbCopySql").addEventListener("click",()=>{const t=sqls[sql.value];if(navigator.clipboard?.writeText)navigator.clipboard.writeText(t).then(()=>status("SQL copied."),()=>status("Copy unavailable; select and copy the query."));else status("Clipboard unavailable; select and copy the query.")});
}
function dupColName(){return headers.includes("encounter_id")?"encounter_id":headers[0]}
function toCSV(cols,data){const q=x=>{const s=String(x??"");return /[",\r\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s};return [cols.map(q).join(","),...data.map(r=>cols.map(c=>q(r[c])).join(","))].join("\r\n")}
function download(name,data,type){const u=URL.createObjectURL(new Blob([data],{type})),a=document.createElement("a");a.href=u;a.download=name;a.click();URL.revokeObjectURL(u)}
const oldRender=render;
render=function(){oldRender();if(rows.length)wireResults()};
render();
})();