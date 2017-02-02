#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/cleanup.log

echo "Cleaning up the database" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/museumsportal
python manage.py cleanup --traceback >> ${CRON_LOG_FILE}  2>&1
python manage.py cleanup_httpstate --traceback >> ${CRON_LOG_FILE}  2>&1
