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
python manage.py migrate --fake --traceback --verbosity=2

echo "- Unapply all migrations"
SQL=$(cat << EOM
TRUNCATE TABLE django_migrations;
EOM
)
echo $SQL | python manage.py dbshell --traceback

echo "- Fake migrations of admin apps"
python manage.py migrate content_types --fake
python manage.py migrate auth --fake
python manage.py migrate sessions --fake
python manage.py migrate sites --fake
python manage.py migrate messages --fake
python manage.py migrate staticfiles --fake
python manage.py migrate admin --fake
python manage.py migrate sitemaps --fake

echo "- Fake migrations of project apps unrelated to Django CMS"
python manage.py migrate accounts --fake
python manage.py migrate advertising --fake
python manage.py migrate babeldjango --fake
python manage.py migrate blocks --fake
python manage.py migrate blog --fake
python manage.py migrate comments --fake
python manage.py migrate configuration --fake
python manage.py migrate crispy_forms --fake
python manage.py migrate editorial --fake
python manage.py migrate events --fake
python manage.py migrate extendedadmin --fake
python manage.py migrate external_services --fake
python manage.py migrate favorites --fake
python manage.py migrate haystack --fake
python manage.py migrate history --fake
python manage.py migrate httpstate --fake
python manage.py migrate i18n --fake
python manage.py migrate image_mods --fake
python manage.py migrate infobanners --fake
python manage.py migrate internal_links --fake
python manage.py migrate mailchimp --fake
python manage.py migrate mailing --fake
python manage.py migrate media_gallery --fake
python manage.py migrate mega_menu --fake
python manage.py migrate museums --fake
python manage.py migrate museumssummer --fake
python manage.py migrate permissions --fake
python manage.py migrate rosetta --fake
python manage.py migrate search --fake
python manage.py migrate shop --fake
python manage.py migrate site_specific --fake
python manage.py migrate slideshows --fake
python manage.py migrate tagging_autocomplete --fake
python manage.py migrate tagging --fake
python manage.py migrate tastypie --fake
python manage.py migrate tips --fake
python manage.py migrate tracker --fake
python manage.py migrate twitterwall --fake
python manage.py migrate utils --fake
python manage.py migrate workshops --fake

echo "- Migrate configuration and image_mods"
python manage.py migrate configuration 0001 --fake
python manage.py migrate configuration
python manage.py migrate image_mods 0001 --fake
python manage.py migrate image_mods

echo "- Migrate apps related to Django CMS"
python manage.py migrate menus
python manage.py migrate cms
python manage.py migrate djangocms_inherit
python manage.py migrate djangocms_picture
python manage.py migrate djangocms_snippet
python manage.py migrate djangocms_teaser
python manage.py migrate cms_extensions
python manage.py migrate richtext
python manage.py migrate filebrowser_image
python manage.py migrate gmap
python manage.py migrate headline
python manage.py migrate editorial
python manage.py migrate exhibitions_plugins
python manage.py migrate cms_ads

echo "- Migrate project apps that have both, normal models and plugins"
python manage.py migrate articles 0001 --fake
python manage.py migrate articles
python manage.py migrate exhibitions 0001 --fake
python manage.py migrate exhibitions

echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
