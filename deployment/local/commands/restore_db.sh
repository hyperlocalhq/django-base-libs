#!/usr/bin/env bash
psql --username=pgsql --dbname=berlinbuehnen --command='SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();'
dropdb --username=pgsql berlinbuehnen
createdb --username=berlinbuehnen berlinbuehnen
pg_restore --dbname=berlinbuehnen --role=berlinbuehnen --schema=public --no-owner berlinbuehnen.backup