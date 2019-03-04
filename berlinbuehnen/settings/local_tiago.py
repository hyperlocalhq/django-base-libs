# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from .local import *

DEBUG = True

SESSION_COOKIE_DOMAIN = "127.0.0.1"
ALLOWED_HOSTS = ['127.0.0.1']

ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost:9200'
    },
}
