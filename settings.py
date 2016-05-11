# -*- coding: utf-8 -*-

# Django settings for museumsportal project.
import os
_ = gettext = lambda s: s

JETSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

execfile(os.path.join(JETSON_PATH, "jetson/settings/base.py"), globals(), locals())

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ("Museumsportal Berlin Webmaster", "bendoraitis@studio38.de"),
    ("Reinhard Knobelspies", "knobelspies@studio38.de"),
)

DEFAULT_FROM_EMAIL = 'museumsportal@kulturprojekte-berlin.de'
MANAGERS = (
    ("Museumsportal Berlin Webmaster", "museumsportal@kulturprojekte-berlin.de"),
)

TIME_ZONE = 'Europe/Berlin'

### LANGUAGES ###
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

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

LANGUAGE_CODE = "de"

SITE_ID = 1
USE_I18N = True
USE_L10N = False # --> no commas in float values for latitude and longitude

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "museumsportal", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "museumsportal", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = PIPELINE_URL = "/static/%s/" % get_git_changeset(os.path.join(PROJECT_PATH, "museumsportal"))

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/%s/admin/' % get_git_changeset(os.path.join(PROJECT_PATH, "museumsportal"))

# Additional locations of static files
STATICFILES_DIRS = [os.path.join(PROJECT_PATH, "museumsportal", "site_static")]
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

#Settings for uploaded images
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 2  # 2 MB


TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS = [
    os.path.join(PROJECT_PATH, "museumsportal", "templates", "museumsportal"),
    os.path.join(PROJECT_PATH, "museumsportal", "templates", "admin"),
] + TEMPLATE_DIRS

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, "museumsportal", "locale"),
)

PATH_TMP = os.path.join(PROJECT_PATH, "museumsportal", "tmp")
CSS_URL = "%scss/default/" % MEDIA_URL
IMG_URL = "%simg/website/" % MEDIA_URL
FILE_UPLOAD_TEMP_DIR = SESSION_FILE_PATH = PATH_TMP
FILE_UPLOAD_PERMISSIONS == 0777

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n%!wr5^+wx6h9*1*rki^1museumsportal4o1@_%$a)8z4w7sf^s-(9d+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'jetson.apps.httpstate.middleware.HttpStateMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'base_libs.middleware.threadlocals.ThreadLocalsMiddleware',
    #"cms.middleware.multilingual.MultilingualURLMiddleware",
    #"jetson.apps.cms_extensions.middleware.MultilingualURLMiddleware",
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'jetson.apps.mobile_detection.middleware.MobileDetectionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'museumsportal.urls'

INSTALLED_APPS = (
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
    "jetson.apps.cms_extensions",
    "jetson.apps.cms_extensions.plugins.richtext",
    "jetson.apps.cms_extensions.plugins.filebrowser_image",
    "jetson.apps.cms_extensions.plugins.gmap",
    "jetson.apps.cms_extensions.plugins.headline",
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
)


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

PREPEND_WWW = False

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

### CMS SETTINGS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/cms.py"), globals(), locals())

# CMS_LANGUAGES = (
#     ('de', 'Deutsch'),
#     ('en', 'English'),
# )
# CMS_HIDE_UNTRANSLATED = True
# CMS_LANGUAGE_FALLBACK = "de"
# CMS_LANGUAGE_CONF = {
#     'de':['en'],
# }
# CMS_FRONTEND_LANGUAGES = ("en", "de")

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

    ('cms/shop_overview.html', gettext(u'Shop – Overview')),
    ('cms/shop_first.html', gettext(u'Shop – First')),

    ('cms/dashboard_default.html', gettext('Dashboard Default')),
]

# UPDATE cms_page SET template = REPLACE(template,'cms/magazine_overview.html','cms/magazine_first.html');
# UPDATE cms_page SET template = REPLACE(template,'cms/magazine_series.html','cms/magazine_second.html');
# UPDATE cms_page SET template = REPLACE(template,'cms/magazine_series_featured.html','cms/magazine_second_featured.html');
# UPDATE cms_page SET template = REPLACE(template,'cms/magazine.html','cms/magazine_third.html');

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

### FILEBROWSER ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/filebrowser.py"), globals(), locals())

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

### DEBUG TOOLBAR ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))

### GRAPPELLI ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/grappelli.py"))
GRAPPELLI_ADMIN_HEADLINE = "Museumsportal Berlin Admin"

### HAYSTACK ###

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "default"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
    'de': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "de"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/de/suche/',
    },
    'en': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "en"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/en/search/',
    },
    'fr': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "fr"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/fr/search/',
    },
    'pl': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "pl"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/pl/search/',
    },
    'tr': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "tr"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/tr/search/',
    },
    'es': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "es"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/es/search/',
    },
    'it': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PATH_TMP, "whoosh_index", "it"),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'URL': 'http://www.museumsportal-berlin.de/it/search/',
    },
}

HAYSTACK_ROUTERS = ['museumsportal.apps.search.router.LanguageRouter']
ALDRYN_SEARCH_LANGUAGE_FROM_ALIAS = lambda alias: alias
ALDRYN_SEARCH_INDEX_BASE_CLASS = "museumsportal.apps.search.search_indexes.CMSPageIndexBase"  # custom index base for pages
ALDRYN_SEARCH_REGISTER_APPHOOK = False  # we'll use a custom app hook for search

### OTHER SETTINGS ###

ARTICLES_HAVE_TYPES = False

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

NOTIFY_ABOUT_SEASONS_TO_EMAIL = "j.boehmler@kulturprojekte-berlin.de"

CRISPY_TEMPLATE_PACK = "bootstrap3"

ALLOWED_HOSTS = ['www.museumsportal-berlin.de', 'museumsportal-berlin.de']

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

MAILING_CONTENT_TYPE_CHOICES = (
    ('exhibitions', _("Exhibitions")),
    ('magazine', _("Magazine")),
    ('events', _("Events")),
    ('social', _("Social")),
    ('authorship', _("Image authorship")),
    #('image_and_text', _("Image and text")),
    #('text', _("Text only")),
)

ROSETTA_STORAGE_CLASS = "rosetta.storage.SessionRosettaStorage"

USE_TZ = True

DISABLE_CONTEXT_PROCESSORS = True

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
    'dsn': 'http://ac6037beb199460a9fe190c75dac8074:8fc8ca56432b4ac28e5670b80ab3e426@sentry.jetsonproject.org/5',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}

### LOCAL SETTINGS ###

try:
    execfile(os.path.join(os.path.dirname(__file__), "local_settings.py"))
except IOError:
    pass
