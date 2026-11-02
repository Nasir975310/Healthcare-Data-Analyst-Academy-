/* v4.7 technical production environment guide */
(()=>{
"use strict";
const host=document.getElementById("technicalV47App");if(!host)return;
const KEY="hda_technical_environment_v47";
let state={platform:"linux",checks:{},notes:""};
try{state={...state,...JSON.parse(localStorage.getItem(KEY)||"{}")}}catch(e){}
const tasks={
linux:[
["Install Python and pip","sudo pacman -S --needed python python-pip","Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"],
["Open project directory","cd technical_environment_v47/starter_project","Open this folder in VS Code"],
["Create isolated environment","python -m venv .venv","Do not install project packages globally"],
["Activate in Fish","source .venv/bin/activate.fish","Bash/Zsh: source .venv/bin/activate"],
["Install project dependencies","python -m pip install -e \".[dev]\"","Installs pandas, NumPy, Matplotlib, pytest, Ruff and JupyterLab"],
["Run tests","python -m pytest -q","Expected: 1 starter-project test passes when dependencies install correctly"],
["Load SQLite dataset","python scripts/load_sqlite.py","Creates data/health_analytics.sqlite"],
["Generate data profile","python -m health_analytics.profile","Writes reports/generated/profile.json"]
],
windows:[
["Install Python 3.10+","py --version","Install Python and reopen PowerShell if py is unavailable"],
["Open project directory","Set-Location technical_environment_v47/starter_project","Open this folder in VS Code"],
["Create isolated environment","py -m venv .venv","Creates project-local Python environment"],
["Activate environment"," .\\.venv\\Scripts\\Activate.ps1","If blocked, use Set-ExecutionPolicy -Scope Process Bypass"],
["Install dependencies","python -m pip install -e \".[dev]\"","Installs project and development tools"],
["Run tests","python -m pytest -q","Expected: 1 starter-project test passes when dependencies install correctly"],
["Load SQLite dataset","python scripts/load_sqlite.py","Creates data/health_analytics.sqlite"],
["Generate data profile","python -m health_analytics.profile","Writes reports/generated/profile.json"]
]};
const save=()=>localStorage.setItem(KEY,JSON.stringify(state));
function render(){
const arr=tasks[state.platform],count=arr.filter((x,i)=>state.checks[state.platform+"-"+i]).length;
host.innerHTML=`<div class="metric-grid"><div class="metric"><b>${count}/${arr.length}</b><span>Setup steps checked</span></div><div class="metric"><b>150</b><span>Synthetic encounter rows</span></div><div class="metric"><b>2</b><span>Supported desktop platforms</span></div></div>
<article class="panel"><h3>Choose your operating system</h3><div class="button-row"><button id="tvLinux" class="${state.platform==="linux"?"":"secondary-small"}">Linux / Ryoku</button><button id="tvWindows" class="${state.platform==="windows"?"":"secondary-small"}">Windows / PowerShell</button></div><p class="muted">Use the matching commands below. The academy browser checklist tracks progress; commands must be run in your computer's terminal.</p></article>
<article class="panel"><h3>Environment setup checklist</h3>${arr.map((x,i)=>`<div class="er-service"><label><input type="checkbox" data-check="${i}" ${state.checks[state.platform+"-"+i]?"checked":""}><b>${i+1}. ${x[0]}</b></label><pre><code>${x[1].replace(/&/g,"&amp;").replace(/</g,"&lt;")}</code></pre><p class="muted">${x[2]}</p></div>`).join("")}<p><button id="tvReset" class="secondary-small">Reset this platform checklist</button></p></article>
<article class="panel"><h3>Project tools and references</h3><ul><li><a href="technical_environment_v47/guides/setup_linux.md" target="_blank">Linux setup guide</a></li><li><a href="technical_environment_v47/guides/setup_windows.md" target="_blank">Windows setup guide</a></li><li><a href="technical_environment_v47/guides/database_workflow.md" target="_blank">SQLite and PostgreSQL workflow</a></li><li><a href="technical_environment_v47/starter_project/README.md" target="_blank">Starter project README</a></li><li><a href="technical_environment_v47/starter_project/pyproject.toml" target="_blank">Python project configuration</a></li><li><a href="technical_environment_v47/starter_project/sql/starter_queries.sql" target="_blank">Starter SQL queries</a></li></ul><p><b>Recommended sequence:</b> Python venv → tests → SQLite → SQL queries → PostgreSQL (optional) → Git commit.</p></article>
<article class="panel"><h3>Environment notes</h3><label>Record your Python version, errors and setup notes<textarea id="tvNotes" rows="4">${state.notes.replace(/&/g,"&amp;").replace(/</g,"&lt;")}</textarea></label><p><button id="tvBackup">Export setup progress</button></p><p class="muted">Checklist state is stored locally in this browser. It does not inspect your computer, install software or confirm that commands succeeded.</p></article>`;
host.querySelector("#tvLinux").onclick=()=>{state.platform="linux";save();render()};
host.querySelector("#tvWindows").onclick=()=>{state.platform="windows";save();render()};
host.querySelectorAll("[data-check]").forEach(el=>el.onchange=()=>{state.checks[state.platform+"-"+el.dataset.check]=el.checked;save();render()});
host.querySelector("#tvReset").onclick=()=>{arr.forEach((x,i)=>delete state.checks[state.platform+"-"+i]);save();render()};
host.querySelector("#tvNotes").onchange=e=>{state.notes=e.target.value;save()};
host.querySelector("#tvBackup").onclick=()=>{const a=document.createElement("a"),u=URL.createObjectURL(new Blob([JSON.stringify(state,null,2)],{type:"application/json"}));a.href=u;a.download="hda-technical-setup-v47.json";a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)};
}
document.addEventListener("click",e=>{if(e.target.closest('[data-view="technical-v47"]'))setTimeout(render,0)});
render();
})();