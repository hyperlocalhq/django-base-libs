PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/start_celeryd.log

echo "Starting Celery" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/ccb    
nohup python manage.py celeryd start --verbosity=2 --loglevel=DEBUG --settings=settings_celery --traceback & >> ${CRON_LOG_FILE}  2>&1
