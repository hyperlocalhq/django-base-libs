DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

PREPEND_WWW = False

SESSION_COOKIE_DOMAIN = "127.0.0.1"
PORT = ":8000"

ALLOWED_HOSTS = [
    "www.creative-city-berlin.de",
    "creative-city-berlin.de",
    # "ccb.jetsonproject.org",
    # 'localhost',
    # '127.0.0.1',
]

HTTPS_PROTOCOL = "http"

SUBDOMAINS_SUPPORTED = False

FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""

## Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
# Using port 1025 to send test emails to MailHog.
# To start MailHog, just enter the following command into the command-line:
# $ MailHog
# If go and MailHog are not installed, install go:
# $ pkg install go
# then install MailHog:
# $ go get github.com/mailhog/MailHog
# remember to set $GOPATH, and to add $GOPATH/bin to your PATH

## Caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'CCB',
        'KEY_PREFIX': "ccb_production_",
        'TIMEOUT': 300,
        'MAX_ENTRIES': 400,
    }
}

## Disable Sentry when running on staging

RAVEN_CONFIG = {
    'dsn': None,
}
