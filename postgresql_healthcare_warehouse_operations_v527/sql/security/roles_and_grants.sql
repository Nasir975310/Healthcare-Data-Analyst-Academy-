-- Run as a database administrator after creating login roles securely.
-- Supply passwords via your secret manager/interactive psql; do not commit credentials.
CREATE ROLE hda_analyst NOLOGIN;
CREATE ROLE hda_loader NOLOGIN;
GRANT USAGE ON SCHEMA hda TO hda_analyst,hda_loader;
GRANT SELECT ON ALL TABLES IN SCHEMA hda TO hda_analyst;
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA hda TO hda_loader;
GRANT USAGE,SELECT ON ALL SEQUENCES IN SCHEMA hda TO hda_loader;
ALTER DEFAULT PRIVILEGES IN SCHEMA hda GRANT SELECT ON TABLES TO hda_analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA hda GRANT SELECT,INSERT,UPDATE,DELETE ON TABLES TO hda_loader;
ALTER DEFAULT PRIVILEGES IN SCHEMA hda GRANT USAGE,SELECT ON SEQUENCES TO hda_loader;
-- Create login users separately and grant one of these group roles.
-- GRANT hda_analyst TO analyst_login;
-- GRANT hda_loader TO etl_service_login;
