-- Demo role is deliberately limited to the schemas needed for analytics.
GRANT USAGE ON SCHEMA raw, curated TO hda_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA raw, curated TO hda_analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA raw
  GRANT SELECT ON TABLES TO hda_analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA curated
  GRANT SELECT ON TABLES TO hda_analyst;
