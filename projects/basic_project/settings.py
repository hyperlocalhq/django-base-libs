# -*- coding: utf-8 -*-
# Django settings for the basic example project.
import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
".."))
JETSON_PROJECTS_PATH = os.path.join(PROJECT_PATH, "subtrees", "jetson", "projects")

execfile(os.path.join(PROJECT_PATH, "jetson/settings/base.py"))

### HOST ###

SESSION_COOKIE_DOMAIN = "127.0.0.1"
PORT = ":8000"
HTTPS_PROTOCOL = "http"


### DIRS AND URLS ###

TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS = [
    os.path.join(JETSON_PROJECTS_PATH, "basic_project", "templates", "default"),
    os.path.join(JETSON_PROJECTS_PATH, "basic_project", "templates", "admin"),
    ] + TEMPLATE_DIRS

MEDIA_ROOT = os.path.join(JETSON_PROJECTS_PATH, "basic_project", "media")
MEDIA_URL = "/media/%s/" % get_media_svn_revision(MEDIA_ROOT)
PATH_TMP = os.path.join(JETSON_PROJECTS_PATH, "basic_project", "tmp")
CSS_URL = "%scss/default/" % MEDIA_URL
IMG_URL = "%simg/default/" % MEDIA_URL
FILE_UPLOAD_TEMP_DIR = PATH_TMP


### DATABASE ###

DATABASE_ENGINE = "sqlite3"
DATABASE_NAME = os.path.join(JETSON_PROJECTS_PATH, "basic_project", "basic_project.sqlite")


### LANGUAGES ###

LANGUAGES = (
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
    "jetson.apps.i18n",
    "jetson.apps.utils",
    "jetson.apps.permissions",
    "jetson.apps.blocks",
    "jetson.apps.flatpages",
    "jetson.apps.optionset",
    "jetson.apps.structure",
    "jetson.apps.navigation",
    "jetson.apps.extendedadmin",
    "jetson.apps.history",
    "jetson.apps.mailing",
    "jetson.apps.configuration",
    "jetson.apps.compress_jetson",

    ### project-specific apps ###
    "basic_project.apps.events",
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

SECRET_KEY = "*z-g$io@_qt9efb5dge+(64aeq4$!gk+62nsyqlgqpf8l6"

ROOT_URLCONF = "basic_project.urls"


### CACHING ###

#CACHE_BACKEND = "locmem://" # passes cache-session test only
CACHE_BACKEND = "dummy://"  # doesn't pass cache-session test


### FILEBROWSER ###

execfile(os.path.join(PROJECT_PATH, "jetson/settings/filebrowser.py"))

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'nd': {'verbose_name': 'News Default (163px)', 'width': 163, 'height': 156, 'opts': 'crop upscale'},
    'nt': {'verbose_name': 'News Thumbnail (75px)', 'width': 163, 'height': 100, 'opts': 'crop upscale'},
    }

FILEBROWSER_ADMIN_VERSIONS = ['nd','nt']


### GRAPPELLI ###

execfile(os.path.join(PROJECT_PATH, "jetson/settings/grappelli.py"))


### OTHER SITE-SPECIFIC SETTINGS ###

IMAGE_MAX_SIZE = "342x342"
IMAGE_PREVIEW_MAX_SIZE = "161x161"
IMAGE_SMALL_SIZE = "75x75"

LOGO_SIZE = (165,165)
LOGO_PREVIEW_SIZE = "161x161"
LOGO_SMALL_SIZE = "50x50"


### LOCAL SETTINGS ###

try:
    execfile(os.path.join(os.path.dirname(__file__), "local_settings.py"))
except IOError:
    pass
