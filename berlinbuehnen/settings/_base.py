# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

import os
import json
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy

_ = gettext = lambda s: s

DEBUG = False

SITE_ID = 1

with open(os.path.join(os.path.dirname(__file__), 'secrets.json')) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    '''Get the secret variable or return explicit exception.'''
    try:
        return secrets[setting]
    except KeyError:
        error_msg = 'Set the {0} secret variable'.format(setting)
        raise ImproperlyConfigured(error_msg)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
JETSON_PATH = BASE_DIR
PROJECT_PATH = os.path.join(BASE_DIR, "berlinbuehnen")

execfile(os.path.join(JETSON_PATH, "jetson/settings/base.py"), globals(), locals())

### DOMAINS ###

SESSION_COOKIE_DOMAIN = "www.berlin-buehnen.de"
STAGING_DOMAIN = "berlinbuehnen.jetsonproject.org"

### EMAILS ###

MANAGERS = (
    ('Berlin Bühnen Webmaster', 'berlin-buehnen@kulturprojekte-berlin.de'),
)

ADMINS = (
    ("Berlin Bühnen Webmaster", "bendoraitis@studio38.de"),
    ("Reinhard Knobelspies", "knobelspies@studio38.de"),
)

CONTENT_ADMINS = (
    ('Berlin Bühnen Webmaster', 'berlin-buehnen@kulturprojekte-berlin.de'),
)

DEFAULT_FROM_EMAIL = 'berlin-buehnen@kulturprojekte-berlin.de'

### DIRS AND URLS ###

MEDIA_ROOT = os.path.join(PROJECT_PATH, "berlinbuehnen", "media")
STATIC_ROOT = os.path.join(PROJECT_PATH, "berlinbuehnen", "static")
STATICFILES_DIRS = [os.path.join(PROJECT_PATH, "berlinbuehnen", "site_static")]
MEDIA_URL = "/media/"
STATIC_URL = PIPELINE_URL = "/static/%s/" % get_git_changeset(os.path.join(PROJECT_PATH, "berlinbuehnen"))
PATH_TMP = os.path.join(PROJECT_PATH, "berlinbuehnen", "tmp")
CSS_URL = "%scss/default/" % MEDIA_URL
IMG_URL = "%simg/website/" % MEDIA_URL
FILE_UPLOAD_TEMP_DIR = SESSION_FILE_PATH = PATH_TMP
FILE_UPLOAD_PERMISSIONS = 0775

LOCALE_PATHS = [
    os.path.join(PROJECT_PATH, "locale"),
]

### LANGUAGES ###

LANGUAGES = (
    ('de', u"Deutsch"),
    ('en', u"English"),
)

FRONTEND_LANGUAGES = (
    ('de', u"Deutsch"),
    ('en', u"English"),
)

OPEN_GRAPH_LOCALE_MAPPER = {
    'de': 'de_DE',
    'en': 'en_US',
}

LANGUAGE_CODE = "de"

### MAIN ###

INSTALLED_APPS = [
    ### third-party apps ###
    "autocomplete_light",
    "grappelli",
    "filebrowser",

    ### django core apps ###
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',

    ### more third-party apps ###
    "tastypie",
    "tagging",
    "tagging_autocomplete",
    "crispy_forms",
    "rosetta",
    "babeldjango",
    "haystack",
    "ajaxuploader",
    "debug_toolbar",
    "raven.contrib.django.raven_compat",
    "bootstrap_pagination",

    ### Required CMS Django 2.4.1 apps ###
    "cms",
    "mptt",
    "menus",
    "south",
    "sekizai",
    "aldryn_search",

    ### CMS plugins ###
    "cms.plugins.inherit",
    "cms.plugins.picture",
    "cms.plugins.snippet",
    "cms.plugins.teaser",
    # "cms.plugins.file",
    # "cms.plugins.flash",
    # "cms.plugins.googlemap",
    # "cms.plugins.link",
    # "cms.plugins.text",
    # "cms.plugins.twitter",
    # "cms.plugins.video",

    ### jetson apps ###
    "jetson.apps.i18n",
    "jetson.apps.image_mods",
    "jetson.apps.httpstate",
    "jetson.apps.history",
    "jetson.apps.utils",
    "jetson.apps.extendedadmin",
    "jetson.apps.permissions",
    "jetson.apps.blocks",
    "jetson.apps.configuration",
    "jetson.apps.mailing",
    "jetson.apps.external_services",
    "jetson.apps.comments",

    ### berlin buehnen apps ###
    "berlinbuehnen.apps.articles",
    "berlinbuehnen.apps.theater_of_the_week",
    "berlinbuehnen.apps.blog",
    "berlinbuehnen.apps.mailchimp",
    "berlinbuehnen.apps.mega_menu",
    "berlinbuehnen.apps.locations",
    "berlinbuehnen.apps.people",
    "berlinbuehnen.apps.festivals",
    "berlinbuehnen.apps.sponsors",
    "berlinbuehnen.apps.productions",
    "berlinbuehnen.apps.multiparts",
    "berlinbuehnen.apps.slideshows",
    "berlinbuehnen.apps.twitter",
    "berlinbuehnen.apps.advertising",
    "berlinbuehnen.apps.education",
    "berlinbuehnen.apps.search",
    "berlinbuehnen.apps.marketplace",
    "berlinbuehnen.apps.accounts",
    "berlinbuehnen.apps.favorites",
    "berlinbuehnen.apps.site_specific",
    "berlinbuehnen.apps.services",
    "berlinbuehnen.apps.infobanners",
    "berlinbuehnen.apps.cms_extensions",
    "berlinbuehnen.apps.cms_extensions.plugins.richtext",
    "berlinbuehnen.apps.cms_extensions.plugins.filebrowser_image",
    "berlinbuehnen.apps.cms_extensions.plugins.gmap",
    "berlinbuehnen.apps.cms_extensions.plugins.headline",
    "berlinbuehnen.apps.cms_extensions.plugins.page_teaser",
    "berlinbuehnen.apps.advent_calendar",
]

MIDDLEWARE_CLASSES = [
    'berlinbuehnen.middleware.SmartUpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'jetson.apps.httpstate.middleware.HttpStateMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'base_libs.middleware.threadlocals.ThreadLocalsMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'jetson.apps.mobile_detection.middleware.MobileDetectionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS = [
    os.path.join(PROJECT_PATH, "berlinbuehnen", "templates", "berlinbuehnen"),
    os.path.join(PROJECT_PATH, "berlinbuehnen", "templates", "admin"),
] + TEMPLATE_DIRS

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
    "jetson.apps.utils.context_processors.general",
    "jetson.apps.configuration.context_processors.configuration",
    "jetson.apps.advertising.context_processors.source_features",
    "django.contrib.messages.context_processors.messages",
    "berlinbuehnen.apps.site_specific.context_processors.languages",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

if not DEBUG:
    TEMPLATE_LOADERS = (
        (
            'django.template.loaders.cached.Loader',
            TEMPLATE_LOADERS
        ),
    )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = get_secret("SECRET_KEY")

ROOT_URLCONF = "berlinbuehnen.urls"

TIME_ZONE = 'Europe/Berlin'
USE_TZ = True
USE_I18N = True
USE_L10N = True

### ADMIN ###

ADMIN_APP_INDEX = (
    {
        'title': gettext('Content'),
        'apps': (
            ('cms', {
                'models': ('Page',),
            }),
            ('blocks', {
                'models': ('InfoBlock',),
            }),
            ('infobanners', {
                'models': ('InfoBanner',),
            }),
            ('locations', {
                'models': ('Service', 'AccessibilityOption', 'LocationCategory', 'District', 'Location',),
            }),
            ('people', {
                'models': ('Prefix', 'InvolvementType', 'AuthorshipType', 'Person'),
            }),
            ('festivals', {
                'models': ('Festival',),
            }),
            ('productions', {
                'models': ('LanguageAndSubtitles','ProductionCategory','ProductionCharacteristics', 'Production', 'EventCharacteristics', 'Event'),
            }),
            ('multiparts', {
                'models': ('Parent',),
            }),
            ('education', {
                'models': ('Department', 'ProjectTargetGroup', 'ProjectFormat', 'Project'),
            }),
            ('advent_calendar', {
                'verbose_name': gettext("Advent Calendar"),
                'models': ('Day',),
            }),
            ('sponsors', {
                'models': ('Sponsor',),
            }),
            ('slideshows', {
                'models': ('Slideshow',),
            }),
            ('articles', {
                'models': ('ArticleCategory','Article',),
            }),
            ('theater_of_the_week', {
                'verbose_name': gettext("Theater of the week"),
                'models': ('TheaterOfTheWeek',),
            }),
            ('blog', {
                'models': ('Blog','Post',),
            }),
            ('mega_menu', {
                'models': ("MenuBlock",),
            }),
            ('marketplace', {
                'models': ("JobType", "JobCategory", "JobOffer",),
            }),
            ('services', {
                'models': ("Banner",),
            }),
        )
    },
    {
        'title': gettext('Community'),
        'apps': (
            ('auth', {
                'verbose_name': gettext("Authentication"),
                'models': ("Group", "User",),
                'icon': 'key',
            }),
            ('permissions', {
                'models': ('PerObjectGroup','RowLevelPermission',),
            }),
            ('institutions', {
                'models': ("Institution",),
            }),
            ('twitterwall', {
                'verbose_name': gettext("Twitter Wall"),
                'models': ("SearchSettings", "UserTimelineSettings", "TwitterUser", "Tweet"),
            }),
            ('favorites', {
                'models': ("Favorite", "FavoriteListOptions"),
            }),
        )
    },
    {
        'title': gettext('Campaign'),
        'apps': (
            ('mailing', {
                'models': ("EmailMessage", "EmailTemplate", "EmailTemplatePlaceholder",),
                'icon': 'email',
            }),
            ('mailchimp', {
                'models': ("Settings", "MList", "Campaign"),
                'icon': 'email',
            }),
            ('advertising', {
                'models': ("Advertiser", "AdCategory", "AdZone", "BannerAd", "AdImpression", "AdClick"),
            }),
        )
    },
    {
        'title': gettext('Configure'),
        'apps': (
            ('structure', {
                'models': ("Vocabulary", "Term", "ContextCategory"),
            }),
            ('image_mods', {
                'verbose_name': gettext("Media"),
                'models': ("ImageModificationGroup","ImageModification","ImageCropping",),
            }),
            ('sites', {
                'verbose_name': gettext('Sites'),
                'models': ('Site',)
            }),
            ('i18n', {
                'models': ("Country", "Area", "Language", "CountryLanguage", "Phone", "Nationality", "TimeZone"),
            }),
            ('tagging', {
                'models': ("TaggedItem", "Tag",),
            }),
            ('external_services', {
                'models': ("Service", "ObjectMapper",),
            }),
            ('tastypie', {
                'models': ("ApiKey",),
            }),
            ('configuration', {
                'models': ("SiteSettings",),
            }),
        )
    }
)


### CACHING ###

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'berlinbuehnen',
    },
    'dummy': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'berlinbuehnen_production_'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

### FILEBROWSER ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/filebrowser.py"))

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff', '.eps'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm', '.swf', '.flv', '.f4v'],
    'Document': ['.pdf', '.doc', '.docx', '.rtf', '.txt',
                 '.xls', '.xlsx', '.csv', '.ppt', '.pptx',
                 ],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
    'Code': ['.html', '.py', '.js', '.css'],
    'Archive': ['.zip', '.rar', '.tar', '.gz'],
}

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
}
FILEBROWSER_MEDIA_URL = UPLOADS_URL = "/media/"

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 2  # 2 MB

### MAILING ###

MAILING_DEFAULT_FROM_NAME = "Berlin Bühnen"
MAILING_DEFAULT_FROM_EMAIL = "berlin-buehnen@kulturprojekte-berlin.de"

MAILING_CONTENT_TYPE_CHOICES = (
    ('authorship', _("Image authorship")),
    ('locations', _("Theaters")),
    ('productions', _("Productions")),
    ('festivals', _("Festivals")),
    ('educational_departments', _("Educational Departments")),
    ('educational_projects', _("Educational Projects")),
    ('article', _("News")),
    ('banner', _("Banner")),
    ('image_and_text', _("Image and text")),
    ('text', _("Text only")),
)

### DEBUG TOOLBAR ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))

### GRAPPELLI ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/grappelli.py"))
GRAPPELLI_ADMIN_HEADLINE = "Berlin Bühnen Admin"

GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    "auth": {
        "user": ("id__iexact", "username__icontains", "first_name__icontains", "last_name__icontains", "email__icontains",)
    }
}

### HAYSTACK ###

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "default"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
    },
    'de': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "de"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.berlin-buehnen.de/de/suche/',
    },
    'en': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "en"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.berlin-buehnen.de/en/search/',
    },
}

HAYSTACK_ITERATOR_LOAD_PER_QUERY = 100
HAYSTACK_ROUTERS = ['berlinbuehnen.apps.search.router.LanguageRouter']
ALDRYN_SEARCH_LANGUAGE_FROM_ALIAS = lambda alias: alias
ALDRYN_SEARCH_INDEX_BASE_CLASS = "berlinbuehnen.apps.search.search_indexes.CMSPageIndexBase"  # custom index base for pages
ALDRYN_SEARCH_REGISTER_APPHOOK = False  # we'll use a custom app hook for search

### MULTILINGUAL URLS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/multilingual_urls.py"))

### OTHER SITE-SPECIFIC SETTINGS ###

APPEND_SLASH = True
PREPEND_WWW = False

TWITTER_USERNAME = "berlinbuehnen"
TWITTER_NUMBER_OF_TWEETS = 3

TWITTER_CONSUMER_KEY = "JXZlfw8Z5jmkjGnQrL8xA"
TWITTER_CONSUMER_SECRET = "DHhs9PuW8macNUh2umWyRPCOwJlTvOibSaHglV9OA"
TWITTER_ACCESS_TOKEN = "21031007-IKGf49uQ0n3IvFkgQgkr272NrfPQTswnTk3KDuFxw"
TWITTER_ACCESS_TOKEN_SECRET = "oxoVdzL9Hv4UpLce1q9JxkxyGzF6qt4B5oxKFP0KuA"

TWITTER_STREAMING_CONSUMER_KEY = "irEv5itOQ4P6tcciZEPQ"
TWITTER_STREAMING_CONSUMER_SECRET = "Ti5v9uFBN7FCU3JwgzHs5N9V2r2K7nkJmWSkcPo3F4"
TWITTER_STREAMING_ACCESS_TOKEN = "21031007-mFG3zFLgfy6Dkr3GVyvUuikL8BtPQJamIgm3L3iuM"
TWITTER_STREAMING_ACCESS_TOKEN_SECRET = "4CSWiMVz9qbwmDOiG9PeaZLag0kvZwG5Zrdl7k"

API_LIMIT_PER_PAGE = 0

GALLERY_IMAGE_MIN_DIMENSIONS = (100, 100)

ROSETTA_STORAGE_CLASS = "rosetta.storage.SessionRosettaStorage"

TIME_INPUT_FORMATS = ("%H:%M:%S", "%H:%M", "%H.%M")

DISABLE_CONTEXT_PROCESSORS = True

COMMENTS_BANNED_USERS_GROUP = ""
ACCOUNTS_DASHBOARD_USER_GROUPS = ["Location Owners"]

ARTICLES_HAVE_TYPES = False

INFO_FILES_USERNAME = "location_owner"
INFO_FILES_PASSWORD = "BbYWnGNrkXbhUzbeUu4rweix"

### DJANGO CRISPY FORMS ###

CRISPY_TEMPLATE_PACK = "bootstrap3"

### DJANGO CMS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/cms.py"), globals(), locals())

CMS_LANGUAGES = {
    1: [
        {
            'code': 'de',
            'hide_untranslated': True,
            'name': u'Deutsch',
            'public': True,
            'redirect_on_fallback': False,
        },
        {
            'code': 'en',
            'hide_untranslated': True,
            'name': u'English',
            'public': True,
            'redirect_on_fallback': False,
        },
    ]
}

CMS_TEMPLATES = [
    ('cms/default.html', gettext('Default')),
    ('cms/start.html', gettext('Homepage')),
    ('services/service_first.html', gettext(u'Service – First')),
    ('services/service_second_grid.html', gettext(u'Service – Second – Grid')),
    ('services/service_second_list.html', gettext(u'Service – Second – List')),
    ('services/service_second_page.html', gettext(u'Service – Second – Page')),
    ('advent_calendar/advent_calendar.html', gettext(u'Advent Calendar')),
]

CMS_APPHOOKS = (
)

CMS_REDIRECTS = True
CMS_MENU_TITLE_OVERWRITE = True

CMS_CACHE_DURATIONS = {
    'content': 60,
    'menus': 3600,
    'permissions': 3600,
}
CMS_CACHE_PREFIX = "cms-"
CMS_SITE_CHOICES_CACHE_KEY = 'CMS:site_choices'
CMS_PAGE_CHOICES_CACHE_KEY = 'CMS:page_choices'

### SOCIAL AUTHENTICATION ###

AUTH_USER_MODEL = "auth.User"

### SENTRY ###

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

import raven

RAVEN_CONFIG = {
    'dsn': 'http://e3688d60c44f414fb5d13c5a455f5354:c337ee733e004b6a91600d78558b0056@46.101.101.159/7',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
}

### API KEYS ###

GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY")

### SSL FIX FOR REQUESTS ###

import os, certifi
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
