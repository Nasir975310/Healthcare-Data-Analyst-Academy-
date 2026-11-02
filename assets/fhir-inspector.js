/**
 * Healthcare Data Analyst Academy — Interactive FHIR R4 Clinical Resource Inspector
 *
 * Provides in-browser exploration, tree inspection, and FHIRPath evaluation
 * for Fast Healthcare Interoperability Resources (HL7 FHIR R4 / US Core).
 */
(() => {
  "use strict";

  const host = document.getElementById("fhirInspectorApp");
  if (!host) return;

  const FHIR_RESOURCES = {
    patient: {
      resourceType: "Patient",
      id: "hda-pat-94021",
      meta: {
        profile: ["http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"]
      },
      active: true,
      name: [
        {
          use: "official",
          family: "Miller",
          given: ["Jonathan", "David"]
        }
      ],
      telecom: [
        {
          system: "phone",
          value: "+1-555-839-2041",
          use: "home"
        }
      ],
      gender: "male",
      birthDate: "1978-04-12",
      address: [
        {
          use: "home",
          line: ["42 Healthcare Parkway"],
          city: "Boston",
          state: "MA",
          postalCode: "02115",
          country: "US"
        }
      ],
      communication: [
        {
          language: {
            coding: [
              {
                system: "urn:ietf:bcp:47",
                code: "en",
                display: "English"
              }
            ]
          },
          preferred: true
        }
      ]
    },
    observation_bp: {
      resourceType: "Observation",
      id: "hda-obs-bp-104",
      meta: {
        profile: ["http://hl7.org/fhir/StructureDefinition/vitalsigns"]
      },
      status: "final",
      category: [
        {
          coding: [
            {
              system: "http://terminology.hl7.org/CodeSystem/observation-category",
              code: "vital-signs",
              display: "Vital Signs"
            }
          ]
        }
      ],
      code: {
        coding: [
          {
            system: "http://loinc.org",
            code: "85354-9",
            display: "Blood pressure panel with all children optional"
          }
        ],
        text: "Blood pressure systolic & diastolic"
      },
      subject: {
        reference: "Patient/hda-pat-94021",
        display: "Jonathan Miller"
      },
      effectiveDateTime: "2026-02-14T09:30:00Z",
      component: [
        {
          code: {
            coding: [
              {
                system: "http://loinc.org",
                code: "8480-6",
                display: "Systolic blood pressure"
              }
            ]
          },
          valueQuantity: {
            value: 142,
            unit: "mmHg",
            system: "http://unitsofmeasure.org",
            code: "mm[Hg]"
          }
        },
        {
          code: {
            coding: [
              {
                system: "http://loinc.org",
                code: "8462-4",
                display: "Diastolic blood pressure"
              }
            ]
          },
          valueQuantity: {
            value: 88,
            unit: "mmHg",
            system: "http://unitsofmeasure.org",
            code: "mm[Hg]"
          }
        }
      ]
    },
    observation_a1c: {
      resourceType: "Observation",
      id: "hda-obs-a1c-302",
      status: "final",
      category: [
        {
          coding: [
            {
              system: "http://terminology.hl7.org/CodeSystem/observation-category",
              code: "laboratory",
              display: "Laboratory"
            }
          ]
        }
      ],
      code: {
        coding: [
          {
            system: "http://loinc.org",
            code: "4548-4",
            display: "Hemoglobin A1c/Hemoglobin.total in Blood"
          }
        ],
        text: "HbA1c"
      },
      subject: {
        reference: "Patient/hda-pat-94021",
        display: "Jonathan Miller"
      },
      effectiveDateTime: "2026-02-10T11:15:00Z",
      valueQuantity: {
        value: 7.8,
        unit: "%",
        system: "http://unitsofmeasure.org",
        code: "%"
      },
      referenceRange: [
        {
          high: {
            value: 6.5,
            unit: "%"
          },
          text: "Diagnostic threshold for Diabetes Mellitus: >= 6.5%"
        }
      ]
    },
    medication_request: {
      resourceType: "MedicationRequest",
      id: "hda-med-req-501",
      status: "active",
      intent: "order",
      medicationCodeableConcept: {
        coding: [
          {
            system: "http://www.nlm.nih.gov/research/umls/rxnorm",
            code: "314076",
            display: "Lisinopril 20 MG Oral Tablet"
          }
        ],
        text: "Lisinopril 20mg Tablet"
      },
      subject: {
        reference: "Patient/hda-pat-94021",
        display: "Jonathan Miller"
      },
      authoredOn: "2026-02-14",
      dosageInstruction: [
        {
          text: "Take 1 tablet (20 mg) orally once daily in the morning",
          timing: {
            repeat: {
              frequency: 1,
              period: 1,
              periodUnit: "d"
            }
          },
          route: {
            coding: [
              {
                system: "http://snomed.info/sct",
                code: "260548002",
                display: "Oral"
              }
            ]
          },
          doseAndRate: [
            {
              doseQuantity: {
                value: 20,
                unit: "mg",
                system: "http://unitsofmeasure.org",
                code: "mg"
              }
            }
          ]
        }
      ]
    },
    condition: {
      resourceType: "Condition",
      id: "hda-cond-htn-201",
      clinicalStatus: {
        coding: [
          {
            system: "http://terminology.hl7.org/CodeSystem/condition-clinical",
            code: "active"
          }
        ]
      },
      verificationStatus: {
        coding: [
          {
            system: "http://terminology.hl7.org/CodeSystem/condition-ver-status",
            code: "confirmed"
          }
        ]
      },
      code: {
        coding: [
          {
            system: "http://hl7.org/fhir/sid/icd-10-cm",
            code: "I10",
            display: "Essential (primary) hypertension"
          },
          {
            system: "http://snomed.info/sct",
            code: "59621000",
            display: "Essential hypertension (disorder)"
          }
        ],
        text: "Essential Hypertension"
      },
      subject: {
        reference: "Patient/hda-pat-94021",
        display: "Jonathan Miller"
      },
      recordedDate: "2025-08-19"
    }
  };

  let currentKey = "patient";
  let activeMode = "visual"; // "visual" | "json"

  function evaluateFHIRPath(resource, path) {
    if (!path.trim()) return resource;
    try {
      const parts = path.split(".").map(p => p.trim()).filter(Boolean);
      let curr = resource;
      for (const p of parts) {
        if (curr === null || curr === undefined) return undefined;
        // Check for array indexing like component[0]
        const match = p.match(/^([a-zA-Z0-9_]+)\[([0-9]+)\]$/);
        if (match) {
          const prop = match[1];
          const idx = Number(match[2]);
          curr = curr[prop]?.[idx];
        } else {
          curr = curr[p];
        }
      }
      return curr;
    } catch (e) {
      return `Error evaluating path: ${e.message}`;
    }
  }

  function render() {
    const resource = FHIR_RESOURCES[currentKey];

    host.innerHTML = `
      <div class="fhir-studio-card">
        <div class="fhir-header">
          <div>
            <span class="status-pill teal">INTEROPERABILITY EXPLORER</span>
            <h3>HL7 FHIR R4 Resource Inspector</h3>
            <p>Inspect clinical data structures conforming to HL7 FHIR R4 and US Core Implementation Guides.</p>
          </div>
          <div class="fhir-controls">
            <label for="fhirResourceSelect"><strong>Resource:</strong></label>
            <select id="fhirResourceSelect" class="preset-select">
              <option value="patient" ${currentKey === 'patient' ? 'selected' : ''}>Patient (US Core Demographics)</option>
              <option value="observation_bp" ${currentKey === 'observation_bp' ? 'selected' : ''}>Observation: Blood Pressure Panel (LOINC 85354-9)</option>
              <option value="observation_a1c" ${currentKey === 'observation_a1c' ? 'selected' : ''}>Observation: HbA1c Lab (LOINC 4548-4)</option>
              <option value="medication_request" ${currentKey === 'medication_request' ? 'selected' : ''}>MedicationRequest: Lisinopril (RxNorm 314076)</option>
              <option value="condition" ${currentKey === 'condition' ? 'selected' : ''}>Condition: Hypertension (ICD-10 I10 & SNOMED)</option>
            </select>
          </div>
        </div>

        <div class="fhir-path-bar">
          <label for="fhirPathInput"><strong>FHIRPath Query:</strong></label>
          <input type="text" id="fhirPathInput" class="fhir-input" placeholder="e.g. resourceType, status, code.text, or component[0].valueQuantity.value" />
          <button class="secondary-small" id="evalPathBtn">Evaluate</button>
        </div>
        <div id="fhirPathOutput" class="fhir-path-result" style="display: none;"></div>

        <div class="fhir-tab-bar">
          <button class="fhir-tab ${activeMode === 'visual' ? 'active' : ''}" data-mode="visual">Clinical Structured View</button>
          <button class="fhir-tab ${activeMode === 'json' ? 'active' : ''}" data-mode="json">Raw FHIR JSON</button>
        </div>

        <div class="fhir-content-area">
          ${activeMode === 'visual' ? renderVisual(resource) : renderJSON(resource)}
        </div>
      </div>
    `;

    bindEvents();
  }

  function renderVisual(r) {
    return `
      <div class="fhir-visual-grid">
        <div class="fhir-prop-card">
          <span class="prop-label">Resource Type</span>
          <strong class="prop-val">${r.resourceType}</strong>
        </div>
        <div class="fhir-prop-card">
          <span class="prop-label">Logical ID</span>
          <strong class="prop-val">${r.id}</strong>
        </div>
        <div class="fhir-prop-card">
          <span class="prop-label">Clinical Status</span>
          <strong class="prop-val">${r.status || (r.clinicalStatus?.coding?.[0]?.code) || (r.active ? "active" : "inactive")}</strong>
        </div>
        <div class="fhir-prop-card">
          <span class="prop-label">Subject / Patient Reference</span>
          <strong class="prop-val">${r.subject?.display || (r.name ? `${r.name[0].given.join(" ")} ${r.name[0].family}` : "N/A")}</strong>
        </div>
      </div>

      <div class="fhir-detail-section">
        <h4>Key Clinical Elements & Vocabulary Standards</h4>
        <table class="fhir-table">
          <thead>
            <tr><th>Element</th><th>Terminology / Code System</th><th>Code</th><th>Display / Clinical Value</th></tr>
          </thead>
          <tbody>
            ${getDetailRows(r)}
          </tbody>
        </table>
      </div>
    `;
  }

  function getDetailRows(r) {
    const rows = [];
    if (r.resourceType === "Patient") {
      rows.push(`<tr><td>Birth Date</td><td>ISO-8601</td><td>${r.birthDate}</td><td>Age calculation baseline</td></tr>`);
      rows.push(`<tr><td>Gender</td><td>AdministrativeGender</td><td>${r.gender}</td><td>US Core Demographic</td></tr>`);
      rows.push(`<tr><td>Language</td><td>BCP-47</td><td>${r.communication[0].language.coding[0].code}</td><td>${r.communication[0].language.coding[0].display}</td></tr>`);
    } else if (r.resourceType === "Observation") {
      if (r.component) {
        r.component.forEach(c => {
          rows.push(`<tr><td>${c.code.coding[0].display}</td><td>LOINC</td><td>${c.code.coding[0].code}</td><td><strong>${c.valueQuantity.value} ${c.valueQuantity.unit}</strong></td></tr>`);
        });
      } else if (r.valueQuantity) {
        rows.push(`<tr><td>${r.code.text}</td><td>LOINC</td><td>${r.code.coding[0].code}</td><td><strong>${r.valueQuantity.value} ${r.valueQuantity.unit}</strong></td></tr>`);
      }
    } else if (r.resourceType === "MedicationRequest") {
      rows.push(`<tr><td>Prescribed Drug</td><td>RxNorm</td><td>${r.medicationCodeableConcept.coding[0].code}</td><td><strong>${r.medicationCodeableConcept.coding[0].display}</strong></td></tr>`);
      rows.push(`<tr><td>Dosage & Route</td><td>SNOMED CT</td><td>${r.dosageInstruction[0].route.coding[0].code}</td><td>${r.dosageInstruction[0].text}</td></tr>`);
    } else if (r.resourceType === "Condition") {
      r.code.coding.forEach(c => {
        rows.push(`<tr><td>Diagnosis</td><td>${c.system.includes("icd") ? "ICD-10-CM" : "SNOMED CT"}</td><td>${c.code}</td><td><strong>${c.display}</strong></td></tr>`);
      });
    }
    return rows.join("");
  }

  function renderJSON(r) {
    const jsonStr = JSON.stringify(r, null, 2);
    return `
      <pre class="fhir-json-block"><code>${escapeHTML(jsonStr)}</code></pre>
    `;
  }

  function escapeHTML(s) {
    return s.replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function bindEvents() {
    const select = host.querySelector("#fhirResourceSelect");
    const pathInput = host.querySelector("#fhirPathInput");
    const evalBtn = host.querySelector("#evalPathBtn");
    const output = host.querySelector("#fhirPathOutput");

    select.addEventListener("change", e => {
      currentKey = e.target.value;
      render();
    });

    host.querySelectorAll(".fhir-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        activeMode = tab.dataset.mode;
        render();
      });
    });

    const doEval = () => {
      const q = pathInput.value;
      if (!q.trim()) {
        output.style.display = "none";
        return;
      }
      const res = evaluateFHIRPath(FHIR_RESOURCES[currentKey], q);
      output.style.display = "block";
      output.innerHTML = `<strong>Result:</strong> <code>${escapeHTML(typeof res === "object" ? JSON.stringify(res, null, 2) : String(res))}</code>`;
    };

    evalBtn.addEventListener("click", doEval);
    pathInput.addEventListener("keydown", e => {
      if (e.key === "Enter") doEval();
    });
  }

  document.addEventListener("DOMContentLoaded", render);
})();
