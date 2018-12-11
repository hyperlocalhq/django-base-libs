#!/usr/bin/env bash
source /usr/local/www/apache24/data/museumsportal-berlin.de/venv/bin/activate
cd /usr/local/www/apache24/data/museumsportal-berlin.de/project/museumsportal/
python manage.py stream_tweets --settings=museumsportal.settings.production &
