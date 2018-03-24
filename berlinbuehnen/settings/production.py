# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DEBUG = False
TEMPLATES_DEBUG = False

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

PREPEND_WWW = True

SESSION_COOKIE_DOMAIN = None

ALLOWED_HOSTS = [
    "www.berlin-buehnen.de",
    "berlin-buehnen.de",
]

SESSION_ENGINE = "django.contrib.sessions.backends.db"
HTTPSTATE_ENGINE = "jetson.apps.httpstate.backends.db"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
HTTPSTATE_COOKIE_SECURE = True
HTTPSTATE_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False


CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
    "LOCATION": "127.0.0.1:11211",
    "KEY_PREFIX": "berlinbuehnen_production_",
    "TIMEOUT": 3000,
    "MAX_ENTRIES": 400,
}

CACHES['session'] = {
    "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
    "LOCATION": "127.0.0.1:11211",
    "KEY_PREFIX": "berlinbuehnen_session_production_",
    "TIMEOUT": 3000,
    "MAX_ENTRIES": 400,
}

CACHE_MIDDLEWARE_KEY_PREFIX = "berlinbuehnen_production_"
SESSION_CACHE_ALIAS = "session"