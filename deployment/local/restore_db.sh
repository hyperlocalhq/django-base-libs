#!/usr/bin/env bash
psql --username=pgsql --dbname=ccb --command='SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();'
dropdb --username=pgsql ccb
createdb --username=ccb ccb
pg_restore --dbname=ccb --role=ccb --schema=public --no-owner ccb.backup