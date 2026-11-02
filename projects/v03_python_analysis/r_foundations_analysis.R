# R foundations: descriptive summary of fictional encounter data
# Run from the academy root or update data_path to the CSV location.

data_path <- file.path("datasets", "v03_python", "encounters.csv")
enc <- read.csv(data_path, stringsAsFactors = FALSE, na.strings = c(""))

stopifnot(all(c("encounter_id", "patient_id", "department_id",
                "admission_date", "encounter_type", "systolic_bp") %in% names(enc)))

enc$admission_date <- as.Date(enc$admission_date, format = "%Y-%m-%d")
enc$systolic_bp <- as.numeric(enc$systolic_bp)

cat("Rows:", nrow(enc), "\\n")
cat("Unique encounters:", length(unique(enc$encounter_id)), "\\n")
cat("Unique patients:", length(unique(enc$patient_id)), "\\n")
cat("Missing SBP:", sum(is.na(enc$systolic_bp)), "\\n")
cat("Nonmissing SBP:", sum(!is.na(enc$systolic_bp)), "\\n")
cat("Mean SBP:", mean(enc$systolic_bp, na.rm = TRUE), "\\n")
cat("Median SBP:", median(enc$systolic_bp, na.rm = TRUE), "\\n")

cat("Encounter type counts:\\n")
print(table(enc$encounter_type, useNA = "ifany"))

department_summary <- aggregate(
  cbind(encounter_n = rep(1, nrow(enc)),
        sbp_nonmissing_n = as.integer(!is.na(enc$systolic_bp))),
  by = list(department_id = enc$department_id),
  FUN = sum
)
department_summary$sbp_missing_n <- department_summary$encounter_n -
  department_summary$sbp_nonmissing_n
print(department_summary)

write.csv(department_summary,
          file.path("projects", "v03_python_analysis", "reports", "r_department_summary.csv"),
          row.names = FALSE)

sessionInfo()
