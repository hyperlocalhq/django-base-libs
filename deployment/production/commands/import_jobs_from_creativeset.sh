#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_jobs_from_creativeset.log

echo "Importing from Creativeset" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ccb    
python manage.py import_jobs_from_creativeset --traceback --verbosity=2 --settings=settings.production >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
