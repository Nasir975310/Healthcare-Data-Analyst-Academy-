const fs=require('fs'),path=require('path'),assert=require('assert');
const base=path.resolve(__dirname,'..'); const rows=JSON.parse(fs.readFileSync(path.join(base,'data/dashboard_data.json'),'utf8'));
const golden=JSON.parse(fs.readFileSync(path.join(__dirname,'reconciliation.json'),'utf8'));
const fields=['diabetes','ckd','ischemic_heart_disease'];
const flag=v=>v===1||v===true||String(v).toLowerCase()==='yes'?true:v===0||v===false||String(v).toLowerCase()==='no'?false:null;
const co=r=>{const a=fields.map(k=>flag(r[k]));return a.includes(true)?true:a.every(v=>v===false)?false:null;};
const validClass=v=>v!==null&&v!==undefined&&String(v).trim()!==''&&String(v).toLowerCase()!=='none';
const band=v=>{const n=Number(v);return !Number.isFinite(n)?null:n<40?'18–39':n<60?'40–59':'60+'};
const plausible=v=>v!==null&&v!==''&&Number.isFinite(Number(v))&&Number(v)>=70&&Number(v)<=250;
function select(f){return rows.filter(r=>(!f.drug||r.primary_drug_class===f.drug)&&(!f.sex||String(r.sex??'')===f.sex)&&(!f.age||band(r.age_years)===f.age)&&(!f.co||(f.co==='yes'?co(r)===true:co(r)===false)));}
function metrics(rs){const pairs=rs.filter(r=>validClass(r.primary_drug_class)&&plausible(r.baseline_sbp_mmhg)&&plausible(r.followup_sbp_mmhg));const avg=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:null;const b=pairs.map(r=>Number(r.baseline_sbp_mmhg)),f=pairs.map(r=>Number(r.followup_sbp_mmhg)),ids=new Set(rs.map(r=>r.record_id));return {filtered_records:rs.length,unique_record_ids:ids.size,paired_sbp_records:pairs.length,mean_baseline_sbp:avg(b),mean_followup_sbp:avg(f),mean_paired_sbp_change:avg(b.map((x,i)=>x-f[i])),duplicate_excess:rs.length-ids.size,missing_followup_sbp:rs.filter(r=>r.followup_sbp_mmhg===null||r.followup_sbp_mmhg==='').length,implausible_followup_sbp:rs.filter(r=>r.followup_sbp_mmhg!==null&&r.followup_sbp_mmhg!==''&&!plausible(r.followup_sbp_mmhg)).length,missing_primary_class:rs.filter(r=>!validClass(r.primary_drug_class)).length};}
let count=0;for(const c of golden.cases){const actual=metrics(select(c.filters));for(const k of Object.keys(c.metrics)){const a=actual[k],e=c.metrics[k];if(typeof e==='number'&&typeof a==='number')assert(Math.abs(a-e)<1e-9,`${c.label}: ${k}: ${a} != ${e}`);else assert.strictEqual(a,e,`${c.label}: ${k}`);}count++;}
console.log(`PASS: ${count} JavaScript/Python reconciliation cases; ${rows.length} source rows.`);
