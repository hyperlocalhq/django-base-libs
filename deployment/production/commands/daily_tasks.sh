#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/daily_tasks.log

echo "Doing daily tasks" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/ccb
python manage.py daily_tasks --verbosity=2 --traceback >> ${CRON_LOG_FILE}  2>&1
