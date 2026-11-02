-- Safe migration template: versioned, transactional, reviewed before execution.
BEGIN;
-- Example additive migration:
ALTER TABLE hda_raw.encounters
  ADD COLUMN IF NOT EXISTS source_system TEXT;
-- Verify before COMMIT; ROLLBACK on unexpected result.
COMMIT;
