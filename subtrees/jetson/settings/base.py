# -*- coding: utf-8 -*-
import platform
import sys
import os

_ = lambda s:s

### MODE ###

INTERNAL_IPS = (
    "127.0.0.1",
    "217.92.175.81"
)

HTTPS_PROTOCOL = 'http' if DEBUG else "https"

### EMAILS ###

SERVER_EMAIL = "jetsonadmin@studio38.de"

### PATHS AND URLS ###

EXTERNAL_LIBS_PATH = os.path.join(JETSON_PATH, "jetson", "externals", "libs")
EXTERNAL_APPS_PATH = os.path.join(JETSON_PATH, "jetson", "externals", "apps")
BASE_LIBS_PATH = os.path.join(JETSON_PATH, "base_libs")
TAGGING_PATH = os.path.join(JETSON_PATH, "tagging")
TAGGING_AUTOCOMPLETE_PATH = os.path.join(JETSON_PATH, "tagging_autocomplete")
FILEBROWSER_PATH = os.path.join(JETSON_PATH, "filebrowser")
sys.path = [
    "",
    EXTERNAL_LIBS_PATH,
    EXTERNAL_APPS_PATH,
    BASE_LIBS_PATH,
    TAGGING_PATH,
    TAGGING_AUTOCOMPLETE_PATH,
    FILEBROWSER_PATH,
    JETSON_PATH,
    PROJECT_PATH,
] + [p for p in sys.path if p]

from jetson.apps.utils.utils import get_git_changeset

# TEMPLATE_DIRS = [
#     os.path.join(JETSON_PATH, "jetson", "templates", "default"),
#     os.path.join(JETSON_PATH, "jetson", "templates", "admin"),
#     # http://code.djangoproject.com/wiki/ExtendingTemplates
#     os.path.join(JETSON_PATH, "jetson", "externals", "apps", "grappelli", "templates", "grappelli"),
#     os.path.join(JETSON_PATH, "jetson", "externals", "apps", "grappelli", "templates"),
# ]

JETSON_MEDIA_ROOT = os.path.join(JETSON_PATH, "jetson", "media")
JETSON_MEDIA_URL = "/jetson-media/%s/" % get_git_changeset(JETSON_MEDIA_ROOT)

LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/"

LOCALE_PATHS = [
    os.path.join(JETSON_PATH, "jetson", "locale"),
    ]

TAGGING_AUTOCOMPLETE_JS_BASE_URL = "%sjs/jquery/autocomplete_1.0" % JETSON_MEDIA_URL

### MAIN ###

# TEMPLATE_CONTEXT_PROCESSORS = [
#     "django.contrib.auth.context_processors.auth",
#     "django.core.context_processors.debug",
#     "django.core.context_processors.i18n",
#     "django.core.context_processors.request",
#     "django.core.context_processors.static",
#     'django.core.context_processors.media',
#     "jetson.apps.utils.context_processors.general",
#     "django.contrib.messages.context_processors.messages",
# ]

AUTHENTICATION_BACKENDS = (
    "jetson.apps.permissions.backends.RowLevelPermissionsBackend",
    "jetson.apps.utils.backends.EmailBackend",
    #"django.contrib.auth.backends.ModelBackend",
)

# TEMPLATE_LOADERS = (
#     "base_libs.template.loaders.cached.Loader",
#     "django.template.loaders.filesystem.Loader",
#     "django.template.loaders.app_directories.Loader",
# )

DEFAULT_CHARSET = "UTF-8"
TEST_DATABASE_CHARSET = "utf8"
TEST_DATABASE_COLLATION = "utf8_general_ci"

TIME_ZONE = "Europe/Berlin"

SITE_ID = 1

PREPEND_WWW = not DEBUG

REDIRECT_FIELD_NAME = "goto_next"

FILE_UPLOAD_PERMISSIONS = 0664

### CACHING ###

# CACHE_BACKEND = "locmem://?timeout=30&max_entries=400" # passes cache-session test only
CACHE_BACKEND = "dummy://" # doesn't pass cache-session test

### SESSION ###

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 14 * 24 * 60 * 60 # 2 weeks
HTTPSTATE_COOKIE_AGE = 24 * 60 * 60 # 1 day

### LOGGING ###

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

### STORAGE ###

DEFAULT_FILE_STORAGE = 'base_libs.storage.ASCIIFileSystemStorage'

### OTHER SETTINGS ###

SUBDOMAINS_SUPPORTED = False

### TESTING ###

TEST_CHARSET = "utf8"
