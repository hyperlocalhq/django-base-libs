# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DATABASES = {
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ccb',
        'USER': "aidas",
        'PASSWORD': "",
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret("DATABASE_NAME"),
        'USER': get_secret("DATABASE_USER"),
        'PASSWORD': get_secret("DATABASE_PASSWORD"),
        'CONN_MAX_AGE': 0,
        'HOST': 'localhost',
        'OPTIONS': {
            'init_command': 'SET character_set_connection=utf8,'
                'collation_connection=utf8_general_ci,'
                'foreign_key_checks=0'
            # 'init_command': 'SET storage_engine=INNODB,'
            #     'character_set_connection=utf8,'
            #     'collation_connection=utf8_general_ci,'
            #     'foreign_key_checks=0'
        },
    }
}
DATABASES['default'] = DATABASES['mysql']
HUEY['name'] = DATABASES['default']['NAME']

HTTPS_PROTOCOL = "http"

SUBDOMAINS_SUPPORTED = False

#SESSION_COOKIE_DOMAIN = "127.0.0.1"
#SESSION_COOKIE_DOMAIN = "local.creative-city-berlin.de"
#SESSION_COOKIE_DOMAIN = "192.168.0.37"
SESSION_COOKIE_DOMAIN = "0.0.0.0"
PORT = ":8000"

#JQUERY_UI_URL = "%sjs/jquery/jquery-ui.min.js" % JETSON_MEDIA_URL

FACEBOOK_APP_ID = "191833660875508"
FACEBOOK_APP_SECRET = "94802409f57a9e18f9ae24880420aadf"
SOCIAL_AUTH_FACEBOOK_KEY = "1219541161394461"
SOCIAL_AUTH_FACEBOOK_SECRET = "0071897e081898cf3d591aee064e45bb"

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


class DisabledMigrations(object):
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return "{}.migrations_not_used_in_tests".format(item)


MIGRATION_MODULES = DisabledMigrations()