#!/usr/bin/env bash
SECONDS=0
PROJECT_PATH=../../../../../

cd ${PROJECT_PATH}
source venv/bin/activate
cd project/museumsportal

echo "------------"
echo "=== Running migrations ==="
date

export DJANGO_SETTINGS_MODULE=museumsportal.settings.local

echo "- Remove column name from content types table, and other deprecated columns"
SQL=$(cat << EOM
ALTER TABLE django_content_type DROP COLUMN name;
ALTER TABLE comments_moderatordeletionreason DROP COLUMN reason_markup_type;
EOM
)
echo $SQL | python manage.py dbshell --traceback

echo "- Create migration history table and missing content types"
python manage.py migrate --fake --traceback

echo "- Unapply all migrations"
SQL=$(cat << EOM
TRUNCATE TABLE django_migrations;
EOM
)
echo $SQL | python manage.py dbshell --traceback

echo "- Fake migrations of admin apps"
python manage.py migrate content_types --fake --noinput
python manage.py migrate auth --fake --noinput
python manage.py migrate sessions --fake --noinput
python manage.py migrate sites --fake --noinput
python manage.py migrate messages --fake --noinput
python manage.py migrate staticfiles --fake --noinput
python manage.py migrate admin --fake --noinput
python manage.py migrate sitemaps --fake --noinput

echo "- Fake migrations of project apps unrelated to Django CMS"
python manage.py migrate accounts --fake --noinput
python manage.py migrate advertising --fake --noinput
python manage.py migrate babeldjango --fake --noinput
python manage.py migrate blocks --fake --noinput
python manage.py migrate blog --fake --noinput
python manage.py migrate comments --fake --noinput
python manage.py migrate configuration --fake --noinput
python manage.py migrate crispy_forms --fake --noinput
python manage.py migrate extendedadmin --fake --noinput
python manage.py migrate external_services --fake --noinput
python manage.py migrate favorites --fake --noinput
python manage.py migrate haystack --fake --noinput
python manage.py migrate history --fake --noinput
python manage.py migrate httpstate --fake --noinput
python manage.py migrate i18n --fake --noinput
python manage.py migrate image_mods --fake --noinput
python manage.py migrate infobanners --fake --noinput
python manage.py migrate mailchimp --fake --noinput
python manage.py migrate mailing --fake --noinput
python manage.py migrate media_gallery --fake --noinput
python manage.py migrate mega_menu --fake --noinput
python manage.py migrate museums --fake --noinput
python manage.py migrate museumssummer --fake --noinput
python manage.py migrate permissions --fake --noinput
python manage.py migrate rosetta --fake --noinput
python manage.py migrate search --fake --noinput
python manage.py migrate site_specific --fake --noinput
python manage.py migrate slideshows --fake --noinput
python manage.py migrate tagging_autocomplete --fake --noinput
python manage.py migrate tagging --fake --noinput
python manage.py migrate tastypie --fake --noinput
python manage.py migrate tips --fake --noinput
python manage.py migrate tracker --fake --noinput
python manage.py migrate twitterwall --fake --noinput
python manage.py migrate utils --fake --noinput

echo "- Migrate configuration and image_mods"
python manage.py migrate configuration 0001 --fake --noinput
python manage.py migrate configuration --noinput
python manage.py migrate image_mods 0001 --fake --noinput
python manage.py migrate image_mods --noinput

echo "- Migrate apps related to Django CMS"
python manage.py migrate menus --noinput
python manage.py migrate cms --noinput
python manage.py migrate djangocms_inherit --noinput
python manage.py migrate djangocms_picture --noinput
python manage.py migrate djangocms_snippet --noinput
python manage.py migrate djangocms_teaser --noinput
python manage.py migrate cms_extensions --noinput
python manage.py migrate richtext --noinput
python manage.py migrate filebrowser_image --noinput
python manage.py migrate gmap --noinput
python manage.py migrate headline --noinput
python manage.py migrate editorial --noinput
python manage.py migrate cms_ads --noinput

echo "- Migrate project apps that have both, normal models and plugins"
python manage.py migrate articles 0001 --fake --noinput
python manage.py migrate articles --noinput
python manage.py migrate exhibitions 0001 --fake --noinput
python manage.py migrate exhibitions --noinput
python manage.py migrate exhibitions_plugins --noinput

echo "- Fake migrations for project apps that have dependencies on apps with plugins"
python manage.py migrate events --fake --noinput
python manage.py migrate workshops --fake --noinput
python manage.py migrate internal_links --fake --noinput
python manage.py migrate shop --fake --noinput

echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
