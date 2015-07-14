#! /usr/bin/env sh
set -eu

mysqldump -u root -p --no-data  -R --triggers ccb > ccb_schema.sql
