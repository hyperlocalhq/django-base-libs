#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/ruhrbuehnen.jetsonproject.org
CRON_LOG_FILE=${PROJECT_PATH}/logs/backup_postgres_db.log
BACKUP_PATH=${PROJECT_PATH}/db_backups/$(date +%w-%A).backup
USER=jp_ruhrbuehnen
DATABASE=jp_ruhrbuehnen

cd ${PROJECT_PATH}
mkdir -p logs
mkdir -p db_backups

echo "Creating DB Backup" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

echo "Dump database" >> ${CRON_LOG_FILE}
pg_dump --format=c --compress=9 --file=${BACKUP_PATH} ${DATABASE}

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
