#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_tweets.log
DJANGO_SETTINGS_MODULE=museumsportal.settings.production

echo "Importing Tweets" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd ${PROJECT_PATH}/project/museumsportal
python manage.py import_tweets --traceback >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
