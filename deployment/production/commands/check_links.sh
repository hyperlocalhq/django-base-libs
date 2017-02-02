#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/check_links.log

echo "Searching for broken links" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/ccb
python manage.py check_links --settings=settings_check_links --traceback >> ${CRON_LOG_FILE}  2>&1
