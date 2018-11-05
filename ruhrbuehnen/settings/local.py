# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

ENVIRONMENT = 'local'

DATABASES = {
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'CONN_MAX_AGE': 600,
    },
}
DATABASES['default'] = DATABASES['postgresql']

HTTPS_PROTOCOL = "http"

SUBDOMAINS_SUPPORTED = False

SESSION_COOKIE_DOMAIN = "127.0.0.1"
PORT = ":8000"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEBUG = True

PREPEND_WWW = False

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ruhrbuehnen',
        'KEY_PREFIX': "bb_production_",
        'TIMEOUT': 300,
        'MAX_ENTRIES': 400,
    }
}

RAVEN_CONFIG = {
    'dsn': None,
}

LOGGING['loggers']['raven'] = {
    'handlers': ['null'],
    'level': 'ERROR',
}
