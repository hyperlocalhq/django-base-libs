# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DEBUG = False
TEMPLATES_DEBUG = False

DATABASES = {
    # 'postgresql': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': get_secret("DATABASE_NAME"),
    #     'USER': get_secret("DATABASE_USER"),
    #     'PASSWORD': get_secret("DATABASE_PASSWORD"),
    # },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB,'
                'character_set_connection=utf8,'
                'collation_connection=utf8_general_ci,'
                'foreign_key_checks=0'
        },
    }
}
DATABASES['default'] = DATABASES['mysql']

PREPEND_WWW = True

SESSION_COOKIE_DOMAIN = ".museumsportal-berlin.de"

ALLOWED_HOSTS = [
    "www.museumsportal-berlin.de",
    "museumsportal-berlin.de",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
HTTPSTATE_ENGINE = "jetson.apps.httpstate.backends.db"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
HTTPSTATE_COOKIE_SECURE = True
HTTPSTATE_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
