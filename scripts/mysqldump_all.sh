#! /usr/bin/env sh
set -eu

mysqldump -u root -p ccb > ccb_all.sql
