# Optional ggplot2 figures for the integrated portfolio.
# Run from the Academy root. Requires readr, dplyr and ggplot2.
suppressPackageStartupMessages({
  library(readr); library(dplyr); library(ggplot2)
})
data_dir <- file.path("datasets", "v03_python")
out_dir <- file.path("projects", "v03_integrated_healthcare_portfolio", "figures", "r")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
enc <- read_csv(file.path(data_dir, "encounters.csv"),
                col_types = cols(admission_date = col_date("%Y-%m-%d"),
                                 systolic_bp = col_double(), .default = col_guess()),
                show_col_types = FALSE)
dept <- read_csv(file.path(data_dir, "departments.csv"), show_col_types = FALSE)
enc <- enc |> filter(admission_date >= as.Date("2026-01-01"),
                     admission_date < as.Date("2026-04-01"))
joined <- enc |> left_join(dept |> select(department_id, department_name),
                           by = "department_id", relationship = "many-to-one")

p1 <- ggplot(joined, aes(x = systolic_bp)) +
  geom_histogram(bins = 12, color = "white") +
  labs(title = "Recorded systolic blood pressure distribution",
       x = "Systolic blood pressure (mmHg)", y = "Encounter count") +
  theme_minimal()
ggsave(file.path(out_dir, "sbp_distribution_r.png"), p1, width = 8, height = 5, dpi = 160)

dept_summary <- joined |> group_by(department_name) |>
  summarise(mean_sbp = mean(systolic_bp, na.rm = TRUE),
            sbp_n = sum(!is.na(systolic_bp)), .groups = "drop")
p2 <- ggplot(dept_summary, aes(x = reorder(department_name, mean_sbp),
                               y = mean_sbp)) +
  geom_col() + coord_flip() +
  geom_text(aes(label = paste0("n=", sbp_n)), hjust = -0.1, size = 3) +
  labs(title = "Mean recorded SBP by department",
       x = "Department", y = "Mean SBP (mmHg)") +
  theme_minimal()
ggsave(file.path(out_dir, "mean_sbp_department_r.png"), p2, width = 8, height = 5, dpi = 160)
