# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

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
        'CONN_MAX_AGE': 0,
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=MYISAM,'
                'character_set_connection=utf8,'
                'collation_connection=utf8_general_ci,'
                'foreign_key_checks=0'
            # 'init_command': 'SET storage_engine=INNODB,'
            #     'character_set_connection=utf8,'
            #     'collation_connection=utf8_general_ci,'
            #     'foreign_key_checks=0'
        },
    }
}
DATABASES['default'] = DATABASES['postgresql']
#DATABASES['default'] = DATABASES['mysql']

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
        'LOCATION': 'berlinbuehnen',
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