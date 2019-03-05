# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *
ENVIRONMENT = 'test'

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
    },
}
DATABASES['default'] = DATABASES['postgresql']

HTTPS_PROTOCOL = "http"

SUBDOMAINS_SUPPORTED = False

SESSION_COOKIE_DOMAIN = "0.0.0.0"
ALLOWED_HOSTS = ['0.0.0.0']
PORT = ":8000"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PREPEND_WWW = False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'berlinbuehnen',
        'KEY_PREFIX': "bb_production_",
        'TIMEOUT': 300,
        'MAX_ENTRIES': 400,
    }
}

RAVEN_CONFIG = {
    'dsn': None,
}


class DisabledMigrations(object):
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return "{}.migrations_not_used_in_tests".format(item)


MIGRATION_MODULES = DisabledMigrations()

WEBSITE_URL = "http://0.0.0.0:8000"