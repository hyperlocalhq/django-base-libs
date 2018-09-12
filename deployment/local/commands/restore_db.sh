#!/usr/bin/env bash
psql --username=pgsql --dbname=museumsportal --command='SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();'
dropdb --username=pgsql museumsportal
createdb --username=museumsportal museumsportal
pg_restore --dbname=museumsportal --role=museumsportal --schema=public --no-owner museumsportal.backup