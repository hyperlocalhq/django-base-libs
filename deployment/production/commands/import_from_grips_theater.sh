#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_from_grips_theater.log

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ruhrbuehnen

echo "Importing from GRIPS Theater" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_grips_theater --settings=ruhrbuehnen.settings.production --traceback >> ${CRON_LOG_FILE}  2>&1

cd ${PROJECT_PATH}/commands/
./fix_permissions_for_media.sh

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
