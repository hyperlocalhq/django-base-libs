#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/creative-city-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/backup_db_now.log
DATE_TIMESTAMP=$(LC_ALL=en_US.UTF-8 date +"%Y%m%d-%H%M")
BACKUP_PATH=${PROJECT_PATH}/db_backups/${DATE_TIMESTAMP}.sql
USER=ccb
DATABASE=ccb
PASS=ot6q4R

EXCLUDED_TABLES=(
httpstate_httpstate
django_session
)

IGNORED_TABLES_STRING=''
for TABLE in "${EXCLUDED_TABLES[@]}"
do :
    IGNORED_TABLES_STRING+=" --ignore-table=${DATABASE}.${TABLE}"
done

echo "Creating DB Backup" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH}
mkdir -p db_backups

echo "Dump structure" >> ${CRON_LOG_FILE}
mysqldump -u ${USER} -p${PASS} --single-transaction --no-data ${DATABASE} > ${BACKUP_PATH} 2>> ${CRON_LOG_FILE}

echo "Dump content" >> ${CRON_LOG_FILE}
mysqldump -u ${USER} -p${PASS} ${DATABASE} ${IGNORED_TABLES_STRING} >> ${BACKUP_PATH} 2>> ${CRON_LOG_FILE}
