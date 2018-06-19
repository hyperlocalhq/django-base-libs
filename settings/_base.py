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
JETSON_PATH = os.path.abspath(os.path.join(BASE_DIR, "ccb", "subtrees"))
PROJECT_PATH = BASE_DIR

execfile(os.path.join(JETSON_PATH, "jetson/settings/base.py"), globals(), locals())

### DOMAINS ###

SESSION_COOKIE_DOMAIN = "www.creative-city-berlin.de"
STAGING_DOMAIN = "ccb.jetsonproject.org"

### EMAILS ###

MANAGERS = (
    ("Creative City Berlin", "ccb-contact@kulturprojekte-berlin.de"),
)

ADMINS = (
    ("Aidas Bendoraitis", "bendoraitis@studio38.de"),
    ("Tiago Henriques", "henriques@studio38.de"),
    ("Reinhard Knobelspies", "knobelspies@studio38.de"),
)

CONTENT_ADMINS = (
    ("Creative City Berlin", "ccb-contact@kulturprojekte-berlin.de"),
)

DEFAULT_FROM_EMAIL = "ccb-contact@kulturprojekte-berlin.de"


### DIRS AND URLS ###

MEDIA_ROOT = os.path.join(PROJECT_PATH, "ccb", "media")
STATIC_ROOT = os.path.join(PROJECT_PATH, "ccb", "static")
STATICFILES_DIRS = [os.path.join(PROJECT_PATH, "ccb", "site_static")]
MEDIA_URL = "/media/"
STATIC_URL = PIPELINE_URL = "/static/%s/" % get_git_changeset(STATIC_ROOT)
PATH_TMP = os.path.join(PROJECT_PATH, "ccb", "tmp")
CSS_URL = "%scss/default/" % MEDIA_URL
IMG_URL = "%simg/website/" % MEDIA_URL
FILE_UPLOAD_TEMP_DIR = SESSION_FILE_PATH = PATH_TMP
FILE_UPLOAD_PERMISSIONS = 0777

LOCALE_PATHS = [
    os.path.join(PROJECT_PATH, "ccb", "locale"),
    os.path.join(JETSON_PATH, "jetson", "locale"),
]

### LANGUAGES ###

LANGUAGES = (
    ("en", gettext("English")),
    ("de", gettext("German")),
)

OPEN_GRAPH_LOCALE_MAPPER = {
    'de': 'de_DE',
    'en': 'en_US',
}

LANGUAGE_CODE = "de"


### MAIN ###

INSTALLED_APPS = [
    ### third-party apps ###
    "crispy_forms",
    "filebrowser",
    "grappelli",

    ### django core apps ###
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.redirects",
    "ccb.project_apps.DjangoContribAuthConfig",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.messages",

    ### more third-party apps ###
    "babeldjango",
    "tagging",
    "tagging_autocomplete",
    "rosetta",
    "haystack",
    "uni_form",
    "mptt",
    "picklefield",
    "captcha",
    "social_django",
    "bootstrap_pagination",
    "raven.contrib.django.raven_compat",
    "ckeditor",
    "ckeditor_uploader",

    ### django-cms ###
    "cms",  # django CMS itself
    "treebeard",  # utilities for implementing a tree
    "menus",  # helper for model independent hierarchical website navigation
    "sekizai",  # for javascript and css management
    # for the admin skin. You **must** add "djangocms_admin_style" in the list **before** "django.contrib.admin".
    "reversion",
    "aldryn_search",

    ### django-cms plug-ins ###
    #"djangocms_column",
    #"djangocms_file",
    "djangocms_flash",
    #"djangocms_inherit",
    "djangocms_link",
    #"djangocms_style",
    #"djangocms_teaser",
    #"djangocms_video",

    ### plug-ins for django-cms ###
    "ccb.apps.cms_extensions.plugins.richtext",
    "ccb.apps.cms_extensions.plugins.filebrowser_image",
    "ccb.apps.cms_extensions.plugins.gmap",
    "ccb.apps.cms_extensions.plugins.headline",
    "ccb.apps.editorial",

    ### jetson apps ###
    "jetson.apps.image_mods",
    "jetson.apps.httpstate",
    "jetson.apps.i18n",
    "jetson.apps.location",
    "jetson.apps.utils",
    "jetson.apps.permissions",
    "jetson.apps.blocks",
    "jetson.apps.flatpages",
    "jetson.apps.optionset",
    "jetson.apps.individual_relations",
    "jetson.apps.structure",
    "jetson.apps.extendedadmin",
    "jetson.apps.history",
    "jetson.apps.memos",
    "jetson.apps.notification",
    "jetson.apps.mailing",
    "jetson.apps.contact_form",
    "jetson.apps.configuration",
    "jetson.apps.bookmarks",
    "jetson.apps.profanity_filter",
    "jetson.apps.messaging",
    "jetson.apps.comments",
    "jetson.apps.mailchimp",

    ### ccb-specific apps ###
    "ccb.apps.blog",
    "ccb.apps.people",
    "ccb.apps.institutions",
    "ccb.apps.resources",
    "ccb.apps.events",
    "ccb.apps.groups_networks",
    "ccb.apps.marketplace",
    "ccb.apps.site_specific",
    "ccb.apps.articles",
    "ccb.apps.tracker",
    "ccb.apps.search",
    "ccb.apps.favorites",
    "ccb.apps.external_services",
    "ccb.apps.media_gallery",
    "ccb.apps.slideshows",
    "ccb.apps.faqs",
    "ccb.apps.async_test",
    "ccb.apps.accounts",
    "ccb.apps.network",
    "ccb.apps.navigation",
    "ccb.apps.bulletin_board",
    "ccb.apps.metro",
    "ccb.apps.partners",
    "ccb.apps.counselling_blog",
    "ccb.apps.counselling_events",
    "ccb.apps.curated_lists",
    "ccb.apps.cms_extensions",
    "ccb.apps.logins",
    "ccb.apps.recommendations",
    "ccb",  # just for i18n in Javascript
    "actstream",
    "huey.contrib.djhuey",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "jetson.apps.httpstate.middleware.HttpStateMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "babeldjango.middleware.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "base_libs.middleware.threadlocals.ThreadLocalsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "jetson.apps.utils.middleware.generic.AdminScriptUpdateMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    "ccb.apps.accounts.middleware.MySocialAuthExceptionMiddleware",
    "base_libs.middleware.traceback.UserTracebackMiddleware",
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, "ccb", "templates", "ccb"),
            os.path.join(PROJECT_PATH, "ccb", "templates", "admin"),
            os.path.join(JETSON_PATH, "jetson", "templates", "default"),
            os.path.join(JETSON_PATH, "jetson", "templates", "admin"),
            os.path.join(JETSON_PATH, "jetson", "externals", "apps", "grappelli", "templates", "grappelli"),
            os.path.join(JETSON_PATH, "jetson", "externals", "apps", "grappelli", "templates"),
        ],
        'OPTIONS': {
            'context_processors': (
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.i18n",
                "django.core.context_processors.request",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
                "jetson.apps.configuration.context_processors.configuration",
                "jetson.apps.utils.context_processors.general",
                "ccb.apps.media_gallery.context_processors.media_gallery",
                "ccb.apps.people.context_processors.people",
                "ccb.apps.institutions.context_processors.institutions",
                "ccb.apps.events.context_processors.events",
                "ccb.apps.groups_networks.context_processors.groups_networks",
                "ccb.apps.marketplace.context_processors.marketplace",
                "ccb.apps.site_specific.context_processors.site_specific",
                "social.apps.django_app.context_processors.backends",
                "social.apps.django_app.context_processors.login_redirect",
            ),
            'loaders': [
                #"base_libs.template.loaders.cached.Loader", # TODO: Do we still need this one? Delete from the base_libs if not.
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        }
    },
]


SECRET_KEY = get_secret("SECRET_KEY")

# ROOT_URLCONF = "urls" # TODO: figure out if this would work
ROOT_URLCONF = "ccb.urls"

### ADMIN ###

ADMIN_APP_INDEX = (
    {
        "title": _("Content"),
        "apps": (
            ("cms", {
                "models": ("Page",),
            }),
            ("events", {
                "models": ("EventType", "EventTimeLabel", "Event",),
                "icon": "date",
            }),
            ("articles", {
                "models": ("ArticleContentProvider", "ArticleType", "Article",),
                "icon": "page_white_text",
            }),
            ("blog", {
                "models": ("Blog", "Post"),
                "icon": "page_white_edit",
            }),
            ("blocks", {
                "models": ("InfoBlock",),
                "icon": "brick",
            }),
            ("media_gallery", {
                "models": ("PortfolioSettings", "Section", "MediaGallery",),
                "icon": "images",
            }),
            ("slideshows", {
                "models": ("Slideshow",),
                "icon": "images",
            }),
            ("metro", {
                "models": ("Tile",),
                "icon": "images",
            }),
            ("recommendations", {
                "models": ("Recommendation",),
            }),
            ("partners", {
                "models": ("PartnerCategory",),
                "icon": "images",
            }),
            ("curated_lists", {
                "models": ("CuratedList",),
            }),
        )
    }, {
        "title": _("Community"),
        "apps": (
            ("people", {
                "models": ("IndividualType", "Person",),
                "icon": "user",
            }),
            ("institutions", {
                "models": ("LegalForm", "InstitutionType", "Institution",),
                "icon": "building",
            }),
            ("marketplace", {
                "models": ("JobOffer", "JobSector", "JobType", "JobQualification",),
                "icon": "page_white",
            }),
            ("bulletin_board", {
                "models": ("BulletinContentProvider", "BulletinCategory", "Bulletin",),
                "icon": "page_white",
            }),
            ("auth", {
                "verbose_name": _("Authentication & Authorization"),
                "models": ("Group", "User"),
                "icon": "key",
            }),
            ("individual_relations", {
                "models": ("IndividualRelationType", "IndividualRelation",),
            }),
            ("favorites", {
                "models": ("Favorite",),
                "icon": "heart",
            }),
            ("bookmarks", {
                "models": ("Bookmark",),
                "icon": "flag_red",
            }),
            ("memos", {
                "models": ("MemoCollection",),
                "icon": "note",
            }),
            ("groups_networks", {
                "models": ("GroupType", "PersonGroup", "GroupMembership"),
                "icon": "group",
            }),
        )
    }, {
        "title": _("Commerce"),
        "apps": ()
    }, {
        "title": _("Campaign"),
        "apps": (
            ("mailing", {
                "models": ("EmailMessage", "EmailTemplate", "EmailTemplatePlaceholder",),
                "icon": "email",
            }),
            ("messaging", {
                "models": ("InternalMessage",),
            }),
            ("mailchimp", {
                "models": ("Settings", "MList", "Campaign",),
                "icon": "transmit",
            }),
        )
    }, {
        "title": _("Configure"),
        "apps": (
            ("navigation", {
                "models": ("NavigationLink",),
            }),
            ("structure", {
                "models": ("Vocabulary", "Term", "ContextCategory", "Category"),
            }),
            ("image_mods", {
                "verbose_name": _("Media"),
                "models": ("ImageModificationGroup", "ImageModification", "ImageCropping",),
            }),
            ("contact_form", {
                "models": ("ContactFormCategory",),
            }),
            ("sites", {
                "verbose_name": _("Sites"),
                "models": ("Site",),
            }),
            ("configuration", {
                "models": ("SiteSettings",),
            }),
            ("redirects", {
                "verbose_name": _("Redirects"),
                "models": ("Redirect",),
            }),
            ("i18n", {
                "models": ("Country", "Area", "Language", "CountryLanguage", "Phone", "Nationality", "TimeZone"),
            }),
            ("optionset", {
                "models": (
                    "Prefix", "Salutation", "IndividualLocationType", "InstitutionalLocationType", "PhoneType",
                    "EmailType",
                    "URLType", "IMType"),
            }),
        )
    }, {
        "title": _("Connect"),
        "apps": (
            ("external_services", {
                "models": ("Service", "ArticleImportSource", "ServiceActionLog", "ObjectMapper"),
            }),
        )
    }, {
        "title": _("Control"),
        "apps": (
            ("logins", {
                "verbose_name": _("Logins"),
                "models": ("LoginAction", "WelcomeMessage")
            }),
            ("comments", {
                "verbose_name": _("Comments"),
                "models": ("Comment", "ModeratorDeletion", "ModeratorDeletionReason",)
            }),
            ("profanity_filter", {
                "models": ("SwearWord", "SwearingCase",),
            }),
            ("site_specific", {
                "models": ("ClaimRequest", "Visit", "ContextItem"),
            }),
            ("tracker", {
                "models": ("Concern", "Ticket",),
            }),
            ("grappelli", {
                "models": ("Bookmark", "Navigation", "Help", "HelpItem",),
            }),
            ("notification", {
                "models": (
                    "NoticeTypeCategory",
                    "NoticeType",
                    "NoticeEmailTemplate",
                    "Notice",
                    "Digest",
                    "DigestNotice",
                    "NoticeSetting",
                    "ObservedItem",
                ),
            }),
            ("location", {
                "models": ("Address", "LocalityType",),
            }),
            ("actstream", {
                "models": ("Action", "Follow",),
            }),
        )
    }
)


### CACHING ###

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
        "LOCATION": "127.0.0.1:11211",
        "KEY_PREFIX": "ccb_production_",
        "TIMEOUT": 3000,
        "MAX_ENTRIES": 400,
    }
}

CACHE_MIDDLEWARE_KEY_PREFIX = "ccb_production_"

### FILEBROWSER ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/filebrowser.py"))

FILEBROWSER_VERSIONS = {
    "fb_thumb": {"verbose_name": "Admin Thumbnail", "width": 60, "height": 60, "opts": "crop upscale"},
    "nd": {"verbose_name": "News Default (163px)", "width": 163, "height": 156, "opts": "crop upscale"},
    "nt": {"verbose_name": "News Thumbnail (75px)", "width": 163, "height": 100, "opts": "crop upscale"},
}
FILEBROWSER_ADMIN_VERSIONS = ["nd", "nt"]
FILEBROWSER_MEDIA_URL = UPLOADS_URL = "/media/"
FILEBROWSER_STRICT_PIL = True

### SEARCH ###

SPHINX_SERVER = "localhost"  # Sphinx server address, default is localhost
SPHINX_PORT = 3312  # Sphinx server port, default is 3312

SEARCH_ENGINE = "MySqlFulltext"  # one of these: "MySqlFulltext", "Proprietary", "Sphinx"


### MAILING ###

MAILING_DEFAULT_FROM_NAME = "Creative City Berlin"
MAILING_DEFAULT_FROM_EMAIL = "ccb-contact@kulturprojekte-berlin.de"


### GRAPPELLI ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/grappelli.py"))
GRAPPELLI_ADMIN_HEADLINE = "Creative City Admin"

GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    "auth": {
        "user": ("id__iexact", "username__icontains", "first_name__icontains", "last_name__icontains", "email__icontains",)
    }
}

### PROFANITY FILTER ###

PROFANITY_DO_REPLACE = False
PROFANITY_MODELS_NOT_TO_CHECK = (
    "admin.LogEntry",
    "auth.Message",
    "contenttypes.ContentType",
    "notification.LogEntry",
    "history.ExtendedLogEntry",
    "configuration.SiteSettings",
    "configuration.PageSettings",
    "permissions.RowLevelPermission",
    "permissions.PerObjectGroup",
    "structure.Vocabulary",
    "structure.Term",
    "structure.ContextCategory",
    "navigation.NavigationLink",
    "tagging.Tag",
    "site_specific.ContextItem",
    "mailchimp.Campaign",
    "mailchimp.MailingContentBlock",
    "mailchimp.Settings",
    "mailchimp.MList",
)

### HAYSTACK ###

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(PATH_TMP, "whoosh_index", "default"),
        "STORAGE": "file",
        "POST_LIMIT": 128 * 1024 * 1024,
        "INCLUDE_SPELLING": False,
        "BATCH_SIZE": 100,
    },
    "de": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(PATH_TMP, "whoosh_index", "de"),
        "STORAGE": "file",
        "POST_LIMIT": 128 * 1024 * 1024,
        "INCLUDE_SPELLING": False,
        "BATCH_SIZE": 100,
        "URL": "http://www.creative-city-berlin.de/de/search/",
    },
    "en": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(PATH_TMP, "whoosh_index", "en"),
        "STORAGE": "file",
        "POST_LIMIT": 128 * 1024 * 1024,
        "INCLUDE_SPELLING": False,
        "BATCH_SIZE": 100,
        "URL": "http://www.creative-city-berlin.de/en/search/",
    },
}

HAYSTACK_ITERATOR_LOAD_PER_QUERY = 100
HAYSTACK_ROUTERS = ["ccb.apps.search.router.LanguageRouter"]
ALDRYN_SEARCH_LANGUAGE_FROM_ALIAS = lambda alias: alias
ALDRYN_SEARCH_INDEX_BASE_CLASS = "ccb.apps.search.search_indexes.CMSPageIndexBase"  # custom index base for pages
ALDRYN_SEARCH_REGISTER_APPHOOK = False  # we"ll use a custom app hook for search
#ALDRYN_SEARCH_CMS_PAGE = False

### MULTILINGUAL URLS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/multilingual_urls.py"))


### OTHER SITE-SPECIFIC SETTINGS ###

APPEND_SLASH = True

THIRD_PARTY_EMAILS = {
    "kulturmanagement.net": "jobs@kulturmanagement.net",
}

CREATIVESET_COMPANY_ID = 632
CREATIVESET_KEY_COMPONENT = "46ea64b3b8cfa113d9bd5e131d598abac171205e"

MEMO_COOKIE_AGE = timedelta(days=365)

# list of urls to prevent from automatic httpstate cleaning
OTHER_URLS_LEAVE_AS_IS = (
    "/logo_contest/",
    "/recrop/",
)

# TODO: crystallize the definitions of MIN and MAX sizes for uploaded images

IMAGE_MAX_SIZE = "850x1700"
IMAGE_PREVIEW_MAX_SIZE = "850x1700"
IMAGE_SMALL_SIZE = "850x1700"

MIN_LOGO_SIZE = (75, 75)
LOGO_SIZE = (270, 281)
LOGO_PREVIEW_SIZE = "270x281"
LOGO_SMALL_SIZE = "50x50"

PATHS_NO_REDIRECTION = (
    "/tagging_autocomplete/",
    "/helper/",
    "/admin/",
    "/recrop/",
    "/grappelli/",
    JETSON_MEDIA_URL,
    STATIC_URL,
    MEDIA_URL,
    ADMIN_MEDIA_PREFIX,
)

TWITTER_USERNAME = "CREATIVEBERLIN"
TWITTER_NUMBER_OF_TWEETS = 3

TWITTER_CONSUMER_KEY = "J1AlfzI5QuW3HOUF9fiU8Q"
TWITTER_CONSUMER_SECRET = "VkIF6bZMLBGHqv8bguK2pmr5Rg1HNK7OuJBx4uGzRgo"
TWITTER_ACCESS_TOKEN = "21031007-meNXTMlI5yPA7KGU3eiYUsfaVOYWAo0FiJB0alpxX"
TWITTER_ACCESS_TOKEN_SECRET = "mOg8VE4SdCseexvdqjOKdWc0dJe6ALbWA89nLsdIMLk"

MAILING_CONTENT_TYPE_CHOICES = (
    ("image_and_text", _("Image and text")),
    ("text", _("Text only")),
    ("news", _("News")),
    ("tenders_and_compet", _("Tenders and Competitions")),
    ("events", _("Events")),
    ("portfolios", _("Portfolios")),
    ("interviews", _("Magazine")),
    ("jobs_and_bulletins", _("Jobs and Bulletins")),
    ("people", _("Profiles")),
)

TIME_INPUT_FORMATS = ("%H:%M:%S", "%H:%M", "%H.%M")

DISABLE_CONTEXT_PROCESSORS = True

RECOMMENDATIONS_WIDGET_TEMPLATE_CHOICES = (
    ('people/includes/latest_published_people_start.html', _("Latest Profiles")),
    ('bulletin_board/includes/latest_bulletins.html', _("Latest Bulletins")),
    ('articles/includes/latest_news_of_the_category.html', _("Latest News of the Category")),
)


### CAPTCHA ###

RECAPTCHA_PUBLIC_KEY = "6LfWkt8SAAAAAPnRowSBDg1GJOk6umAqdwVcpUFK"
RECAPTCHA_PRIVATE_KEY = "6LfWkt8SAAAAABAOx3-qsJYDt76jSpUlIkg8ZgcD"
RECAPTCHA_USE_SSL = False

RECAPTCHA_SITE_KEY = "6LdUIhUTAAAAAPzqpanSC53BVXrkLzPNZ9_ItKKn"
RECAPTCHA_SECRET_KEY = "6LdUIhUTAAAAAEuAAai-3CZp3cEevEiSWBvkSWM4"

### DJANGO CRISPY FORMS ###

CRISPY_TEMPLATE_PACK = "bootstrap3"
CRISPY_ALLOWED_TEMPLATE_PACKS = ("bootstrap3", "ccb_form")

### DJANGO CMS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/cms.py"), globals(), locals())

CMS_TEMPLATES = (
    ("cms/start.html", "Start Page"),
    ("cms/page.html", "Page"),
    ("cms/page_sidebar.html", "Page with Sidebar"),
    ("cms/page_sidebar_under_architecture.html", "Page with Sidebar - Architecture"),
    ("cms/page_sidebar_under_visual_arts.html", "Page with Sidebar - Visual Arts"),
    ("cms/page_sidebar_under_design.html", "Page with Sidebar - Design"),
    ("cms/page_sidebar_under_event_industry.html", "Page with Sidebar - Event Industry"),
    ("cms/page_sidebar_under_film_broadcast.html", "Page with Sidebar - Film & Broadcast"),
    ("cms/page_sidebar_under_photography.html", "Page with Sidebar - Photography"),
    ("cms/page_sidebar_under_games_interactive.html", "Page with Sidebar - Games & Interactive"),
    ("cms/page_sidebar_under_literature_publishing.html", "Page with Sidebar - Literature & Publishing"),
    ("cms/page_sidebar_under_fashion_textile.html", "Page with Sidebar - Fashion & Textile"),
    ("cms/page_sidebar_under_music.html", "Page with Sidebar - Music"),
    ("cms/page_sidebar_under_theatre_dance.html", "Page with Sidebar - Theatre & Dance"),
    ("cms/page_sidebar_under_advertising_pr.html", "Page with Sidebar - Advertising & PR"),

    ("cms/start_counselling.html", "Start Page Counselling"),
    ("cms/page_counselling.html", "Page Counselling"),
    ("cms/page_sidebar_counselling.html", "Page Counselling with Sidebar"),
)

CMS_LANGUAGES = {
    "default": {
        "public": True,
        "hide_untranslated": False,
        "redirect_on_fallback": True,
    },
    1: [
        {
            "public": True,
            "code": "de",
            "hide_untranslated": False,
            "name": gettext("de"),
            "redirect_on_fallback": True,
        },
        {
            "public": True,
            "code": "en",
            "hide_untranslated": False,
            "name": gettext("en"),
            "redirect_on_fallback": True,
        },
    ],
}

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

MIGRATION_MODULES = {
    "cms": "cms.migrations",
    "menus": "menus.migrations",

    # Add also the following modules if you"re using these plugins:
    #"djangocms_file": "djangocms_file.migrations_django",
    "djangocms_flash": "djangocms_flash.migrations_django",
    "djangocms_googlemap": "djangocms_googlemap.migrations_django",
    #"djangocms_inherit": "djangocms_inherit.migrations_django",
    "djangocms_link": "djangocms_link.migrations_django",
    "djangocms_picture": "djangocms_picture.migrations_django",
    "djangocms_snippet": "djangocms_snippet.migrations_django",
    #"djangocms_teaser": "djangocms_teaser.migrations_django",
    #"djangocms_video": "djangocms_video.migrations_django",
    #"djangocms_style": "djangocms_style.migrations_django",
    #"djangocms_column": "djangocms_column.migrations_django",
}

### PERSISTENT DATABASE CONNECTIONS ###

CONN_MAX_AGE = 600

### SOCIAL AUTHENTICATION ###

AUTHENTICATION_BACKENDS = (
    "social_core.backends.facebook.FacebookOAuth2",
    "jetson.apps.permissions.backends.RowLevelPermissionsBackend",
    "jetson.apps.utils.backends.EmailBackend",
    "social_core.backends.username.UsernameAuth",
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_USER_MODEL = "auth.User"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "dashboard"
URL_PATH = ""
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile"
]
SOCIAL_AUTH_USERNAME_FORM_HTML = "username_signup.html"


SOCIAL_AUTH_FACEBOOK_KEY = FACEBOOK_APP_ID = get_secret("FACEBOOK_APP_ID")
SOCIAL_AUTH_FACEBOOK_SECRET = FACEBOOK_APP_SECRET = get_secret("FACEBOOK_APP_SECRET")
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  "fields": "id, name, email, first_name, last_name",
}

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "ccb.apps.accounts.pipeline.login_or_registration",
    "ccb.apps.accounts.pipeline.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    "social_core.pipeline.disconnect.get_entries",
    "social_core.pipeline.disconnect.revoke_tokens",
    "social_core.pipeline.disconnect.disconnect"
)

### DJANGO ACTIVITY STREAM ###

ACTSTREAM_SETTINGS = {
    "MANAGER": "actstream.managers.ActionManager",
    "FETCH_RELATIONS": True,
    "USE_PREFETCH": True,
    "USE_JSONFIELD": False,
    "GFK_FETCH_DEPTH": 1,
}

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
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
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
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
        },
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
    'dsn': 'http://ffc5ae7c26dd49ed8f14ca113cb0f7de:29e74466fdaa4af7a245f7a3eae16543@46.101.101.159/2',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.path.dirname(__file__))),
}

### API KEYS ###

GOOGLE_API_KEY = "AIzaSyDWz29t8VlkHoR6e5rYg8So98_SfPhMfCc"

HUEY = {
    'name': "ccb",  # Use db name for huey.
    'result_store': True,  # Store return values of tasks.
    'events': True,  # Consumer emits events allowing real-time monitoring.
    'store_none': False,  # If a task returns None, do not save to results.
    # 'always_eager': DEBUG,  # If DEBUG=True, run synchronously.
    'always_eager': False,
    'store_errors': True,  # Store error info if task throws exception.
    'blocking': False,  # Poll the queue rather than do blocking pop.
    'connection': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'connection_pool': None,  # Definitely you should use pooling!
        # ... tons of other options, see redis-py for details.

        # huey-specific connection parameters.
        'read_timeout': 1,  # If not polling (blocking pop), use timeout.
        'max_errors': 1000,  # Only store the 1000 most recent errors.
    },
    'consumer': {
        'workers': 1,
        'worker_type': 'thread',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'utc': True,  # Treat ETAs and schedules as UTC datetimes.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
    },
}

### PLACEHOLDER PATHS ###
# TODO: eliminate as they are probably outdated

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

## CKEDITOR
CKEDITOR_UPLOAD_PATH = "user-uploads/"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_RESTRICT_BY_DATE = False
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_BROWSE_SHOW_DIRS = False

CKEDITOR_CONFIGS = {
    'basic': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            [
                #'Format', '-',
                'Bold', 'Italic', '-',
                'BulletedList', 'NumberedList', '-',
                #'BulletedList', 'NumberedList', 'Blockquote', '-',
                'Link', 'Unlink', '-',
                'Image', 'oembed',
             ]
        ],
        #'format_tags': 'p;h2;h4;h5',
        'removeDialogTabs': 'link:advanced;link:target;image:Link;image:advanced',
        'extraPlugins': 'oembed,widget',
        'oembed_maxWidth': '560',
        'oembed_maxHeight': '315',
        'oembed_WrapperClass': 'embededContent',
        'allowedContent': True,
        'width': '',
        'removePlugins': "elementspath",
        'contentsCss': STATIC_URL + "site/css/richtext-basic.css",
        'filebrowserUploadUrl': "",
        'filebrowserImageUploadUrl': reverse_lazy('ckeditor_upload'),
        'filebrowserBrowseUrl': "",
        'filebrowserImageBrowseUrl': reverse_lazy('ckeditor_browse'),
    },
}
CKEDITOR_EXTERNAL_PLUGIN_SOURCES = [
    ('oembed', '{}ckeditor/plugins/oembed/'.format(JETSON_MEDIA_URL), 'plugin.js'),
]
