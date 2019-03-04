# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from .local import *

DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE_CLASSES.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
execfile(os.path.join(JETSON_PATH, "jetson/settings/debug_toolbar.py"))
