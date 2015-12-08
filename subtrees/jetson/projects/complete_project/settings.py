# -*- coding: utf-8 -*-
# Django settings for the complete example project.
import os
gettext = lambda s: s

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
JETSON_PROJECTS_PATH = os.path.join(PROJECT_PATH, "subtrees", "jetson", "projects")

execfile(os.path.join(PROJECT_PATH, "jetson/settings/base.py"))

### HOST ###

SESSION_COOKIE_DOMAIN = "127.0.0.1"
PORT = ":8000"
HTTPS_PROTOCOL = "http"


### EMAILS ###

MANAGERS = ADMINS = (
    ("Website Admin", "jetsonadmin@studio38.de"),
    )

CONTENT_ADMINS = (
    ("Content Admin", "jetsonadmin@studio38.de"),
    )

DEFAULT_FROM_EMAIL = "jetsonadmin@studio38.de"


### DIRS AND URLS ###

MEDIA_ROOT = os.path.join(JETSON_PROJECTS_PATH, "complete_project", "media")
MEDIA_URL = UPLOADS_URL = "/media/"
STATIC_ROOT = os.path.join(JETSON_PROJECTS_PATH, "complete_project", "static")
STATIC_URL = PIPELINE_URL = "/static/%s/" % get_git_changeset(JETSON_PROJECTS_PATH)

PATH_TMP = os.path.join(JETSON_PROJECTS_PATH, "complete_project", "tmp")
CSS_URL = "%scss/default/" % MEDIA_URL
IMG_URL = "%simg/default/" % MEDIA_URL
SESSION_FILE_PATH = FILE_UPLOAD_TEMP_DIR = PATH_TMP

STATICFILES_DIRS = [os.path.join(JETSON_PROJECTS_PATH, "complete_project", "site_static")]

TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS = [
    os.path.join(JETSON_PROJECTS_PATH, "complete_project", "templates", "default"),
    os.path.join(JETSON_PROJECTS_PATH, "complete_project", "templates", "admin"),
    ] + TEMPLATE_DIRS

### DATABASE ###

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(JETSON_PROJECTS_PATH, "complete_project", "complete_project.sqlite"),
    }
}

### LANGUAGES ###

LANGUAGES = (
    ('de', gettext("German")),
    ('en', gettext("English")),
)

LANGUAGE_CODE = "en"

TIME_ZONE = 'Europe/Berlin'

### MAIN ###

INSTALLED_APPS = (
    ### third-party apps ###
    "grappelli",
    "filebrowser",
    
    ### django core apps ###
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes", 
    "django.contrib.markup",
    "django.contrib.staticfiles",    
    "django.contrib.messages",    
    
    ### more third-party apps ###
    "babeldjango",
    "tagging",
    "south",
    "pipeline",
    "crispy_forms",
    "djcelery",
    "kombu.transport.django",
    
    ### jetson apps ###
    "jetson.apps.image_mods",
    "jetson.apps.httpstate",
    "jetson.apps.i18n",
    "jetson.apps.location",
    "jetson.apps.media_gallery",
    "jetson.apps.utils",
    "jetson.apps.permissions",
    "jetson.apps.blocks",
    "jetson.apps.flatpages",
    "jetson.apps.optionset",
    "jetson.apps.individual_relations",
    "jetson.apps.forum",
    "jetson.apps.structure",
    "jetson.apps.navigation",
    "jetson.apps.extendedadmin",
    "jetson.apps.history",
    "jetson.apps.memos",
    "jetson.apps.notification",
    "jetson.apps.rating",
    "jetson.apps.mailing",
    "jetson.apps.messaging",
    "jetson.apps.contact_form",
    "jetson.apps.configuration",
    "jetson.apps.ratings",
    "jetson.apps.favorites",
    "jetson.apps.recommendations",
    "jetson.apps.flaggings",
    "jetson.apps.priorities",
    "jetson.apps.reminders",
    "jetson.apps.bookmarks",
    "jetson.apps.comments",
    "jetson.apps.people",
    "jetson.apps.institutions",
    "jetson.apps.resources",
    "jetson.apps.events",
    "jetson.apps.groups_networks",
    "jetson.apps.articles",
    "jetson.apps.tracker",
    "jetson.apps.blog",
    "jetson.apps.faqs",
    "jetson.apps.compress_jetson",

    ### project-specific apps ###
    # ...
    )

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "jetson.apps.httpstate.middleware.HttpStateMiddleware",
    "base_libs.middleware.multilingual.MultilingualURLMiddleware",
    "django.middleware.common.CommonMiddleware",
    "jetson.apps.utils.middleware.urlrewrite.URLRewriteMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "jetson.apps.flatpages.middleware.FlatpageMiddleware",
    "base_libs.middleware.threadlocals.ThreadLocalsMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "jetson.apps.utils.middleware.generic.AdminScriptUpdateMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    )

TEMPLATE_CONTEXT_PROCESSORS += [
    "django.contrib.messages.context_processors.messages",
    "jetson.apps.configuration.context_processors.configuration",
    "jetson.apps.people.context_processors.people",
    "jetson.apps.institutions.context_processors.institutions",
    "jetson.apps.events.context_processors.events",
    "jetson.apps.resources.context_processors.resources",
    "jetson.apps.groups_networks.context_processors.groups_networks",
    "jetson.apps.media_gallery.context_processors.media_gallery",
    ]

SECRET_KEY = "*z-g$io@_qt9efb5dge+(64aeq4$!gk+62nsyqlgqpf8l6"

ROOT_URLCONF = "complete_project.urls"


### CACHING ###

#CACHE_BACKEND = "locmem://" # passes cache-session test only
CACHE_BACKEND = "dummy://"  # doesn't pass cache-session test


### FILEBROWSER ###

execfile(os.path.join(PROJECT_PATH, "jetson/settings/filebrowser.py"))

FILEBROWSER_VERSIONS = {}
FILEBROWSER_ADMIN_VERSIONS = []


### GRAPPELLI ###

execfile(os.path.join(PROJECT_PATH, "jetson/settings/grappelli.py"))

### COMPRESS ###

execfile(os.path.join(PROJECT_PATH, "jetson/settings/pipeline.py"))
PIPELINE_ROOT = os.path.join(PROJECT_PATH, "ccb", "site_static")
PIPELINE = False

COMPRESS_JETSON_JS['admin_person_change'] = {
    'source_filenames': (
        "js/admin/person_change.js",
        ),
    'output_filename': 'js/admin/person_change_compressed.js',
    }

COMPRESS_JETSON_JS['admin_institution_change'] = {
    'source_filenames': (
        "js/admin/institution_change.js",
        ),
    'output_filename': 'js/admin/institution_change_compressed.js',
    }

COMPRESS_JETSON_JS['autocomplete'] = {
    'source_filenames': (
        "js/jquery/autocomplete_1.0/jquery.bgiframe.min.js",
        "js/jquery/autocomplete_1.0/jquery.autocomplete.js",
        "js/website/autocomplete.js",
        ),
    'output_filename': 'js/jquery/autocomplete_compressed.js',
    }

COMPRESS_JETSON_JS['admin_event_change'] = {
    'source_filenames': (
        "js/admin/event_change.js",
        ),
    'output_filename': 'js/admin/event_change_compressed.js',
    }

COMPRESS_JETSON_JS['admin_document_change'] = {
    'source_filenames': (
        "js/admin/document_change.js",
        ),
    'output_filename': 'js/admin/document_change_compressed.js',
    }

COMPRESS_JETSON_JS['admin_job_offer_change'] = {
    'source_filenames': (
        "js/admin/job_offer_change.js",
        ),
    'output_filename': 'js/admin/job_offer_change_compressed.js',
    }
    
COMPRESS_JETSON_JS['jquery_plugins'] = {
    'source_filenames': (
        "js/jquery/jquery.ba-hashchange.min.js",
        "js/jquery/jquery.cookie.js",
        "js/jquery/jquery.popup.js",
        "js/jquery/uni-form.jquery.min.js",
        ),
    'output_filename': 'js/jquery/jquery_plugins_compressed.js',
    }


### CELERY ###

CELERY_RESULT_BACKEND = 'database'
# For scheduled jobs. 
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler" 
CELERY_TRACK_STARTED = True 
CELERY_SEND_EVENTS = True 
CELERYD_LOG_FILE = os.path.join(JETSON_PROJECTS_PATH, "complete_project/tmp/celery.log")

BROKER_URL = "django://"

import djcelery
djcelery.setup_loader()

### OTHER SETTINGS  ###

PATHS_NO_REDIRECTION = (
    "/tagging_autocomplete/",
    "/helper/",
    "/admin/",
    "/recrop/",
    "/grappelli/",
    STATIC_URL,
    MEDIA_URL,
    ADMIN_MEDIA_PREFIX,
    )

CRISPY_TEMPLATE_PACK = "bootstrap"

### LOCAL SETTINGS ###

try:
    execfile(os.path.join(os.path.dirname(__file__), "local_settings.py"))
except IOError:
    pass
