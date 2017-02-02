#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/collect_advertising_stats.log

echo "Collecting stats" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
. bin/activate
cd project/berlinbuehnen
python manage.py collect_advertising_stats --traceback >> ${CRON_LOG_FILE}  2>&1
python manage.py remove_old_advertising_stats --traceback >> ${CRON_LOG_FILE}  2>&1

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
