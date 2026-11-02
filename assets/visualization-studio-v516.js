(() => {
 "use strict";
 const select=document.getElementById("viz-filter-v516");
 const gallery=document.getElementById("viz-gallery-v516");
 if(!select||!gallery)return;
 select.addEventListener("change",()=>{
  const value=select.value;
  gallery.querySelectorAll("figure").forEach(fig=>{
   fig.hidden=value!=="all"&&fig.dataset.kind!==value;
  });
 });
})();