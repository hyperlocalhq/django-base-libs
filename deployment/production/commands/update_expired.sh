#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/update_expired.log
DJANGO_SETTINGS_MODULE=museumsportal.settings.production

echo "Updating expired objects" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/museumsportal
python manage.py update_expired_exhibitions --traceback >> ${CRON_LOG_FILE}  2>&1
python manage.py update_expired_events --traceback >> ${CRON_LOG_FILE}  2>&1
python manage.py update_expired_workshops --traceback >> ${CRON_LOG_FILE}  2>&1
python manage.py update_expired_seasons --traceback >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
