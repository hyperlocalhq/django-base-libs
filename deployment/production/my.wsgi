#!/usr/local/www/apache24/data/berlin-buehnen.de/venv/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import site

#django_path = os.path.abspath(
#    os.path.join(os.path.dirname(__file__), '../lib/python2.7/site-packages/'),
#)
django_path = '/usr/local/www/apache24/data/berlin-buehnen.de/venv/lib/python2.7/site-packages'

site.addsitedir(django_path)
site.addsitedir('/usr/local/lib/python2.7/site-packages/')

project_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../project/berlinbuehnen'),
)
sys.path += [project_path]
os.environ['DJANGO_SETTINGS_MODULE'] = 'berlinbuehnen.settings.production'

import newrelic.agent
NEW_RELIC_INI = '/usr/local/www/apache24/data/berlin-buehnen.de/project/berlinbuehnen/newrelic.ini'
newrelic.agent.initialize(NEW_RELIC_INI, 'production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
