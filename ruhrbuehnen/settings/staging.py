# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *
ENVIRONMENT = 'staging'

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
    },
}
DATABASES['default'] = DATABASES['postgresql']

PREPEND_WWW = False

SESSION_COOKIE_DOMAIN = "ruhrbuehnen.jetsonproject.org"

ALLOWED_HOSTS = [
    "ruhrbuehnen.jetsonproject.org",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
HTTPSTATE_ENGINE = "jetson.apps.httpstate.backends.db"
