# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret("MYSQL_DATABASE_NAME"),
        'USER': get_secret("MYSQL_DATABASE_USER"),
        'PASSWORD': get_secret("MYSQL_DATABASE_PASSWORD"),
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=MyISAM,'
                'character_set_connection=utf8,'
                'collation_connection=utf8_general_ci,'
                'foreign_key_checks=0'
        },
    }
}
DATABASES['default'] = DATABASES['mysql']

PREPEND_WWW = False

SESSION_COOKIE_DOMAIN = "museumsportal.jetsonproject.org"

ALLOWED_HOSTS = [
    "museumsportal.jetsonproject.org",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
HTTPSTATE_ENGINE = "jetson.apps.httpstate.backends.db"
