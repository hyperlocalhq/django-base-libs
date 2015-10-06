PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/actualize_production_date_and_time.log

echo "Actualizing production date and time" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/berlinbuehnen
python manage.py actualize_production_date_and_time --traceback >> ${CRON_LOG_FILE}  2>&1
