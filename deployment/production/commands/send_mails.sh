#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/send_mails.log
DJANGO_SETTINGS_MODULE=museumsportal.settings.production

echo "Sending emails" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/museumsportal
python manage.py send_mails --traceback >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
