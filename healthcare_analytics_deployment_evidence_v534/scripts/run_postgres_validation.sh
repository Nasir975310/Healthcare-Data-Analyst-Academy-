#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE"
if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker Engine is not installed or not on PATH." >&2; exit 2
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "ERROR: Docker Compose plugin is unavailable." >&2; exit 2
fi
echo "Starting the disposable synthetic-data PostgreSQL practicum."
echo "This resets only this Compose project's database volume."
docker compose down --volumes --remove-orphans
docker compose up -d --wait
RESULT="$(docker compose exec -T postgres psql -U hda_analyst -d hda_practicum -At -F '|' -c "
SELECT
 (SELECT COUNT(*) FROM raw.encounters),
 (SELECT COUNT(*) FROM curated.fact_encounter),
 (SELECT COUNT(*) FROM curated.encounter_exception),
 (SELECT COUNT(*) FROM curated.fact_observation),
 (SELECT COUNT(*) FROM curated.fact_medication_order),
 (SELECT COUNT(*) FROM curated.fact_encounter e LEFT JOIN curated.dim_patient p USING(patient_id) WHERE p.patient_id IS NULL),
 (SELECT COUNT(*) FROM pg_indexes WHERE schemaname='curated');
")"
IFS='|' read -r RAW ACCEPTED REJECTED OBS MED ORPHANS INDEXES <<< "$RESULT"
printf 'raw=%s accepted=%s rejected=%s observations=%s medication_orders=%s orphan_fks=%s indexes=%s\n' "$RAW" "$ACCEPTED" "$REJECTED" "$OBS" "$MED" "$ORPHANS" "$INDEXES"
if [[ "$RAW" != "91" || "$ACCEPTED" != "90" || "$REJECTED" != "1" || "$ORPHANS" != "0" || "$INDEXES" -lt "3" ]]; then
  echo "FAIL: PostgreSQL acceptance criteria were not met." >&2; exit 1
fi
mkdir -p evidence
cat > evidence/postgres_validation.json <<EOF
{
  "status": "PASS",
  "engine": "PostgreSQL 16 Alpine",
  "raw_encounters": $RAW,
  "accepted_encounters": $ACCEPTED,
  "rejected_encounters": $REJECTED,
  "curated_observations": $OBS,
  "curated_medication_orders": $MED,
  "orphan_foreign_key_rows": $ORPHANS,
  "curated_indexes": $INDEXES,
  "scope": "synthetic educational dataset",
  "generated_by": "scripts/run_postgres_validation.sh"
}
EOF
echo "PASS: PostgreSQL acceptance evidence written to evidence/postgres_validation.json"
