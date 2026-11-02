# PostgreSQL setup guide

Recommended: PostgreSQL 15 or newer. Keep the service bound to localhost for this training environment.

## CachyOS / Ryoku (Fish shell)
```fish
sudo pacman -Syu
sudo pacman -S postgresql
sudo -iu postgres initdb -D /var/lib/postgres/data
sudo systemctl enable --now postgresql
sudo -iu postgres createuser --pwprompt hda_admin
sudo -iu postgres createdb -O hda_admin hda_training
psql -U hda_admin -d hda_training -h 127.0.0.1
```
If the data directory is already initialised, do not run initdb again. Check `systemctl status postgresql` and the package's current Arch Wiki instructions before changing an existing cluster.

## Windows
Install PostgreSQL using the official interactive installer. Select the command-line tools and optionally pgAdmin. Record the port and database superuser password securely. In PowerShell, verify:
```powershell
psql --version
psql -h localhost -p 5432 -U postgres -d postgres
```
Create a dedicated database and role; do not use the postgres superuser for day-to-day analytics.

## Docker alternative (Linux / Windows with Docker Desktop)
From this directory, set a strong temporary training password and start the container:
```bash
export HDA_PG_ADMIN_PASSWORD='replace-with-a-local-training-password'
docker compose up -d
docker compose ps
```
PowerShell:
```powershell
$env:HDA_PG_ADMIN_PASSWORD = 'replace-with-a-local-training-password'
docker compose up -d
docker compose ps
```
The port is bound to 127.0.0.1 only. Keep the password out of Git. Stop with `docker compose down`; `docker compose down -v` deletes the training database volume.

## Load the training model
Connect to database `hda_training`, then execute `sql/postgresql_mastery/schema.sql` followed by `seed.sql`. In DBeaver, use SQL Editor > Open SQL Script and execute each file. In psql, use `\i /absolute/path/to/file.sql`.

## Notes
PostgreSQL SQL is not identical to SQLite. This lab uses PostgreSQL features including FILTER, ::numeric casts, INCLUDE indexes, materialized views, PL/pgSQL and EXPLAIN ANALYZE. Never point training scripts at a production database.
