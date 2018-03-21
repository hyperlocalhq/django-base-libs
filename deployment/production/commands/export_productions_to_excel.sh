#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/export_productions_to_excel.log

echo "Exporting data to Excel" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/berlinbuehnen
python manage.py export_productions_to_excel --settings=berlinbuehnen.settings.production --traceback >> ${CRON_LOG_FILE} 2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
