#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/rebuild_index.log

echo "Rebuilding search index" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/berlinbuehnen
python manage.py rebuild_index --noinput --traceback >> ${CRON_LOG_FILE} 2>&1

cd ${PROJECT_PATH}/commands/
./fix_permissions_for_tmp.sh
