#!/usr/local/www/apache24/data/ruhr-buehnen.de/venv/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import site

django_path = '/usr/local/www/apache24/data/ruhr-buehnen.de/venv/lib/python2.7/site-packages'

site.addsitedir(django_path)
site.addsitedir('/usr/local/lib/python2.7/site-packages/')

project_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../project/ruhrbuehnen'),
)
sys.path += [project_path]
os.environ['DJANGO_SETTINGS_MODULE'] = 'ruhrbuehnen.settings.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
