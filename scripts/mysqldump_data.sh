#! /usr/bin/env sh
set -eu

mysqldump -u root -p --replace --no-create-info  -R --triggers ccb > ccb_data.sql
