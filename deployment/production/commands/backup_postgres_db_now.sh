#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/backup_postgres_db_now.log
DATE_TIMESTAMP=$(LC_ALL=en_US.UTF-8 date +"%Y%m%d-%H%M")
BACKUP_PATH=${PROJECT_PATH}/db_backups/${DATE_TIMESTAMP}.backup
LATEST_PATH=${PROJECT_PATH}/db_backups/latest.backup
USER=berlinbuehnen
DATABASE=berlinbuehnen

cd ${PROJECT_PATH} || exit 1
mkdir -p logs
mkdir -p db_backups

echo "Creating DB Backup" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

echo "Dump database" >> ${CRON_LOG_FILE}
pg_dump --format=c --compress=9 --file="${BACKUP_PATH}" ${DATABASE}

if [ -e ${LATEST_PATH} ]; then
    rm ${LATEST_PATH}
fi
ln -s "${BACKUP_PATH}" ${LATEST_PATH}

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$((duration / 60)) minutes and $((duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
