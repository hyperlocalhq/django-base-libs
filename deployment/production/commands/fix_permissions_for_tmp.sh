#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/fix_permissions_for_tmp.log

echo "Fixing permissions for tmp directory" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/berlinbuehnen/berlinbuehnen/tmp

find . -type f -exec chmod 664 {} ';' >> ${CRON_LOG_FILE}  2>&1
find . -type d -exec chmod 775 {} ';' >> ${CRON_LOG_FILE}  2>&1
