# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from .local import *

DEBUG = True

SESSION_COOKIE_DOMAIN = "127.0.0.1"
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE_CLASSES.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))

# Start a dummy SMTP server with:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

WEBSITE_URL = "http://127.0.0.1:8000"  # no trailing slash