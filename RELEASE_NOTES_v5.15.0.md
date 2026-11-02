# Healthcare Data Analyst Academy — v5.15.0

## Clinical Research Interpretation & Evidence Engine

### New capabilities
- Risk difference, relative risk, odds ratio, ARR/NNT and absolute risk increase/NNH.
- Wilson intervals for event risks; approximate Wald/log-Wald intervals for effects and ratios.
- Explicit zero-cell handling: ratios remain not estimable unless the user selects a continuity correction.
- Diagnostic sensitivity, specificity, PPV, NPV, LR+ and LR−.
- Prevalence-adjusted PPV/NPV using an explicitly entered target prevalence.
- Interactive critical-appraisal domain prompts for randomized, observational and diagnostic studies, plus GRADE considerations.
- Python CLI calculators and educational interpretation guide.

### QA
- 5 v5.15 automated tests passed.
- 3 v5.13 regression tests passed.
- Both Python calculator CLI examples executed successfully and wrote JSON outputs.
- NNT floating-point rounding edge case tested and corrected.
- New JavaScript passed `node --check`.
- Full Python compilation and JSON parsing checked before packaging.
- ZIP integrity and required file presence checked after packaging.

### Limitations
Calculations use approximate intervals in some cases. The appraisal prompts are not official tool implementations and do not assign validated ratings. No clinical recommendations are generated. Example data are synthetic.
