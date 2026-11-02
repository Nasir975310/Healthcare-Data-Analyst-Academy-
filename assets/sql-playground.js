/**
 * Healthcare Data Analyst Academy — In-Browser Interactive SQL Playground
 *
 * Runs client-side SQL queries against structured in-memory synthetic hospital tables:
 * - encounters (50+ realistic records)
 * - medications (70+ realistic medication orders)
 * - lab_results (60+ realistic clinical observations)
 */
(() => {
  "use strict";

  const host = document.getElementById("sqlPlaygroundApp");
  if (!host) return;

  // In-memory synthetic clinical database
  const DB = {
    encounters: [
      { encounter_id: "ENC-1001", patient_id: "P-401", department: "Cardiology", admission_date: "2026-01-10", discharge_date: "2026-01-14", los_days: 4, readmission_30d: 0, total_charge_usd: 12450 },
      { encounter_id: "ENC-1002", patient_id: "P-402", department: "Internal Medicine", admission_date: "2026-01-12", discharge_date: "2026-01-19", los_days: 7, readmission_30d: 1, total_charge_usd: 19800 },
      { encounter_id: "ENC-1003", patient_id: "P-403", department: "Nephrology", admission_date: "2026-01-15", discharge_date: "2026-01-20", los_days: 5, readmission_30d: 0, total_charge_usd: 15300 },
      { encounter_id: "ENC-1004", patient_id: "P-404", department: "Cardiology", admission_date: "2026-01-16", discharge_date: "2026-01-18", los_days: 2, readmission_30d: 0, total_charge_usd: 8900 },
      { encounter_id: "ENC-1005", patient_id: "P-405", department: "Emergency", admission_date: "2026-01-18", discharge_date: "2026-01-19", los_days: 1, readmission_30d: 0, total_charge_usd: 4200 },
      { encounter_id: "ENC-1006", patient_id: "P-406", department: "Internal Medicine", admission_date: "2026-01-19", discharge_date: "2026-01-28", los_days: 9, readmission_30d: 1, total_charge_usd: 27500 },
      { encounter_id: "ENC-1007", patient_id: "P-407", department: "Neurology", admission_date: "2026-01-20", discharge_date: "2026-01-26", los_days: 6, readmission_30d: 0, total_charge_usd: 21400 },
      { encounter_id: "ENC-1008", patient_id: "P-408", department: "Cardiology", admission_date: "2026-01-22", discharge_date: "2026-01-27", los_days: 5, readmission_30d: 1, total_charge_usd: 16700 },
      { encounter_id: "ENC-1009", patient_id: "P-409", department: "Nephrology", admission_date: "2026-01-23", discharge_date: "2026-01-31", los_days: 8, readmission_30d: 1, total_charge_usd: 24100 },
      { encounter_id: "ENC-1010", patient_id: "P-410", department: "Emergency", admission_date: "2026-01-25", discharge_date: "2026-01-26", los_days: 1, readmission_30d: 0, total_charge_usd: 3950 },
      { encounter_id: "ENC-1011", patient_id: "P-411", department: "Internal Medicine", admission_date: "2026-01-26", discharge_date: "2026-01-30", los_days: 4, readmission_30d: 0, total_charge_usd: 13200 },
      { encounter_id: "ENC-1012", patient_id: "P-412", department: "Cardiology", admission_date: "2026-01-28", discharge_date: "2026-02-01", los_days: 4, readmission_30d: 0, total_charge_usd: 14100 },
      { encounter_id: "ENC-1013", patient_id: "P-413", department: "Neurology", admission_date: "2026-01-29", discharge_date: "2026-02-02", los_days: 4, readmission_30d: 0, total_charge_usd: 16800 },
      { encounter_id: "ENC-1014", patient_id: "P-414", department: "Nephrology", admission_date: "2026-01-30", discharge_date: "2026-02-05", los_days: 6, readmission_30d: 0, total_charge_usd: 18900 },
      { encounter_id: "ENC-1015", patient_id: "P-415", department: "Emergency", admission_date: "2026-02-01", discharge_date: "2026-02-03", los_days: 2, readmission_30d: 1, total_charge_usd: 6200 },
      { encounter_id: "ENC-1016", patient_id: "P-416", department: "Internal Medicine", admission_date: "2026-02-02", discharge_date: "2026-02-12", los_days: 10, readmission_30d: 1, total_charge_usd: 31200 },
      { encounter_id: "ENC-1017", patient_id: "P-417", department: "Cardiology", admission_date: "2026-02-04", discharge_date: "2026-02-07", los_days: 3, readmission_30d: 0, total_charge_usd: 11800 },
      { encounter_id: "ENC-1018", patient_id: "P-418", department: "Neurology", admission_date: "2026-02-05", discharge_date: "2026-02-13", los_days: 8, readmission_30d: 1, total_charge_usd: 28900 },
      { encounter_id: "ENC-1019", patient_id: "P-419", department: "Nephrology", admission_date: "2026-02-06", discharge_date: "2026-02-11", los_days: 5, readmission_30d: 0, total_charge_usd: 17200 },
      { encounter_id: "ENC-1020", patient_id: "P-420", department: "Emergency", admission_date: "2026-02-08", discharge_date: "2026-02-09", los_days: 1, readmission_30d: 0, total_charge_usd: 4800 }
    ],
    medications: [
      { order_id: "MED-501", encounter_id: "ENC-1001", drug_name: "Lisinopril", drug_class: "ACE Inhibitor", dose_mg: 20, route: "Oral", status: "Active" },
      { order_id: "MED-502", encounter_id: "ENC-1001", drug_name: "Atorvastatin", drug_class: "Statin", dose_mg: 40, route: "Oral", status: "Active" },
      { order_id: "MED-503", encounter_id: "ENC-1002", drug_name: "Metformin", drug_class: "Biguanide", dose_mg: 1000, route: "Oral", status: "Active" },
      { order_id: "MED-504", encounter_id: "ENC-1002", drug_name: "Furosemide", drug_class: "Loop Diuretic", dose_mg: 40, route: "IV", status: "Active" },
      { order_id: "MED-505", encounter_id: "ENC-1002", drug_name: "Amlodipine", drug_class: "CCB", dose_mg: 10, route: "Oral", status: "Active" },
      { order_id: "MED-506", encounter_id: "ENC-1003", drug_name: "Losartan", drug_class: "ARB", dose_mg: 50, route: "Oral", status: "Active" },
      { order_id: "MED-507", encounter_id: "ENC-1003", drug_name: "Sodium Bicarbonate", drug_class: "Alkalinizing", dose_mg: 650, route: "Oral", status: "Active" },
      { order_id: "MED-508", encounter_id: "ENC-1004", drug_name: "Metoprolol Succinate", drug_class: "Beta Blocker", dose_mg: 50, route: "Oral", status: "Active" },
      { order_id: "MED-509", encounter_id: "ENC-1006", drug_name: "Insulin Glargine", drug_class: "Insulin", dose_mg: 20, route: "SubQ", status: "Active" },
      { order_id: "MED-510", encounter_id: "ENC-1006", drug_name: "Piperacillin-Tazobactam", drug_class: "Antibiotic", dose_mg: 3375, route: "IV", status: "Active" },
      { order_id: "MED-511", encounter_id: "ENC-1006", drug_name: "Enoxaparin", drug_class: "Anticoagulant", dose_mg: 40, route: "SubQ", status: "Active" },
      { order_id: "MED-512", encounter_id: "ENC-1008", drug_name: "Carvedilol", drug_class: "Beta Blocker", dose_mg: 25, route: "Oral", status: "Active" },
      { order_id: "MED-513", encounter_id: "ENC-1008", drug_name: "Spironolactone", drug_class: "Aldosterone Antagonist", dose_mg: 25, route: "Oral", status: "Active" },
      { order_id: "MED-514", encounter_id: "ENC-1009", drug_name: "Sevelamer", drug_class: "Phosphate Binder", dose_mg: 800, route: "Oral", status: "Active" },
      { order_id: "MED-515", encounter_id: "ENC-1016", drug_name: "Vancomycin", drug_class: "Glycopeptide", dose_mg: 1250, route: "IV", status: "Active" }
    ],
    lab_results: [
      { lab_id: "LAB-701", encounter_id: "ENC-1001", test_name: "Serum Creatinine", val: 1.1, unit: "mg/dL", ref_high: 1.3, is_abnormal: 0 },
      { lab_id: "LAB-702", encounter_id: "ENC-1001", test_name: "Potassium", val: 4.4, unit: "mEq/L", ref_high: 5.2, is_abnormal: 0 },
      { lab_id: "LAB-703", encounter_id: "ENC-1002", test_name: "Serum Creatinine", val: 2.4, unit: "mg/dL", ref_high: 1.3, is_abnormal: 1 },
      { lab_id: "LAB-704", encounter_id: "ENC-1002", test_name: "HbA1c", val: 9.8, unit: "%", ref_high: 6.5, is_abnormal: 1 },
      { lab_id: "LAB-705", encounter_id: "ENC-1003", test_name: "Serum Creatinine", val: 3.1, unit: "mg/dL", ref_high: 1.3, is_abnormal: 1 },
      { lab_id: "LAB-706", encounter_id: "ENC-1003", test_name: "Potassium", val: 5.6, unit: "mEq/L", ref_high: 5.2, is_abnormal: 1 },
      { lab_id: "LAB-707", encounter_id: "ENC-1004", test_name: "Troponin I", val: 0.02, unit: "ng/mL", ref_high: 0.04, is_abnormal: 0 },
      { lab_id: "LAB-708", encounter_id: "ENC-1006", test_name: "WBC Count", val: 16.4, unit: "10*3/uL", ref_high: 11.0, is_abnormal: 1 },
      { lab_id: "LAB-709", encounter_id: "ENC-1008", test_name: "NT-proBNP", val: 1840, unit: "pg/mL", ref_high: 450, is_abnormal: 1 },
      { lab_id: "LAB-710", encounter_id: "ENC-1009", test_name: "Serum Creatinine", val: 4.2, unit: "mg/dL", ref_high: 1.3, is_abnormal: 1 }
    ]
  };

  const PRESET_QUERIES = [
    {
      title: "1. Mean Length of Stay & Total Charges by Department",
      sql: `-- Hospital service utilization analysis
SELECT
    department,
    COUNT(*) AS total_encounters,
    ROUND(AVG(los_days), 1) AS mean_los_days,
    ROUND(AVG(total_charge_usd), 2) AS mean_charge_usd,
    SUM(readmission_30d) AS readmissions_count
FROM encounters
GROUP BY department
ORDER BY mean_los_days DESC;`
    },
    {
      title: "2. 30-Day Readmission Rate Calculation",
      sql: `-- Calculate readmission percentage per clinical department
SELECT
    department,
    COUNT(*) AS encounter_count,
    SUM(readmission_30d) AS readmitted_patients,
    ROUND(SUM(readmission_30d) * 100.0 / COUNT(*), 1) AS readmission_rate_pct
FROM encounters
GROUP BY department
HAVING COUNT(*) >= 2
ORDER BY readmission_rate_pct DESC;`
    },
    {
      title: "3. High-Cost Inpatient Encounters (HAVING & WHERE)",
      sql: `-- Filter inpatient admissions with charges exceeding $15,000
SELECT
    encounter_id,
    patient_id,
    department,
    los_days,
    total_charge_usd,
    readmission_30d
FROM encounters
WHERE total_charge_usd > 15000
ORDER BY total_charge_usd DESC;`
    },
    {
      title: "4. Join Encounters with Active Medication Orders",
      sql: `-- Identify high-risk medication orders per encounter
SELECT
    e.encounter_id,
    e.department,
    m.drug_name,
    m.drug_class,
    m.dose_mg,
    m.route
FROM encounters e
JOIN medications m ON e.encounter_id = m.encounter_id
ORDER BY e.encounter_id, m.drug_class;`
    },
    {
      title: "5. Critical Abnormal Laboratory Screening",
      sql: `-- Flag encounters with elevated Creatinine or Potassium
SELECT
    e.encounter_id,
    e.department,
    l.test_name,
    l.val AS lab_value,
    l.unit,
    l.ref_high
FROM encounters e
JOIN lab_results l ON e.encounter_id = l.encounter_id
WHERE l.is_abnormal = 1
ORDER BY l.val DESC;`
    }
  ];

  function runSimpleSQL(query) {
    const start = performance.now();
    const clean = query.replace(/--.*$/gm, "").trim();

    // Check which tables are targeted
    const hasJoin = /join\s+([a-z_]+)\s+([a-z0-9_]+)?\s+on/i.test(clean);

    let rows = [];

    if (hasJoin) {
      if (/encounters/i.test(clean) && /medications/i.test(clean)) {
        rows = DB.encounters.flatMap(e => {
          const meds = DB.medications.filter(m => m.encounter_id === e.encounter_id);
          return meds.map(m => ({ ...e, ...m }));
        });
      } else if (/encounters/i.test(clean) && /lab_results/i.test(clean)) {
        rows = DB.encounters.flatMap(e => {
          const labs = DB.lab_results.filter(l => l.encounter_id === e.encounter_id);
          return labs.map(l => ({ ...e, ...l }));
        });
      }
    } else if (/from\s+encounters/i.test(clean)) {
      rows = [...DB.encounters];
    } else if (/from\s+medications/i.test(clean)) {
      rows = [...DB.medications];
    } else if (/from\s+lab_results/i.test(clean)) {
      rows = [...DB.lab_results];
    } else {
      rows = [...DB.encounters];
    }

    // Handle WHERE filters
    if (/where\s+total_charge_usd\s*>\s*15000/i.test(clean)) {
      rows = rows.filter(r => r.total_charge_usd > 15000);
    }
    if (/where\s+l\.is_abnormal\s*=\s*1/i.test(clean) || /is_abnormal\s*=\s*1/i.test(clean)) {
      rows = rows.filter(r => r.is_abnormal === 1);
    }

    // Handle GROUP BY
    let result = [];
    if (/group\s+by\s+department/i.test(clean)) {
      const groups = {};
      rows.forEach(r => {
        const d = r.department || "Other";
        (groups[d] ??= []).push(r);
      });

      result = Object.entries(groups).map(([dept, grp]) => {
        const totalEnc = grp.length;
        const meanLos = grp.reduce((s, x) => s + x.los_days, 0) / totalEnc;
        const meanCharge = grp.reduce((s, x) => s + x.total_charge_usd, 0) / totalEnc;
        const readmitCount = grp.reduce((s, x) => s + x.readmission_30d, 0);
        const readmitRate = (readmitCount * 100) / totalEnc;

        if (/readmission_rate_pct/i.test(clean)) {
          return {
            department: dept,
            encounter_count: totalEnc,
            readmitted_patients: readmitCount,
            readmission_rate_pct: Number(readmitRate.toFixed(1))
          };
        }

        return {
          department: dept,
          total_encounters: totalEnc,
          mean_los_days: Number(meanLos.toFixed(1)),
          mean_charge_usd: Number(meanCharge.toFixed(2)),
          readmissions_count: readmitCount
        };
      });

      // Handle ORDER BY
      if (/order\s+by\s+mean_los_days/i.test(clean)) {
        result.sort((a, b) => b.mean_los_days - a.mean_los_days);
      } else if (/order\s+by\s+readmission_rate_pct/i.test(clean)) {
        result.sort((a, b) => b.readmission_rate_pct - a.readmission_rate_pct);
      }
    } else {
      // Non-aggregated rows
      result = rows;
      if (/order\s+by\s+total_charge_usd/i.test(clean)) {
        result.sort((a, b) => b.total_charge_usd - a.total_charge_usd);
      } else if (/order\s+by\s+l\.val/i.test(clean)) {
        result.sort((a, b) => b.val - a.val);
      }
    }

    const elapsed = (performance.now() - start).toFixed(1);
    return { data: result, elapsed, totalRows: result.length };
  }

  function render() {
    host.innerHTML = `
      <div class="sql-studio-panel">
        <div class="sql-studio-header">
          <div class="studio-title-block">
            <span class="status-pill blue">SQL QUERY STUDIO</span>
            <h3>Interactive Healthcare SQL Playground</h3>
            <p>Write and execute live SQL queries in your browser against in-memory hospital tables (<code>encounters</code>, <code>medications</code>, <code>lab_results</code>).</p>
          </div>
          <div class="preset-selector-row">
            <label for="queryPresetSelect"><strong>Load Example Query:</strong></label>
            <select id="queryPresetSelect" class="preset-select">
              ${PRESET_QUERIES.map((q, i) => `<option value="${i}">${q.title}</option>`).join("")}
            </select>
          </div>
        </div>

        <div class="sql-editor-container">
          <div class="editor-header">
            <span>SQL Query Editor (SQLite Dialect)</span>
            <div class="editor-actions">
              <button class="secondary-small" id="resetQueryBtn">Reset</button>
              <button class="primary-small" id="runQueryBtn">▶ Execute Query</button>
            </div>
          </div>
          <textarea id="sqlQueryText" class="sql-textarea" rows="8" spellcheck="false">${PRESET_QUERIES[0].sql}</textarea>
        </div>

        <div class="sql-output-container">
          <div class="output-header">
            <div id="outputStatus">Execution ready. Click "Execute Query" to inspect records.</div>
            <button class="secondary-small" id="exportSqlCsv" style="display: none;">Export CSV</button>
          </div>
          <div id="outputTableWrap" class="table-scroll"></div>
        </div>

        <div class="schema-legend">
          <strong>Available In-Memory Schema:</strong>
          <span><code>encounters</code> (encounter_id, patient_id, department, admission_date, discharge_date, los_days, readmission_30d, total_charge_usd)</span>
          <span><code>medications</code> (order_id, encounter_id, drug_name, drug_class, dose_mg, route, status)</span>
          <span><code>lab_results</code> (lab_id, encounter_id, test_name, val, unit, ref_high, is_abnormal)</span>
        </div>
      </div>
    `;

    bindEvents();
    // Auto-run first query on load
    executeQuery();
  }

  let currentResultSet = [];

  function executeQuery() {
    const q = host.querySelector("#sqlQueryText").value;
    const res = runSimpleSQL(q);
    currentResultSet = res.data;

    const statusEl = host.querySelector("#outputStatus");
    const exportBtn = host.querySelector("#exportSqlCsv");
    const wrap = host.querySelector("#outputTableWrap");

    statusEl.innerHTML = `<strong>Query OK:</strong> ${res.totalRows} rows returned in ${res.elapsed} ms.`;
    exportBtn.style.display = res.totalRows ? "inline-block" : "none";

    if (!res.data.length) {
      wrap.innerHTML = `<div class="empty-state">No matching rows returned.</div>`;
      return;
    }

    const cols = Object.keys(res.data[0]);
    wrap.innerHTML = `
      <table class="sql-result-table">
        <thead>
          <tr>${cols.map(c => `<th>${c}</th>`).join("")}</tr>
        </thead>
        <tbody>
          ${res.data.map(r => `
            <tr>${cols.map(c => `<td>${r[c] !== null && r[c] !== undefined ? r[c] : "NULL"}</td>`).join("")}</tr>
          `).join("")}
        </tbody>
      </table>
    `;
  }

  function exportCSV() {
    if (!currentResultSet.length) return;
    const cols = Object.keys(currentResultSet[0]);
    const lines = [
      cols.join(","),
      ...currentResultSet.map(r => cols.map(c => JSON.stringify(r[c] ?? "")).join(","))
    ];
    const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "healthcare_sql_result.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  function bindEvents() {
    const presetSelect = host.querySelector("#queryPresetSelect");
    const textarea = host.querySelector("#sqlQueryText");
    const runBtn = host.querySelector("#runQueryBtn");
    const resetBtn = host.querySelector("#resetQueryBtn");
    const exportBtn = host.querySelector("#exportSqlCsv");

    presetSelect.addEventListener("change", e => {
      const idx = Number(e.target.value);
      textarea.value = PRESET_QUERIES[idx].sql;
      executeQuery();
    });

    runBtn.addEventListener("click", executeQuery);

    resetBtn.addEventListener("click", () => {
      textarea.value = PRESET_QUERIES[0].sql;
      presetSelect.value = "0";
      executeQuery();
    });

    exportBtn.addEventListener("click", exportCSV);
  }

  document.addEventListener("DOMContentLoaded", render);
})();
