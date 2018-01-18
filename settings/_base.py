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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
JETSON_PATH = BASE_DIR
PROJECT_PATH = BASE_DIR

execfile(os.path.join(JETSON_PATH, "jetson/settings/base.py"), globals(), locals())

### DOMAINS ###

SESSION_COOKIE_DOMAIN = "www.museumsportal-berlin.de"
STAGING_DOMAIN = "museumsportal.jetsonproject.org"

### EMAILS ###

MANAGERS = (
    ('Museumsportal Berlin Webmaster', 'museumsportal@kulturprojekte-berlin.de'),
)

ADMINS = (
    ("Museumsportal Berlin Webmaster", "bendoraitis@studio38.de"),
    ("Reinhard Knobelspies", "knobelspies@studio38.de"),
)

CONTENT_ADMINS = (
    ('Museumsportal Berlin Webmaster', 'museumsportal@kulturprojekte-berlin.de'),
)

DEFAULT_FROM_EMAIL = 'museumsportal@kulturprojekte-berlin.de'

### DIRS AND URLS ###

MEDIA_ROOT = os.path.join(PROJECT_PATH, "museumsportal", "media")
STATIC_ROOT = os.path.join(PROJECT_PATH, "museumsportal", "static")
STATICFILES_DIRS = [os.path.join(PROJECT_PATH, "museumsportal", "site_static")]
MEDIA_URL = "/media/"
STATIC_URL = PIPELINE_URL = "/static/%s/" % get_git_changeset(os.path.join(PROJECT_PATH, "museumsportal"))
PATH_TMP = os.path.join(PROJECT_PATH, "museumsportal", "tmp")
CSS_URL = "%scss/default/" % MEDIA_URL
IMG_URL = "%simg/website/" % MEDIA_URL
FILE_UPLOAD_TEMP_DIR = SESSION_FILE_PATH = PATH_TMP
FILE_UPLOAD_PERMISSIONS = 0775

LOCALE_PATHS = [
    os.path.join(PROJECT_PATH, "museumsportal", "locale"),
]

### LANGUAGES ###

LANGUAGES = (
    ('de', u"Deutsch"),
    ('en', u"English"),
    ('fr', u"Français"),
    ('pl', u"Polski"),
    ('tr', u"Türkçe"),
    ('es', u"Español"),
    ('it', u"Italiano"),
)

FRONTEND_LANGUAGES = (
    ('de', u"Deutsch"),
    ('en', u"English"),
)

OPEN_GRAPH_LOCALE_MAPPER = {
    'de': 'de_DE',
    'en': 'en_US',
    'fr': 'fr_FR',
    'pl': 'pl_PL',
    'tr': 'tr_TR',
    'es': 'es_ES',
    'it': 'it_IT',
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
    "pipeline",
    "uni_form",
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
    #"jetson.apps.external_services",
    "jetson.apps.favorites",
    "jetson.apps.blog",

    ### museumsportal apps ###
    "museumsportal.apps.permissions",
    "museumsportal.apps.museums",
    "museumsportal.apps.exhibitions",
    "museumsportal.apps.exhibitions_plugins",
    "museumsportal.apps.slideshows",
    "museumsportal.apps.editorial",
    "museumsportal.apps.articles",
    "museumsportal.apps.twitterwall",
    "museumsportal.apps.events",
    "museumsportal.apps.workshops",
    "museumsportal.apps.site_specific",
    "museumsportal.apps.search",
    "museumsportal.apps.external_services",
    "museumsportal.apps.internal_links",
    "museumsportal.apps.shop",
    "museumsportal.apps.museumssummer",
    "museumsportal.apps.tips",

    # the following apps are copied and converted from jetson
    "museumsportal.apps.mailchimp",
    "museumsportal.apps.blocks",
    "museumsportal.apps.media_gallery",
    "museumsportal.apps.configuration",
    "museumsportal.apps.advertising",
    "museumsportal.apps.advertising.plugins.cms_ads",
    "museumsportal.apps.comments",
    "museumsportal.apps.mega_menu",
    "museumsportal.apps.mailing",
    "museumsportal.apps.tracker",
    "museumsportal.apps.accounts",
    "museumsportal.apps.cms_extensions",
    "museumsportal.apps.cms_extensions.plugins.richtext",
    "museumsportal.apps.cms_extensions.plugins.filebrowser_image",
    "museumsportal.apps.cms_extensions.plugins.gmap",
    "museumsportal.apps.cms_extensions.plugins.headline",
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'jetson.apps.httpstate.middleware.HttpStateMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'base_libs.middleware.threadlocals.ThreadLocalsMiddleware',
    #"cms.middleware.multilingual.MultilingualURLMiddleware",
    #"museumsportal.apps.cms_extensions.middleware.MultilingualURLMiddleware",
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'jetson.apps.mobile_detection.middleware.MobileDetectionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS = [
    os.path.join(PROJECT_PATH, "museumsportal", "templates", "museumsportal"),
    os.path.join(PROJECT_PATH, "museumsportal", "templates", "admin"),
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
    "museumsportal.apps.site_specific.context_processors.languages",
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

ROOT_URLCONF = "museumsportal.urls"

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
            ('museums', {
                'models': ('MuseumCategory','MuseumService','AccessibilityOption', 'Museum',),
            }),
            ('museumssummer', {
                'models': ('Location',),
            }),
            ('exhibitions', {
                'models': ('ExhibitionCategory','Exhibition',),
            }),
            ('events', {
                'models': ('EventCategory','Event',),
            }),
            ('workshops', {
                'models': ('WorkshopType', 'Workshop',),
            }),
            ('slideshows', {
                'models': ('Slideshow',),
            }),
            ('tips', {
                'models': ('TipOfTheDay',),
            }),
            ('internal_links', {
                'models': ('LinkGroup',),
            }),
            ('articles', {
                'models': ('ArticleCategory','Article',),
            }),
            ('blog', {
                'models': ('Blog','Post',),
            }),
            ('shop', {
                'models': ('ShopProductCategory','ShopProductType','ShopProduct',),
            }),
            ('mega_menu', {
                'models': ("MenuBlock",),
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
            ('accounts', {
                'verbose_name': gettext("Privacy Settings"),
                'models': ("PrivacySettings",),
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
                'models': ("Favorite",),
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
    },
    {
        'title': gettext('Control'),
        'apps': (
            ('tracker', {
                'models': ("Concern", "Ticket"),
            }),
        ),
    },
)

### CACHING ###

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'museumsportal',
    },
    'dummy': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'museumsportal_production_'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

### FILEBROWSER ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/filebrowser.py"))

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm','.swf','.flv','.f4v'],
    'Document': ['.pdf','.doc','.docx','.rtf','.txt',
        '.xls','.xlsx','.csv','.ppt','.pptx',
        ],
    'Audio': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css'],
    'Archive': ['.zip','.rar','.tar','.gz'],
}

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
}
FILEBROWSER_MEDIA_URL = UPLOADS_URL = "/media/"

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 2  # 2 MB

### MAILING ###

MAILING_DEFAULT_FROM_NAME = "Museumsportal Berlin"
MAILING_DEFAULT_FROM_EMAIL = "museumsportal@kulturprojekte-berlin.de"

MAILING_CONTENT_TYPE_CHOICES = (
    ('exhibitions', _("Exhibitions")),
    ('magazine', _("Magazine")),
    ('events', _("Events")),
    ('social', _("Social")),
    ('authorship', _("Image authorship")),
    #('image_and_text', _("Image and text")),
    #('text', _("Text only")),
)

### DEBUG TOOLBAR ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))

### GRAPPELLI ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/grappelli.py"))
GRAPPELLI_ADMIN_HEADLINE = "Museumsportal Berlin Admin"

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
        'URL': 'http://www.museumsportal-berlin.de/de/suche/',
    },
    'en': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "en"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/en/search/',
    },
    'fr': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "fr"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/fr/search/',
    },
    'pl': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "pl"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/pl/search/',
    },
    'tr': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "tr"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/tr/search/',
    },
    'es': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "es"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/es/search/',
    },
    'it': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "it"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/it/search/',
    },
}

HAYSTACK_ITERATOR_LOAD_PER_QUERY = 100
HAYSTACK_ROUTERS = ['museumsportal.apps.search.router.LanguageRouter']
ALDRYN_SEARCH_LANGUAGE_FROM_ALIAS = lambda alias: alias
ALDRYN_SEARCH_INDEX_BASE_CLASS = "museumsportal.apps.search.search_indexes.CMSPageIndexBase"  # custom index base for pages
ALDRYN_SEARCH_REGISTER_APPHOOK = False  # we'll use a custom app hook for search

### MULTILINGUAL URLS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/multilingual_urls.py"))

### OTHER SITE-SPECIFIC SETTINGS ###

APPEND_SLASH = True
PREPEND_WWW = False

TWITTER_USERNAME = "museumsportal"
TWITTER_NUMBER_OF_TWEETS = 4

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

NOTIFY_ABOUT_SEASONS_TO_EMAIL = "j.boehmler@kulturprojekte-berlin.de"

EDITORIAL_CONTENT_CSS_CLASSES = (
    # ('col-xs-1', 'item'),
    # ('col-xs-2', 'item'),
    # ('col-xs-3', 'item'),
    # ('col-xs-4', 'item'),
    # ('col-xs-5', 'item'),
    # ('col-xs-6', 'item'),
    # ('col-xs-7', 'item'),
    # ('col-xs-8', 'item'),
    # ('col-xs-9', 'item'),
    # ('col-xs-10', 'item'),
    # ('col-xs-11', 'item'),
    # ('col-xs-12', 'item'),

    # ('col-sm-1', 'item'),
    # ('col-sm-2', 'item'),
    # ('col-sm-3', 'item'),
    # ('col-sm-4', 'item'),
    # ('col-sm-5', 'item'),
    # ('col-sm-6', 'item'),
    # ('col-sm-7', 'item'),
    # ('col-sm-8', 'item'),
    # ('col-sm-9', 'item'),
    # ('col-sm-10', 'item'),
    # ('col-sm-11', 'item'),
    # ('col-sm-12', 'item'),

    # ('col-md-1', 'item'),
    # ('col-md-2', 'item'),
    # ('col-md-3', 'item'),
    # ('col-md-4', 'item'),
    # ('col-md-5', 'item'),
    # ('col-md-6', 'item'),
    # ('col-md-7', 'item'),
    # ('col-md-8', 'item'),
    # ('col-md-9', 'item'),
    # ('col-md-10', 'item'),
    # ('col-md-11', 'item'),
    # ('col-md-12', 'item'),

    # ('col-lg-1', 'item'),
    # ('col-lg-2', 'item'),
    # ('col-lg-3', 'item'),
    # ('col-lg-4', 'item'),
    # ('col-lg-5', 'item'),
    # ('col-lg-6', 'item'),
    # ('col-lg-7', 'item'),
    # ('col-lg-8', 'item'),
    # ('col-lg-9', 'item'),
    # ('col-lg-10', 'item'),
    # ('col-lg-11', 'item'),
    # ('col-lg-12', 'item'),
)

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
        {
            'code': 'fr',
            'hide_untranslated': True,
            'name': u'Français',
            'public': True,
            'redirect_on_fallback': False,
        },
        {
            'code': 'pl',
            'hide_untranslated': True,
            'name': u'Polski',
            'public': True,
            'redirect_on_fallback': False,
        },
        {
            'code': 'tr',
            'hide_untranslated': True,
            'name': u'Türkçe',
            'public': True,
            'redirect_on_fallback': False,
        },
        {
            'code': 'es',
            'hide_untranslated': True,
            'name': u'Español',
            'public': True,
            'redirect_on_fallback': False,
        },
        {
            'code': 'it',
            'hide_untranslated': True,
            'name': u'Italiano',
            'public': True,
            'redirect_on_fallback': False,
        },
    ]
}

CMS_TEMPLATES = [
    ('cms/default.html', gettext('Default')),
    ('cms/start.html', gettext('Homepage')),

    ('cms/plan_organize_first.html', gettext(u'Plan & Organize – First')),
    ('cms/plan_organize_second.html', gettext(u'Plan & Organize - Second')),              # previous: visitor_info.html
    ('cms/plan_organize_third.html', gettext(u'Plan & Organize - Third')),              # previous: visitor_info.html

    ('cms/magazine_first.html', gettext(u'Magazine – First')),
    ('cms/magazine_first_with_ad.html', gettext(u'Magazine – First with ad')),
    ('cms/magazine_second.html', gettext(u'Magazine – Second')),                   # previous: series.html
    ('cms/magazine_second_featured.html', gettext(u'Magazine – Second - Featured')), # previous: series_with_featured.html
    ('cms/magazine_third.html', gettext(u'Magazine - Third')),
    ('cms/magazine_special_event.html', gettext(u'Magazine – Special Event')),

    ('cms/museumssummer_first.html', gettext(u'Museums Summer – First')),
    ('cms/museumssummer_second.html', gettext(u'Museums Summer – Second')),
    ('cms/museumssummer_second_featured.html', gettext(u'Museums Summer – Second - Featured')),
    ('cms/museumssummer_third.html', gettext(u'Museums Summer - Third')),
    ('cms/museumssummer_special_event.html', gettext(u'Museums Summer – Special Event')),

    ('cms/shop_overview.html', gettext(u'Shop – Overview')),
    ('cms/shop_first.html', gettext(u'Shop – First')),

    ('cms/dashboard_default.html', gettext('Dashboard Default')),
]

# Customized placeholders
CMS_PLACEHOLDER_CONF = {
    'typehead': {
        'plugins': ("RichTextPlugin", "HeadlinePlugin"),
        'name': _("Typehead")
    },

    'top_image': {
        'plugins': ("FilebrowserImagePlugin",),
        'name': _("Top Image")
    },

    'intro': {
        'plugins': ("IntroPlugin","FilebrowserImagePlugin"),
        'name': _("Intro")
    },

    'main_content': {
        'plugins': ("EditorialContentPlugin","RichTextPlugin", "FilebrowserImagePlugin", "GMapPlugin", "ArticleSelectionPlugin", "FootnotePlugin"),
        'name': _("Main Content")
    },

    'ad': {
        'plugins': ("AdZonePlugin"),
        'name': _("Ad"),
    },

    'footnotes': {
        'plugins': ("RichTextPlugin",),
        'name': _("Footnotes")
    },

    'editorial_notices': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("editorial notices")
    },

    'plan_organize_first': {
        'plugins': ("EditorialContentPlugin", "AdZonePlugin"),
        'name': _("Plan & Organize - First"),
    },

    'series_items_featured': {
        'plugins': ("EditorialContentPlugin", "AdZonePlugin"),
        'name': _("Series Items Featured")
    },

    'series_items': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("Series Items")
    },

    'jewish_museum': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("Jewish Museum")
    },

    'series_exhibitions': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("Series Exhibitions")
    },

    'series_images': {
        'plugins': ("RichTextPlugin",),
        'name': _("Series Images")
    },

    'start_page_content': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("Start Page Content")
    },

    'left_column': {
        'plugins': ("EditorialContentPlugin","NewlyOpenedExhibitionPlugin","NewlyOpenedExhibitionExtPlugin",),
        'name': _("Left Column")
    },

    'center_column': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("Center Column")
    },

    'right_column': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("Right Column")
    },

    'featured_magazin': {
        'plugins': ("EditorialContentPlugin",),
        'name': _("Featured Magazin")
    },

    'start_page_left': {
        'plugins': ("EditorialContentPlugin", "FrontpageTeaserPlugin",),
        'name': _("Start page left")
    },
    'start_page_center': {
        'plugins': ("EditorialContentPlugin", "FrontpageTeaserPlugin",),
        'name': _("Start page center")
    },
    'start_page_right': {
        'plugins': ("EditorialContentPlugin", "FrontpageTeaserPlugin",),
        'name': _("Start page right")
    },
}

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
    'dsn': 'http://ac6037beb199460a9fe190c75dac8074:8fc8ca56432b4ac28e5670b80ab3e426@46.101.101.159/5',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.path.dirname(__file__))),
}

### API KEYS ###

GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY")
