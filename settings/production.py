# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

DATABASES = {
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
    },
}
DATABASES['default'] = DATABASES['postgresql']
HUEY['name'] = DATABASES['default']['NAME']

PREPEND_WWW = True

SESSION_COOKIE_DOMAIN = None

ALLOWED_HOSTS = [
    "www.creative-city-berlin.de",
    "creative-city-berlin.de",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
HTTPSTATE_ENGINE = "jetson.apps.httpstate.backends.db"

CELERY_BROKER_URL = "redis://:protectst38@localhost:6379/0"
REDIS_PASSWORD = CELERY_REDIS_PASSWORD = BROKER_PASSWORD = CELERY_RESULT_PASSWORD = "protectst38"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
HTTPSTATE_COOKIE_SECURE = True
HTTPSTATE_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
        "LOCATION": "127.0.0.1:11212",
        "KEY_PREFIX": "ccb_production_",
        "TIMEOUT": 3000,
        "MAX_ENTRIES": 4000,
    },
    'dummy': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

WEBSITE_URL = "https://www.creative-city-berlin.de/"
