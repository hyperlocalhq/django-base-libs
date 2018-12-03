#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=../../../../../

cd ${PROJECT_PATH} || exit 1
# shellcheck source=../../../venv/bin/activate
source venv/bin/activate
cd project/berlinbuehnen || exit 1

echo "------------"
echo "=== Running migrations ==="
date

echo "- Remove column name from content types table, and other deprecated columns"
SQL=$(cat << EOM
ALTER TABLE django_content_type DROP COLUMN name;
ALTER TABLE comments_moderatordeletionreason DROP COLUMN reason_markup_type;
EOM
)
echo "$SQL" | python manage.py dbshell --settings=berlinbuehnen.settings.local --traceback

echo "- Create migration history table and missing content types"
python manage.py migrate --fake --settings=berlinbuehnen.settings.local

echo "- Unapply all migrations"
SQL=$(cat << EOM
TRUNCATE TABLE django_migrations;
EOM
)
echo "$SQL" | python manage.py dbshell --settings=berlinbuehnen.settings.local --traceback

echo "- Fake migrations of admin apps"
python manage.py migrate content_types --fake --settings=berlinbuehnen.settings.local
python manage.py migrate auth --fake --settings=berlinbuehnen.settings.local
python manage.py migrate sessions --fake --settings=berlinbuehnen.settings.local
python manage.py migrate sites --fake --settings=berlinbuehnen.settings.local
python manage.py migrate messages --fake --settings=berlinbuehnen.settings.local
python manage.py migrate staticfiles --fake --settings=berlinbuehnen.settings.local
python manage.py migrate admin --fake --settings=berlinbuehnen.settings.local
python manage.py migrate sitemaps --fake --settings=berlinbuehnen.settings.local

echo "- Fake migrations of project apps unrelated to Django CMS"
python manage.py migrate accounts --fake --settings=berlinbuehnen.settings.local
python manage.py migrate advent_calendar --fake --settings=berlinbuehnen.settings.local
python manage.py migrate advertising --fake --settings=berlinbuehnen.settings.local
python manage.py migrate ajaxuploader --fake --settings=berlinbuehnen.settings.local
python manage.py migrate aldryn_search --fake --settings=berlinbuehnen.settings.local
python manage.py migrate autocomplete_light --fake --settings=berlinbuehnen.settings.local
python manage.py migrate babeldjango --fake --settings=berlinbuehnen.settings.local
python manage.py migrate blocks --fake --settings=berlinbuehnen.settings.local
python manage.py migrate blog --fake --settings=berlinbuehnen.settings.local
python manage.py migrate bootstrap_pagination --fake --settings=berlinbuehnen.settings.local
python manage.py migrate comments --fake --settings=berlinbuehnen.settings.local
python manage.py migrate crispy_forms --fake --settings=berlinbuehnen.settings.local
python manage.py migrate debug_toolbar --fake --settings=berlinbuehnen.settings.local
python manage.py migrate education --fake --settings=berlinbuehnen.settings.local
python manage.py migrate extendedadmin --fake --settings=berlinbuehnen.settings.local
python manage.py migrate external_services --fake --settings=berlinbuehnen.settings.local
python manage.py migrate favorites --fake --settings=berlinbuehnen.settings.local
python manage.py migrate festivals --fake --settings=berlinbuehnen.settings.local
python manage.py migrate filebrowser --fake --settings=berlinbuehnen.settings.local
python manage.py migrate grappelli --fake --settings=berlinbuehnen.settings.local
python manage.py migrate haystack --fake --settings=berlinbuehnen.settings.local
python manage.py migrate history --fake --settings=berlinbuehnen.settings.local
python manage.py migrate httpstate --fake --settings=berlinbuehnen.settings.local
python manage.py migrate i18n --fake --settings=berlinbuehnen.settings.local
python manage.py migrate infobanners --fake --settings=berlinbuehnen.settings.local
python manage.py migrate locations --fake --settings=berlinbuehnen.settings.local
python manage.py migrate mailchimp --fake --settings=berlinbuehnen.settings.local
python manage.py migrate mailing --fake --settings=berlinbuehnen.settings.local
python manage.py migrate marketplace --fake --settings=berlinbuehnen.settings.local
python manage.py migrate mega_menu --fake --settings=berlinbuehnen.settings.local
python manage.py migrate mptt --fake --settings=berlinbuehnen.settings.local
python manage.py migrate multiparts --fake --settings=berlinbuehnen.settings.local
python manage.py migrate people --fake --settings=berlinbuehnen.settings.local
python manage.py migrate permissions --fake --settings=berlinbuehnen.settings.local
python manage.py migrate productions --fake --settings=berlinbuehnen.settings.local
python manage.py migrate raven_compat --fake --settings=berlinbuehnen.settings.local
python manage.py migrate rosetta --fake --settings=berlinbuehnen.settings.local
python manage.py migrate search --fake --settings=berlinbuehnen.settings.local
python manage.py migrate sekizai --fake --settings=berlinbuehnen.settings.local
python manage.py migrate site_specific --fake --settings=berlinbuehnen.settings.local
python manage.py migrate slideshows --fake --settings=berlinbuehnen.settings.local
python manage.py migrate sponsors --fake --settings=berlinbuehnen.settings.local
python manage.py migrate tagging --fake --settings=berlinbuehnen.settings.local
python manage.py migrate tagging_autocomplete --fake --settings=berlinbuehnen.settings.local
python manage.py migrate tastypie --fake --settings=berlinbuehnen.settings.local
python manage.py migrate treebeard --fake --settings=berlinbuehnen.settings.local
python manage.py migrate twitter --fake --settings=berlinbuehnen.settings.local
python manage.py migrate utils --fake --settings=berlinbuehnen.settings.local

echo "- Migrate configuration and image_mods"
python manage.py migrate configuration 0001 --fake --settings=berlinbuehnen.settings.local
python manage.py migrate configuration --settings=berlinbuehnen.settings.local
python manage.py migrate image_mods 0001 --fake --settings=berlinbuehnen.settings.local
python manage.py migrate image_mods --settings=berlinbuehnen.settings.local

echo "- Migrate apps related to Django CMS"
python manage.py migrate menus --settings=berlinbuehnen.settings.local
python manage.py migrate cms --settings=berlinbuehnen.settings.local
#python manage.py migrate djangocms_inherit --settings=berlinbuehnen.settings.local
#python manage.py migrate djangocms_snippet --settings=berlinbuehnen.settings.local
#python manage.py migrate djangocms_teaser --settings=berlinbuehnen.settings.local
python manage.py migrate cms_extensions --settings=berlinbuehnen.settings.local
python manage.py migrate richtext --settings=berlinbuehnen.settings.local
python manage.py migrate filebrowser_image --settings=berlinbuehnen.settings.local
python manage.py migrate gmap --settings=berlinbuehnen.settings.local
python manage.py migrate headline --settings=berlinbuehnen.settings.local
python manage.py migrate page_teaser --settings=berlinbuehnen.settings.local

echo "- Migrate project apps that have both, normal models and plugins"
python manage.py migrate articles 0001 --fake --settings=berlinbuehnen.settings.local
python manage.py migrate articles --settings=berlinbuehnen.settings.local
python manage.py migrate services 0001 --fake --settings=berlinbuehnen.settings.local
python manage.py migrate services --settings=berlinbuehnen.settings.local
python manage.py migrate theater_of_the_week 0001 --fake --settings=berlinbuehnen.settings.local
python manage.py migrate theater_of_the_week --settings=berlinbuehnen.settings.local

echo "Finished."
duration=$SECONDS
echo "$((duration / 60)) minutes and $((duration % 60)) seconds elapsed."
