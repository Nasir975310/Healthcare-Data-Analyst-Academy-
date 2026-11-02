# Statistical validation methods and interpretation

## Group diagnostics
- Shapiro–Wilk is reported within each group as a normality diagnostic. It is not an automatic test-selection switch. It can be underpowered in small samples and overly sensitive in large samples.
- Median-centred Levene test assesses variance homogeneity. Welch's t-test is suggested for a mean-difference estimand when comparing independent groups; design and distribution still matter.
- Inspect histograms and Q–Q plots in addition to formal diagnostics. This release does not automatically generate Q–Q plots.

## Regression
- Linear regression includes residual Shapiro–Wilk, Breusch–Pagan, HC3 heteroscedasticity-consistent coefficient standard errors, Cook's distance screening, leverage and VIF.
- HC3 changes coefficient uncertainty estimates, not the OLS point estimates. Robust SEs do not repair confounding, nonlinearity, dependence, poor measurement or model misspecification.
- Logistic regression reports convergence, coefficients, odds ratios and Wald intervals. It does not implement Firth correction, robust covariance, calibration, ROC validation or separation correction.

## Bootstrap
- Percentile bootstrap for the mean resamples independent observations with replacement. It assumes the observed sample is a reasonable empirical representation of the target population.
- It is not appropriate to resample individual rows naively for clustered, paired, repeated-measures, stratified or complex survey data. Small samples and extreme skew can produce poor coverage.

## Multiplicity
- Holm controls family-wise error; Benjamini–Hochberg controls false discovery rate under its assumptions. Bonferroni is also available.
- The user must define the inferential family before looking at results. The software corrects only the p-values supplied together in a family. It does not choose the family.

## General safeguards
- Diagnostics are evidence for judgement, not a certificate that assumptions hold.
- Complete-case regression may be biased when missingness is informative.
- Outlier/influence flags are review prompts, not deletion rules.
- This software is educational and not clinical decision support.
