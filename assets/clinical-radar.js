/**
 * Healthcare Data Analyst Academy — Interactive Clinical Analytics & Diagnostic Radar
 *
 * Implements client-side clinical analytics simulators:
 * 1. Bayesian Diagnostic Accuracy & 2x2 Contingency Matrix (Sensitivity, Specificity, Prevalence, PPV, NPV)
 * 2. LACE+ 30-Day Hospital Readmission Risk Calculator with dynamic visual risk gauge
 * 3. Proportion of Days Covered (PDC) Medication Adherence Simulator
 */
(() => {
  "use strict";

  const host = document.getElementById("clinicalRadarApp");
  if (!host) return;

  let activeTab = "diagnostic"; // "diagnostic" | "lace" | "pdc"

  // State for Diagnostic Simulator
  const diagState = {
    prevalence: 5,   // %
    sensitivity: 92, // %
    specificity: 90, // %
    population: 10000
  };

  // State for LACE Readmission Simulator
  const laceState = {
    los: 3,           // days
    acute: 1,         // 1 = emergency/acute, 0 = elective
    charlson: 2,      // comorbidity score (0, 1, 2, 3+)
    edVisits: 1       // past 6 months (0, 1, 2, 3, 4+)
  };

  // State for PDC Adherence Simulator
  const pdcState = {
    daysSupply: 30,
    gapDays: 14,
    totalPeriod: 180
  };

  function calculateDiagnostic() {
    const total = diagState.population;
    const prev = diagState.prevalence / 100;
    const sens = diagState.sensitivity / 100;
    const spec = diagState.specificity / 100;

    const diseased = Math.round(total * prev);
    const healthy = total - diseased;

    const tp = Math.round(diseased * sens);
    const fn = diseased - tp;

    const tn = Math.round(healthy * spec);
    const fp = healthy - tn;

    const ppv = (tp + fp) > 0 ? (tp / (tp + fp)) * 100 : 0;
    const npv = (tn + fn) > 0 ? (tn / (tn + fn)) * 100 : 0;
    const accuracy = ((tp + tn) / total) * 100;

    return { total, diseased, healthy, tp, fn, tn, fp, ppv, npv, accuracy };
  }

  function calculateLACE() {
    // Length of stay scoring: 1d=1, 2d=2, 3d=3, 4-6d=4, 7-13d=5, >=14d=7
    let l = 0;
    const d = laceState.los;
    if (d === 1) l = 1;
    else if (d === 2) l = 2;
    else if (d === 3) l = 3;
    else if (d >= 4 && d <= 6) l = 4;
    else if (d >= 7 && d <= 13) l = 5;
    else if (d >= 14) l = 7;

    // Acute admission: 3 points if yes, 0 if no
    const a = laceState.acute ? 3 : 0;

    // Charlson comorbidity: 0=0, 1=1, 2=2, 3=3, >=4=5
    let c = Math.min(laceState.charlson, 5);
    if (c >= 4) c = 5;

    // ED visits in past 6 months: 0=0, 1=1, 2=2, 3=3, >=4=4
    const e = Math.min(laceState.edVisits, 4);

    const score = l + a + c + e; // Max 19

    let riskLevel = "Low";
    let riskColor = "#10b981"; // green
    let riskClass = "risk-low";
    let recommendation = "Standard discharge summary and routine primary care follow-up within 14 days.";

    if (score >= 10) {
      riskLevel = "High";
      riskColor = "#ef4444"; // red
      riskClass = "risk-high";
      recommendation = "Intensive transitional care: 48-hour clinical phone follow-up, bedside pharmacist medication reconciliation, home health visit, and priority PCP appointment within 7 days.";
    } else if (score >= 5) {
      riskLevel = "Moderate";
      riskColor = "#f59e0b"; // amber
      riskClass = "risk-med";
      recommendation = "Enhanced discharge support: pharmacy counseling on high-risk medications and scheduled follow-up call within 72 hours.";
    }

    return { score, l, a, c, e, riskLevel, riskColor, riskClass, recommendation };
  }

  function calculatePDC() {
    const totalDays = pdcState.totalPeriod;
    const fillSize = pdcState.daysSupply;
    const gap = pdcState.gapDays;

    // Simulate timeline of fills: each fill covers fillSize days, then followed by gap days
    let coveredDays = 0;
    let currentDay = 0;
    const intervals = [];

    while (currentDay < totalDays) {
      const coverEnd = Math.min(currentDay + fillSize, totalDays);
      const daysCovered = coverEnd - currentDay;
      coveredDays += daysCovered;
      intervals.push({ start: currentDay, end: coverEnd, covered: true });

      currentDay = coverEnd;
      if (currentDay < totalDays && gap > 0) {
        const gapEnd = Math.min(currentDay + gap, totalDays);
        intervals.push({ start: currentDay, end: gapEnd, covered: false });
        currentDay = gapEnd;
      }
    }

    const pdc = Math.min(100, Math.round((coveredDays / totalDays) * 100));
    const isAdherent = pdc >= 80;

    return { totalDays, coveredDays, pdc, isAdherent, intervals };
  }

  function render() {
    host.innerHTML = `
      <div class="radar-card">
        <div class="radar-header">
          <div class="radar-title">
            <span class="radar-live-badge"><span class="pulse-dot"></span> LIVE CLINICAL RADAR</span>
            <h3>Interactive Clinical Analytics Studio</h3>
          </div>
          <div class="radar-tabs" role="tablist">
            <button class="radar-tab ${activeTab === 'diagnostic' ? 'active' : ''}" data-radar-tab="diagnostic">Diagnostic 2×2 Matrix</button>
            <button class="radar-tab ${activeTab === 'lace' ? 'active' : ''}" data-radar-tab="lace">LACE+ Readmission Risk</button>
            <button class="radar-tab ${activeTab === 'pdc' ? 'active' : ''}" data-radar-tab="pdc">PDC Medication Adherence</button>
          </div>
        </div>

        <div class="radar-body">
          ${activeTab === 'diagnostic' ? renderDiagnosticTab() : ''}
          ${activeTab === 'lace' ? renderLaceTab() : ''}
          ${activeTab === 'pdc' ? renderPdcTab() : ''}
        </div>
      </div>
    `;

    bindEvents();
  }

  function renderDiagnosticTab() {
    const res = calculateDiagnostic();
    return `
      <div class="radar-grid">
        <div class="radar-controls">
          <div class="radar-slider-group">
            <div class="slider-label-row">
              <label for="prevSlider">Disease Prevalence (P)</label>
              <span class="slider-val">${diagState.prevalence}%</span>
            </div>
            <input type="range" id="prevSlider" min="1" max="50" value="${diagState.prevalence}" class="radar-slider">
            <span class="radar-hint">Baseline prevalence in screening cohort (1% to 50%)</span>
          </div>

          <div class="radar-slider-group">
            <div class="slider-label-row">
              <label for="sensSlider">Test Sensitivity (True Positive Rate)</label>
              <span class="slider-val">${diagState.sensitivity}%</span>
            </div>
            <input type="range" id="sensSlider" min="50" max="99" value="${diagState.sensitivity}" class="radar-slider">
            <span class="radar-hint">P(Test+ | Disease+): ability to detect true cases</span>
          </div>

          <div class="radar-slider-group">
            <div class="slider-label-row">
              <label for="specSlider">Test Specificity (True Negative Rate)</label>
              <span class="slider-val">${diagState.specificity}%</span>
            </div>
            <input type="range" id="specSlider" min="50" max="99" value="${diagState.specificity}" class="radar-slider">
            <span class="radar-hint">P(Test- | Disease-): ability to correctly exclude healthy</span>
          </div>
        </div>

        <div class="radar-visualization">
          <div class="matrix-2x2">
            <div class="matrix-header-cell"></div>
            <div class="matrix-header-cell"><strong>Disease Present</strong> (${res.diseased.toLocaleString()})</div>
            <div class="matrix-header-cell"><strong>Disease Absent</strong> (${res.healthy.toLocaleString()})</div>

            <div class="matrix-row-label"><strong>Test Positive (+)</strong></div>
            <div class="matrix-cell tp-cell">
              <span class="cell-label">True Positive (TP)</span>
              <strong class="cell-num">${res.tp.toLocaleString()}</strong>
              <small class="cell-sub">${((res.tp / res.total) * 100).toFixed(1)}% of total</small>
            </div>
            <div class="matrix-cell fp-cell">
              <span class="cell-label">False Positive (FP)</span>
              <strong class="cell-num">${res.fp.toLocaleString()}</strong>
              <small class="cell-sub">${((res.fp / res.total) * 100).toFixed(1)}% of total</small>
            </div>

            <div class="matrix-row-label"><strong>Test Negative (-)</strong></div>
            <div class="matrix-cell fn-cell">
              <span class="cell-label">False Negative (FN)</span>
              <strong class="cell-num">${res.fn.toLocaleString()}</strong>
              <small class="cell-sub">${((res.fn / res.total) * 100).toFixed(1)}% of total</small>
            </div>
            <div class="matrix-cell tn-cell">
              <span class="cell-label">True Negative (TN)</span>
              <strong class="cell-num">${res.tn.toLocaleString()}</strong>
              <small class="cell-sub">${((res.tn / res.total) * 100).toFixed(1)}% of total</small>
            </div>
          </div>

          <div class="radar-kpi-deck">
            <div class="kpi-mini-card">
              <span class="kpi-mini-label">Positive Predictive Value (PPV)</span>
              <strong class="kpi-mini-val ${res.ppv < 50 ? 'kpi-warn' : 'kpi-good'}">${res.ppv.toFixed(1)}%</strong>
              <span class="kpi-mini-sub">P(Disease | Test+)</span>
            </div>
            <div class="kpi-mini-card">
              <span class="kpi-mini-label">Negative Predictive Value (NPV)</span>
              <strong class="kpi-mini-val kpi-good">${res.npv.toFixed(1)}%</strong>
              <span class="kpi-mini-sub">P(Healthy | Test-)</span>
            </div>
            <div class="kpi-mini-card">
              <span class="kpi-mini-label">Diagnostic Accuracy</span>
              <strong class="kpi-mini-val">${res.accuracy.toFixed(1)}%</strong>
              <span class="kpi-mini-sub">(TP + TN) / Total</span>
            </div>
          </div>

          <div class="clinical-takeaway">
            <strong>Clinical Biostatistical Insight:</strong>
            ${res.prevalence <= 10
              ? `At low prevalence (${diagState.prevalence}%), even with high sensitivity (${diagState.sensitivity}%) and specificity (${diagState.specificity}%), the False Positive count (${res.fp.toLocaleString()}) rival or exceed True Positives (${res.tp.toLocaleString()}), dragging PPV down to ${res.ppv.toFixed(1)}%. This explains why universal clinical screening for rare conditions requires high-specificity confirmatory tests.`
              : `At higher prevalence (${diagState.prevalence}%), True Positives predominate and PPV rises to ${res.ppv.toFixed(1)}%. Bayes' Theorem confirms that predictive value is intrinsically dependent on pre-test probability.`}
          </div>
        </div>
      </div>
    `;
  }

  function renderLaceTab() {
    const res = calculateLACE();
    const circumference = 2 * Math.PI * 45;
    const progressOffset = circumference - (res.score / 19) * circumference;

    return `
      <div class="radar-grid">
        <div class="radar-controls">
          <div class="control-row">
            <label for="losInput">Length of Stay (days)</label>
            <input type="number" id="losInput" min="1" max="30" value="${laceState.los}" class="radar-input">
          </div>

          <div class="control-row">
            <label>Admission Acuity</label>
            <div class="btn-toggle-group">
              <button class="toggle-btn ${laceState.acute === 1 ? 'active' : ''}" data-acute="1">Emergency / Acute</button>
              <button class="toggle-btn ${laceState.acute === 0 ? 'active' : ''}" data-acute="0">Elective Planned</button>
            </div>
          </div>

          <div class="control-row">
            <label for="charlsonInput">Charlson Comorbidity Index</label>
            <select id="charlsonInput" class="radar-select">
              <option value="0" ${laceState.charlson === 0 ? 'selected' : ''}>0 — No recorded comorbidities</option>
              <option value="1" ${laceState.charlson === 1 ? 'selected' : ''}>1 — Mild (e.g. uncomplicated Diabetes)</option>
              <option value="2" ${laceState.charlson === 2 ? 'selected' : ''}>2 — Moderate (e.g. Mild CKD, Hemiplegia)</option>
              <option value="3" ${laceState.charlson === 3 ? 'selected' : ''}>3 — Severe (e.g. Heart Failure + COPD)</option>
              <option value="4" ${laceState.charlson >= 4 ? 'selected' : ''}>4+ — Metastatic solid tumor / severe liver disease</option>
            </select>
          </div>

          <div class="control-row">
            <label for="edInput">ED Visits in Past 6 Months</label>
            <input type="number" id="edInput" min="0" max="10" value="${laceState.edVisits}" class="radar-input">
          </div>
        </div>

        <div class="radar-visualization">
          <div class="gauge-container">
            <div class="circular-gauge">
              <svg viewBox="0 0 120 120" class="gauge-svg">
                <circle cx="60" cy="60" r="45" class="gauge-bg" />
                <circle cx="60" cy="60" r="45" class="gauge-fg"
                  style="stroke: ${res.riskColor}; stroke-dasharray: ${circumference}; stroke-dashoffset: ${progressOffset};" />
              </svg>
              <div class="gauge-center-text">
                <span class="gauge-score">${res.score}</span>
                <span class="gauge-max">/ 19</span>
              </div>
            </div>

            <div class="gauge-details">
              <span class="risk-badge ${res.riskClass}">${res.riskLevel} Readmission Risk</span>
              <p class="gauge-breakdown">
                <strong>Score Breakdown:</strong> L=${res.l} (LOS), A=${res.a} (Acuity), C=${res.c} (Comorbidity), E=${res.e} (ED history).
              </p>
            </div>
          </div>

          <div class="clinical-takeaway">
            <strong>Care Coordination Directive:</strong>
            <p>${res.recommendation}</p>
          </div>
        </div>
      </div>
    `;
  }

  function renderPdcTab() {
    const res = calculatePDC();
    return `
      <div class="radar-grid">
        <div class="radar-controls">
          <div class="radar-slider-group">
            <div class="slider-label-row">
              <label for="supplySlider">Days Supply per Prescription Fill</label>
              <span class="slider-val">${pdcState.daysSupply} days</span>
            </div>
            <input type="range" id="supplySlider" min="15" max="90" step="15" value="${pdcState.daysSupply}" class="radar-slider">
            <span class="radar-hint">Typical 30-day (retail) or 90-day (mail-order) fill</span>
          </div>

          <div class="radar-slider-group">
            <div class="slider-label-row">
              <label for="gapSlider">Average Refill Gap Interval</label>
              <span class="slider-val">${pdcState.gapDays} days</span>
            </div>
            <input type="range" id="gapSlider" min="0" max="45" value="${pdcState.gapDays}" class="radar-slider">
            <span class="radar-hint">Lapse between exhausting supply and obtaining next fill</span>
          </div>

          <div class="radar-slider-group">
            <div class="slider-label-row">
              <label for="periodSlider">Measurement Window</label>
              <span class="slider-val">${pdcState.totalPeriod} days</span>
            </div>
            <input type="range" id="periodSlider" min="90" max="365" step="30" value="${pdcState.totalPeriod}" class="radar-slider">
            <span class="radar-hint">CMS Quality / HEDIS evaluation interval</span>
          </div>
        </div>

        <div class="radar-visualization">
          <div class="timeline-container">
            <div class="timeline-label-row">
              <span>Day 0</span>
              <span>Timeline: Days Covered (Green) vs Gap Days (Red)</span>
              <span>Day ${res.totalDays}</span>
            </div>
            <div class="timeline-bar">
              ${res.intervals.map(iv => `
                <div class="timeline-segment ${iv.covered ? 'seg-covered' : 'seg-gap'}"
                     style="width: ${((iv.end - iv.start) / res.totalDays) * 100}%;"
                     title="Days ${iv.start}–${iv.end}: ${iv.covered ? 'Medication Covered' : 'Refill Gap'}"></div>
              `).join('')}
            </div>
          </div>

          <div class="radar-kpi-deck">
            <div class="kpi-mini-card">
              <span class="kpi-mini-label">Calculated PDC</span>
              <strong class="kpi-mini-val ${res.isAdherent ? 'kpi-good' : 'kpi-warn'}">${res.pdc}%</strong>
              <span class="kpi-mini-sub">${res.coveredDays} of ${res.totalDays} days</span>
            </div>
            <div class="kpi-mini-card">
              <span class="kpi-mini-label">CMS Benchmark</span>
              <strong class="kpi-mini-val">80.0%</strong>
              <span class="kpi-mini-sub">Star Rating Threshold</span>
            </div>
            <div class="kpi-mini-card">
              <span class="kpi-mini-label">Adherence Status</span>
              <strong class="kpi-mini-val ${res.isAdherent ? 'kpi-good' : 'kpi-warn'}">${res.isAdherent ? 'Adherent ✓' : 'Non-Adherent ✕'}</strong>
              <span class="kpi-mini-sub">${res.isAdherent ? 'Eligible for Numerator' : 'Requires MTM Outreach'}</span>
            </div>
          </div>

          <div class="clinical-takeaway">
            <strong>Pharmacy Quality Alliance (PQA) Standard:</strong>
            ${res.isAdherent
              ? `Patient achieved ≥80% Proportion of Days Covered (${res.pdc}%), meeting the CMS Star Rating threshold for chronic disease management (Hypertension/Diabetes/Cholesterol).`
              : `PDC of ${res.pdc}% falls below the 80% threshold. In real health plans, this triggers a Medication Therapy Management (MTM) consultation or 90-day refill sync program.`}
          </div>
        </div>
      </div>
    `;
  }

  function bindEvents() {
    // Tab switching
    host.querySelectorAll(".radar-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        activeTab = tab.dataset.radarTab;
        render();
      });
    });

    if (activeTab === "diagnostic") {
      const prev = host.querySelector("#prevSlider");
      const sens = host.querySelector("#sensSlider");
      const spec = host.querySelector("#specSlider");

      const updateDiag = () => {
        diagState.prevalence = Number(prev.value);
        diagState.sensitivity = Number(sens.value);
        diagState.specificity = Number(spec.value);
        render();
      };

      if (prev) prev.addEventListener("input", updateDiag);
      if (sens) sens.addEventListener("input", updateDiag);
      if (spec) spec.addEventListener("input", updateDiag);
    } else if (activeTab === "lace") {
      const los = host.querySelector("#losInput");
      const charlson = host.querySelector("#charlsonInput");
      const ed = host.querySelector("#edInput");
      const acuteBtns = host.querySelectorAll("[data-acute]");

      if (los) los.addEventListener("input", e => { laceState.los = Math.max(1, Number(e.target.value)); render(); });
      if (charlson) charlson.addEventListener("change", e => { laceState.charlson = Number(e.target.value); render(); });
      if (ed) ed.addEventListener("input", e => { laceState.edVisits = Math.max(0, Number(e.target.value)); render(); });

      acuteBtns.forEach(btn => {
        btn.addEventListener("click", () => {
          laceState.acute = Number(btn.dataset.acute);
          render();
        });
      });
    } else if (activeTab === "pdc") {
      const supply = host.querySelector("#supplySlider");
      const gap = host.querySelector("#gapSlider");
      const period = host.querySelector("#periodSlider");

      const updatePdc = () => {
        pdcState.daysSupply = Number(supply.value);
        pdcState.gapDays = Number(gap.value);
        pdcState.totalPeriod = Number(period.value);
        render();
      };

      if (supply) supply.addEventListener("input", updatePdc);
      if (gap) gap.addEventListener("input", updatePdc);
      if (period) period.addEventListener("input", updatePdc);
    }
  }

  // Initialize
  document.addEventListener("DOMContentLoaded", render);
})();
