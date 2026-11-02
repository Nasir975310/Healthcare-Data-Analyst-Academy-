-- Portable SQL reference; adapt date syntax to the target RDBMS.
-- Fact grain: one row per EncounterID / ObservationID / MedicationID respectively.
SELECT COUNT(*) AS encounter_count, COUNT(DISTINCT EncounterID) AS unique_encounters FROM FactEncounter;
SELECT EncounterType, COUNT(*) AS encounters FROM FactEncounter GROUP BY EncounterType ORDER BY encounters DESC;
SELECT DrugClass, COUNT(*) AS medication_orders FROM FactMedication GROUP BY DrugClass ORDER BY medication_orders DESC;
SELECT Measure, ROUND(AVG(Value),2) AS mean_value, COUNT(*) AS reading_count
FROM FactObservation WHERE Measure IN ('Systolic BP','Diastolic BP') GROUP BY Measure;
-- Orphan checks must return zero rows.
SELECT e.EncounterID FROM FactEncounter e LEFT JOIN DimPatient p ON p.PatientID=e.PatientID WHERE p.PatientID IS NULL;
SELECT o.ObservationID FROM FactObservation o LEFT JOIN FactEncounter e ON e.EncounterID=o.EncounterID WHERE e.EncounterID IS NULL;
SELECT m.MedicationID FROM FactMedication m LEFT JOIN FactEncounter e ON e.EncounterID=m.EncounterID WHERE e.EncounterID IS NULL;
