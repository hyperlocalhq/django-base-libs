#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/museumsportal-berlin.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/backup_db.log
BACKUP_PATH=${PROJECT_PATH}/db_backups/$(date +%w-%A).sql
LATEST_PATH=${PROJECT_PATH}/db_backups/latest.backup
USER=museumsportal
DATABASE=museumsportal
PASS=yg@VkV

EXCLUDED_TABLES=(
httpstate_httpstate
django_session
)

IGNORED_TABLES_STRING=''
for TABLE in "${EXCLUDED_TABLES[@]}"; do
    IGNORED_TABLES_STRING+=" --ignore-table=${DATABASE}.${TABLE}"
done

echo "Creating DB Backup" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}

cd ${PROJECT_PATH} || exit
mkdir -p db_backups

echo "Dump structure" >> ${CRON_LOG_FILE}
mysqldump -u ${USER} -p${PASS} --single-transaction --no-data ${DATABASE} > "${BACKUP_PATH}" 2>> ${CRON_LOG_FILE}

echo "Dump content" >> ${CRON_LOG_FILE}
mysqldump -u ${USER} -p${PASS} ${DATABASE} "${IGNORED_TABLES_STRING}" >> "${BACKUP_PATH}" 2>> ${CRON_LOG_FILE}

if [ -e ${LATEST_PATH} ]; then
    rm ${LATEST_PATH}
fi
ln -s "${BACKUP_PATH}" ${LATEST_PATH}

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$((duration / 60)) minutes and $((duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
