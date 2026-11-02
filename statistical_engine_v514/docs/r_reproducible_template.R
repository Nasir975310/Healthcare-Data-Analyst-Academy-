# R reproducible analysis template (source example; not executed by the Python QA run)
# Install once: install.packages(c("readr", "dplyr", "broom", "ggplot2"))
library(readr)
library(dplyr)
library(broom)

dat <- read_csv("data/synthetic_bp_study.csv", show_col_types = FALSE)
stopifnot(all(c("group", "baseline_sbp", "followup_sbp") %in% names(dat)))

# Data completeness and descriptive summaries
missingness <- summarise(dat, across(everything(), ~sum(is.na(.x))))
descriptives <- dat |>
  group_by(group) |>
  summarise(n = sum(!is.na(followup_sbp)),
            mean = mean(followup_sbp, na.rm = TRUE),
            sd = sd(followup_sbp, na.rm = TRUE),
            median = median(followup_sbp, na.rm = TRUE),
            .groups = "drop")

# Independent-group comparison: Welch t-test
welch <- t.test(followup_sbp ~ group, data = dat, var.equal = FALSE)

# Paired comparison across complete cases
paired <- dat |> filter(!is.na(baseline_sbp), !is.na(followup_sbp))
paired_test <- t.test(paired$followup_sbp, paired$baseline_sbp, paired = TRUE)

# Baseline-adjusted linear model; review design and assumptions before use
ancova <- lm(followup_sbp ~ group + baseline_sbp, data = dat)
write_csv(descriptives, "outputs/r_descriptives.csv")
write_csv(tidy(ancova, conf.int = TRUE), "outputs/r_ancova_coefficients.csv")
capture.output(welch, paired_test, summary(ancova), file = "outputs/r_model_output.txt")
