(() => {
 "use strict";
 const $=id=>document.getElementById(id);
 const num=id=>{const v=$(id).value.trim(); if(v==="") return null; const n=Number(v); if(!Number.isFinite(n)||!Number.isInteger(n)||n<0) throw Error("Enter valid non-negative integer counts."); return n;};
 const fmt=x=>x===null||x===undefined?"Not estimable":(Math.abs(x)<.001||Math.abs(x)>=1000?x.toExponential(3):x.toFixed(4));
 const wilson=(k,n)=>{if(n<=0||k<0||k>n)throw Error("Counts must satisfy 0 ≤ events ≤ denominator.");const z=1.95996398454,p=k/n,d=1+z*z/n,c=(p+z*z/(2*n))/d,h=z*Math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return [c-h,c+h];};
 const pct=x=>(100*x).toFixed(1)+"%";
 function effects(){
  const et=num("ev-t-v515"),nt=num("n-t-v515"),ec=num("ev-c-v515"),nc=num("n-c-v515");
  if(nt===null||nc===null||et===null||ec===null||nt<1||nc<1||et>nt||ec>nc)throw Error("Check counts: totals must be positive and events cannot exceed totals.");
  const rt=et/nt,rc=ec/nc,rd=rt-rc,arr=rc-rt, se=Math.sqrt(rt*(1-rt)/nt+rc*(1-rc)/nc),z=1.95996398454;
  let rr=null,or=null,rrci=null,orci=null,corrected=false;
  let a=et,b=nt-et,c=ec,d=nc-ec;
  if(Math.min(a,b,c,d)===0){
    if($("cc-v515").checked){a+=.5;b+=.5;c+=.5;d+=.5;corrected=true;}
  }
  if(Math.min(a,b,c,d)>0){
    rr=(a/(a+b))/(c/(c+d));or=(a*d)/(b*c);
    const serr=Math.sqrt(1/a-1/(a+b)+1/c-1/(c+d)),seor=Math.sqrt(1/a+1/b+1/c+1/d);
    rrci=[Math.exp(Math.log(rr)-z*serr),Math.exp(Math.log(rr)+z*serr)];
    orci=[Math.exp(Math.log(or)-z*seor),Math.exp(Math.log(or)+z*seor)];
  }
  const nnt=arr>0?Math.ceil(1/arr-1e-12):null,nnh=rd>0?Math.ceil(1/rd-1e-12):null;
  $("effects-result-v515").innerHTML=`<h3>Results</h3><table><tbody>
  <tr><th>Intervention risk</th><td>${pct(rt)} (Wilson 95% CI ${pct(wilson(et,nt)[0])}–${pct(wilson(et,nt)[1])})</td></tr>
  <tr><th>Control risk</th><td>${pct(rc)} (Wilson 95% CI ${pct(wilson(ec,nc)[0])}–${pct(wilson(ec,nc)[1])})</td></tr>
  <tr><th>Risk difference (I − C)</th><td>${pct(rd)} (approx. Wald 95% CI ${pct(rd-z*se)} to ${pct(rd+z*se)})</td></tr>
  <tr><th>Relative risk</th><td>${fmt(rr)} ${rrci?`(log-Wald 95% CI ${fmt(rrci[0])}–${fmt(rrci[1])})`:"(not estimable without zero-cell correction)"}</td></tr>
  <tr><th>Odds ratio</th><td>${fmt(or)} ${orci?`(log-Wald 95% CI ${fmt(orci[0])}–${fmt(orci[1])})`:"(not estimable without zero-cell correction)"}</td></tr>
  <tr><th>ARR / NNT</th><td>${arr>0?pct(arr)+" / "+nnt:"No point-estimate benefit-based NNT"}</td></tr>
  <tr><th>Absolute risk increase / NNH</th><td>${rd>0?pct(rd)+" / "+nnh:"No point-estimate harm-based NNH"}</td></tr></tbody></table>
  <p class="muted">Continuity correction ${corrected?"was applied":"was not applied"}. Wald/log-Wald intervals are approximations. If the risk-difference interval crosses zero, NNT/NNH is not represented by one stable point estimate. State follow-up and outcome in any report.</p>`;
 }
 function diagnostic(){
  const tp=num("tp-v515"),fn=num("fn-v515"),fp=num("fp-v515"),tn=num("tn-v515");
  if([tp,fn,fp,tn].some(x=>x===null)||tp+fn===0||fp+tn===0)throw Error("Enter all four counts and include at least one reference-positive and one reference-negative participant.");
  const sens=tp/(tp+fn),spec=tn/(tn+fp),ppv=tp+fp?tp/(tp+fp):null,npv=tn+fn?tn/(tn+fn):null;
  const lrpos=spec<1?sens/(1-spec):null,lrneg=spec>0?(1-sens)/spec:null;
  const prev=$("prev-v515").value.trim();let adjusted="";
  if(prev!==""){
   const p=Number(prev);if(!(p>0&&p<1))throw Error("Target prevalence must be greater than 0 and less than 1.");
   const den1=sens*p+(1-spec)*(1-p),den2=spec*(1-p)+(1-sens)*p;
   adjusted=`<tr><th>PPV at target prevalence ${pct(p)}</th><td>${pct(sens*p/den1)}</td></tr><tr><th>NPV at target prevalence ${pct(p)}</th><td>${pct(spec*(1-p)/den2)}</td></tr>`;
  }
  $("diagnostic-result-v515").innerHTML=`<h3>Results</h3><table><tbody>
   <tr><th>Sensitivity</th><td>${pct(sens)} (Wilson 95% CI ${pct(wilson(tp,tp+fn)[0])}–${pct(wilson(tp,tp+fn)[1])})</td></tr>
   <tr><th>Specificity</th><td>${pct(spec)} (Wilson 95% CI ${pct(wilson(tn,tn+fp)[0])}–${pct(wilson(tn,tn+fp)[1])})</td></tr>
   <tr><th>PPV</th><td>${ppv===null?"Not estimable":pct(ppv)}</td></tr><tr><th>NPV</th><td>${npv===null?"Not estimable":pct(npv)}</td></tr>
   <tr><th>LR+</th><td>${fmt(lrpos)}</td></tr><tr><th>LR−</th><td>${fmt(lrneg)}</td></tr>
   <tr><th>Sample prevalence</th><td>${pct((tp+fn)/(tp+fn+fp+tn))}</td></tr>${adjusted}</tbody></table>
   <p class="muted">Predictive values depend on prevalence. The adjusted values assume sensitivity and specificity transport unchanged to the target setting. AUC cannot be calculated from this single 2×2 table.</p>`;
 }
 let appraisal={};
 function renderAppraisal(){
  const key=$("appraisal-type-v515").value, item=appraisal.frameworks[key];
  $("appraisal-checklist-v515").innerHTML=`<h3>${item.name}</h3><ul>${item.domains.map((d,i)=>`<li><label class="inline-check"><input type="checkbox" data-appraisal="${i}"> ${d}</label></li>`).join("")}</ul><p class="muted">Mark domains reviewed—not “passed”. Document supporting evidence and reviewer rationale separately. Suggested judgment categories: ${item.judgments.join("; ")}.</p>`;
 }
 async function init(){
  try{const r=await fetch("clinical_evidence_engine_v515/config/appraisal_domains.json");if(!r.ok)throw Error("Could not load appraisal domain data.");appraisal=await r.json();renderAppraisal();}
  catch(e){$("appraisal-checklist-v515").textContent="Appraisal guide is available in the release documentation; interactive domain data could not be loaded.";}
  $("calc-effects-v515").addEventListener("click",()=>{try{effects();}catch(e){$("effects-result-v515").textContent=e.message;}});
  $("calc-diagnostic-v515").addEventListener("click",()=>{try{diagnostic();}catch(e){$("diagnostic-result-v515").textContent=e.message;}});
  $("appraisal-type-v515").addEventListener("change",renderAppraisal);
  effects();diagnostic();
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();