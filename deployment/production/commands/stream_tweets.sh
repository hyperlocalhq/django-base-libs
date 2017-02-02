#!/usr/bin/env bash
source /usr/local/www/apache24/data/museumsportal-berlin.de/bin/activate
cd /usr/local/www/apache24/data/museumsportal-berlin.de/project/museumsportal/
python manage.py stream_tweets &
