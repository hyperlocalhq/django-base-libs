#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=../../../../../

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/ruhrbuehnen

echo "------------"
echo "=== Running migrations ==="
date

echo "- Remove column name from content types table, and other deprecated columns"
SQL=$(cat << EOM
ALTER TABLE django_content_type DROP COLUMN name;
ALTER TABLE comments_moderatordeletionreason DROP COLUMN reason_markup_type;
EOM
)
echo $SQL | python manage.py dbshell --settings=ruhrbuehnen.settings.local --traceback

echo "- Create migration history table and missing content types"
python manage.py migrate --fake --settings=ruhrbuehnen.settings.local

echo "- Unapply all migrations"
SQL=$(cat << EOM
TRUNCATE TABLE django_migrations;
EOM
)
echo $SQL | python manage.py dbshell --settings=ruhrbuehnen.settings.local --traceback

echo "- Fake migrations of admin apps"
python manage.py migrate content_types --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate auth --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate sessions --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate sites --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate messages --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate staticfiles --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate admin --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate sitemaps --fake --settings=ruhrbuehnen.settings.local

echo "- Fake migrations of project apps unrelated to Django CMS"
python manage.py migrate accounts --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate advent_calendar --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate advertising --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate ajaxuploader --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate aldryn_search --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate autocomplete_light --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate babeldjango --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate blocks --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate blog --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate bootstrap_pagination --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate comments --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate crispy_forms --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate debug_toolbar --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate education --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate extendedadmin --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate external_services --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate favorites --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate festivals --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate filebrowser --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate grappelli --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate haystack --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate history --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate httpstate --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate i18n --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate infobanners --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate locations --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate mailchimp --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate mailing --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate marketplace --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate mega_menu --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate mptt --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate multiparts --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate people --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate permissions --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate productions --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate raven_compat --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate rosetta --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate search --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate sekizai --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate site_specific --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate slideshows --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate sponsors --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate tagging --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate tagging_autocomplete --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate tastypie --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate treebeard --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate twitter --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate utils --fake --settings=ruhrbuehnen.settings.local

echo "- Migrate configuration and image_mods"
python manage.py migrate configuration 0001 --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate configuration --settings=ruhrbuehnen.settings.local
python manage.py migrate image_mods 0001 --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate image_mods --settings=ruhrbuehnen.settings.local

echo "- Migrate apps related to Django CMS"
python manage.py migrate menus --settings=ruhrbuehnen.settings.local
python manage.py migrate cms --settings=ruhrbuehnen.settings.local
#python manage.py migrate djangocms_inherit --settings=ruhrbuehnen.settings.local
#python manage.py migrate djangocms_snippet --settings=ruhrbuehnen.settings.local
#python manage.py migrate djangocms_teaser --settings=ruhrbuehnen.settings.local
python manage.py migrate cms_extensions --settings=ruhrbuehnen.settings.local
python manage.py migrate richtext --settings=ruhrbuehnen.settings.local
python manage.py migrate filebrowser_image --settings=ruhrbuehnen.settings.local
python manage.py migrate gmap --settings=ruhrbuehnen.settings.local
python manage.py migrate headline --settings=ruhrbuehnen.settings.local
python manage.py migrate page_teaser --settings=ruhrbuehnen.settings.local

echo "- Migrate project apps that have both, normal models and plugins"
python manage.py migrate articles 0001 --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate articles --settings=ruhrbuehnen.settings.local
python manage.py migrate services 0001 --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate services --settings=ruhrbuehnen.settings.local
python manage.py migrate theater_of_the_week 0001 --fake --settings=ruhrbuehnen.settings.local
python manage.py migrate theater_of_the_week --settings=ruhrbuehnen.settings.local

echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
