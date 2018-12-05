#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/ruhrbuehnen.jetsonproject.org
CRON_LOG_FILE=${PROJECT_PATH}/logs/rebuild_elasticsearch_index.log

echo "Rebuilding Elasticsearch index" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ruhrbuehnen
python manage.py search_index --rebuild --settings=ruhrbuehnen.settings.production --noinput --traceback >> ${CRON_LOG_FILE} 2>&1

cd ${PROJECT_PATH}/commands/
./fix_permissions_for_tmp.sh

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
