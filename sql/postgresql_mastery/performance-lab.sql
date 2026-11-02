SET search_path TO hda, public;
EXPLAIN (COSTS, VERBOSE)
SELECT order_id, order_date, order_status FROM medication_orders
WHERE encounter_id='ENC-0001' AND order_date >= DATE '2025-01-01' ORDER BY order_date;
CREATE INDEX IF NOT EXISTS ix_orders_encounter_date_cover
ON medication_orders(encounter_id, order_date) INCLUDE(order_status);
ANALYZE medication_orders;
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT order_id, order_date, order_status FROM medication_orders
WHERE encounter_id='ENC-0001' AND order_date >= DATE '2025-01-01' ORDER BY order_date;
CREATE INDEX IF NOT EXISTS ix_orders_pending ON medication_orders(order_date)
WHERE order_status='Pending';
