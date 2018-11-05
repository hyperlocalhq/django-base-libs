#!/usr/bin/env bash
psql --username=pgsql --dbname=ruhrbuehnen --command='SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();'
dropdb --username=pgsql ruhrbuehnen
createdb --username=ruhrbuehnen ruhrbuehnen
pg_restore --dbname=ruhrbuehnen --role=ruhrbuehnen --schema=public ../db_backups/ruhrbuehnen.backup