#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_from_grips_theater.log

cd ${PROJECT_PATH}
. bin/activate
cd project/berlinbuehnen

echo "Importing from GRIPS Theater" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_grips_theater --traceback >> ${CRON_LOG_FILE}  2>&1

cd ${PROJECT_PATH}/commands/
./fix_permissions_for_media.sh
