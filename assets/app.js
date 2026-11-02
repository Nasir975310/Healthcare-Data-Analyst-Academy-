/**
 * Healthcare Data Analyst Academy — Core Web Application Engine
 *
 * Provides offline-first state management, client-side routing,
 * dynamic curriculum rendering, interactive calculators, practical labs,
 * and assessment tracking.
 *
 * @version 5.60.3
 * @license MIT
 */

const state = {
  completed: [],
  theme: "light",
  lesson: "V01-C01"
};
let curriculum = null,
  lessons = [],
  glossary = [],
  quiz = [],
  practicalLabs = [],
  jobAssignments = [],
  sqlChallenges = [],
  sqlCompleted = [];
const $ = s => document.querySelector(s),
  $$ = s => Array.from(document.querySelectorAll(s));
const key = (v, c) => `${v}:${c}`;
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;"
} [c]));
async function getJSON(path) {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`Could not load ${path}`);
  return r.json();
}

function loadState() {
  try {
    const x = JSON.parse(localStorage.getItem("hda-academy-progress") || "{}");
    state.completed = Array.isArray(x.completed) ? x.completed : [];
    state.theme = x.theme === "dark" ? "dark" : "light";
  } catch (e) {
    state.completed = [];
  }
}

function saveState() {
  try {
    localStorage.setItem("hda-academy-progress", JSON.stringify({
      completed: state.completed,
      theme: state.theme,
      updatedAt: new Date().toISOString()
    }));
    $("#lastSaved") && ($("#lastSaved").textContent = "Progress saved on this device");
  } catch (e) {
    alert("Progress could not be saved. Export a backup or check browser storage settings.");
  }
}
const allChapters = () => curriculum.volumes.flatMap(v => v.chapters.map(c => ({
  ...c,
  volumeId: v.id
})));

function progress(v) {
  const done = v.chapters.filter(c => state.completed.includes(key(v.id, c.number))).length;
  return {
    done,
    total: v.chapters.length,
    pct: Math.round(done / v.chapters.length * 100)
  };
}

function stats() {
  const all = allChapters(),
    done = state.completed.length;
  $("#volumeCount").textContent = curriculum.volumes.length;
  $("#chapterCount").textContent = all.length;
  $("#completedCount").textContent = done;
  $("#completionRate").textContent = `${all.length?Math.round(done/all.length*100):0}%`;
}

function volumeCard(v) {
  const p = progress(v);
  return `<article class="volume-card"><div class="volume-top"><span class="volume-code">${v.id}</span><span class="volume-level">${esc(v.level)}</span></div><h3>${esc(v.title)}</h3><p>${esc(v.purpose)}</p><div class="progress-track"><i style="width:${p.pct}%"></i></div><div class="volume-meta"><span>${p.done}/${p.total} chapters checked</span><span>${p.pct}%</span></div></article>`;
}

function renderDashboard() {
  $("#dashboardVolumes").innerHTML = curriculum.volumes.map(volumeCard).join("");
  stats();
}

function renderCurriculum(filter = "") {
  const q = filter.trim().toLowerCase();
  let n = 0;
  const html = curriculum.volumes.map(v => {
    const chapters = v.chapters.filter(c => !q || [v.id, v.title, v.purpose, c.title, c.scope].join(" ").toLowerCase().includes(q));
    if (!chapters.length) return "";
    n++;
    const p = progress(v);
    return `<article class="curriculum-volume"><div class="volume-summary" role="button" tabindex="0" aria-expanded="false"><div class="volume-badge">${v.id}</div><div><h3>${esc(v.title)}</h3><p>${esc(v.purpose)}</p></div><div class="right">${p.done}/${p.total} checked<br>${esc(v.level)}</div><span class="expand-mark">＋</span></div><div class="chapter-list" hidden>${chapters.map(c=>{const done=state.completed.includes(key(v.id,c.number));const hasLesson=lessons.some(l=>l.id===`${v.id}-C${c.number}`);return `<div class="chapter-row"><span class="chapter-num">${c.number}</span><span class="chapter-title">${esc(c.title)}</span><span class="chapter-scope">${esc(c.scope)}</span><div class="chapter-actions">${hasLesson?`<button class="study-btn" data-lesson="${v.id}-C${c.number}">Study chapter →</button>`:"<span class='chapter-status'>Content planned</span>"}<label class="chapter-check"><input type="checkbox" data-volume="${v.id}" data-chapter="${c.number}" ${done?"checked":""}> Done</label></div></div>`}).join("")}</div></article>`;
  }).join("");
  $("#curriculumList").innerHTML = html || '<div class="empty-state"><b>No matching curriculum items.</b><span>Try another search term.</span></div>';
  $("#searchCount").textContent = q ? `${n} matching volumes` : "All volumes";
  bindCurriculum();
}

function bindCurriculum() {
  $$(".volume-summary").forEach(el => {
    const toggle = () => {
      const box = el.nextElementSibling,
        open = box.hidden;
      box.hidden = !open;
      el.setAttribute("aria-expanded", String(open));
      el.querySelector(".expand-mark").textContent = open ? "−" : "＋";
    };
    el.addEventListener("click", toggle);
    el.addEventListener("keydown", e => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggle();
      }
    });
  });
  $$(".chapter-check input").forEach(el => el.addEventListener("change", () => {
    const k = key(el.dataset.volume, el.dataset.chapter);
    state.completed = el.checked ? [...new Set([...state.completed, k])] : state.completed.filter(x => x !== k);
    saveState();
    renderDashboard();
    const opened = $$(".volume-summary").filter(x => !x.nextElementSibling.hidden).map(x => x.querySelector("h3").textContent);
    renderCurriculum($("#curriculumSearch").value);
    $$(".volume-summary").forEach(x => {
      if (opened.includes(x.querySelector("h3").textContent)) {
        x.nextElementSibling.hidden = false;
        x.setAttribute("aria-expanded", "true");
        x.querySelector(".expand-mark").textContent = "−";
      }
    });
  }));
  $$(".study-btn").forEach(b => b.addEventListener("click", () => openLesson(b.dataset.lesson)));
}

function renderRoadmap() {
  const stages = [
    ["01", "Digital and analytical foundations", "Build confidence with files, data concepts, mathematics and descriptive statistics.", ["Data literacy", "Healthcare data", "Statistics foundations"]],
    ["02", "Spreadsheet and database competence", "Use Excel for structured analysis and SQL for reliable data extraction.", ["Excel", "SQL", "Relational databases"]],
    ["03", "Reproducible programming", "Clean, analyze and communicate data with Python or R.", ["Python", "pandas", "Visualization", "Reproducible reports"]],
    ["04", "Research and clinical analytics", "Design valid analyses and interpret healthcare evidence responsibly.", ["Biostatistics", "Epidemiology", "Clinical research", "Pharmacy analytics"]],
    ["05", "BI and data workflow delivery", "Create governed reporting and understand the data lifecycle.", ["Power BI", "Data modeling", "ETL", "Git"]],
    ["06", "Advanced specialization", "Develop advanced analytics skills only after strong foundations.", ["Machine learning", "Interoperability", "Cloud", "Responsible AI"]],
    ["07", "Professional transition", "Demonstrate skills, apply strategically and prepare for remote work.", ["Portfolio", "Interviews", "Applications", "Remote practice"]]
  ];
  $("#roadmap").innerHTML = stages.map(s => `<div class="roadmap-stage"><div class="stage-dot">${s[0]}</div><article class="stage-card"><h3>${s[1]}</h3><p>${s[2]}</p><ul>${s[3].map(x=>`<li>✓ ${x}</li>`).join("")}</ul></article></div>`).join("");
}

function blockHTML(b) {
  if (b.type === "p") return `<p>${esc(b.text)}</p>`;
  if (b.type === "callout") return `<div class="lesson-callout"><strong>${esc(b.label)}</strong><p>${esc(b.text)}</p></div>`;
  if (b.type === "list") return `<ul>${b.items.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>`;
  if (b.type === "table") return `<div class="lesson-table-wrap"><table class="lesson-table"><thead><tr>${b.headers.map(x=>`<th>${esc(x)}</th>`).join("")}</tr></thead><tbody>${b.rows.map(r=>`<tr>${r.map(x=>`<td>${esc(x)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  if (b.type === "download") return `<p class="download-row"><a class="download-link" href="${esc(b.href)}" download>⇩ ${esc(b.label)}</a></p>`;
  if (b.type === "calculator") return calculatorBlockHTML(b);
  return "";
}

function calculatorBlockHTML(b) {
  const head = `<div class="calc-panel lesson-calculator"><h3>${esc(b.title)}</h3>`;
  const note = `<div class="calc-note">${esc(b.note)}</div>`;
  if (b.kind === "descriptive") return `${head}<label>Observations (comma-separated)<input class="calc-data" data-role="values" value="118, 124, 126, 130, 152"></label><button class="secondary-small" data-action="calculate">Calculate</button><div class="calc-result" data-role="result" aria-live="polite">Enter values and calculate.</div>${note}</div>`;
  if (b.kind === "bayes") return `${head}<div class="calc-fields"><label>Prevalence (%)<input data-role="prevalence" type="number" min="0" max="100" step="0.01" value="1"></label><label>Sensitivity (%)<input data-role="sensitivity" type="number" min="0" max="100" step="0.1" value="90"></label><label>Specificity (%)<input data-role="specificity" type="number" min="0" max="100" step="0.1" value="95"></label></div><button class="secondary-small" data-action="calculate">Calculate</button><div class="calc-result" data-role="result" aria-live="polite">Adjust inputs and calculate.</div>${note}</div>`;
  if (b.kind === "mean-ci") return `${head}<div class="calc-fields"><label>Sample mean<input data-role="mean" type="number" step="any" value="130"></label><label>Sample SD<input data-role="sd" type="number" min="0" step="any" value="12"></label><label>Sample size (n)<input data-role="n" type="number" min="2" step="1" value="36"></label></div><button class="secondary-small" data-action="calculate">Calculate</button><div class="calc-result" data-role="result" aria-live="polite">Adjust inputs and calculate.</div>${note}</div>`;
  return "";
}

function bindLessonCalculators() {
  document.querySelectorAll(".lesson-calculator").forEach(panel => {
    const btn = panel.querySelector('[data-action="calculate"]'),
      out = panel.querySelector('[data-role="result"]');
    if (!btn || !out) return;
    btn.addEventListener("click", () => {
      const val = r => Number(panel.querySelector(`[data-role="${r}"]`)?.value);
      const fmt = x => Number(x).toLocaleString(undefined, {
        maximumFractionDigits: 3
      });
      const fail = "Check inputs: values must be finite and within the stated limits.";
      try {
        if (panel.querySelector('[data-role="values"]')) {
          const raw = panel.querySelector('[data-role="values"]').value.split(",").map(x => x.trim()).filter(Boolean),
            a = raw.map(Number);
          if (a.length < 2 || a.some(x => !Number.isFinite(x))) throw Error(fail);
          a.sort((x, y) => x - y);
          const n = a.length,
            mean = a.reduce((s, x) => s + x, 0) / n,
            med = n % 2 ? a[(n - 1) / 2] : (a[n / 2 - 1] + a[n / 2]) / 2,
            counts = new Map();
          a.forEach(x => counts.set(x, (counts.get(x) || 0) + 1));
          const max = Math.max(...counts.values()),
            modes = max === 1 ? ["No repeated mode"] : [...counts].filter(x => x[1] === max).map(x => fmt(x[0]));
          const q = (arr, p) => {
            const pos = (arr.length - 1) * p,
              lo = Math.floor(pos),
              hi = Math.ceil(pos);
            return arr[lo] + (arr[hi] - arr[lo]) * (pos - lo);
          };
          const sd = Math.sqrt(a.reduce((s, x) => s + (x - mean) ** 2, 0) / (n - 1));
          out.innerHTML = `n = ${n}<br>Mean = ${fmt(mean)}<br>Median = ${fmt(med)}<br>Mode = ${modes.join(", ")}<br>Range = ${fmt(a[n-1]-a[0])}<br>Sample SD = ${fmt(sd)}<br>Q1 = ${fmt(q(a,.25))}; Q3 = ${fmt(q(a,.75))}; IQR = ${fmt(q(a,.75)-q(a,.25))}`;
        } else if (panel.querySelector('[data-role="prevalence"]')) {
          const prev = val("prevalence"),
            sens = val("sensitivity"),
            spec = val("specificity");
          if ([prev, sens, spec].some(x => !Number.isFinite(x) || x < 0 || x > 100)) throw Error(fail);
          const N = 100000,
            d = N * prev / 100,
            nd = N - d,
            tp = d * sens / 100,
            fn = d - tp,
            tn = nd * spec / 100,
            fp = nd - tn,
            ppv = tp / (tp + fp),
            npv = tn / (tn + fn);
          out.innerHTML = `Hypothetical cohort: ${N.toLocaleString()}<br>True positives = ${fmt(tp)}; false positives = ${fmt(fp)}<br>True negatives = ${fmt(tn)}; false negatives = ${fmt(fn)}<br>PPV = ${(ppv*100).toFixed(2)}%<br>NPV = ${(npv*100).toFixed(2)}%`;
        } else {
          const mean = val("mean"),
            sd = val("sd"),
            n = val("n");
          if (!Number.isFinite(mean) || !Number.isFinite(sd) || !Number.isInteger(n) || sd < 0 || n < 2) throw Error(fail);
          const se = sd / Math.sqrt(n),
            lo = mean - 1.96 * se,
            hi = mean + 1.96 * se;
          out.innerHTML = `Standard error = ${fmt(se)}<br>Approximate 95% normal CI = ${fmt(lo)} to ${fmt(hi)}`;
        }
      } catch (e) {
        out.textContent = e.message || fail;
      }
    });
  });
}

function openLesson(id) {
  const l = lessons.find(x => x.id === id);
  if (!l) return;
  state.lesson = id;
  $("#lessonContent").innerHTML = `<header class="lesson-header"><div class="eyebrow">${esc(l.volume)} · ${esc(l.level)} · ${l.estimated_minutes} MIN</div><h1>${esc(l.title)}</h1><p>This chapter introduces the professional purpose, workflow and judgment required in healthcare analytics. Read actively, work through the examples and complete the chapter assessment.</p></header><article class="outcome-panel"><h3>Learning outcomes</h3><ul>${l.learning_outcomes.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></article>${l.sections.map((sec,i)=>`<section class="lesson-section"><h2>${esc(sec.heading)}</h2>${sec.blocks.map(blockHTML).join("")}${i===6?calculatorHTML():""}</section>`).join("")}${l.references?.length?`<article class="lesson-exercises"><h2>Further reading and authoritative references</h2>${l.references.map(r=>`<p><a class="reference-link" href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.title)}</a><br><span class="muted small">${esc(r.note)}</span></p>`).join("")}<p class="muted small">External references are supplementary. The chapter is designed to explain the foundational concepts without requiring these links.</p></article>`:""}<article class="lesson-exercises"><h2>Practice exercises with worked answers</h2>${l.exercises.map((e,i)=>`<details class="exercise"><summary>Exercise ${i+1}: ${esc(e.question)}</summary><p><b>Worked solution:</b></p><div class="worked-answer">${esc(e.answer).replace(/\*\*(.*?)\*\*/g,"<strong>$1</strong>")}</div></details>`).join("")}</article><div class="lesson-footer"><button class="secondary-small" id="lessonQuiz">Take chapter assessment →</button><button class="primary-small" id="markLesson">${state.completed.includes(l.id.replace("-C",":"))?"✓ Chapter marked complete":"Mark chapter complete"}</button></div>`;
  navigate("reader");
  bindLessonCalculators();
  $("#lessonQuiz").addEventListener("click", async () => {
    try {
      quiz = await getJSON(`content/quiz-${l.id.toLowerCase()}.json`);
    } catch (e) {
      quiz = [];
    }
    navigate("assessments");
    renderQuiz();
  });
  $("#markLesson").addEventListener("click", () => {
    const k = l.id.replace("-C", ":");
    if (!state.completed.includes(k)) state.completed.push(k);
    saveState();
    renderDashboard();
    $("#markLesson").textContent = "✓ Chapter marked complete";
  });
  const a = $("#numerator"),
    b = $("#denominator");
  if (a && b) {
    const update = () => {
      const n = Number(a.value),
        d = Number(b.value);
      $("#calcOutput").textContent = d > 0 && Number.isFinite(n) ? `${(n/d*100).toFixed(2)}%` : "Enter a denominator greater than zero";
    };
    a.addEventListener("input", update);
    b.addEventListener("input", update);
  }
}
const calculatorHTML = () => `<div class="calc-panel"><h3>Try it: calculate a proportion</h3><div class="calc-fields"><label>Numerator<input id="numerator" type="number" min="0" value="120"></label><label>Denominator<input id="denominator" type="number" min="1" value="600"></label></div><div class="calc-result" id="calcOutput">20.00%</div><div class="calc-note">Formula: numerator ÷ denominator × 100. This calculator performs arithmetic only; you must still determine whether the numerator and denominator are valid for your clinical question.</div></div>`;

function renderGlossary(filter = "") {
  const q = filter.toLowerCase().trim(),
    items = glossary.filter(x => [x.term, x.definition, x.healthcare, x.caution].join(" ").toLowerCase().includes(q));
  $("#glossaryCount").textContent = `${items.length} terms`;
  $("#glossaryList").innerHTML = items.map(x => `<article class="glossary-card"><h3>${esc(x.term)}</h3><p>${esc(x.definition)}</p><p><b>Healthcare example:</b> ${esc(x.healthcare)}</p><p><b>Watch out:</b> ${esc(x.caution)}</p></article>`).join("") || '<div class="empty-state"><b>No matching terms.</b><span>Try a different search.</span></div>';
}

function renderQuiz() {
  let submitted = false;
  $("#quizContainer").innerHTML = quiz.map((q, i) => `<article class="quiz-card" data-q="${q.id}"><p class="quiz-question">${i+1}. ${esc(q.q)}</p>${q.options.map((o,j)=>`<label class="quiz-option"><input type="radio" name="${q.id}" value="${j}"><span>${esc(o)}</span></label>`).join("")}<div class="quiz-feedback" id="feedback-${q.id}"></div></article>`).join("") + `<div class="quiz-actions"><button class="primary-small" id="submitQuiz">Submit answers</button><button class="secondary-small" id="resetQuiz">Reset</button></div><div id="quizResult"></div>`;
  $("#submitQuiz").addEventListener("click", () => {
    let correct = 0,
      answered = 0;
    quiz.forEach(q => {
      const selected = $(`input[name="${q.id}"]:checked`),
        box = $(`#feedback-${q.id}`);
      box.className = "quiz-feedback show";
      if (selected) {
        answered++;
        const ok = Number(selected.value) === q.correct;
        if (ok) correct++;
        box.classList.add(ok ? "correct" : "incorrect");
        box.innerHTML = `<b>${ok?"Correct.":"Not quite."}</b> ${esc(q.why)}`;
      } else {
        box.classList.add("incorrect");
        box.innerHTML = `<b>Not answered.</b> ${esc(q.why)}`;
      }
    });
    const pct = Math.round(correct / quiz.length * 100);
    $("#quizResult").innerHTML = `<div class="quiz-result"><strong>${correct}/${quiz.length} · ${pct}%</strong><p>${answered} of ${quiz.length} questions answered. ${pct>=75?"You reached the suggested practice threshold. Review explanations and apply the concepts in a project.":"Review the explanations, revisit the chapter and retake the assessment. This is formative practice, not a professional credential."}</p></div>`;
  });
  $("#resetQuiz").addEventListener("click", renderQuiz);
}

function renderLabs(filter = "") {
  const q = filter.trim().toLowerCase();
  const items = practicalLabs.filter(l => [l.id, l.title, l.volume, l.level, l.tools, l.objective].join(" ").toLowerCase().includes(q));
  $("#labCount").textContent = `${items.length} of ${practicalLabs.length} labs`;
  $("#labList").innerHTML = items.map(l => `<article class="lab-card">
 <div class="lab-card-top"><span class="volume-code">${esc(l.id)}</span><span class="volume-level">${esc(l.level)}</span></div>
 <h3>${esc(l.title)}</h3><p class="lab-meta">${esc(l.volume)} · ${esc(l.duration)} · ${esc(l.tools)}</p>
 <p>${esc(l.objective)}</p><p><b>Deliverable:</b> ${esc(l.deliverable)}</p>
 <details><summary>Open full lab instructions</summary>
 <div class="lab-detail"><h4>Prerequisites</h4><ul>${l.prerequisites.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Linux — ${esc(l.linux.shell)}</h4><pre><code>${l.linux.commands.map(esc).join("\n")}</code></pre>
 <h4>Windows — ${esc(l.windows.shell)}</h4><pre><code>${l.windows.commands.map(esc).join("\n")}</code></pre>
 <h4>Execution steps</h4><ol>${l.steps.map(x=>`<li>${esc(x)}</li>`).join("")}</ol>
 <h4>Acceptance criteria</h4><ul>${l.acceptance.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Troubleshooting</h4><ul>${l.troubleshooting.map(x=>`<li><b>${esc(x[0])}:</b> ${esc(x[1])}</li>`).join("")}</ul>
 <h4>Precautions</h4><ul>${l.precautions.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Portfolio evidence</h4><p>${esc(l.portfolio)}</p></div></details></article>`).join("") || '<div class="empty-state">No matching practical labs.</div>';
}


function loadSqlProgress() {
  try {
    const x = JSON.parse(localStorage.getItem("hda-sql-mastery") || "[]");
    sqlCompleted = Array.isArray(x) ? x : [];
  } catch (e) {
    sqlCompleted = [];
  }
}

function saveSqlProgress() {
  try {
    localStorage.setItem("hda-sql-mastery", JSON.stringify(sqlCompleted));
  } catch (e) {
    alert("SQL progress could not be saved on this browser.");
  }
}

function renderSqlMastery(filter = "") {
  const q = filter.trim().toLowerCase();
  const items = sqlChallenges.filter(c => [c.id, c.level, c.title, c.skill, c.scenario, c.task].join(" ").toLowerCase().includes(q));
  $("#sqlChallengeCount").textContent = `${items.length} of ${sqlChallenges.length} challenges`;
  $("#sqlDoneCount").textContent = sqlCompleted.length;
  $("#sqlProgressPct").textContent = `${sqlChallenges.length?Math.round(sqlCompleted.length/sqlChallenges.length*100):0}%`;
  $("#sqlChallengeList").innerHTML = items.map(c => {
    const done = sqlCompleted.includes(c.id);
    return `<article class="lab-card sql-challenge ${done?"is-done":""}">
 <div class="lab-card-top"><span class="volume-code">${esc(c.id)}</span><span class="volume-level">${esc(c.level)}</span></div>
 <h3>${esc(c.title)}</h3><p class="lab-meta">${esc(c.skill)} · ${esc(c.time)}</p>
 <p>${esc(c.scenario)}</p><p><b>Your task:</b> ${esc(c.task)}</p>
 <h4>Requirements</h4><ul>${c.requirements.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <details><summary>Starter query</summary><pre><code>${esc(c.starter)}</code></pre></details>
 <details><summary>Reveal hint</summary><p>${esc(c.hint)}</p></details>
 <details><summary>Reveal worked solution</summary><pre><code>${esc(c.solution)}</code></pre><p><b>Expected result:</b> ${esc(c.expected)}</p><p><b>Validation:</b> ${esc(c.check)}</p></details>
 <button class="sql-done-btn ${done?"completed":""}" data-sql-done="${esc(c.id)}">${done?"✓ Completed — mark incomplete":"Mark challenge complete"}</button>
 </article>`;
  }).join("") || '<div class="empty-state">No matching SQL challenges.</div>';
  $$("#sqlChallengeList [data-sql-done]").forEach(b => b.addEventListener("click", () => {
    const id = b.dataset.sqlDone;
    sqlCompleted = sqlCompleted.includes(id) ? sqlCompleted.filter(x => x !== id) : [...sqlCompleted, id];
    saveSqlProgress();
    renderSqlMastery($("#sqlSearch").value);
  }));
}

function renderAssignments(filter = "") {
  const q = filter.trim().toLowerCase();
  const items = jobAssignments.filter(a => [a.id, a.title, a.track, a.level, a.role, a.scenario].join(" ").toLowerCase().includes(q));
  $("#assignmentCount").textContent = `${items.length} of ${jobAssignments.length} assignments`;
  $("#assignmentList").innerHTML = items.map(a => `<article class="lab-card">
 <div class="lab-card-top"><span class="volume-code">${esc(a.id)}</span><span class="volume-level">${esc(a.level)}</span></div>
 <h3>${esc(a.title)}</h3><p class="lab-meta">${esc(a.track)} · ${esc(a.time)} · ${esc(a.role)}</p>
 <p>${esc(a.scenario)}</p><p><b>Business question:</b> ${esc(a.business_question)}</p>
 <details><summary>Open assignment brief, instructions and scoring rubric</summary><div class="lab-detail">
 <h4>Data and starter files</h4><ul>${a.data.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Requirements</h4><ul>${a.requirements.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Execution steps</h4><ol>${a.steps.map(x=>`<li>${esc(x)}</li>`).join("")}</ol>
 <h4>Linux — ${esc(a.linux.tools)}</h4><pre><code>${a.linux.commands.map(esc).join("\n")}</code></pre>
 <h4>Windows — ${esc(a.windows.tools)}</h4><pre><code>${a.windows.commands.map(esc).join("\n")}</code></pre>
 <h4>Deliverables</h4><ul>${a.deliverables.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Scoring rubric (100 points)</h4><table class="assignment-rubric"><thead><tr><th>Criterion</th><th>Points</th></tr></thead><tbody>${a.rubric.map(x=>`<tr><td>${esc(x[0])}</td><td>${x[1]}</td></tr>`).join("")}</tbody></table>
 <h4>Acceptance criteria</h4><ul>${a.acceptance.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Common pitfalls</h4><ul>${a.pitfalls.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>
 <h4>Portfolio evidence</h4><p>${esc(a.portfolio)}</p>
 </div></details></article>`).join("") || '<div class="empty-state">No matching assignments.</div>';
}

function navigate(view) {
  $$(".view").forEach(x => x.classList.toggle("active", x.id === `view-${view}`));
  $$(".nav-item[data-view]").forEach(x => x.classList.toggle("active", x.dataset.view === view));
  const activeBtn = $(`.nav-item[data-view="${view}"]`);
  const dynamicTitle = activeBtn ? activeBtn.textContent.trim().replace(/^[\s\S]{1,2}\s+/, "") : null;
  const titles = {
    dashboard: "Dashboard",
    curriculum: "Curriculum",
    roadmap: "Learning roadmap",
    glossary: "Glossary",
    projects: "Projects",
    assessments: "Assessments",
    career: "Career centre",
    labs: "Practical labs",
    assignments: "Job simulations",
    "sql-mastery": "Healthcare SQL mastery",
    reader: "Chapter reader"
  };
  $("#crumb").textContent = titles[view] || dynamicTitle || "Dashboard";
  $("#sidebar").classList.remove("open");
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
}

function applyTheme() {
  document.body.classList.toggle("dark", state.theme === "dark");
}

function exportProgress() {
  const p = {
    product: "Healthcare Data Analyst Academy",
    formatVersion: 1,
    exportedAt: new Date().toISOString(),
    completed: state.completed,
    theme: state.theme
  };
  const blob = new Blob([JSON.stringify(p, null, 2)], {
      type: "application/json"
    }),
    url = URL.createObjectURL(blob),
    a = document.createElement("a");
  a.href = url;
  a.download = "hda-academy-progress.json";
  a.click();
  URL.revokeObjectURL(url);
}

function importProgress(file) {
  const r = new FileReader();
  r.onload = () => {
    try {
      const x = JSON.parse(r.result);
      if (!Array.isArray(x.completed)) throw Error();
      const valid = new Set(allChapters().map(c => key(c.volumeId, c.number)));
      state.completed = x.completed.filter(k => valid.has(k));
      state.theme = x.theme === "dark" ? "dark" : "light";
      saveState();
      applyTheme();
      renderDashboard();
      renderCurriculum($("#curriculumSearch").value);
      alert("Progress imported.");
    } catch (e) {
      alert("Invalid Academy progress backup.");
    }
  };
  r.readAsText(file);
}
document.addEventListener("DOMContentLoaded", async () => {
  loadState();
  applyTheme();
  try {
    [curriculum, lessons, glossary, quiz, practicalLabs, jobAssignments, sqlChallenges] = await Promise.all([getJSON("content/curriculum.json"), getJSON("content/lessons.json"), getJSON("content/glossary.json"), getJSON("content/quiz-v01-c01.json"), getJSON("content/practical-labs.json"), getJSON("assignments/assignments.json"), getJSON("content/sql-mastery.json")]);
    renderDashboard();
    renderCurriculum();
    renderRoadmap();
    renderGlossary();
    renderLabs();
    renderAssignments();
    loadSqlProgress();
    renderSqlMastery();
    renderQuiz();
  } catch (e) {
    $(".content").insertAdjacentHTML("afterbegin", `<div class="notice"><b>Could not load local learning content.</b> Use the included local server instructions and check that the content folder is present.</div>`);
  }
  $$(".nav-item[data-view]").forEach(b => b.addEventListener("click", async () => {
    if (b.dataset.view === "assessments" && quiz.length === 0) {
      try {
        quiz = await getJSON("content/quiz-v01-c01.json");
      } catch (e) {
        quiz = [];
      }
      renderQuiz();
    }
    navigate(b.dataset.view);
  }));
  $$("[data-goto]").forEach(b => b.addEventListener("click", () => navigate(b.dataset.goto)));
  $("#continueBtn").addEventListener("click", () => navigate("curriculum"));
  $("#curriculumSearch").addEventListener("input", e => renderCurriculum(e.target.value));
  $("#glossarySearch").addEventListener("input", e => renderGlossary(e.target.value));
  $("#labSearch").addEventListener("input", e => renderLabs(e.target.value));
  $("#assignmentSearch").addEventListener("input", e => renderAssignments(e.target.value));
  $("#sqlSearch").addEventListener("input", e => renderSqlMastery(e.target.value));
  $("#themeToggle").addEventListener("click", () => {
    state.theme = state.theme === "dark" ? "light" : "dark";
    applyTheme();
    saveState();
  });
  $("#exportProgress").addEventListener("click", exportProgress);
  $("#importProgress").addEventListener("change", e => {
    if (e.target.files[0]) importProgress(e.target.files[0]);
    e.target.value = "";
  });
  $("#menuToggle").addEventListener("click", () => $("#sidebar").classList.toggle("open"));
  $("#searchFocus").addEventListener("click", () => {
    navigate("curriculum");
    $("#curriculumSearch").focus();
  });
  $("#backToCurriculum").addEventListener("click", () => navigate("curriculum"));
});