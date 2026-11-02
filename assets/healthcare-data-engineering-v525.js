(function(){
  const button=document.getElementById("fhirV525Progress");
  const status=document.getElementById("fhirV525Status");
  if(!button || !status) return;
  const key="hda_fhir_interoperability_v525_reviewed";
  const refresh=()=>{const done=localStorage.getItem(key)==="true";status.textContent=done?" Reviewed locally.":" Not yet marked reviewed.";button.textContent=done?"Mark as not reviewed":"Mark module reviewed";};
  button.addEventListener("click",()=>{const done=localStorage.getItem(key)==="true";localStorage.setItem(key,String(!done));refresh();});
  refresh();
})();