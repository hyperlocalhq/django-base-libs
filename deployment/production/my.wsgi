#!/usr/local/www/apache24/data/berlin-buehnen.de/bin/python
# -*- coding: utf-8 -*-
"""
WSGI config for berlinbuehnen project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os
import sys
import site


DJANGO_PATH = '/usr/local/www/apache24/data/berlin-buehnen.de/lib/python2.7/site-packages'

site.addsitedir(DJANGO_PATH)
site.addsitedir('/usr/local/lib/python2.7/site-packages/')

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

sys.path += [PROJECT_PATH]

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "temp.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "berlinbuehnen.settings")

import newrelic.agent
NEW_RELIC_INI = os.path.join(PROJECT_PATH, 'newrelic.ini')
newrelic.agent.initialize(NEW_RELIC_INI, 'production')

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
application = newrelic.agent.wsgi_application()(application)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
