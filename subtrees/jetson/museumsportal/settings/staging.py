# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
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

PREPEND_WWW = False

SESSION_COOKIE_DOMAIN = "museumsportal.jetsonproject.org"

ALLOWED_HOSTS = [
    "museumsportal.jetsonproject.org",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
HTTPSTATE_ENGINE = "jetson.apps.httpstate.backends.db"
