#!/usr/local/www/apache24/data/creative-city-berlin.de/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import site

django_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../lib/python2.7/site-packages/'
    ),
)

site.addsitedir(django_path)
site.addsitedir('/usr/local/lib/python2.7/site-packages/')

project_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../project/ccb'),
)
sys.path += [project_path]
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import newrelic.agent
newrelic.agent.initialize('/usr/local/www/apache24/data/creative-city-berlin.de/project/ccb/deployment/production/newrelic.ini', 'production')

from django.core.wsgi import get_wsgi_application
try:
    application = get_wsgi_application()
    application = newrelic.agent.wsgi_application()(application)
except Exception:
    if 'mod_wsgi' in sys.modules:
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
    raise
