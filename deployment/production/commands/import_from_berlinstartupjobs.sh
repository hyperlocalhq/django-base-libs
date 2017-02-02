#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_from_berlinstartupjobs.log

echo "Importing from Berlin Startup Jobs" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/ccb    
python manage.py import_from_berlinstartupjobs --traceback >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
