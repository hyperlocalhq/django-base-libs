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
}
DATABASES['default'] = DATABASES['postgresql']
HUEY['name'] = DATABASES['default']['NAME']

HTTPS_PROTOCOL = "http"

SUBDOMAINS_SUPPORTED = False

#SESSION_COOKIE_DOMAIN = "127.0.0.1"
#SESSION_COOKIE_DOMAIN = "local.creative-city-berlin.de"
#SESSION_COOKIE_DOMAIN = "192.168.0.37"
SESSION_COOKIE_DOMAIN = "0.0.0.0"
PORT = ":8000"

FACEBOOK_APP_ID = get_secret("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = get_secret("FACEBOOK_APP_SECRET")

COMPRESS = False

JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_ccb'

PATHS_NO_REDIRECTION = (
    "/tagging_autocomplete/",
    "/helper/",
    "/admin/",
    "/recrop/",
    "/grappelli/",
    JETSON_MEDIA_URL,
    STATIC_URL,
    MEDIA_URL,
    ADMIN_MEDIA_PREFIX,
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEBUG = True
# ALLOWED_HOSTS = ['local.creative-city-berlin.de']

PREPEND_WWW = False

ALLOWED_HOSTS = ['0.0.0.0']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'CCB',
        'KEY_PREFIX': "ccb_production_",
        'TIMEOUT': 300,
        'MAX_ENTRIES': 400,
    }
}

RAVEN_CONFIG = {
    'dsn': None,
}

WEBSITE_URL = "http://0.0.0.0:8000/"
