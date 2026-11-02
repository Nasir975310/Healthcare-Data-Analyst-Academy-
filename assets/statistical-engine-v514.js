(() => {
  "use strict";
  const byId = id => document.getElementById(id);
  const plans = {
    continuous: {
      "two-independent": ["Welch independent-samples t-test; report mean difference and 95% CI. Consider Mann–Whitney U when a rank/distribution estimand is appropriate.", "Check independence, group distributions, influential outliers and variance structure. Do not choose a test solely from a normality-test p-value."],
      paired: ["Paired t-test on within-person differences; report mean change and 95% CI. Consider a signed-rank method when justified by the estimand and distribution.", "Verify that records are correctly paired and inspect the distribution of differences."],
      one: ["Summarise mean/SD and median/IQR; add a confidence interval for the prespecified estimand.", "Describe sampling frame, missingness, distribution and outliers."],
      association: ["Pearson correlation for linear association or Spearman correlation for monotonic/rank association.", "Inspect scatterplots, non-linearity, outliers and range restriction. Correlation is not causation."]
    },
    binary: {
      "two-independent": ["Estimate risks and a risk difference / risk ratio with confidence intervals; logistic regression may adjust for prespecified covariates.", "Check event counts, sparse data, confounding, separation and whether the design supports risk estimation."],
      paired: ["Use paired binary methods such as McNemar's test for matched before/after binary outcomes.", "Only discordant pairs inform McNemar's test; preserve pairing and report counts."],
      one: ["Report numerator, denominator, proportion and confidence interval.", "Define the denominator and missing outcome handling."],
      association: ["Logistic regression for a binary outcome with prespecified predictors.", "Assess events per parameter, separation, functional form, calibration and confounding."]
    },
    categorical: {
      "two-independent": ["Cross-tabulation with chi-square; use Fisher's exact test for sparse 2×2 tables.", "Check independent observations and expected cell counts."],
      paired: ["Use a paired categorical method appropriate to the number of categories (e.g., McNemar for paired binary data).", "Do not treat paired observations as independent."],
      one: ["Report counts and proportions with denominators and confidence intervals.", "Make category definitions mutually exclusive where required; state missingness."],
      association: ["Cross-tabulation and chi-square / exact methods; consider multinomial models for adjusted analyses.", "Check sparse cells, clustering and the target association measure."]
    },
    ordinal: {
      "two-independent": ["Consider Mann–Whitney U or an ordinal regression model, depending on the estimand.", "Check category ordering, ties, distribution shape and proportional-odds assumption for ordinal logistic regression."],
      paired: ["Use a paired ordinal method or ordinal mixed model suitable for repeated observations.", "Preserve within-person dependence and category ordering."],
      one: ["Report ordered category counts and proportions; median category may be useful.", "Do not assume equal distances between ordinal categories."],
      association: ["Use Spearman correlation or ordinal regression as appropriate.", "Check monotonicity, proportional odds and confounding."]
    },
    time: {
      "two-independent": ["Kaplan–Meier curves and log-rank test; Cox regression for adjusted hazard ratios when appropriate.", "Define time origin/event/censoring; assess proportional hazards and competing risks."],
      paired: ["Use a repeated-event or clustered survival approach appropriate to the paired structure.", "A standard independent-groups log-rank test is not automatically valid."],
      one: ["Estimate survival with Kaplan–Meier and report numbers at risk and confidence intervals.", "State censoring rules and follow-up completeness."],
      association: ["Cox or other survival regression based on the event process and estimand.", "Assess proportional hazards, functional form, informative censoring and competing events."]
    }
  };
  function renderPlan() {
    const type=byId("stat-outcome-v514").value, structure=byId("stat-structure-v514").value;
    const design=byId("stat-design-v514").value, objective=byId("stat-objective-v514").value;
    const chosen=plans[type][structure];
    const notes=[];
    if (design==="casecontrol") notes.push("Case-control design: do not estimate incidence or risk directly from sampled case/control proportions; odds-ratio methods are commonly used.");
    if (design==="rct") notes.push("Randomized trial: preserve randomized allocation in the primary analysis; define estimand, intercurrent-event strategy and analysis population.");
    if (design==="cohort") notes.push("Cohort design: assess confounding, selection, time-related bias and loss to follow-up.");
    if (design==="diagnostic") notes.push("Diagnostic accuracy: define reference standard and index test; report sensitivity, specificity and confidence intervals; consider ROC/AUC for continuous tests.");
    if (objective==="prediction") notes.push("Prediction objective: plan internal/external validation, calibration, discrimination and optimism control; a significant predictor is not a validated prediction model.");
    if (objective==="description") notes.push("Descriptive objective: prioritise estimates, denominators and uncertainty; hypothesis testing may be unnecessary.");
    if (objective==="association") notes.push("Association objective: define the effect measure and distinguish unadjusted from adjusted estimates.");
    const target=byId("stat-plan-result-v514");
    target.innerHTML="<h3>Candidate analysis</h3><p><strong>Primary method:</strong> "+chosen[0]+"</p><p><strong>Assumption and design checks:</strong> "+chosen[1]+"</p>"+notes.map(n=>"<p>• "+n+"</p>").join("")+"<p><strong>Always add:</strong> prespecified estimand, missing-data summary, effect estimate, confidence interval, analysis population and transparent limitations.</p><p class='muted'>Planning suggestion only. Confirm with the protocol, data dictionary and qualified statistical review before analysis.</p>";
  }
  const button=byId("stat-plan-btn-v514");
  if(button) button.addEventListener("click",renderPlan);
})();