# -*- coding: utf-8 -*-

# Django settings for museumsportal project.
import os
gettext = lambda s: s

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

execfile(os.path.join(ROOT_PATH, "jetson/settings/base.py"), globals(), locals())

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Berliner Museumsportal Webmaster', 'bendoraitis@studio38.de'),
)

MANAGERS = ( 
     ('Berliner Museumsportal Webmaster', 'museumsportal@kulturprojekte-berlin.de'),
)

TIME_ZONE = 'Europe/Berlin'

### LANGUAGES ###
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGES = (
    ('de', gettext("German")),
    ('en', gettext("English")),
)

FRONTEND_LANGUAGES = (
    ('de', gettext("German")),
    ('en', gettext("English")),
)

LANGUAGE_CODE = "de"

SITE_ID = 1
USE_I18N = True
USE_L10N = False # --> no commas in float values for latitude and longitude

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH, "museumsportal", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH, "museumsportal", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = PIPELINE_URL = "/static/%s/" % get_git_changeset(STATIC_ROOT)

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/%s/admin/' % get_git_changeset(STATIC_ROOT)

# Additional locations of static files
STATICFILES_DIRS = [os.path.join(ROOT_PATH, "museumsportal", "site_static")]
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

#Settings for uploaded images
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 2 # 2 MB


TEMPLATESADMIN_TEMPLATE_DIRS = TEMPLATE_DIRS = [
    os.path.join(ROOT_PATH, "museumsportal", "templates", "museumsportal"),
    os.path.join(ROOT_PATH, "museumsportal", "templates", "admin"),
    ] + TEMPLATE_DIRS

PATH_TMP = os.path.join(ROOT_PATH, "museumsportal", "tmp")
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
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "jetson.apps.httpstate.middleware.HttpStateMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "base_libs.middleware.threading.ThreadLocalsMiddleware",    
    #"cms.middleware.multilingual.MultilingualURLMiddleware",
    "jetson.apps.cms_extensions.middleware.MultilingualURLMiddleware",
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'museumsportal.urls'

INSTALLED_APPS = (
    ### third-party apps ###
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
        
    ### more third-party apps ###    
    "pipeline",
    "uni_form",
    "tastypie",
    "tagging",
    "tagging_autocomplete",
    "crispy_forms",
    "rosetta",
    "babeldjango",
    
    ### Required CMS Django 2.2 apps ###
    "cms",
    "mptt",
    "menus",
    "south",
    "sekizai",
    
    ### CMS plugins ###
    "cms.plugins.*",

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
    "jetson.apps.mailing",
    "jetson.apps.permissions",
    "jetson.apps.external_services",
    "jetson.apps.mailchimp",
    "jetson.apps.blocks",
    "jetson.apps.media_gallery",
    "jetson.apps.configuration",
    "jetson.apps.favorites",
    
    ### museumsportal apps ###
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
)


### ADMIN ###

ADMIN_APP_INDEX = (
    {
        'title':gettext('Content'),
        'apps':(
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
                'models': ('WorkshopCategory','AgeGroup','Workshop',),
                }),
            ('slideshows', {
                'models': ('Slideshow',),
                }),     
            ('articles', {
                'models': ('ArticleCategory','Article',),
                }),
         )
    },
    {
        'title':gettext('Community'),
        'apps':(
            
             ('auth', {
                'verbose_name': gettext("Authentication"),
                'models':("Group", "User",),
                'icon': 'key',
             }),
             ('permissions', {
                'models': ('PerObjectGroup','RowLevelPermission',),
              }),
             ('institutions', {
                'models':("Institution",),                
                }),
             ('twitterwall', {
                'verbose_name': gettext("Twitter Wall"),
                'models':("SearchSettings", "UserTimelineSettings", "TwitterUser", "Tweet"),                
                }),
        )
    },
    {
        'title':gettext('Campaign'),
        'apps':(         
            ('mailing', {
                'models':("EmailMessage", "EmailTemplate", "EmailTemplatePlaceholder",),
                'icon': 'email',             
             }),
            ('mailchimp', {
                'models':("Settings", "MList", "Subscription", "Campaign"),
                'icon': 'email',             
             }),
            ('lottery', {
                'models':("LotteryEntry", ),
             }),
        )
    },
    {
        'title':gettext('Configure'),
        'apps':(
            ('structure', {
                'models':("Vocabulary", "Term", "ContextCategory"),
                }),
             ('image_mods', {
                'verbose_name': gettext("Media"),
                'models':("ImageModificationGroup","ImageModification","ImageCropping",),
                }),
             ('sites', {
                'verbose_name': gettext('Sites'),
                'models': ('Site',)
                }),
             ('i18n', {
                'models':("Country", "Area", "Language", "CountryLanguage", "Phone", "Nationality", "TimeZone"),
                }),
             ('tagging', {
                'models':("TaggedItem", "Tag",),
                }),
             ('external_services', {
                'models':("Service", "ObjectMapper",),
                }),
             ('tagging', {
                'models':("Tag", "TaggedItem",),
                }),
             ('tastypie', {
                'models':("ApiKey",),
                }),
            ('configuration', {
                'models':("SiteSettings",),
                }),
        )
    }
 
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
            'class': 'django.utils.log.AdminEmailHandler'
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

ARTICLES_HAVE_TYPES = False

### CMS SETTINGS ###

execfile(os.path.join(ROOT_PATH, "jetson/settings/cms.py"), globals(), locals())

CMS_LANGUAGES = (
    ('de', gettext('German')),
    ('en', gettext('English')),
    )

CMS_SITE_LANGUAGES = {
    1:['en','de'],
}

# Customized placeholders
CMS_PLACEHOLDER_CONF = {
    'typehead': {
        'plugins': ("RichTextPlugin", "HeadlinePlugin"),
        'name': _("Typehead")
    },
    'top_image': {
        'plugins': ("FilebrowserImagePlugin"),
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

    'footnotes': {
        'plugins': ("RichTextPlugin",),
        'name': _("Footnotes")
    },

    'series_items_featured': {
        'plugins': ("EditorialContentPlugin", "TeaserPlugin"),
        'name': _("Series Items Featured")
    },
    
    'series_items': {
        'plugins': ("EditorialContentPlugin", "TeaserPlugin"),
        'name': _("Series Items")
    },
    
    'series_exhibitions': {
        'plugins': ("EditorialContentPlugin", "TeaserPlugin"),
        'name': _("Series Exhibitions")
    },
    
    'series_images': {
        'plugins': ("RichTextPlugin",),
        'name': _("Series Images")
    },

    'start_page_content': {
        'plugins': ("EditorialContentPlugin", "TeaserPlugin"),
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
}

CMS_TEMPLATES = (
    ('cms/default.html', gettext('Default')),
    ('cms/start.html', gettext('Homepage')),   

    ('cms/plan_organize_overview.html', gettext('Plan & Organize – Overview')),
    ('cms/plan_organize.html', gettext('Plan & Organize - Detail')),              # previous: visitor_info.html

    ('cms/magazine_overview.html', gettext('Magazine – Overview')),
    ('cms/magazine.html', gettext('Magazine - Detail')),
    ('cms/magazine_series.html', gettext('Magazine – Series')),                   # previous: series.html
    ('cms/magazine_series_featured.html', gettext('Magazine – Featured Series')), # previous: series_with_featured.html
)

# UPDATE cms_page SET template = REPLACE(template,'cms/visitor_info.html','cms/plan_organize.html');
# UPDATE cms_page SET template = REPLACE(template,'cms/series.html','cms/magazine_series.html');
# UPDATE cms_page SET template = REPLACE(template,'cms/series_with_featured.html','cms/magazine_series_featured.html');

CMS_APPHOOKS = (
    )

CMS_REDIRECTS = True
CMS_MENU_TITLE_OVERWRITE = True

CMS_LANGUAGE_CONF = { 
    'de':['en'], 
}
CMS_FRONTEND_LANGUAGES = ("en", "de")
CMS_LANGUAGE_FALLBACK = "de"
CMS_HIDE_UNTRANSLATED = True
CMS_CACHE_DURATIONS = {
    'content': 60,
    'menus': 3600,
    'permissions': 3600,
}
CMS_CACHE_PREFIX = "cms-"
CMS_SITE_CHOICES_CACHE_KEY = 'CMS:site_choices'
CMS_PAGE_CHOICES_CACHE_KEY = 'CMS:page_choices'

### FILEBROWSER ###

execfile(os.path.join(ROOT_PATH, "jetson/settings/filebrowser.py"), globals(), locals())

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
}

FILEBROWSER_MEDIA_URL = UPLOADS_URL = "/media/"

### GRAPPELLI ###

execfile(os.path.join(ROOT_PATH, "jetson/settings/grappelli.py"))
GRAPPELLI_ADMIN_HEADLINE = "Berliner Museumsportal Admin"

### OTHER SETTINGS ###

ARTICLES_HAVE_TYPES = False

TWITTER_USERNAME = "museumsportal"
TWITTER_NUMBER_OF_TWEETS = 3

API_LIMIT_PER_PAGE = 0

GALLERY_IMAGE_MIN_DIMENSIONS = (800, 800)

### LOCAL SETTINGS ###

try:
    execfile(os.path.join(os.path.dirname(__file__), "local_settings.py"))
except IOError:
    pass
