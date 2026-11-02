"""NumPy lab: summarize SBP while preserving missingness explicitly."""
from pathlib import Path
import csv
import numpy as np

DATA_FILE = Path(__file__).resolve().parents[3] / "datasets" / "v03_python" / "encounters.csv"

with DATA_FILE.open("r", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

raw_values = [row["systolic_bp"].strip() for row in rows]
missing_n = sum(value == "" for value in raw_values)
sbp = np.array([float(value) for value in raw_values if value != ""], dtype=np.float64)

print("Encounter rows:", len(rows))
print("Nonmissing SBP n:", sbp.size)
print("Missing SBP n:", missing_n)
print("Mean SBP:", round(float(np.mean(sbp)), 2))
print("Median SBP:", round(float(np.median(sbp)), 2))
print("SBP >= 140 count:", int(np.sum(sbp >= 140)))

# Demonstrate missing-aware calculation.
with_nan = np.array(
    [float(value) if value != "" else np.nan for value in raw_values],
    dtype=np.float64
)
print("np.mean with NaN:", np.mean(with_nan))
print("np.nanmean:", round(float(np.nanmean(with_nan)), 2))
print("2D axis demonstration:")
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print("axis=0:", matrix.mean(axis=0))
print("axis=1:", matrix.mean(axis=1))
