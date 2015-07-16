#! /usr/bin/env sh
set -eu

## Before loading data dump, make sure the following tables have been renamed:
## external_objectmapper to external_services_objectmapper
## external_service to external_services_service
./manage.py sqlflush | ./manage.py dbshell
mysql -u root -p ccb_myisam < ccb_data.sql
