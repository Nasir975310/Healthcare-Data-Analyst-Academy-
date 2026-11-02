(() => {
 "use strict";
 const select=document.getElementById("reporting-standard-v517");
 const target=document.getElementById("reporting-checklist-v517");
 if(!select||!target)return;
 let data={};
 const render=()=>{
  const items=data[select.value]||[];
  target.innerHTML=items.map((item,i)=>`<label class="publication-check"><input type="checkbox" data-report-item="${i}"><span>${item}</span></label>`).join("");
 };
 fetch("research_publication_workbench_v517/config/reporting_checklists.json")
  .then(r=>{if(!r.ok)throw Error("Checklist data unavailable");return r.json();})
  .then(j=>{data=j;render();})
  .catch(()=>{target.textContent="Checklist file could not be loaded. The concise lists are available in the module configuration file.";});
 select.addEventListener("change",render);
})();