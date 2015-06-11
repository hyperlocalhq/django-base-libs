# -*- coding: utf-8 -*-
# Django settings for the complete example project.
import os

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
JETSON_PROJECTS_PATH = os.path.join(ROOT_PATH, "jetson", "projects")

execfile(os.path.join(ROOT_PATH, "jetson/settings/base.py"))

### HOST ###

SESSION_COOKIE_DOMAIN = "127.0.0.1"
PORT = ":8000"
HTTPS_PROTOCOL = "http"


### DIRS AND URLS ###

TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS = [
    os.path.join(JETSON_PROJECTS_PATH, "complete_project", "templates", "default"),
    os.path.join(JETSON_PROJECTS_PATH, "complete_project", "templates", "admin"),
    ] + TEMPLATE_DIRS

MEDIA_ROOT = os.path.join(JETSON_PROJECTS_PATH, "complete_project", "media")
MEDIA_URL = "/media/%s/" % get_media_svn_revision(MEDIA_ROOT)
PATH_TMP = os.path.join(JETSON_PROJECTS_PATH, "complete_project", "tmp")
CSS_URL = "%scss/default/" % MEDIA_URL
IMG_URL = "%simg/default/" % MEDIA_URL
SESSION_FILE_PATH = FILE_UPLOAD_TEMP_DIR = PATH_TMP


### DATABASE ###

DATABASE_ENGINE = "sqlite3"
DATABASE_NAME = os.path.join(JETSON_PROJECTS_PATH, "complete_project", "complete_project.sqlite")


### LANGUAGES ###

LANGUAGES = (
    ('de', "Deutsch"),
    ('en', "English"),
)

LANGUAGE_CODE = "en"


### MAIN ###

INSTALLED_APPS = (
    ### django core apps ###
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes", 
    "django.contrib.markup",
    
    ### third-party apps ###
    "babeldjango",
    "filebrowser",
    "grappelli",
    "tagging",
    "south",
    "compress",
    
    ### jetson apps ###
    "jetson.apps.image_mods",
    "jetson.apps.httpstate",
    "jetson.apps.templatesadmin",
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
    "jetson.apps.email_campaigns",
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
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "jetson.apps.utils.middleware.urlrewrite.URLRewriteMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "jetson.apps.flatpages.middleware.FlatpageMiddleware",
    "base_libs.middleware.threadlocals.ThreadLocalsMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "jetson.apps.utils.middleware.generic.AdminScriptUpdateMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    )

TEMPLATE_CONTEXT_PROCESSORS += [
    "jetson.apps.people.context_processors.people",
    "jetson.apps.institutions.context_processors.institutions",
    "jetson.apps.events.context_processors.events",
    "jetson.apps.resources.context_processors.resources",
    "jetson.apps.groups_networks.context_processors.groups_networks",
    "jetson.apps.media_gallery.context_processors.media_gallery",
    ]

SECRET_KEY = "*z-g$io@_qt9efb5dge+(64aeq4$!gk+62nsyqlgqpf8l6"

ROOT_URLCONF = "complete_project.urls"

AUTH_PROFILE_MODULE = "people.Person"


### CACHING ###

#CACHE_BACKEND = "locmem://" # passes cache-session test only
CACHE_BACKEND = "dummy:///"  # doesn't pass cache-session test


### FILEBROWSER ###

execfile(os.path.join(ROOT_PATH, "jetson/settings/filebrowser.py"))

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'nd': {'verbose_name': 'News Default (163px)', 'width': 163, 'height': 156, 'opts': 'crop upscale'},
    'nt': {'verbose_name': 'News Thumbnail (75px)', 'width': 163, 'height': 100, 'opts': 'crop upscale'},
}

FILEBROWSER_ADMIN_VERSIONS = ['nd','nt']


### OTHER SITE-SPECIFIC SETTINGS ###

IMAGE_MAX_SIZE = "342x342"
IMAGE_PREVIEW_MAX_SIZE = "161x161"
IMAGE_SMALL_SIZE = "75x75"

LOGO_SIZE = (165,165)
LOGO_PREVIEW_SIZE = "161x161"
LOGO_SMALL_SIZE = "50x50"


### GRAPPELLI ###

execfile(os.path.join(ROOT_PATH, "jetson/settings/grappelli.py"))


### LOCAL SETTINGS ###

try:
    execfile(os.path.join(os.path.dirname(__file__), "local_settings.py"))
except IOError:
    pass
