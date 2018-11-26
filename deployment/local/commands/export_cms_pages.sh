#!/usr/bin/env bash
SECONDS=0
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_PATH=$DIR/../../../../../

source ${PROJECT_PATH}bin/activate
cd ${PROJECT_PATH}project/ruhrbuehnen


echo "------------"
echo "Exporting CMS pages and plugins"
date

python manage.py dumpdata --settings=ruhrbuehnen.settings.local --traceback --indent=4 \
cms inherit picture snippet teaser richtext filebrowser_image gmap headline page_teaser \
articles.ArticleSelection theater_of_the_week.TheaterOfTheWeekSelection \
services.IndexItem services.ServicePageBanner services.ServiceGridItem services.ServiceListItem \
services.LinkCategory services.Link services.TitleAndText services.ImageAndText > ${PROJECT_PATH}cms_pages.json

echo "Finished."
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
