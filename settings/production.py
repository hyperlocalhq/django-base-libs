# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from ._base import *

DEBUG = False
TEMPLATE_DEBUG = False

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

CACHE_MIDDLEWARE_KEY_PREFIX = "ccb_production_"

DEFAULT_LOGO_4_PERSON = "%ssite/img/website/placeholder/person.png" % STATIC_URL
DEFAULT_FORM_LOGO_4_PERSON = "%ssite/img/website/placeholder/person_f.png" % STATIC_URL
DEFAULT_SMALL_LOGO_4_PERSON = "%ssite/img/website/placeholder/person_s.png" % STATIC_URL

DEFAULT_LOGO_4_INSTITUTION = "%ssite/img/website/placeholder/institution.png" % STATIC_URL
DEFAULT_FORM_LOGO_4_INSTITUTION = "%ssite/img/website/placeholder/institution_f.png" % STATIC_URL
DEFAULT_SMALL_LOGO_4_INSTITUTION = "%ssite/img/website/placeholder/institution_s.png" % STATIC_URL

DEFAULT_LOGO_4_EVENT = "%ssite/img/website/placeholder/event.png" % STATIC_URL
DEFAULT_FORM_LOGO_4_EVENT = "%ssite/img/website/placeholder/event_f.png" % STATIC_URL
DEFAULT_SMALL_LOGO_4_EVENT = "%ssite/img/website/placeholder/event_s.png" % STATIC_URL

DEFAULT_LOGO_4_DOCUMENT = "%ssite/img/website/placeholder/document.png" % STATIC_URL
DEFAULT_FORM_LOGO_4_DOCUMENT = "%ssite/img/website/placeholder/document_f.png" % STATIC_URL
DEFAULT_SMALL_LOGO_4_DOCUMENT = "%ssite/img/website/placeholder/document_s.png" % STATIC_URL

CELERY_BROKER_URL = "redis://:protectst38@localhost:6379/0"
REDIS_PASSWORD = CELERY_REDIS_PASSWORD = BROKER_PASSWORD = CELERY_RESULT_PASSWORD = "protectst38"
