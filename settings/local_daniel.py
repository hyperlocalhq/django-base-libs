# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from .local import *

DEBUG = True

SESSION_COOKIE_DOMAIN = "127.0.0.1"
#SESSION_COOKIE_DOMAIN = "192.168.2.102"
ALLOWED_HOSTS = ['127.0.0.1', '192.168.2.102']

WEBSITE_URL = "http://127.0.0.1:8000"  # no trailing slash
