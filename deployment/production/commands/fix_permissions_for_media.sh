#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/fix_permissions_for_media.log

echo "Fixing permissions for media directory" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/kb/media

find . -type f -exec chmod 664 {} ';' >> ${CRON_LOG_FILE}  2>&1
find . -type d -exec chmod 775 {} ';' >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
