#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/ruhrbuehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/cleanup.log

echo "Cleaning up the database" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ruhrbuehnen
python manage.py cleanup --settings=ruhrbuehnen.settings.production --traceback >> ${CRON_LOG_FILE}  2>&1
python manage.py cleanup_httpstate --settings=ruhrbuehnen.settings.production --traceback >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
