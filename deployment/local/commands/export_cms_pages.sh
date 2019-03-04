#!/usr/bin/env bash
SECONDS=0
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_PATH=$DIR/../../../../../

source ${PROJECT_PATH}bin/activate
cd ${PROJECT_PATH}project/museumsportal


echo "------------"
echo "Exporting CMS pages and plugins"
date

python manage.py dumpdata --settings=settings.local --traceback --indent=4 \
cms inherit picture snippet teaser richtext filebrowser_image gmap headline editorial \
cms_ads.CMSAdZone articles.ArticleSelection \
exhibitions.NewlyOpenedExhibition exhibitions_plugins.NewlyOpenedExhibitionExt > ${PROJECT_PATH}cms_pages.json

echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
