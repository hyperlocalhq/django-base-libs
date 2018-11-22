#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/backup_postgres_db_now.log
DATE_TIMESTAMP=$(LC_ALL=en_US.UTF-8 date +"%Y%m%d-%H%M")
BACKUP_PATH=${PROJECT_PATH}/db_backups/${DATE_TIMESTAMP}.backup
BACKUP_PATH_ALT=${PROJECT_PATH}/db_backups/latest.backup
USER=creativeberlin
DATABASE=creativeberlin

cd ${PROJECT_PATH}
mkdir -p logs
mkdir -p db_backups

echo "Creating DB Backup" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

echo "Dump database" >> ${CRON_LOG_FILE}
pg_dump --format=c --compress=9 --file=${BACKUP_PATH} ${DATABASE}
cp ${BACKUP_PATH}  ${BACKUP_PATH_ALT}

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
