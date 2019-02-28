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

PREPEND_WWW = False

SESSION_COOKIE_DOMAIN = None

ALLOWED_HOSTS = [
    "ccb.jetsonproject.org",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
HTTPSTATE_ENGINE = "jetson.apps.httpstate.backends.db"

CELERY_BROKER_URL = "redis://:protectst38@localhost:6379/0"
REDIS_PASSWORD = CELERY_REDIS_PASSWORD = BROKER_PASSWORD = CELERY_RESULT_PASSWORD = "protectst38"

WEBSITE_URL = "http://ccb.jetsonproject.org/"
