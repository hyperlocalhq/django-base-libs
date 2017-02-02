#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=/usr/local/www/apache24/data/berlin-buehnen.de
CRON_LOG_FILE=${PROJECT_PATH}/logs/import_from_individual_sources.log

cd ${PROJECT_PATH}
. bin/activate
cd project/berlinbuehnen

echo "Importing from Berliner Philharmonie" > ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_berliner_philharmonie --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Deutsches Theater" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_deutsches_theater --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from HAU" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_hau --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Komische Oper Berlin" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_komische_oper_berlin --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Maxim Gorki Theater" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_maxim_gorki_theater --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Schaubuehne" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_schaubuehne --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Schlosspark Theater (New)" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_schlosspark_theater_new --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Konzerthaus (New)" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_konzerthaus_new --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Sophiensaele" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_sophiensaele --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Staatsballet Berlin" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_staatsballet_berlin --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Volksbuehne" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_volksbuehne --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Wuehlmaeuse" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_wuehlmaeuse --traceback >> ${CRON_LOG_FILE}  2>&1

#echo "------------" >> ${CRON_LOG_FILE}
#echo "Importing from Theater an der Parkaue" >> ${CRON_LOG_FILE}
#date >> ${CRON_LOG_FILE}
#python manage.py import_from_parkaue --traceback >> ${CRON_LOG_FILE} 2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Deutsche Oper Berlin" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_culturebase_dob --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from RADIALSYSTEM V" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_culturebase_radialsystem --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Staatsoper im Schiller Theater" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_culturebase_sob --traceback >> ${CRON_LOG_FILE}  2>&1

echo "------------" >> ${CRON_LOG_FILE}
echo "Importing from Pierre Boulez Saal" >> ${CRON_LOG_FILE}
date >> ${CRON_LOG_FILE}
python manage.py import_from_boulezsaal --traceback >> ${CRON_LOG_FILE}  2>&1

cd ${PROJECT_PATH}/commands/
./fix_permissions_for_media.sh

echo "Finished." >> ${CRON_LOG_FILE}
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed." >> ${CRON_LOG_FILE}
