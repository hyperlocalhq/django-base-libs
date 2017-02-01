PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_from_kulturmanagement.log

echo "Importing from Kulturmanagement" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/ccb    
python manage.py import_from_kulturmanagement --traceback >> ${CRON_LOG_FILE}  2>&1
