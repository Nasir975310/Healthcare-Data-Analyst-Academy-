/**
 * Healthcare Data Analyst Academy — Interactive Biostatistics & Survival Analysis Studio
 *
 * Implements:
 * 1. Interactive Kaplan-Meier Survival Curve Simulator (Monotherapy vs Dual Therapy)
 * 2. CONSORT Observational Cohort Attrition Flowchart Visualizer
 */
(() => {
  "use strict";

  const host = document.getElementById("cohortSurvivalStudioApp");
  if (!host) return;

  let activeMode = "kaplan-meier"; // "kaplan-meier" | "consort"
  let selectedEndpoint = "bp_control"; // "bp_control" | "readmission"

  // Synthetic Kaplan-Meier survival curves
  const KM_DATA = {
    bp_control: {
      title: "Time to Blood Pressure Control Event (Days to SBP < 140/90 mmHg)",
      endpointName: "Event-Free Survival (Sustained BP Control)",
      timePoints: [0, 30, 60, 90, 180, 270, 365],
      groupA: {
        name: "Monotherapy (ACEi / ARB)",
        rates: [1.0, 0.88, 0.76, 0.68, 0.58, 0.52, 0.48],
        atRisk: [450, 396, 342, 306, 261, 234, 216],
        color: "#2563eb"
      },
      groupB: {
        name: "Dual Combination (ACEi + CCB)",
        rates: [1.0, 0.94, 0.89, 0.82, 0.77, 0.73, 0.70],
        atRisk: [480, 451, 427, 393, 369, 350, 336],
        color: "#0d9488"
      },
      hazardRatio: "0.56",
      ci95: "0.45 – 0.70",
      pValue: "< 0.001",
      interpretation: "Patients receiving combination therapy (ACEi + CCB) demonstrated a 44% hazard reduction in failing blood pressure target milestones compared to monotherapy over 12 months (HR 0.56, 95% CI 0.45-0.70, Log-Rank p < 0.001)."
    },
    readmission: {
      title: "Time to 30-Day All-Cause Cardiovascular Hospital Readmission",
      endpointName: "Readmission-Free Probability",
      timePoints: [0, 30, 60, 90, 180, 270, 365],
      groupA: {
        name: "Usual Outpatient Care",
        rates: [1.0, 0.82, 0.74, 0.70, 0.64, 0.60, 0.58],
        atRisk: [510, 418, 377, 357, 326, 306, 295],
        color: "#dc2626"
      },
      groupB: {
        name: "Pharmacist-Led MTM Transitional Care",
        rates: [1.0, 0.93, 0.88, 0.85, 0.81, 0.78, 0.76],
        atRisk: [520, 483, 457, 442, 421, 405, 395],
        color: "#059669"
      },
      hazardRatio: "0.49",
      ci95: "0.38 – 0.63",
      pValue: "< 0.001",
      interpretation: "The pharmacist-led medication reconciliation and transitional care arm achieved a statistically significant 51% reduction in hospital readmission rate at 12 months compared to usual care (HR 0.49, 95% CI 0.38-0.63, p < 0.001)."
    }
  };

  // CONSORT Cohort Filter Criteria
  const consortCriteria = {
    screened: 2400,
    filters: [
      { id: "age", label: "Adult Patients (Age 18–75)", excluded: 210, reason: "Pediatric (<18) or Geriatric (>75) exclusions" },
      { id: "dx", label: "Confirmed Hypertension (ICD-10 I10)", excluded: 340, reason: "Secondary HTN or isolated white-coat reading" },
      { id: "sbp", label: "Valid Baseline & Follow-up SBP Pairs", excluded: 195, reason: "Missing 90-day follow-up encounter or unverified manual cuff" },
      { id: "ckd", label: "Exclude Severe End-Stage Renal Disease (eGFR < 15)", excluded: 85, reason: "Dialysis-dependent confounders" }
    ]
  };

  function render() {
    host.innerHTML = `
      <div class="survival-studio-card">
        <div class="survival-header">
          <div class="survival-title-block">
            <span class="status-pill teal">BIOSTATISTICS & EPIDEMIOLOGY STUDIO</span>
            <h3>Clinical Cohort & Survival Analysis Laboratory</h3>
            <p>Interactive step-function Kaplan–Meier survival curves, hazard ratio estimation, and CONSORT cohort attrition analysis.</p>
          </div>
          <div class="survival-tab-group">
            <button class="survival-tab ${activeMode === 'kaplan-meier' ? 'active' : ''}" data-mode="kaplan-meier">Kaplan–Meier Curves</button>
            <button class="survival-tab ${activeMode === 'consort' ? 'active' : ''}" data-mode="consort">CONSORT Cohort Attrition</button>
          </div>
        </div>

        <div class="survival-body">
          ${activeMode === 'kaplan-meier' ? renderKMView() : renderConsortView()}
        </div>
      </div>
    `;

    bindEvents();
  }

  function renderKMView() {
    const data = KM_DATA[selectedEndpoint];
    const width = 680;
    const height = 300;
    const padLeft = 55;
    const padRight = 30;
    const padTop = 30;
    const padBottom = 45;

    const plotW = width - padLeft - padRight;
    const plotH = height - padTop - padBottom;
    const maxT = 365;

    // Generate SVG path for a step curve
    const makeStepPath = (times, rates) => {
      let path = "";
      for (let i = 0; i < times.length; i++) {
        const x = padLeft + (times[i] / maxT) * plotW;
        const y = padTop + (1.0 - rates[i]) * plotH;
        if (i === 0) {
          path += `M ${x} ${y} `;
        } else {
          const prevY = padTop + (1.0 - rates[i - 1]) * plotH;
          path += `L ${x} ${prevY} L ${x} ${y} `;
        }
      }
      return path;
    };

    const pathA = makeStepPath(data.timePoints, data.groupA.rates);
    const pathB = makeStepPath(data.timePoints, data.groupB.rates);

    return `
      <div class="km-container">
        <div class="km-toolbar">
          <label><strong>Clinical Endpoint:</strong></label>
          <select id="endpointSelect" class="preset-select">
            <option value="bp_control" ${selectedEndpoint === 'bp_control' ? 'selected' : ''}>Blood Pressure Target Achievement (Monotherapy vs Dual Therapy)</option>
            <option value="readmission" ${selectedEndpoint === 'readmission' ? 'selected' : ''}>30-Day Hospital Readmission (Usual Care vs MTM Care)</option>
          </select>
        </div>

        <div class="km-plot-wrap">
          <svg viewBox="0 0 ${width} ${height}" class="km-svg" role="img" aria-label="${data.title}">
            <!-- Grid lines -->
            <line x1="${padLeft}" y1="${padTop}" x2="${width - padRight}" y2="${padTop}" stroke="var(--line)" stroke-dasharray="4" />
            <line x1="${padLeft}" y1="${padTop + plotH * 0.25}" x2="${width - padRight}" y2="${padTop + plotH * 0.25}" stroke="var(--line)" stroke-dasharray="4" />
            <line x1="${padLeft}" y1="${padTop + plotH * 0.5}" x2="${width - padRight}" y2="${padTop + plotH * 0.5}" stroke="var(--line)" stroke-dasharray="4" />
            <line x1="${padLeft}" y1="${padTop + plotH * 0.75}" x2="${width - padRight}" y2="${padTop + plotH * 0.75}" stroke="var(--line)" stroke-dasharray="4" />
            <line x1="${padLeft}" y1="${padTop + plotH}" x2="${width - padRight}" y2="${padTop + plotH}" stroke="currentColor" />

            <!-- Y Axis Labels -->
            <text x="${padLeft - 10}" y="${padTop + 4}" text-anchor="end" font-size="11" fill="currentColor">1.0</text>
            <text x="${padLeft - 10}" y="${padTop + plotH * 0.25 + 4}" text-anchor="end" font-size="11" fill="currentColor">0.75</text>
            <text x="${padLeft - 10}" y="${padTop + plotH * 0.5 + 4}" text-anchor="end" font-size="11" fill="currentColor">0.50</text>
            <text x="${padLeft - 10}" y="${padTop + plotH * 0.75 + 4}" text-anchor="end" font-size="11" fill="currentColor">0.25</text>
            <text x="${padLeft - 10}" y="${padTop + plotH + 4}" text-anchor="end" font-size="11" fill="currentColor">0.0</text>

            <!-- X Axis Ticks & Labels -->
            ${data.timePoints.map(t => {
              const x = padLeft + (t / maxT) * plotW;
              return `
                <line x1="${x}" y1="${padTop + plotH}" x2="${x}" y2="${padTop + plotH + 6}" stroke="currentColor" />
                <text x="${x}" y="${padTop + plotH + 18}" text-anchor="middle" font-size="11" fill="currentColor">${t}d</text>
              `;
            }).join("")}

            <!-- Step Curves -->
            <path d="${pathA}" fill="none" stroke="${data.groupA.color}" stroke-width="2.8" />
            <path d="${pathB}" fill="none" stroke="${data.groupB.color}" stroke-width="2.8" />

            <!-- Censoring ticks / dots -->
            ${data.timePoints.slice(1).map((t, i) => {
              const x = padLeft + (t / maxT) * plotW;
              const yA = padTop + (1.0 - data.groupA.rates[i + 1]) * plotH;
              const yB = padTop + (1.0 - data.groupB.rates[i + 1]) * plotH;
              return `
                <circle cx="${x}" cy="${yA}" r="3.5" fill="${data.groupA.color}" />
                <circle cx="${x}" cy="${yB}" r="3.5" fill="${data.groupB.color}" />
              `;
            }).join("")}
          </svg>
        </div>

        <!-- Legend and Statistical Summary Deck -->
        <div class="km-stat-deck">
          <div class="km-legend-row">
            <span class="legend-badge" style="background: ${data.groupA.color};"></span>
            <strong>${data.groupA.name}</strong>
            <span class="legend-badge" style="background: ${data.groupB.color}; margin-left: 20px;"></span>
            <strong>${data.groupB.name}</strong>
          </div>

          <div class="km-metrics-grid">
            <div class="km-metric-card">
              <span class="km-metric-lbl">Hazard Ratio (HR)</span>
              <strong class="km-metric-val">${data.hazardRatio}</strong>
              <small>Cox Proportional Hazards</small>
            </div>
            <div class="km-metric-card">
              <span class="km-metric-lbl">95% Confidence Interval</span>
              <strong class="km-metric-val">${data.ci95}</strong>
              <small>Wald 95% CI</small>
            </div>
            <div class="km-metric-card">
              <span class="km-metric-lbl">Log-Rank Test p-value</span>
              <strong class="km-metric-val km-sig">${data.pValue}</strong>
              <small>Statistically Significant</small>
            </div>
          </div>
        </div>

        <!-- Number at Risk Table -->
        <div class="at-risk-table-wrap">
          <h4>Number at Risk by Follow-Up Interval</h4>
          <table class="at-risk-table">
            <thead>
              <tr>
                <th>Cohort / Intervention</th>
                ${data.timePoints.map(t => `<th>Day ${t}</th>`).join("")}
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color: ${data.groupA.color}">${data.groupA.name}</strong></td>
                ${data.groupA.atRisk.map(n => `<td>${n}</td>`).join("")}
              </tr>
              <tr>
                <td><strong style="color: ${data.groupB.color}">${data.groupB.name}</strong></td>
                ${data.groupB.atRisk.map(n => `<td>${n}</td>`).join("")}
              </tr>
            </tbody>
          </table>
        </div>

        <div class="clinical-takeaway">
          <strong>Epidemiological Interpretation:</strong>
          <p>${data.interpretation}</p>
        </div>
      </div>
    `;
  }

  function renderConsortView() {
    let currentCount = consortCriteria.screened;
    const stages = [];

    stages.push({
      stepName: "Initial Screening Cohort",
      n: currentCount,
      retainedPct: 100,
      details: "Total patient encounters identified in synthetic hospital EHR"
    });

    consortCriteria.filters.forEach(f => {
      currentCount -= f.excluded;
      const pct = Math.round((currentCount / consortCriteria.screened) * 100);
      stages.push({
        stepName: `Included: ${f.label}`,
        n: currentCount,
        excludedCount: f.excluded,
        excludedReason: f.reason,
        retainedPct: pct
      });
    });

    return `
      <div class="consort-container">
        <div class="consort-intro">
          <strong>CONSORT (Consolidated Standards of Reporting Trials) Diagram:</strong>
          <p>Transparent clinical cohort selection protocol. Review step-by-step exclusions to eliminate selection bias and ensure reproducible observational analytics.</p>
        </div>

        <div class="consort-flow">
          ${stages.map((st, idx) => `
            <div class="consort-node">
              <div class="consort-box">
                <div class="node-header">
                  <strong>${st.stepName}</strong>
                  <span class="node-n">N = ${st.n.toLocaleString()}</span>
                </div>
                <div class="node-progress-track">
                  <div class="node-progress-fill" style="width: ${st.retainedPct}%;"></div>
                </div>
                <div class="node-footer">
                  <span>${st.retainedPct}% retained</span>
                  <small>${st.details || "Meets clinical inclusion criteria"}</small>
                </div>
              </div>

              ${st.excludedCount ? `
                <div class="consort-exclusion-branch">
                  <div class="branch-arrow">↳</div>
                  <div class="exclusion-card">
                    <span class="excl-count">Excluded (n = ${st.excludedCount.toLocaleString()})</span>
                    <span class="excl-reason">${st.excludedReason}</span>
                  </div>
                </div>
              ` : ''}
            </div>
            ${idx < stages.length - 1 ? '<div class="consort-connector">↓</div>' : ''}
          `).join("")}
        </div>

        <div class="clinical-takeaway" style="margin-top: 20px;">
          <strong>Data Governance Note:</strong>
          <p>Of 2,400 screened records, <strong>${currentCount.toLocaleString()}</strong> patients (${Math.round((currentCount / 2400) * 100)}%) fulfilled all eligibility requirements. Documenting this attrition pipeline ensures study validity for regulatory submissions and peer-reviewed journals.</p>
        </div>
      </div>
    `;
  }

  function bindEvents() {
    host.querySelectorAll(".survival-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        activeMode = tab.dataset.mode;
        render();
      });
    });

    const epSelect = host.querySelector("#endpointSelect");
    if (epSelect) {
      epSelect.addEventListener("change", e => {
        selectedEndpoint = e.target.value;
        render();
      });
    }
  }

  document.addEventListener("DOMContentLoaded", render);
})();
