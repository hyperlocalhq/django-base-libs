APP_DEPENDENCIES = {
    # django.contrib
    'sitemaps': {
        'required_apps': ["sites"],
        'optional_apps': [],
    },
    'sites': {
        'required_apps': [],
        'optional_apps': [],
    },
    'redirects': {
        'required_apps': [],
        'optional_apps': [],
    },
    'auth': {
        'required_apps': ["contenttypes"],
        'optional_apps': [],
    },
    'admin': {
        'required_apps': ["auth", "contenttypes"],
        'optional_apps': [],
    },
    'sessions': {
        'required_apps': [],
        'optional_apps': [],
    },
    'contenttypes': {
        'required_apps': [],
        'optional_apps': [],
    },
    'markup': {
        'required_apps': [],
        'optional_apps': [],
    },

    # third-party
    'babeldjango': {
        'required_apps': [],
        'optional_apps': [],
    },
    'filebrowser': {
        'required_apps': ["admin"],
        'optional_apps': [],
    },
    'grappelli':
        {
            'required_apps': ["admin", "filebrowser"],
            'optional_apps': ["sites"],
        },
    'tagging': {
        'required_apps': ["contenttypes"],
        'optional_apps': [],
    },
    'tagging_autocomplete':
        {
            'required_apps': ["tagging"],
            'optional_apps': [],
        },
    'rosetta': {
        'required_apps': ["auth"],
        'optional_apps': [],
    },
    'south': {
        'required_apps': [],
        'optional_apps': [],
    },
    'debug_toolbar': {
        'required_apps': [],
        'optional_apps': [],
    },
    'compress': {
        'required_apps': [],
        'optional_apps': [],
    },
    'tinymce': {
        'required_apps': [],
        'optional_apps': [],
    },
    'menus': {
        'required_apps': [],
        'optional_apps': [],
    },
    'cms':
        {
            'required_apps': ["admin", "mptt", "publisher", "menus"],
            'optional_apps': ["reversion", "tinymce"],
        },
    'mptt': {
        'required_apps': [],
        'optional_apps': [],
    },
    'publisher': {
        'required_apps': [],
        'optional_apps': [],
    },
    'reversion': {
        'required_apps': [],
        'optional_apps': [],
    },
}
