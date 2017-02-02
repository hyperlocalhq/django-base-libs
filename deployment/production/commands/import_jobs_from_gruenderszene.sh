#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_jobs_from_gruenderszene.log

echo "Importing from Gründerszene" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/ccb    
python manage.py import_jobs_from_gruenderszene --verbosity=2 --traceback >> ${CRON_LOG_FILE} 2>&1
