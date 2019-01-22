#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/ccb.jetsonproject.org
CRON_LOG_FILE=${PROJECT_PATH}/logs/backup_postgres_db_now.log
DATE_TIMESTAMP=$(LC_ALL=en_US.UTF-8 date +"%Y%m%d-%H%M")
BACKUP_PATH=${PROJECT_PATH}/db_backups/${DATE_TIMESTAMP}.backup
USER=jp_ccb
DATABASE=jp_ccb

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
