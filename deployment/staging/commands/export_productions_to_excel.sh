#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/ruhrbuehnen.jetsonproject.org
CRON_LOG_FILE=${PROJECT_PATH}/logs/export_productions_to_excel.log

echo "Exporting data to Excel" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ruhrbuehnen
python manage.py export_productions_to_excel --settings=ruhrbuehnen.settings.production --traceback >> ${CRON_LOG_FILE} 2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
