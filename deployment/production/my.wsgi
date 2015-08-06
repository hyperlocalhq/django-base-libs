#!/usr/local/www/apache24/data/creative-city-berlin.de/bin/python

# -*- coding: utf-8 -*-
import os
import sys
import site

django_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../lib/python2.7/site-packages/'),
)

site.addsitedir(django_path)
site.addsitedir('/usr/local/lib/python2.7/site-packages/')

project_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../project/ccb'),
)
sys.path += [project_path]
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
