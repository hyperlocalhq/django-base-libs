# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from .local import *

DEBUG = True

SESSION_COOKIE_DOMAIN = "127.0.0.1"
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost'
]

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE_CLASSES.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))
