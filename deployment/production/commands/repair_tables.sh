#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/repair_tables.log

echo "Repairing tables" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/museumsportal
echo "REPAIR TABLE httpstate_httpstate;" | python manage.py dbshell --traceback >> ${CRON_LOG_FILE} 2>&1
echo "REPAIR TABLE django_session;" | python manage.py dbshell --traceback >> ${CRON_LOG_FILE} 2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
