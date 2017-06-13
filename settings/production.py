# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = True

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
