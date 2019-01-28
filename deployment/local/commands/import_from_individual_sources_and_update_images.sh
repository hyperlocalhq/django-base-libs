#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=../../../../../

cd ${PROJECT_PATH} || exit 1
source venv/bin/activate
cd project/berlinbuehnen || exit 1

echo "------------"
echo "Importing from Maxim Gorki Theater (New)"
date
python manage.py import_from_maxim_gorki_theater --update_images --settings=berlinbuehnen.settings.local --traceback

echo "------------"
echo "Importing from Schaubuehne"
date
python manage.py import_from_schaubuehne --update_images --settings=berlinbuehnen.settings.local --traceback

echo "------------"
echo "Importing from RADIALSYSTEM V"
date
python manage.py import_from_culturebase_radialsystem --update_images --settings=berlinbuehnen.settings.local --traceback

echo "------------"
echo "Importing from Berliner Ensemble (New)"
date
python manage.py import_from_berliner_ensemble --update_images --settings=berlinbuehnen.settings.local --traceback

echo "Finished."
duration=$SECONDS
echo "$((duration / 60)) minutes and $((duration % 60)) seconds elapsed."
