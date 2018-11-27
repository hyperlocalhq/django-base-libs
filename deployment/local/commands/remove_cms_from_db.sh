#!/usr/bin/env bash
SECONDS=0
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_PATH=$DIR/../../../../../

source ${PROJECT_PATH}bin/activate
cd ${PROJECT_PATH}project/museumsportal

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
DROP TABLE IF EXISTS cmsplugin_cmsadzone;
DROP TABLE IF EXISTS cmsplugin_editorialcontent;
DROP TABLE IF EXISTS cmsplugin_file;
DROP TABLE IF EXISTS cmsplugin_filebrowserimage;
DROP TABLE IF EXISTS cmsplugin_flash;
DROP TABLE IF EXISTS cmsplugin_footnote;
DROP TABLE IF EXISTS cmsplugin_frontpageteaser;
DROP TABLE IF EXISTS cmsplugin_gmap;
DROP TABLE IF EXISTS cmsplugin_googlemap;
DROP TABLE IF EXISTS cmsplugin_headline;
DROP TABLE IF EXISTS cmsplugin_inheritpageplaceholder;
DROP TABLE IF EXISTS cmsplugin_intro;
DROP TABLE IF EXISTS cmsplugin_link;
DROP TABLE IF EXISTS cmsplugin_newlyopenedexhibition;
DROP TABLE IF EXISTS cmsplugin_newlyopenedexhibitionext;
DROP TABLE IF EXISTS cmsplugin_picture;
DROP TABLE IF EXISTS cmsplugin_richtext;
DROP TABLE IF EXISTS cmsplugin_snippetptr;
DROP TABLE IF EXISTS cmsplugin_teaser;
DROP TABLE IF EXISTS cmsplugin_teaserblock;
DROP TABLE IF EXISTS cmsplugin_text;
DROP TABLE IF EXISTS cmsplugin_twitterrecententries;
DROP TABLE IF EXISTS cmsplugin_twittersearch;
DROP TABLE IF EXISTS cmsplugin_video;
DELETE FROM django_content_type WHERE app_label LIKE 'cms%';
DELETE FROM django_content_type WHERE app_label='menus';
DELETE FROM django_content_type WHERE app_label='cms_ads' AND model='cmsadzone';
DELETE FROM django_content_type WHERE app_label='articles' AND model='articleselection';
DELETE FROM django_content_type WHERE app_label='filebrowser_image' AND model='filebrowserimage';
DELETE FROM django_content_type WHERE app_label='gmap' AND model='gmap';
DELETE FROM django_content_type WHERE app_label='headline' AND model='headline';
DELETE FROM django_content_type WHERE app_label='jquery_ui_tab' AND model='jqueryuitab';
DELETE FROM django_content_type WHERE app_label='richtext' AND model='richtext';
DELETE FROM django_content_type WHERE app_label='editorial' AND model='editorialcontent';
DELETE FROM django_content_type WHERE app_label='editorial' AND model='teaserblock';
DELETE FROM django_content_type WHERE app_label='editorial' AND model='footnote';
DELETE FROM django_content_type WHERE app_label='editorial' AND model='intro';
DELETE FROM django_content_type WHERE app_label='editorial' AND model='frontpageteaser';
DELETE FROM django_content_type WHERE app_label='exhibitions' AND model='newlyopenedexhibition';
DELETE FROM django_content_type WHERE app_label='exhibitions_plugins' AND model='newlyopenedexhibitionext';
DELETE FROM auth_permission WHERE codename LIKE '%_cmsadzone';
DELETE FROM auth_permission WHERE codename LIKE '%_articleselection';
DELETE FROM auth_permission WHERE codename LIKE '%_filebrowserimage';
DELETE FROM auth_permission WHERE codename LIKE '%_gmap';
DELETE FROM auth_permission WHERE codename LIKE '%_headline';
DELETE FROM auth_permission WHERE codename LIKE '%_jqueryuitab';
DELETE FROM auth_permission WHERE codename LIKE '%_richtext';
DELETE FROM auth_permission WHERE codename LIKE '%_editorialcontent';
DELETE FROM auth_permission WHERE codename LIKE '%_teaserblock';
DELETE FROM auth_permission WHERE codename LIKE '%_footnote';
DELETE FROM auth_permission WHERE codename LIKE '%_intro';
DELETE FROM auth_permission WHERE codename LIKE '%_frontpageteaser';
DELETE FROM auth_permission WHERE codename LIKE '%_newlyopenedexhibition';
DELETE FROM auth_permission WHERE codename LIKE '%_newlyopenedexhibitionext';
EOM
)

python manage.py migrate cms zero --fake --settings=settings.local --traceback
python manage.py migrate cms_extensions zero --fake --settings=settings.local --traceback
python manage.py migrate menus zero --fake --settings=settings.local --traceback
echo $SQL | python manage.py dbshell --settings=settings.local --traceback


echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
