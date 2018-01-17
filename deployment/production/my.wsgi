#!/usr/local/www/apache24/data/museumsportal-berlin.de/bin/python

# -*- coding: utf-8 -*-
import os
import sys
import site

django_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
        '../../../data/museumsportal-berlin.de/lib/python2.7/site-packages/'),
)

site.addsitedir(django_path)
site.addsitedir('/usr/local/lib/python2.7/site-packages/')

project_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../project/museumsportal'),
)
sys.path += [project_path]
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
