# v5.15.0 — Clinical Research Interpretation & Evidence Engine

## Python calculators
Requires Python 3.10+; standard library only.
```bash
python scripts/evidence_calculator.py effects --event-intervention 18 --total-intervention 120 --event-control 30 --total-control 120
python scripts/evidence_calculator.py diagnostic --tp 82 --fn 18 --fp 24 --tn 176 --prevalence 0.10
python -m pytest -q tests
```
Optional `--continuity-correction` applies a 0.5 Haldane–Anscombe correction to ratio measures if a zero cell is present; it is explicit and recorded.

## Included
- Risk, risk difference, relative risk, odds ratio, ARR/NNT and absolute risk increase/NNH.
- Wilson intervals for each arm's event risk; approximate Wald/log-Wald intervals for contrasts/ratios.
- Diagnostic sensitivity, specificity, PPV, NPV, likelihood ratios and predictive values at an explicitly supplied target prevalence.
- Educational appraisal domains for randomized, observational and diagnostic studies, plus GRADE certainty considerations.
- Interactive browser calculators and appraisal prompts.

## Limitations
The calculations are educational and do not replace prespecified statistical methods or specialist review. The risk-difference CI is a Wald approximation; small samples and extreme risks may require exact or score-based methods. NNT/NNH uncertainty is not reduced to a single number when the risk-difference interval crosses zero. The appraisal module does not reproduce official framework algorithms or assign validated ratings. Synthetic examples are not clinical evidence. No patient-level or treatment recommendations are generated.
