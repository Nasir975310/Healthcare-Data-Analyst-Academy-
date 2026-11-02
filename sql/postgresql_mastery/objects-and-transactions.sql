SET search_path TO hda, public;
CREATE OR REPLACE VIEW v_department_summary AS
SELECT d.department_name, COUNT(DISTINCT e.encounter_id) AS encounter_count,
       ROUND(AVG(e.length_of_stay_days),2) AS mean_los_days
FROM departments d LEFT JOIN encounters e USING(department_id)
GROUP BY d.department_name;
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_class_utilisation AS
SELECT dr.therapeutic_class, COUNT(*) AS order_count, SUM(o.quantity) AS total_quantity
FROM medication_orders o JOIN drugs dr USING(drug_id) GROUP BY dr.therapeutic_class;
REFRESH MATERIALIZED VIEW mv_class_utilisation;
CREATE OR REPLACE FUNCTION reject_nonpositive_order_quantity()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NEW.quantity <= 0 THEN RAISE EXCEPTION 'quantity must be positive'; END IF;
 RETURN NEW;
END; $$;
DROP TRIGGER IF EXISTS trg_positive_order_quantity ON medication_orders;
CREATE TRIGGER trg_positive_order_quantity BEFORE INSERT OR UPDATE OF quantity
ON medication_orders FOR EACH ROW EXECUTE FUNCTION reject_nonpositive_order_quantity();
BEGIN;
INSERT INTO medication_orders(order_id,encounter_id,drug_id,order_date,order_status,quantity)
SELECT 'TEST-ROLLBACK-001', e.encounter_id, d.drug_id, CURRENT_DATE, 'Training', 1
FROM encounters e CROSS JOIN drugs d
WHERE e.encounter_id=(SELECT MIN(encounter_id) FROM encounters)
AND d.drug_id=(SELECT MIN(drug_id) FROM drugs) LIMIT 1;
SELECT COUNT(*) AS visible_inside_transaction FROM medication_orders WHERE order_id='TEST-ROLLBACK-001';
ROLLBACK;
SELECT COUNT(*) AS should_be_zero FROM medication_orders WHERE order_id='TEST-ROLLBACK-001';
