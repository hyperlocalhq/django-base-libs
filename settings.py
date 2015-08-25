# -*- coding: utf-8 -*-
# Django settings for the Creative-City-Berlin project.
import os
from datetime import timedelta

gettext = lambda s: s

SITE_ID = 1

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
JETSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "subtrees"))
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

execfile(os.path.join(JETSON_PATH, "jetson/settings/base.py"), globals(), locals())


### DOMAINS ###

SESSION_COOKIE_DOMAIN = "www.creative-city-berlin.de"
STAGING_DOMAIN = "test.creative-city-berlin.de"


### EMAILS ###

MANAGERS = ADMINS = (
    ("Creative City Berlin", "webmaster@creative-city-berlin.de"),
    # ('Aidas Bendoraitis', 'bendoraitis@studio38.de'),
    ('Tiago Henriques', 'henriques@studio38.de'),
)

CONTENT_ADMINS = (
    ("Creative City Berlin", "ccb-contact@kulturprojekte-berlin.de"),
)

DEFAULT_FROM_EMAIL = "contact@creative-city-berlin.de"


### DIRS AND URLS ###

TEMPLATE_DIRS = [
                    os.path.join(PROJECT_PATH, "ccb", "templates", "ccb"),
                    os.path.join(PROJECT_PATH, "ccb", "templates", "admin"),
                ] + TEMPLATE_DIRS

TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS

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

### LANGUAGES ###

LANGUAGES = (
    ('en', gettext('English')),
    ('de', gettext('German')),
)

LANGUAGE_CODE = "de"


### MAIN ###

INSTALLED_APPS = [
    ### third-party apps ###
    "grappelli",
    "filebrowser",
    "crispy_forms",

    ### django core apps ###
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.auth",
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
    # "debug_toolbar",
    # "memcache_toolbar",
    "pipeline",
    "haystack",
    "uni_form",
    "mptt",
    "picklefield",
    "djcelery",
    "kombu.transport.django",
    "captcha",

    ### django-cms ###
    'cms',  # django CMS itself
    'treebeard',  # utilities for implementing a tree
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for javascript and css management
    'djangocms_admin_style',
    # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    'djangocms_text_ckeditor',
    'reversion',

    ### django-cms plug-ins ###
    'djangocms_style',
    'djangocms_column',
    'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',

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
    "jetson.apps.navigation",
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
    "jetson.apps.blog",
    "jetson.apps.comments",
    "jetson.apps.compress_jetson",
    "jetson.apps.mailchimp",

    ### ccb-specific apps ###
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
    "ccb.apps.facebook_app",
    "ccb.apps.slideshows",
    "ccb.apps.faqs",
    "ccb.apps.celerytest",
    "ccb",  # just for i18n in Javascript
]

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    "jetson.apps.httpstate.middleware.HttpStateMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "babeldjango.middleware.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "jetson.apps.flatpages.middleware.FlatpageMiddleware",
    "base_libs.middleware.threadlocals.ThreadLocalsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "jetson.apps.utils.middleware.generic.AdminScriptUpdateMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]
# if not DEVELOPMENT_MODE:
#    MIDDLEWARE_CLASSES.insert(0, "django.middleware.cache.UpdateCacheMiddleware")
#    MIDDLEWARE_CLASSES.append("django.middleware.cache.FetchFromCacheMiddleware")


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'sekizai.context_processors.sekizai',
    'cms.context_processors.cms_settings',
    "jetson.apps.configuration.context_processors.configuration",
    "jetson.apps.utils.context_processors.general",
    "ccb.apps.media_gallery.context_processors.media_gallery",
    "ccb.apps.people.context_processors.people",
    "ccb.apps.institutions.context_processors.institutions",
    "ccb.apps.events.context_processors.events",
    "ccb.apps.resources.context_processors.resources",
    "ccb.apps.groups_networks.context_processors.groups_networks",
    "ccb.apps.marketplace.context_processors.marketplace",
    "ccb.apps.site_specific.context_processors.site_specific",
    "ccb.apps.facebook_app.context_processors.facebook",
)

SECRET_KEY = "*z-g$creativeberlinio@_qt9efb5dge+(64aeq4$!gk+62nsyqlgqpf8l6"

ROOT_URLCONF = "ccb.urls"

### ADMIN ###

ADMIN_APP_INDEX = (
    {
        'title': _('Content'),
        'apps': (
            ('cms', {
                'models': ('Page',),
            }),
            ('events', {
                'models': ("EventType", "EventTimeLabel", "Event",),
                'icon': 'date',
            }),
            ('resources', {
                'models': ("DocumentType", "Medium", "Document",),
                'icon': 'link',
            }),
            ('articles', {
                'models': ("ArticleContentProvider", "ArticleType", "Article",),
                'icon': 'page_white_text',
            }),
            ('blog', {
                'models': ("Blog", "Post"),
                'icon': 'page_white_edit',
            }),
            ('flatpages', {
                'models': ("FlatPage",),
                'icon': 'page_white',
            }),
            ('blocks', {
                'models': ("InfoBlock",),
                'icon': 'brick',
            }),
            ('faqs', {
                'models': ("FaqContainer", "FaqCategory", "QuestionAnswer"),
                'icon': 'help',
            }),
            ('media_gallery', {
                'models': ("PortfolioSettings", "Section", "MediaGallery",),
                'icon': 'images',
            }),
            ('slideshows', {
                'models': ("Slideshow",),
                'icon': 'images',
            }),
        )
    }, {
        'title': _('Community'),
        'apps': (
            ('people', {
                'models': ("IndividualType", "Person",),
                'icon': 'user',
            }),
            ('institutions', {
                'models': ("LegalForm", "InstitutionType", "Institution",),
                'icon': 'building',
            }),
            ('marketplace', {
                'models': ("JobOffer", "JobSector", "JobType", "JobQualification",),
                'icon': 'page_white',
            }),
            ('auth', {
                'verbose_name': _("Authentication"),
                'models': ("Group", "User"),
                'icon': 'key',
            }),
            ('individual_relations', {
                'models': ("IndividualRelationType", "IndividualRelation",),
            }),
            ('favorites', {
                'models': ("Favorite",),
                'icon': 'heart',
            }),
            ('bookmarks', {
                'models': ("Bookmark",),
                'icon': 'flag_red',
            }),
            ('memos', {
                'models': ("MemoCollection",),
                'icon': 'note',
            }),
            ('groups_networks', {
                'models': ("GroupType", "PersonGroup", "GroupMembership"),
                'icon': 'group',
            }),
            ('facebook_app', {
                'models': ("FacebookAppSettings",),
            }),
        )
    }, {
        'title': _('Commerce'),
        'apps': ()
    }, {
        'title': _('Campaign'),
        'apps': (
            ('mailing', {
                'models': ("EmailMessage", "EmailTemplate", "EmailTemplatePlaceholder",),
                'icon': 'email',
            }),
            ('messaging', {
                'models': ("InternalMessage",),
            }),
            ('mailchimp', {
                'models': ("Settings", "MList", "Subscription", "Campaign",),
                'icon': 'transmit',
            }),
        )
    }, {
        'title': _('Control'),
        'apps': ()
    }, {
        'title': _('Configure'),
        'apps': (
            ('navigation', {
                'models': ("NavigationLink",),
            }),
            # ('chronograph', {
            #    'models':("Job", "Log",),
            #    }),
            ('structure', {
                'models': ("Vocabulary", "Term", "ContextCategory"),
            }),
            ('image_mods', {
                'verbose_name': _("Media"),
                'models': ("ImageModificationGroup", "ImageModification", "ImageCropping",),
            }),
            ('contact_form', {
                'models': ("ContactFormCategory",),
            }),
            ('sites', {
                'verbose_name': _("Sites"),
                'models': ("Site",),
            }),
            ('configuration', {
                'models': ("SiteSettings",),
            }),
            ('redirects', {
                'verbose_name': _("Redirects"),
                'models': ("Redirect",),
            }),
            ('i18n', {
                'models': ("Country", "Area", "Language", "CountryLanguage", "Phone", "Nationality", "TimeZone"),
            }),
            ('optionset', {
                'models': (
                    "Prefix", "Salutation", "IndividualLocationType", "InstitutionalLocationType", "PhoneType",
                    "EmailType",
                    "URLType", "IMType"),
            }),
        )
    }, {
        'title': _('Connect'),
        'apps': (
            # ('jovoto', {
            #    'models':("Idea",),
            #    }),
            ('external_services', {
                'models': ("Service", "ArticleImportSource", "ServiceActionLog"),
            }),
        )
    }, {
        'title': _('Control'),
        'apps': (
            ('comments', {
                'verbose_name': _("Comments"),
                'models': ('Comment', 'ModeratorDeletion', 'ModeratorDeletionReason',)
            }),
            ('profanity_filter', {
                'models': ("SwearWord", "SwearingCase",),
            }),
            ('site_specific', {
                'models': ("ClaimRequest", "Visit"),
            }),
            ('tracker', {
                'models': ("Concern", "Ticket",),
            }),
            ('grappelli', {
                'models': ("Bookmark", "Navigation", "Help", "HelpItem",),
            }),
            ('notification', {
                'models': ("NoticeTypeCategory", "NoticeType", "NoticeEmailTemplate", "Notice", "Digest",),
            }),
        )
    }
)


### CACHING ###

if not DEVELOPMENT_MODE and False:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'KEY_PREFIX': "ccb_production_",
            'TIMEOUT': 300,
            'MAX_ENTRIES': 400,
        }
    }


### FILEBROWSER ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/filebrowser.py"))

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'nd': {'verbose_name': 'News Default (163px)', 'width': 163, 'height': 156, 'opts': 'crop upscale'},
    'nt': {'verbose_name': 'News Thumbnail (75px)', 'width': 163, 'height': 100, 'opts': 'crop upscale'},
}
FILEBROWSER_ADMIN_VERSIONS = ['nd', 'nt']
FILEBROWSER_MEDIA_URL = UPLOADS_URL = "/media/"
FILEBROWSER_STRICT_PIL = True

### SEARCH ###

SPHINX_SERVER = 'localhost'  # Sphinx server address, default is localhost
SPHINX_PORT = 3312  # Sphinx server port, default is 3312

SEARCH_ENGINE = "MySqlFulltext"  # one of these: "MySqlFulltext", "Proprietary", "Sphinx"


### MAILING ###

MAILING_DEFAULT_FROM_NAME = 'Creative City Berlin'
MAILING_DEFAULT_FROM_EMAIL = 'ccb-contact@kulturprojekte-berlin.de'
MAILING_HTML_REPLACE = ()
# (
#    (r'<p([^>]*)>', r'<p\1 style="font-size: 12px;margin: 0;padding: 0;line-height: 1.5em;margin-bottom: 18px;">'),
#    (r'<ul([^>]*)>', r'<ul\1 style="font-size: 12px;margin: 0;padding: 0;line-height: 1.5em;margin-bottom: 18px; margin-left: 18px;">'),
#    (r'<li([^>]*)>', r'<li\1 style="margin: 0;padding: 0;list-style-type: square;">'),
#    (r'<a([^>]*)>', r'<a\1 style="color:#6994A6;text-decoration:none;cursor:pointer;">'),
# )


### DEBUG TOOLBAR ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))


### GRAPPELLI ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/grappelli.py"))
GRAPPELLI_ADMIN_HEADLINE = "Creative City Admin"

### COMPRESS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/pipeline.py"))
PIPELINE_ROOT = os.path.join(PROJECT_PATH, "ccb", "site_static")
PIPELINE = False

PIPELINE_CSS['screen'] = {
    'source_filenames': (
        "site/yaml/core/base.css",
        "site/css/screen/basemod.css",
        "site/css/screen/uni-form.css",
        "site/css/screen/default.uni-form.css",
        "site/css/screen/forms.css",
        "site/css/screen/navigation.css",
        "site/css/screen/layout.css",
        "site/css/screen/content.css",
        "site/css/screen/icons.css",
        "site/css/screen/portfolio.css",
    ),
    'output_filename': "site/css/screen/screen_compressed.css",
    'extra_context': {'media': "screen"},
}
PIPELINE_CSS['kreativarbeiten'] = {
    'source_filenames': (
        "site/yaml/core/base.css",
        "site/css/screen/basemod.css",
        "site/css/screen/uni-form.css",
        "site/css/screen/default.uni-form.css",
        "site/css/screen/forms.css",
        "site/css/screen/navigation.css",
        "site/css/screen/layout.css",
        "site/css/screen/content.css",
        "site/css/screen/icons.css",
        "site/css/screen/portfolio.css",
        "site/css/exceptions/kreativarbeiten.css",
    ),
    'output_filename': "site/css/exceptions/kreativarbeiten_compressed.css",
    'extra_context': {'media': "screen"},
}
PIPELINE_CSS['screen_ie'] = {
    'source_filenames': (
        "site/yaml/core/iehacks.css",
        "site/css/patches/patch_layout.css",
    ),
    'output_filename': "site/css/screen/screen_ie_compressed.css",
    'extra_context': {'media': "screen"},
}
PIPELINE_CSS['print'] = {
    'source_filenames': (
        "site/css/print/print.css",
    ),
    'output_filename': "site/css/print/print_compressed.css",
    'extra_context': {'media': "print"},
}

PIPELINE_JS['common'] = {
    'source_filenames': (
        "site/js/collapse.js",
        "site/js/website/common.js",
    ),
    'output_filename': 'site/js/website/common_compressed.js',
}

PIPELINE_JS['common'] = {
    'source_filenames': (
        "site/js/collapse.js",
        "site/js/website/common.js",
    ),
    'output_filename': 'site/js/website/common_compressed.js',
}

PIPELINE_JS['person_details'] = {
    'source_filenames': (
        "site/js/website/categories.js",
        "site/js/website/gmaps_for_address.js",
        "site/js/website/contact_details.js",
        "site/js/website/profile.js",
    ),
    'output_filename': 'site/js/website/person_details_compressed.js',
}

PIPELINE_JS['institution_details'] = {
    'source_filenames': (
        "site/js/website/categories.js",
        "site/js/website/gmaps_for_address.js",
        "site/js/website/contact_details.js",
        "site/js/website/profile.js",
        "site/js/website/opening_hours.js",
    ),
    'output_filename': 'site/js/website/institution_details_compressed.js',
}

PIPELINE_JS['event_details'] = {
    'source_filenames': (
        "site/js/website/categories.js",
        "site/js/website/gmaps_for_address.js",
        "site/js/website/contact_details.js",
        "site/js/website/profile.js",
        "site/js/website/opening_hours.js",
        "site/js/website/event_times.js",
        "site/js/website/formsets.js",
        "site/js/website/multipleselectautocomplete.js",
    ),
    'output_filename': 'site/js/website/event_details_compressed.js',
}

PIPELINE_JS['document_details'] = {
    'source_filenames': (
        "site/js/website/categories.js",
        "site/js/website/profile.js",
    ),
    'output_filename': 'site/js/website/document_details_compressed.js',
}

PIPELINE_JS['job_offer_details'] = {
    'source_filenames': (
        "site/js/website/categories.js",
        "site/js/website/contact_details.js",
        "site/js/website/profile.js",
        "site/js/website/formsets.js",
        "site/js/website/multipleselectautocomplete.js",
    ),
    'output_filename': 'site/js/website/job_offer_details_compressed.js',
}

PIPELINE_JS['map'] = {
    'source_filenames': (
        "site/js/website/map.js",
    ),
    'output_filename': 'site/js/website/map_compressed.js',
}

PIPELINE_JS['blog'] = {
    'source_filenames': (
        "site/js/website/comment.js",
        "site/js/website/blog.js",
    ),
    'output_filename': 'site/js/website/blog_compressed.js',
}

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
    "mailchimp.Subscription",
    "mailchimp.MList",
)

### HAYSTACK ###

HAYSTACK_SITECONF = "ccb.apps.site_specific.search_site"
HAYSTACK_SEARCH_ENGINE = "whoosh"
HAYSTACK_WHOOSH_PATH = os.path.join(PATH_TMP, "site_index")
HAYSTACK_BATCH_SIZE = 100000
HAYSTACK_ENABLE_REGISTRATIONS = True

### MULTILINGUAL URLS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/multilingual_urls.py"))


### OTHER SITE-SPECIFIC SETTINGS ###

APPEND_SLASH = True

THIRD_PARTY_EMAILS = {
    'kulturmanagement.net': "jobs@kulturmanagement.net",
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

IMAGE_MAX_SIZE = "342x342"
IMAGE_PREVIEW_MAX_SIZE = "161x161"
IMAGE_SMALL_SIZE = "75x75"

MIN_LOGO_SIZE = (75, 75)
LOGO_SIZE = (165, 165)
LOGO_PREVIEW_SIZE = "161x161"
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
    ('image_and_text', _("Image and text")),
    ('text', _("Text only")),
    ('news', _("News")),
    ('events', _("Events")),
    ('documents', _("Infolinks")),
    ('portfolios', _("Portfolios")),
    ('people', _("People")),
    ('institutions', _("Institutions")),
)

TIME_INPUT_FORMATS = ('%H:%M:%S', '%H:%M', '%H.%M')

### CELERY ###

CELERY_RESULT_BACKEND = 'database'
# For scheduled jobs. 
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_TRACK_STARTED = True
CELERY_SEND_EVENTS = True
CELERYD_LOG_FILE = os.path.join(PROJECT_PATH, "ccb/tmp/celery.log")

BROKER_URL = "django://"
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

import djcelery

djcelery.setup_loader()

### CAPTCHA ###

RECAPTCHA_PUBLIC_KEY = '6LfWkt8SAAAAAPnRowSBDg1GJOk6umAqdwVcpUFK'
RECAPTCHA_PRIVATE_KEY = '6LfWkt8SAAAAABAOx3-qsJYDt76jSpUlIkg8ZgcD'
RECAPTCHA_USE_SSL = False

### DJANGO CRISPY FORMS ###

CRISPY_TEMPLATE_PACK = 'bootstrap3'

### DJANGO CMS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/cms.py"), globals(), locals())

CMS_TEMPLATES = (
    ('cms/page.html', 'Page'),
    ('cms/feature.html', 'Page with Feature')
)

CMS_LANGUAGES = {
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'de',
            'hide_untranslated': False,
            'name': gettext('de'),
            'redirect_on_fallback': True,
        },
        {
            'public': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': gettext('en'),
            'redirect_on_fallback': True,
        },
    ],
}

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

### LOCAL SETTINGS ###

try:
    execfile(os.path.join(os.path.dirname(__file__), "local_settings.py"))
except IOError:
    pass
