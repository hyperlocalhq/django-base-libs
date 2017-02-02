#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_from_theaterjobs.log

echo "Importing from Theaterjobs" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/ccb    
python manage.py import_from_theaterjobs --traceback >> ${CRON_LOG_FILE}  2>&1
