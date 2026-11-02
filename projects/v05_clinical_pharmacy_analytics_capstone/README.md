# V05 capstone

Requirements: Python 3.10+ and pandas.

From this project directory:
```bash
python -m pip install pandas
python python/analyze_capstone.py
```
Outputs are created in `reports/outputs/`. The script checks key uniqueness, referential integrity and date chronology before generating summaries. It intentionally does not calculate laboratory completion because no expected-test denominator exists.
