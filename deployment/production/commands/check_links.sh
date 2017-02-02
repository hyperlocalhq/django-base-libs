#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/check_links.log

echo "Checking links" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/museumsportal
python manage.py check_links --verbosity=2 --traceback >> ${CRON_LOG_FILE}  2>&1
