#! /usr/bin/env sh
set -eu

./manage.py sqlflush | ./manage.py dbshell
mysql -u root -p ccb_myisam < ccb_data.sql
