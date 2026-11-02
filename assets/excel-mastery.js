/* HDA Academy v2.2.0 — Excel mastery */
(()=>{
"use strict";
const STORE="hda-excel-mastery-v220";
const host=document.getElementById("excelMasteryApp");
if(!host)return;
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let challenges=[],state={done:[],query:"",startedAt:null,timerEnds:null,remaining:2700};
const read=()=>{try{state={...state,...JSON.parse(localStorage.getItem(STORE)||"{}")}}catch(e){}};
const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(state));}catch(e){}};
function render(){
 const done=new Set(state.done||[]);
 const filtered=challenges.filter(c=>(c.id+" "+c.title+" "+c.scenario+" "+c.level).toLowerCase().includes((state.query||"").toLowerCase()));
 host.innerHTML=`
 <div class="excel-mastery-summary">
  <div><b>${challenges.length}</b><span>Progressive challenges</span></div>
  <div><b>${done.size}/${challenges.length}</b><span>Marked complete on this device</span></div>
  <div><b>${Math.round(done.size/Math.max(1,challenges.length)*100)}%</b><span>Completion progress</span></div>
  <div><b>45 min</b><span>Timed client simulation</span></div>
 </div>
 <div class="excel-lab-note"><b>Required files</b><div class="excel-file-links">
 <a href="assignments/starter/healthcare_excel_powerquery_lab.xlsx" download>Download Excel practice workbook</a>
 <a href="assignments/data/excel_encounters.csv" download>Encounters CSV</a>
 <a href="assignments/data/excel_raw_medication_orders.csv" download>Raw orders CSV</a>
 <a href="assignments/data/synthetic_formulary_reference.csv" download>Formulary CSV</a>
 <a href="powerquery/clean_orders.m" download>Power Query M reference</a>
 <a href="scripts/excel_lab_cleaning.py" download>Python/pandas alternative</a>
 <a href="assignments/EXCEL_LAB_DATA_DICTIONARY.md" download>Data dictionary</a>
 </div><p><b>Platform distinction:</b> Use Microsoft Excel desktop on Windows for full XLOOKUP/PivotTable/Power Query practice. On Linux, use LibreOffice Calc for compatible spreadsheet work and Python/pandas for ETL; this is not full Power Query parity.</p></div>
 <div class="excel-mastery-toolbar"><input id="excelChallengeSearch" type="search" placeholder="Search challenges…" value="${esc(state.query)}"><button class="secondary-small" id="excelResetProgress">Reset Excel challenge progress</button></div>
 <div id="excelChallengeList">${filtered.map(c=>`
 <article class="excel-challenge">
  <div class="challenge-top"><span class="level">${esc(c.id)} · ${esc(c.level)} · ${esc(c.time)}</span><label><input type="checkbox" data-excel-done="${esc(c.id)}" ${done.has(c.id)?"checked":""}> Completed</label></div>
  <h3>${esc(c.title)}</h3><p>${esc(c.scenario)}</p>
  <details><summary>View task and acceptance criteria</summary><div class="lab-detail"><h4>Tasks</h4><ul>${c.tasks.map(x=>`<li>${esc(x)}</li>`).join("")}</ul><h4>Acceptance criteria</h4><ul>${c.acceptance.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div></details>
  <details><summary>Show starter formulas / query pattern</summary><pre>${esc(c.starter)}</pre></details>
  <details><summary>Show hint</summary><p>${esc(c.hint)}</p></details>
  <details><summary>Show worked solution and expected result</summary><p>${esc(c.solution)}</p><p><b>Expected result:</b> ${esc(c.expected)}</p></details>
 </article>`).join("")||'<div class="empty-state">No matching challenges.</div>'}</div>
 <div class="excel-timed"><h3>Timed client simulation — EX08</h3><p>Set a 45-minute limit. Start only when your workbook and source files are ready. The timer is a local practice aid; it does not lock files or enforce exam conditions.</p><div id="excelTimerDisplay"><b>${formatTime(state.remaining||2700)}</b></div><div class="excel-file-links"><button id="excelTimerStart">Start / restart 45-minute timer</button><button id="excelTimerPause">Pause timer</button><button id="excelTimerReset">Reset timer</button></div><p><b>Scoring rubric:</b> Accuracy 30; cleaning and quality controls 20; formulas/PivotTables 15; reconciliation 15; communication and caveats 10; reproducibility and file hygiene 10. Target ≥75/100. Redo any critical grain or denominator error.</p></div>
 <div class="excel-lab-note"><b>Reference controls</b><p>80 encounters · 151 raw order rows · mean LOS 3.875 days · supplied readmission flag 7/80 = 8.75% · total ordered quantity 3,038 · synthetic order value INR 100,279.75. Raw source includes one missing cost, one blank class, one orphan encounter reference and a duplicate-like business record. See the workbook's Reference_Checks tab.</p><p>These are synthetic training data. The supplied flag is not independently validated; medication orders are not dispensing, administration or adherence evidence; costs are synthetic.</p></div>`;
 bind();
}
function formatTime(s){s=Math.max(0,Number(s)||0);return String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0");}
let timer=null;
function updateTimer(){const el=document.getElementById("excelTimerDisplay");if(el)el.innerHTML="<b>"+formatTime(state.remaining)+"</b>";if(state.remaining<=0){clearInterval(timer);timer=null;alert("45-minute practice timer complete. Save your workbook and review the rubric.");}}
function bind(){
 const search=document.getElementById("excelChallengeSearch");
 search?.addEventListener("input",e=>{state.query=e.target.value;const pos=e.target.selectionStart;save();render();const next=document.getElementById("excelChallengeSearch");next?.focus();next?.setSelectionRange(pos,pos);});
 host.querySelectorAll("[data-excel-done]").forEach(x=>x.addEventListener("change",()=>{state.done=state.done||[];state.done=x.checked?[...new Set([...state.done,x.dataset.excelDone])]:state.done.filter(id=>id!==x.dataset.excelDone);save();render();}));
 document.getElementById("excelResetProgress")?.addEventListener("click",()=>{if(confirm("Reset all Excel mastery completion marks on this device?")){state.done=[];save();render();}});
 document.getElementById("excelTimerStart")?.addEventListener("click",()=>{clearInterval(timer);state.remaining=2700;save();updateTimer();timer=setInterval(()=>{state.remaining=Math.max(0,state.remaining-1);save();updateTimer();},1000);});
 document.getElementById("excelTimerPause")?.addEventListener("click",()=>{clearInterval(timer);timer=null;save();});
 document.getElementById("excelTimerReset")?.addEventListener("click",()=>{clearInterval(timer);timer=null;state.remaining=2700;save();updateTimer();});
 updateTimer();
}
read();
fetch("content/excel-mastery.json").then(r=>{if(!r.ok)throw Error("Challenge content could not be loaded");return r.json();}).then(x=>{challenges=x.challenges||[];render();}).catch(e=>{host.innerHTML='<div class="empty-state">Excel mastery content failed to load. Run the Academy through its local HTTP server rather than opening index.html directly.</div>';console.error(e);});
document.querySelectorAll('.nav-item[data-view="excel-mastery"]').forEach(btn=>btn.addEventListener("click",()=>{document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active",v.id==="view-excel-mastery"));document.querySelectorAll(".nav-item[data-view]").forEach(v=>v.classList.toggle("active",v===btn));const crumb=document.getElementById("crumb");if(crumb)crumb.textContent="Excel mastery";document.getElementById("sidebar")?.classList.remove("open");window.scrollTo({top:0,behavior:"smooth"});}));
})();