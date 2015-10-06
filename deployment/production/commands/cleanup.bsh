PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/cleanup.log

echo "Cleaning up the database" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/berlinbuehnen
python manage.py cleanup --traceback >> ${CRON_LOG_FILE}  2>&1
python manage.py cleanup_httpstate --traceback >> ${CRON_LOG_FILE}  2>&1
