#! /usr/bin/env sh
set -eu

mysqldump -u root -p --complete-insert --replace --no-create-info  -R --triggers ccb > ccb_data.sql
