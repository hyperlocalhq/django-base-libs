#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/ruhrbuehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/fix_permissions_for_tmp.log

echo "Fixing permissions for tmp directory" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ruhrbuehnen/ruhrbuehnen/tmp

find . -type f -exec chmod 664 {} ';' >> ${CRON_LOG_FILE}  2>&1
find . -type d -exec chmod 775 {} ';' >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
