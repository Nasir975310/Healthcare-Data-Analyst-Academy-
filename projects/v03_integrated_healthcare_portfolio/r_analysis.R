# Independent R implementation of the synthetic encounter analysis.
# Run from the Academy root. Requires readr and dplyr.
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

input_dir <- file.path("datasets", "v03_python")
output_dir <- file.path("projects", "v03_integrated_healthcare_portfolio", "reports", "r_run")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

enc <- read_csv(file.path(input_dir, "encounters.csv"),
                col_types = cols(
                  encounter_id = col_character(),
                  patient_id = col_character(),
                  department_id = col_character(),
                  admission_date = col_date(format = "%Y-%m-%d"),
                  systolic_bp = col_double(),
                  .default = col_guess()
                ), show_col_types = FALSE)
dept <- read_csv(file.path(input_dir, "departments.csv"),
                 col_types = cols(department_id = col_character(), .default = col_guess()),
                 show_col_types = FALSE)

stopifnot(!any(is.na(enc$encounter_id)))
stopifnot(!anyDuplicated(enc$encounter_id))
stopifnot(!anyDuplicated(dept$department_id))

cohort <- enc |>
  filter(admission_date >= as.Date("2026-01-01"),
         admission_date < as.Date("2026-04-01"))

joined <- cohort |>
  left_join(dept |> select(department_id, department_name),
            by = "department_id", relationship = "many-to-one")

unmatched <- sum(is.na(joined$department_name))
stopifnot(nrow(joined) == nrow(cohort))

summary <- joined |>
  group_by(department_name) |>
  summarise(
    encounter_n = n(),
    unique_patients = n_distinct(patient_id),
    sbp_nonmissing_n = sum(!is.na(systolic_bp)),
    sbp_missing_n = sum(is.na(systolic_bp)),
    mean_sbp = mean(systolic_bp, na.rm = TRUE),
    median_sbp = median(systolic_bp, na.rm = TRUE),
    .groups = "drop"
  ) |>
  mutate(
    sbp_completeness_pct = 100 * sbp_nonmissing_n / encounter_n,
    across(c(mean_sbp, median_sbp, sbp_completeness_pct), ~ round(.x, 2))
  )

write_csv(summary, file.path(output_dir, "department_summary_r.csv"))
metrics <- tibble(
  cohort_encounters = nrow(cohort),
  unique_patients = n_distinct(cohort$patient_id),
  sbp_nonmissing = sum(!is.na(cohort$systolic_bp)),
  sbp_missing = sum(is.na(cohort$systolic_bp)),
  unmatched_departments = unmatched,
  department_encounter_sum = sum(summary$encounter_n)
)
write_csv(metrics, file.path(output_dir, "run_metrics_r.csv"))
print(metrics)
print(summary)
