#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/rebuild_index.log

echo "Updating search index" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/kb
python manage.py rebuild_index --verbosity=2 --traceback --noinput >> ${CRON_LOG_FILE} 2>&1
#python manage.py update_index --verbosity=2 --traceback >> ${CRON_LOG_FILE} 2>&1
chmod -R 777 tmp >> ${CRON_LOG_FILE}  2>&1
date >> ${CRON_LOG_FILE}

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
