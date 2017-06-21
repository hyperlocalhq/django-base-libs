#!/usr/local/www/apache24/data/kb.jetsonproject.org/bin/python
# -*- coding: utf-8 -*-
import os
import site
import sys

django_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../lib/python2.7/site-packages/'
    ),
)

site.addsitedir(django_path)
site.addsitedir('/usr/local/lib/python2.7/site-packages/')

project_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../project/kb'),
)
sys.path += [project_path]
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
