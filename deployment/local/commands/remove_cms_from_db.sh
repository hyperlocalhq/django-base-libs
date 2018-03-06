#!/usr/bin/env bash
SECONDS=0
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_PATH=$DIR/../../../../../

source ${PROJECT_PATH}bin/activate
cd ${PROJECT_PATH}project/berlinbuehnen

echo "------------"
echo "Removing CMS migrations"
date

SQL=$(cat << EOM
DROP TABLE IF EXISTS menus_cachekey;
DROP TABLE IF EXISTS cms_cmsplugin;
DROP TABLE IF EXISTS cms_extensions_cmspageopengraph;
DROP TABLE IF EXISTS cms_globalpagepermission;
DROP TABLE IF EXISTS cms_globalpagepermission_sites;
DROP TABLE IF EXISTS cms_page;
DROP TABLE IF EXISTS cms_page_placeholders;
DROP TABLE IF EXISTS cms_pagemoderator;
DROP TABLE IF EXISTS cms_pagemoderatorstate;
DROP TABLE IF EXISTS cms_pagepermission;
DROP TABLE IF EXISTS cms_pageuser;
DROP TABLE IF EXISTS cms_pageusergroup;
DROP TABLE IF EXISTS cms_placeholder;
DROP TABLE IF EXISTS cms_title;
DROP TABLE IF EXISTS cmsplugin_articleselection;
DROP TABLE IF EXISTS cmsplugin_filebrowserimage;
DROP TABLE IF EXISTS cmsplugin_gmap;
DROP TABLE IF EXISTS cmsplugin_headline;
DROP TABLE IF EXISTS cmsplugin_imageandtext;
DROP TABLE IF EXISTS cmsplugin_indexitem;
DROP TABLE IF EXISTS cmsplugin_inheritpageplaceholder;
DROP TABLE IF EXISTS cmsplugin_linkcategory;
DROP TABLE IF EXISTS cmsplugin_pageteaser;
DROP TABLE IF EXISTS cmsplugin_picture;
DROP TABLE IF EXISTS cmsplugin_richtext;
DROP TABLE IF EXISTS cmsplugin_servicegriditem;
DROP TABLE IF EXISTS cmsplugin_servicelistitem;
DROP TABLE IF EXISTS cmsplugin_servicepagebanner;
DROP TABLE IF EXISTS cmsplugin_snippetptr;
DROP TABLE IF EXISTS cmsplugin_teaser;
DROP TABLE IF EXISTS cmsplugin_theateroftheweekselection;
DROP TABLE IF EXISTS cmsplugin_titleandtext;
DROP TABLE IF EXISTS services_link;
DELETE FROM django_content_type WHERE app_label LIKE 'cms%';
DELETE FROM django_content_type WHERE app_label='menus';
DELETE FROM django_content_type WHERE app_label='articles' AND model='articleselection';
DELETE FROM django_content_type WHERE app_label='services' AND model='indexitem';
DELETE FROM django_content_type WHERE app_label='services' AND model='servicepagebanner';
DELETE FROM django_content_type WHERE app_label='services' AND model='servicegriditem';
DELETE FROM django_content_type WHERE app_label='services' AND model='servicelistitem';
DELETE FROM django_content_type WHERE app_label='services' AND model='linkcategory';
DELETE FROM django_content_type WHERE app_label='services' AND model='link';
DELETE FROM django_content_type WHERE app_label='services' AND model='titleandtext';
DELETE FROM django_content_type WHERE app_label='services' AND model='imageandtext';
DELETE FROM django_content_type WHERE app_label='theater_of_the_week' AND model='theateroftheweekselection';
DELETE FROM auth_permission WHERE codename LIKE '%_articleselection';
DELETE FROM auth_permission WHERE codename LIKE '%_indexitem';
DELETE FROM auth_permission WHERE codename LIKE '%_servicepagebanner';
DELETE FROM auth_permission WHERE codename LIKE '%_servicegriditem';
DELETE FROM auth_permission WHERE codename LIKE '%_servicelistitem';
DELETE FROM auth_permission WHERE codename LIKE '%_linkcategory';
DELETE FROM auth_permission WHERE codename LIKE '%_link';
DELETE FROM auth_permission WHERE codename LIKE '%_titleandtext';
DELETE FROM auth_permission WHERE codename LIKE '%_imageandtext';
DELETE FROM auth_permission WHERE codename LIKE '%_theateroftheweekselection';
EOM
)

python manage.py migrate cms zero --fake --settings=berlinbuehnen.settings.local --traceback
python manage.py migrate cms_extensions zero --fake --settings=berlinbuehnen.settings.local --traceback
python manage.py migrate menus zero --fake --settings=berlinbuehnen.settings.local --traceback
echo $SQL | python manage.py dbshell --settings=berlinbuehnen.settings.local --traceback


echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
