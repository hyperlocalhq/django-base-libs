#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=../../../../../

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ruhrbuehnen

#echo "Importing from Berliner Philharmonie"
#date
#python manage.py import_from_berliner_philharmonie --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from Deutsches Theater"
#date
#python manage.py import_from_deutsches_theater --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from HAU"
#date
#python manage.py import_from_hau --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from Komische Oper Berlin"
#date
#python manage.py import_from_komische_oper_berlin --settings=ruhrbuehnen.settings.local --traceback
#
echo "------------"
echo "Importing from Maxim Gorki Theater (New)"
date
python manage.py import_from_maxim_gorki_theater --update_images --settings=ruhrbuehnen.settings.local --traceback


echo "------------"
echo "Importing from Schaubuehne"
date
python manage.py import_from_schaubuehne --update_images --settings=ruhrbuehnen.settings.local --traceback

#echo "------------"
#echo "Importing from Schlosspark Theater (New)"
#date
#python manage.py import_from_schlosspark_theater_new --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from Konzerthaus (New)"
#date
#python manage.py import_from_konzerthaus_new --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from Sophiensaele"
#date
#python manage.py import_from_sophiensaele --update_images --settings=ruhrbuehnen.settings.local --traceback

#echo "------------"
#echo "Importing from Staatsballet Berlin"
#date
#python manage.py import_from_staatsballet_berlin --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from Volksbuehne"
#date
#python manage.py import_from_volksbuehne --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from Wuehlmaeuse"
#date
#python manage.py import_from_wuehlmaeuse --settings=ruhrbuehnen.settings.local --traceback
#
##echo "------------"
##echo "Importing from Theater an der Parkaue"
##date
##python manage.py import_from_parkaue --settings=ruhrbuehnen.settings.local --traceback 2>&1
#
#echo "------------"
#echo "Importing from Deutsche Oper Berlin"
#date
#python manage.py import_from_culturebase_dob --settings=ruhrbuehnen.settings.local --traceback
#
echo "------------"
echo "Importing from RADIALSYSTEM V"
date
python manage.py import_from_culturebase_radialsystem --update_images --settings=ruhrbuehnen.settings.local --traceback


#echo "------------"
#echo "Importing from Staatsoper im Schiller Theater"
#date
#python manage.py import_from_culturebase_sob --update_images --settings=ruhrbuehnen.settings.local --traceback

#echo "------------"
#echo "Importing from Pierre Boulez Saal (New)"
#date
#python manage.py import_from_boulezsaal --settings=ruhrbuehnen.settings.local --traceback
#

echo "------------"
echo "Importing from Berliner Ensemble (New)"
date
python manage.py import_from_berliner_ensemble --update_images --settings=ruhrbuehnen.settings.local --traceback

#echo "------------"
#echo "Importing from Volksbühne (New)"
#date
#python manage.py import_from_volksbuehne --settings=ruhrbuehnen.settings.local --traceback
#
#echo "------------"
#echo "Importing from Staatsoper Berlin (New)"
#date
#python manage.py import_from_staatsoper_berlin --settings=ruhrbuehnen.settings.local --traceback

echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
