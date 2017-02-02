#!/usr/bin/env bash
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/backup_db.log
BACKUP_PATH=${PROJECT_PATH}/db_backups/$(date +%w-%A).sql
USER=berlinbuehnen
DATABASE=berlinbuehnen
PASS=pP-vaJ

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