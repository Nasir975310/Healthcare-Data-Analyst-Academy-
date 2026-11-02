(function(){
 const b=document.getElementById("warehouseV526Review"),s=document.getElementById("warehouseV526Status");
 if(!b||!s)return;const k="hda_clinical_warehouse_v526_reviewed";
 function refresh(){const done=localStorage.getItem(k)==="true";s.textContent=done?" Reviewed locally.":" Not yet marked reviewed.";b.textContent=done?"Mark as not reviewed":"Mark module reviewed";}
 b.addEventListener("click",()=>{localStorage.setItem(k,String(localStorage.getItem(k)!=="true"));refresh();});refresh();
})();