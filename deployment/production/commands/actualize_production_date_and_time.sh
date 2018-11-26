#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/actualize_production_date_and_time.log

echo "Actualizing production date and time" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. venv/bin/activate
cd project/ruhrbuehnen
python manage.py actualize_production_date_and_time --settings=ruhrbuehnen.settings.production --traceback >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
