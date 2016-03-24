DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ccb_dj_1_7',
        'USER': "",
        'PASSWORD': "",
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB,'
                'character_set_connection=utf8,'
                'collation_connection=utf8_general_ci,'
                'foreign_key_checks=0'
        },
    }
}

HTTPS_PROTOCOL = "http"

SUBDOMAINS_SUPPORTED = False

SESSION_COOKIE_DOMAIN = "127.0.0.1"
PORT = ":8000"

FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""
SOCIAL_AUTH_FACEBOOK_KEY = ""
SOCIAL_AUTH_FACEBOOK_SECRET = ""

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEBUG = TEMPLATE_DEBUG = True

PREPEND_WWW = False

ALLOWED_HOSTS = ['127.0.0.1']

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