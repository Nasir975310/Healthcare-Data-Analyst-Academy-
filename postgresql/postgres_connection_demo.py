"""Minimal parameterised PostgreSQL connection example for synthetic training data."""
import os
import sys
import psycopg
from psycopg.rows import dict_row

required = ["HDA_PG_HOST", "HDA_PG_DB", "HDA_PG_USER", "HDA_PG_PASSWORD"]
missing = [key for key in required if not os.getenv(key)]
if missing:
    sys.exit("Set environment variables: " + ", ".join(missing))

conninfo = {
    "host": os.environ["HDA_PG_HOST"],
    "port": int(os.getenv("HDA_PG_PORT", "5432")),
    "dbname": os.environ["HDA_PG_DB"],
    "user": os.environ["HDA_PG_USER"],
    "password": os.environ["HDA_PG_PASSWORD"],
    "connect_timeout": 5,
}
with psycopg.connect(**conninfo, row_factory=dict_row) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT encounter_id, admission_date, length_of_stay_days "
            "FROM hda.encounters WHERE length_of_stay_days >= %s "
            "ORDER BY length_of_stay_days DESC LIMIT %s",
            (5, 10),
        )
        for row in cur.fetchall():
            print(row)
