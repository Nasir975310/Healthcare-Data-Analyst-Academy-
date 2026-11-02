# Reproducible R workflow: synthetic teaching cohort
# Run from the statistics directory.
data <- read.csv("data/synthetic_clinical_cohort.csv", stringsAsFactors=FALSE)
stopifnot(!anyDuplicated(data$patient_id))
stopifnot(all(data$event_observed %in% c(0,1)))
stopifnot(all(data$event_time_days > 0 & data$event_time_days <= data$followup_days))
data$treatment_group <- factor(data$treatment_group)
print(aggregate(followup_sbp_mmhg ~ treatment_group, data,
                function(x) c(n=length(x), mean=mean(x), sd=sd(x), median=median(x))))
print(t.test(followup_sbp_mmhg ~ treatment_group, data=data, var.equal=FALSE))
fit <- lm(followup_sbp_mmhg ~ treatment_group + baseline_sbp_mmhg +
          age_years + diabetes + ckd, data=data)
print(summary(fit))
par(mfrow=c(2,2)); plot(fit); par(mfrow=c(1,1))
# Time-to-event analysis: event_time_days is observed time or censoring time.
if (requireNamespace("survival", quietly=TRUE)) {
  library(survival)
  km <- survfit(Surv(event_time_days, event_observed) ~ treatment_group, data=data)
  print(summary(km))
  cox <- coxph(Surv(event_time_days, event_observed) ~ treatment_group +
               age_years + diabetes + ckd, data=data)
  print(summary(cox))
  print(cox.zph(cox)) # proportional-hazards diagnostic
} else {
  message("Package 'survival' is not installed; install it to run Kaplan-Meier/Cox examples.")
}
