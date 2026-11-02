# Quality assurance log — v2.2.0

## Executed checks
- [x] Excel challenge JSON parses; eight unique challenge IDs and required fields present.
- [x] Workbook opens with openpyxl; eight expected worksheets and three structured Excel tables present.
- [x] Workbook contains 14 formula cells; formulas are authored but not calculated by openpyxl.
- [x] Synthetic source controls independently recomputed: 80 encounters, 151 order rows, one missing cost, one blank class, one orphan encounter reference.
- [x] Mean LOS 3.875 days; supplied flag count 7; total ordered quantity 3,038; synthetic value INR 100,279.75.
- [x] Python/pandas cleaning alternative executed successfully; output reports one missing class, one missing cost, one orphan reference and two rows in the duplicate-candidate set.
- [x] HTML parsed with Python HTMLParser.
- [x] New JavaScript file passed `node --check`.
- [x] ZIP integrity test passed (see release artifact).

## Not tested / limitations
- Microsoft Excel desktop recalculation, PivotTable rendering, XLOOKUP behaviour and Power Query M execution were not tested in this environment.
- No Windows execution or browser automation/cross-device test was performed.
- Power Query M script is a reference pattern; users must adapt the file path and query names.
- The Academy browser UI records completion locally only; it does not execute spreadsheet formulas or Power Query.
- No clinical validation or independent peer review of synthetic dataset assumptions was performed.

## Data interpretation safeguards
- Dataset is entirely synthetic.
- The readmission flag is supplied and not independently validated.
- Medication orders are not evidence of dispensing, administration, adherence or appropriateness.
- Synthetic unit costs are training values, not real procurement prices.
- The duplicate-like source row requires a documented business-key review; do not delete it automatically.
