-- Run after importing CSVs with explicit ID values into academy tables.
-- This advances identity sequences so future generated IDs do not collide.
SET search_path TO academy;

SELECT setval(pg_get_serial_sequence('academy.departments','department_id'),
              COALESCE((SELECT MAX(department_id) FROM departments),1),
              EXISTS(SELECT 1 FROM departments));
SELECT setval(pg_get_serial_sequence('academy.patients','patient_id'),
              COALESCE((SELECT MAX(patient_id) FROM patients),1),
              EXISTS(SELECT 1 FROM patients));
SELECT setval(pg_get_serial_sequence('academy.encounters','encounter_id'),
              COALESCE((SELECT MAX(encounter_id) FROM encounters),1),
              EXISTS(SELECT 1 FROM encounters));
SELECT setval(pg_get_serial_sequence('academy.diagnoses','diagnosis_id'),
              COALESCE((SELECT MAX(diagnosis_id) FROM diagnoses),1),
              EXISTS(SELECT 1 FROM diagnoses));
SELECT setval(pg_get_serial_sequence('academy.prescriptions','prescription_id'),
              COALESCE((SELECT MAX(prescription_id) FROM prescriptions),1),
              EXISTS(SELECT 1 FROM prescriptions));
SELECT setval(pg_get_serial_sequence('academy.laboratory_results','result_id'),
              COALESCE((SELECT MAX(result_id) FROM laboratory_results),1),
              EXISTS(SELECT 1 FROM laboratory_results));
