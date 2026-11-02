/* v5.3 Healthcare Analytics Dashboard Studio */
(()=>{
"use strict";
const host=document.getElementById("dashboardStudioV53");if(!host)return;
let headers=[],rows=[],filename="",filtered=[],groups=[],chartSvg="",qa=[];
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function parse(text){const out=[];let row=[],f="",q=false;for(let i=0;i<text.length;i++){let c=text[i],n=text[i+1];if(q){if(c==='"'&&n==='"'){f+='"';i++}else if(c==='"')q=false;else f+=c}else if(c==='"')q=true;else if(c===","){row.push(f);f=""}else if(c==="\n"){row.push(f);out.push(row);row=[];f=""}else if(c!=="\r")f+=c}if(f||row.length){row.push(f);out.push(row)}if(out.length<2)throw Error("CSV requires a header and data rows.");headers=out.shift().map(x=>x.trim());if(new Set(headers).size!==headers.length||headers.some(x=>!x))throw Error("Column names must be unique and nonblank.");rows=out.filter(r=>r.some(x=>x!=="")).map(r=>Object.fromEntries(headers.map((h,i)=>[h,(r[i]??"").trim()])));filename="uploaded.csv"}
const options=(arr,sel)=>arr.map(x=>`<option value="${esc(x)}" ${x===sel?"selected":""}>${esc(x)}</option>`).join("");
function render(){host.innerHTML=`<article class="panel"><h3>1 · Load dashboard data</h3><input type="file" id="dsFile" accept=".csv,text/csv"><button class="secondary-small" id="dsSample">Load synthetic sample</button><span id="dsStatus" class="muted">${rows.length?esc(filename):"No dataset loaded."}</span></article><div id="dsApp">${rows.length?controls():"<article class='panel'>Load a CSV to build a dashboard.</article>"}</div>`;
host.querySelector("#dsFile").addEventListener("change",async e=>{let f=e.target.files?.[0];if(!f)return;try{parse(await f.text());render()}catch(x){host.querySelector("#dsStatus").textContent=x.message}});
host.querySelector("#dsSample").addEventListener("click",async()=>{try{let r=await fetch("dashboard_studio_v53/data/dashboard_sample.csv");if(!r.ok)throw Error("Start the Academy using its local HTTP server.");parse(await r.text());filename="dashboard_sample.csv";render()}catch(x){host.querySelector("#dsStatus").textContent=x.message}});
}
function controls(){
const date=headers.find(x=>/date|time/i.test(x))||headers[0],dept=headers.find(x=>/department|dept/i.test(x))||headers[0],patient=headers.find(x=>/patient/i.test(x))||headers[0];
const nums=headers.filter(h=>rows.some(r=>r[h]!==""&&Number.isFinite(Number(r[h]))));
return `<article class="panel"><h3>2 · Dashboard configuration</h3><div class="module-toolbar"><label>Date field<select id="dsDate">${options(headers,date)}</select></label><label>Department/category field<select id="dsDept">${options(headers,dept)}</select></label><label>Category filter<select id="dsFilter"><option value="">All categories</option>${[...new Set(rows.map(r=>r[dept]).filter(Boolean))].sort().map(x=>`<option>${esc(x)}</option>`).join("")}</select></label><label>Start date<input id="dsStart" type="date"></label><label>End date<input id="dsEnd" type="date"></label><label>Metric<select id="dsMetric"><option value="rows">Encounter/row count</option><option value="patients">Unique patients</option>${nums.map(n=>`<option value="${esc(n)}">Average ${esc(n)}</option>`).join("")}</select></label><label>Patient ID field<select id="dsPatient">${options(headers,patient)}</select></label><label>Chart type<select id="dsChart"><option value="bar">Bar</option><option value="line">Line</option><option value="donut">Donut</option><option value="table">Table</option></select></label><label>Layout<select id="dsLayout"><option value="standard">Standard</option><option value="compact">Compact</option><option value="wide">Wide</option></select></label></div><label>Metric definition / denominator note</label><input id="dsDefinition" value="Encounter-level summary; confirm row grain and exclusions before interpretation."><button id="dsBuild">Update dashboard</button></article><div id="dsDashboard"></div>`;
}
function aggregate(){
const date=host.querySelector("#dsDate").value,dept=host.querySelector("#dsDept").value,filter=host.querySelector("#dsFilter").value,start=host.querySelector("#dsStart").value,end=host.querySelector("#dsEnd").value,metric=host.querySelector("#dsMetric").value,patient=host.querySelector("#dsPatient").value,chart=host.querySelector("#dsChart").value;
filtered=rows.filter(r=>(!filter||r[dept]===filter)&&(!start||!r[date]||r[date]>=start)&&(!end||!r[date]||r[date]<=end));
const val=r=>metric==="rows"?1:metric==="patients"?r[patient]:Number(r[metric]);
const chartType=host.querySelector("#dsChart").value;
const groupField=chartType==="line"?date:dept;
const catMap={};filtered.forEach(r=>{const k=r[groupField]||"(Missing)";(catMap[k]??=[]).push(r)});
groups=Object.entries(catMap).map(([label,rs])=>({label,value:metric==="patients"?new Set(rs.map(r=>r[patient]).filter(Boolean)).size:metric==="rows"?rs.length:rs.map(val).filter(Number.isFinite).reduce((a,b)=>a+b,0)/Math.max(1,rs.map(val).filter(Number.isFinite).length),n:rs.length})).sort((a,b)=>b.value-a.value);
const total=metric==="patients"?new Set(filtered.map(r=>r[patient]).filter(Boolean)).size:metric==="rows"?filtered.length:filtered.map(val).filter(Number.isFinite).length?filtered.map(val).filter(Number.isFinite).reduce((a,b)=>a+b,0)/filtered.map(val).filter(Number.isFinite).length:0;
if(chartType==="line")groups.sort((a,b)=>a.label.localeCompare(b.label));
const allDates=filtered.map(r=>r[date]).filter(x=>x).sort();
qa=[
["Dataset loaded",rows.length>0],
["Reporting period visible",Boolean(start||end)||allDates.length>0],
["Category filter disclosed",true],
["Metric definition documented",host.querySelector("#dsDefinition").value.trim().length>15],
["Patient identifier available",headers.includes(patient)],
["Row grain reviewed",false],
["Missingness reviewed",false],
["Clinical interpretation bounded",true]
];
let chartHtml=chart==="table"?`<div class="table-wrap"><table><thead><tr><th>${esc(dept)}</th><th>Metric value</th><th>Rows</th></tr></thead><tbody>${groups.map(g=>`<tr><td>${esc(g.label)}</td><td>${g.value.toFixed(2)}</td><td>${g.n}</td></tr>`).join("")}</tbody></table></div>`:drawChart(groups,chart);
const missing=filtered.reduce((n,r)=>n+headers.filter(h=>r[h]==="").length,0);
const pct=filtered.length?missing/(filtered.length*headers.length)*100:0;
const layout=host.querySelector("#dsLayout").value;
return `<section class="panel" data-layout="${layout}" style="${layout==="compact"?"max-width:760px":layout==="wide"?"width:100%;":""}"><div class="eyebrow">LIVE DASHBOARD · ${esc(filename)}</div><h3>Hospital analytics summary</h3><p class="muted">${allDates.length?esc(allDates[0])+" to "+esc(allDates[allDates.length-1]):"No date values detected"} · ${filtered.length} filtered rows · ${esc(host.querySelector("#dsDefinition").value)}</p><div class="metric-grid"><div class="metric"><b>${filtered.length}</b><span>Rows in scope</span></div><div class="metric"><b>${total.toFixed(2)}</b><span>${metric==="rows"?"Encounter count":metric==="patients"?"Unique patients":"Mean "+metric}</span></div><div class="metric"><b>${pct.toFixed(1)}%</b><span>Cell missingness</span></div></div><h4>${esc(chart.toUpperCase())} · ${esc(chart==="line"?date:dept)} ${chart==="line"?"trend":"comparison"}</h4><div class="dashboard-chart">${chartHtml}</div><p class="muted">Values are descriptive. The metric is calculated within each category. For numeric metrics, category values are means; row count and unique patient count are counts.</p><button id="dsExport">Export standalone HTML dashboard</button></section><section class="panel"><h3>Dashboard quality gate</h3><p>Complete the manual checks before publication. Some items require your review and cannot be verified automatically.</p>${qa.map((x,i)=>`<label class="er-service"><input type="checkbox" data-qa="${i}" ${x[1]?"checked":""} ${i===5||i===6?"":" "}> ${esc(x[0])} ${x[1]?"— detected/assumed":"— requires analyst review"}</label>`).join("")}<p class="muted">The “row grain reviewed” and “missingness reviewed” items intentionally remain unchecked.</p></section>`;
}
function drawChart(data,type){
if(!data.length)return "<p>No records match these filters.</p>";
const W=700,H=300,pad=48,vals=data.map(x=>x.value),max=Math.max(...vals,1);
if(type==="donut"){const sum=vals.reduce((a,b)=>a+b,0)||1;let a=-Math.PI/2;const colors=["#2563eb","#0f766e","#d97706","#9333ea","#dc2626","#64748b"];let paths=data.map((d,i)=>{let b=a+d.value/sum*Math.PI*2,large=b-a>Math.PI?1:0,x1=350+105*Math.cos(a),y1=150+105*Math.sin(a),x2=350+105*Math.cos(b),y2=150+105*Math.sin(b),path=`<path d="M ${x1} ${y1} A 105 105 0 ${large} 1 ${x2} ${y2}" fill="none" stroke="${colors[i%colors.length]}" stroke-width="36"/>`;a=b;return path}).join("");return `<svg viewBox="0 0 700 300" role="img" aria-label="Donut chart">${paths}<text x="350" y="145" text-anchor="middle" font-size="18" fill="currentColor">${data.length}</text><text x="350" y="168" text-anchor="middle" font-size="12" fill="currentColor">categories</text>${data.map((d,i)=>`<text x="500" y="${70+i*24}" fill="currentColor" font-size="13">${esc(d.label)}: ${d.value.toFixed(1)}</text>`).join("")}</svg>`}
if(type==="line"){const pts=data.map((d,i)=>`${pad+i*(W-2*pad)/Math.max(1,data.length-1)},${H-pad-(d.value/max)*(H-2*pad)}`).join(" ");return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Line chart"><line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" stroke="currentColor"/><polyline points="${pts}" fill="none" stroke="#2563eb" stroke-width="3"/>${data.map((d,i)=>`<circle cx="${pad+i*(W-2*pad)/Math.max(1,data.length-1)}" cy="${H-pad-(d.value/max)*(H-2*pad)}" r="4" fill="#2563eb"><title>${esc(d.label)}: ${d.value.toFixed(2)}</title></circle>`).join("")}</svg>`}
const bw=Math.min(90,(W-2*pad)/data.length*.65),step=(W-2*pad)/data.length;
return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Bar chart"><line x1="${pad}" y1="${H-pad}" x2="${W-pad}" y2="${H-pad}" stroke="currentColor"/>${data.map((d,i)=>{const h=(d.value/max)*(H-2*pad),x=pad+i*step+(step-bw)/2,y=H-pad-h;return `<rect x="${x}" y="${y}" width="${bw}" height="${h}" fill="#2563eb"><title>${esc(d.label)}: ${d.value.toFixed(2)}</title></rect><text x="${x+bw/2}" y="${H-pad+18}" text-anchor="middle" fill="currentColor" font-size="11">${esc(d.label.slice(0,12))}</text>`}).join("")}</svg>`;
}
function exportHtml(){
const title="Healthcare Analytics Dashboard";
const content=host.querySelector("#dsDashboard").innerHTML;
const html=`<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>body{font:15px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#172033}section{border:1px solid #ccd3df;border-radius:12px;padding:1.2rem;margin:1rem 0}.metric-grid{display:flex;gap:1rem;flex-wrap:wrap}.metric{padding:1rem;border:1px solid #ccd3df;border-radius:8px;min-width:130px}.metric b{display:block;font-size:1.7rem}svg{width:100%;height:auto;max-height:360px}.muted{color:#5b6472}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:.5rem;text-align:left}</style></head><body><h1>${title}</h1><p>Exported dashboard snapshot. Synthetic/training use unless otherwise specified.</p>${content}<p>Review metric definitions, source grain, missingness and exclusions before publication. This is not clinical decision support.</p></body></html>`;
download("healthcare_analytics_dashboard.html",html,"text/html");
}
function download(name,data,type){const u=URL.createObjectURL(new Blob([data],{type})),a=document.createElement("a");a.href=u;a.download=name;a.click();URL.revokeObjectURL(u)}
function wire(){host.querySelector("#dsBuild").addEventListener("click",()=>{const date=host.querySelector("#dsDate").value;host.querySelector("#dsDashboard").innerHTML=aggregate();host.querySelector("#dsExport").addEventListener("click",exportHtml)});host.querySelector("#dsMetric").addEventListener("change",()=>{});
host.querySelector("#dsDept").addEventListener("change",()=>{const f=host.querySelector("#dsFilter"),d=host.querySelector("#dsDept").value,old=f.value;f.innerHTML='<option value="">All categories</option>'+[...new Set(rows.map(r=>r[d]).filter(Boolean))].sort().map(x=>`<option value="${esc(x)}">${esc(x)}</option>`).join("");if([...f.options].some(o=>o.value===old))f.value=old;});
}
render();
const observer=new MutationObserver(()=>{const app=host.querySelector("#dsApp");if(app&&!app.dataset.wired&&rows.length){app.dataset.wired="1";wire();}});
observer.observe(host,{childList:true,subtree:true});
})();