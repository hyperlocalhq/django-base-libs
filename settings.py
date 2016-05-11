# -*- coding: utf-8 -*-
# Django settings for the Creative-City-Berlin project.
from datetime import timedelta

import os

gettext = lambda s: s

DEBUG = TEMPLATE_DEBUG = False

SITE_ID = 1

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
JETSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "subtrees"))
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

execfile(os.path.join(JETSON_PATH, "jetson/settings/base.py"), globals(), locals())


### DOMAINS ###

SESSION_COOKIE_DOMAIN = "www.creative-city-berlin.de"
STAGING_DOMAIN = "ccb.jetsonproject.org"

ALLOWED_HOSTS = [
    "www.creative-city-berlin.de",
    "creative-city-berlin.de",
    "ccb.jetsonproject.org",
]

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
    ("en", gettext("English")),
    ("de", gettext("German")),
)

LANGUAGE_CODE = "de"


### MAIN ###

INSTALLED_APPS = [
    ### third-party apps ###
    "crispy_forms",
    # "django_extensions",
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
    "pipeline",
    "uni_form",
    "mptt",
    "picklefield",
    "djcelery",
    "kombu.transport.django",
    "captcha",
    "social.apps.django_app.default",
    "bootstrap_pagination",
    "raven.contrib.django.raven_compat",

    ### django-cms ###
    "cms",  # django CMS itself
    "treebeard",  # utilities for implementing a tree
    "menus",  # helper for model independent hierarchical website navigation
    "sekizai",  # for javascript and css management
    # for the admin skin. You **must** add "djangocms_admin_style" in the list **before** "django.contrib.admin".
    "reversion",
    "aldryn_search",

    ### django-cms plug-ins ###
    "djangocms_column",
    "djangocms_file",
    "djangocms_flash",
    "djangocms_inherit",
    "djangocms_link",
    "djangocms_style",
    "djangocms_teaser",
    "djangocms_video",

    ### plug-ins for django-cms ###
    "jetson.apps.cms_extensions.plugins.richtext",
    "jetson.apps.cms_extensions.plugins.filebrowser_image",
    "jetson.apps.cms_extensions.plugins.gmap",
    "jetson.apps.cms_extensions.plugins.headline",
    "ccb.apps.editorial",

    ### base libs ###
    # "base_libs",

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
    "jetson.apps.compress_jetson",
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
    "ccb.apps.celerytest",
    "ccb.apps.accounts",
    "ccb.apps.network",
    "ccb.apps.navigation",
    "ccb.apps.bulletin_board",
    "ccb.apps.metro",
    "ccb.apps.partners",
    "ccb.apps.counselling_blog",
    "ccb.apps.counselling_events",
    "ccb.apps.curated_lists",
    "ccb",  # just for i18n in Javascript
    "actstream",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "jetson.apps.httpstate.middleware.HttpStateMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "babeldjango.middleware.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    #"jetson.apps.flatpages.middleware.FlatpageMiddleware",
    "base_libs.middleware.threadlocals.ThreadLocalsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "jetson.apps.utils.middleware.generic.AdminScriptUpdateMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    #"django.middleware.clickjacking.XFrameOptionsMiddleware", # we can"t have this, because KB is using some content from Kreativ Arbeiten section in an iframe
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    "ccb.apps.accounts.middleware.MySocialAuthExceptionMiddleware",
    "base_libs.middleware.traceback.UserTracebackMiddleware",
]
# if not DEVELOPMENT_MODE:
#    MIDDLEWARE_CLASSES.insert(0, "django.middleware.cache.UpdateCacheMiddleware")
#    MIDDLEWARE_CLASSES.append("django.middleware.cache.FetchFromCacheMiddleware")


TEMPLATE_CONTEXT_PROCESSORS = (
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
    "ccb.apps.resources.context_processors.resources",
    "ccb.apps.groups_networks.context_processors.groups_networks",
    "ccb.apps.marketplace.context_processors.marketplace",
    "ccb.apps.site_specific.context_processors.site_specific",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
)

SECRET_KEY = "*z-g$creativeberlinio@_qt9efb5dge+(64aeq4$!gk+62nsyqlgqpf8l6"

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
            ("resources", {
                "models": ("DocumentType", "Medium", "Document",),
                "icon": "link",
            }),
            ("articles", {
                "models": ("ArticleContentProvider", "ArticleType", "Article",),
                "icon": "page_white_text",
            }),
            ("blog", {
                "models": ("Blog", "Post"),
                "icon": "page_white_edit",
            }),
            ("flatpages", {
                "models": ("FlatPage",),
                "icon": "page_white",
            }),
            ("blocks", {
                "models": ("InfoBlock",),
                "icon": "brick",
            }),
            ("faqs", {
                "models": ("FaqContainer", "FaqCategory", "QuestionAnswer"),
                "icon": "help",
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
                "models": ("Settings", "MList", "Subscription", "Campaign",),
                "icon": "transmit",
            }),
        )
    }, {
        "title": _("Configure"),
        "apps": (
            ("navigation", {
                "models": ("NavigationLink",),
            }),
            # ("chronograph", {
            #    "models":("Job", "Log",),
            #    }),
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
                "models": ("NoticeTypeCategory", "NoticeType", "NoticeEmailTemplate", "Notice", "Digest",),
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
        "TIMEOUT": 300,
        "MAX_ENTRIES": 400,
    }
}

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

### COMPRESS ###

execfile(os.path.join(JETSON_PATH, "jetson/settings/pipeline.py"))
PIPELINE_ROOT = os.path.join(PROJECT_PATH, "ccb", "site_static")
PIPELINE = False

PIPELINE_CSS["screen"] = {
    "source_filenames": (
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
    "output_filename": "site/css/screen/screen_compressed.css",
    "extra_context": {"media": "screen"},
}
PIPELINE_CSS["kreativarbeiten"] = {
    "source_filenames": (
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
    "output_filename": "site/css/exceptions/kreativarbeiten_compressed.css",
    "extra_context": {"media": "screen"},
}
PIPELINE_CSS["screen_ie"] = {
    "source_filenames": (
        "site/yaml/core/iehacks.css",
        "site/css/patches/patch_layout.css",
    ),
    "output_filename": "site/css/screen/screen_ie_compressed.css",
    "extra_context": {"media": "screen"},
}
PIPELINE_CSS["print"] = {
    "source_filenames": (
        "site/css/print/print.css",
    ),
    "output_filename": "site/css/print/print_compressed.css",
    "extra_context": {"media": "print"},
}

PIPELINE_JS["common"] = {
    "source_filenames": (
        "site/js/collapse.js",
        "site/js/website/common.js",
    ),
    "output_filename": "site/js/website/common_compressed.js",
}

PIPELINE_JS["common"] = {
    "source_filenames": (
        "site/js/collapse.js",
        "site/js/website/common.js",
    ),
    "output_filename": "site/js/website/common_compressed.js",
}

PIPELINE_JS["person_details"] = {
    "source_filenames": (
        "site/js/website/categories.js",
        "site/js/website/gmaps_for_address.js",
        "site/js/website/contact_details.js",
        "site/js/website/profile.js",
    ),
    "output_filename": "site/js/website/person_details_compressed.js",
}

PIPELINE_JS["institution_details"] = {
    "source_filenames": (
        "site/js/website/categories.js",
        "site/js/website/gmaps_for_address.js",
        "site/js/website/contact_details.js",
        "site/js/website/profile.js",
        "site/js/website/opening_hours.js",
    ),
    "output_filename": "site/js/website/institution_details_compressed.js",
}

PIPELINE_JS["event_details"] = {
    "source_filenames": (
        "site/js/website/categories.js",
        "site/js/website/gmaps_for_address.js",
        "site/js/website/contact_details.js",
        "site/js/website/profile.js",
        "site/js/website/opening_hours.js",
        "site/js/website/event_times.js",
        "site/js/website/formsets.js",
        "site/js/website/multipleselectautocomplete.js",
    ),
    "output_filename": "site/js/website/event_details_compressed.js",
}

PIPELINE_JS["document_details"] = {
    "source_filenames": (
        "site/js/website/categories.js",
        "site/js/website/profile.js",
    ),
    "output_filename": "site/js/website/document_details_compressed.js",
}

PIPELINE_JS["job_offer_details"] = {
    "source_filenames": (
        "site/js/website/categories.js",
        "site/js/website/contact_details.js",
        "site/js/website/gmaps_for_address.js",
        "site/js/website/profile.js",
        "site/js/website/formsets.js",
        "site/js/website/multipleselectautocomplete.js",
    ),
    "output_filename": "site/js/website/job_offer_details_compressed.js",
}

PIPELINE_JS["map"] = {
    "source_filenames": (
        "site/js/website/map.js",
    ),
    "output_filename": "site/js/website/map_compressed.js",
}

PIPELINE_JS["blog"] = {
    "source_filenames": (
        "site/js/website/comment.js",
        "site/js/website/blog.js",
    ),
    "output_filename": "site/js/website/blog_compressed.js",
}

PIPELINE_JS["autocomplete"] = {
    "source_filenames": (
        "site/js/jquery/autocomplete_1.0/jquery.bgiframe.min.js",
        "site/js/jquery/autocomplete_1.0/jquery.autocomplete.js",
        "site/js/website/autocomplete.js",
    ),
    "output_filename": "site/js/jquery/autocomplete_compressed.js",
}

COMPRESS_JETSON_JS["admin_person_change"] = {
    "source_filenames": (
        "js/admin/person_change.js",
    ),
    "output_filename": "js/admin/person_change_compressed.js",
}

COMPRESS_JETSON_JS["admin_institution_change"] = {
    "source_filenames": (
        "js/admin/institution_change.js",
    ),
    "output_filename": "js/admin/institution_change_compressed.js",
}

COMPRESS_JETSON_JS["autocomplete"] = {
    "source_filenames": (
        "js/jquery/autocomplete_1.0/jquery.bgiframe.min.js",
        "js/jquery/autocomplete_1.0/jquery.autocomplete.js",
        "js/website/autocomplete.js",
    ),
    "output_filename": "js/jquery/autocomplete_compressed.js",
}

COMPRESS_JETSON_JS["admin_event_change"] = {
    "source_filenames": (
        "js/admin/event_change.js",
    ),
    "output_filename": "js/admin/event_change_compressed.js",
}

COMPRESS_JETSON_JS["admin_document_change"] = {
    "source_filenames": (
        "js/admin/document_change.js",
    ),
    "output_filename": "js/admin/document_change_compressed.js",
}

COMPRESS_JETSON_JS["admin_job_offer_change"] = {
    "source_filenames": (
        "js/admin/job_offer_change.js",
    ),
    "output_filename": "js/admin/job_offer_change_compressed.js",
}

COMPRESS_JETSON_JS["jquery_plugins"] = {
    "source_filenames": (
        "js/jquery/jquery.ba-hashchange.min.js",
        "js/jquery/jquery.cookie.js",
        "js/jquery/jquery.popup.js",
        "js/jquery/uni-form.jquery.min.js",
    ),
    "output_filename": "js/jquery/jquery_plugins_compressed.js",
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

### CELERY ###

CELERY_RESULT_BACKEND = "database"
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
    "djangocms_file": "djangocms_file.migrations_django",
    "djangocms_flash": "djangocms_flash.migrations_django",
    "djangocms_googlemap": "djangocms_googlemap.migrations_django",
    "djangocms_inherit": "djangocms_inherit.migrations_django",
    "djangocms_link": "djangocms_link.migrations_django",
    "djangocms_picture": "djangocms_picture.migrations_django",
    "djangocms_snippet": "djangocms_snippet.migrations_django",
    "djangocms_teaser": "djangocms_teaser.migrations_django",
    "djangocms_video": "djangocms_video.migrations_django",
    "djangocms_style": "djangocms_style.migrations_django",
    "djangocms_column": "djangocms_column.migrations_django",
}

### PERSISTENT DATABASE CONNECTIONS ###

CONN_MAX_AGE = 600

### SOCIAL AUTHENTICATION ###

AUTHENTICATION_BACKENDS = (
    #"social.backends.behance.BehanceOAuth2",
    #"social.backends.disqus.DisqusOAuth2",
    "social.backends.facebook.FacebookOAuth2",
    #"social.backends.flickr.FlickrOAuth",
    #"social.backends.google.GoogleOAuth",
    #"social.backends.google.GoogleOAuth2",
    #"social.backends.google.GooglePlusAuth",
    #"social.backends.google.GoogleOpenIdConnect",
    #"social.backends.instagram.InstagramOAuth2",
    #"social.backends.linkedin.LinkedinOAuth",
    #"social.backends.linkedin.LinkedinOAuth2",
    #"social.backends.mixcloud.MixcloudOAuth2",
    #"social.backends.open_id.OpenIdAuth",
    #"social.backends.soundcloud.SoundcloudOAuth2",
    #"social.backends.spotify.SpotifyOAuth2",
    #"social.backends.tumblr.TumblrOAuth",
    #"social.backends.twitter.TwitterOAuth",
    #"social.backends.xing.XingOAuth",
    #"social.backends.yahoo.YahooOAuth",
    #"social.backends.yahoo.YahooOpenId",
    #"social.backends.vimeo.VimeoOAuth1",
    "jetson.apps.permissions.backends.RowLevelPermissionsBackend",
    "jetson.apps.utils.backends.EmailBackend",
    "social.backends.username.UsernameAuth",
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_USER_MODEL = "auth.User"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "dashboard"
URL_PATH = ""
SOCIAL_AUTH_STRATEGY = "social.strategies.django_strategy.DjangoStrategy"
SOCIAL_AUTH_STORAGE = "social.apps.django_app.default.models.DjangoStorage"
SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile"
]
SOCIAL_AUTH_USERNAME_FORM_HTML = "username_signup.html"

SOCIAL_AUTH_FACEBOOK_KEY = "217188838296370"
SOCIAL_AUTH_FACEBOOK_SECRET = "66548a2c23317f70ff1e20bd982a5f68"
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  "fields": "id, name, email, first_name, last_name",
}

SOCIAL_AUTH_PIPELINE = (
    "social.pipeline.social_auth.social_details",
    "social.pipeline.social_auth.social_uid",
    "social.pipeline.social_auth.auth_allowed",
    "social.pipeline.social_auth.social_user",
    "social.pipeline.user.get_username",
    #"example.app.pipeline.require_email",
    #"social.pipeline.mail.mail_validation",
    "ccb.apps.accounts.pipeline.login_or_registration",
    "ccb.apps.accounts.pipeline.create_user",
    "social.pipeline.social_auth.associate_user",
    #"social.pipeline.debug.debug",
    "social.pipeline.social_auth.load_extra_data",
    "social.pipeline.user.user_details",
    #"social.pipeline.debug.debug",
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    #"social.pipeline.disconnect.allowed_to_disconnect",
    "social.pipeline.disconnect.get_entries",
    "social.pipeline.disconnect.revoke_tokens",
    "social.pipeline.disconnect.disconnect"
)

### DJANGO ACTIVITY STREAM ###

ACTSTREAM_SETTINGS = {
    "MANAGER": "actstream.managers.ActionManager",
    "FETCH_RELATIONS": True,
    "USE_PREFETCH": True,
    "USE_JSONFIELD": True,
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
    'dsn': 'http://ffc5ae7c26dd49ed8f14ca113cb0f7de:29e74466fdaa4af7a245f7a3eae16543@sentry.jetsonproject.org/2',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}

### LOCAL SETTINGS ###

try:
    execfile(os.path.join(os.path.dirname(__file__), "local_settings.py"))
except IOError:
    pass

### DEBUG TOOLBAR ###

if DEBUG:
    import debug_toolbar

    INSTALLED_APPS += [
        "debug_toolbar",
        # "memcache_toolbar",
    ]
    execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))
