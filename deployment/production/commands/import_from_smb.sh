#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_from_smb.log

echo "Importing from SMB" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd ${PROJECT_PATH}/project/museumsportal
python manage.py import_from_smb_smart --settings=settings.production --traceback >> ${CRON_LOG_FILE}  2>&1

cd ${PROJECT_PATH}/project/museumsportal/media
find . -type f -exec chmod 664 {} ';' >> ${CRON_LOG_FILE}  2>&1
find . -type d -exec chmod 775 {} ';' >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
