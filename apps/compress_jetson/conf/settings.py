# -*- coding: UTF-8 -*-

from compress.conf.settings import *
from django.conf import settings

COMPRESS_JETSON_CSS = getattr(settings, "COMPRESS_JETSON_CSS", {})
COMPRESS_JETSON_JS = getattr(settings, "COMPRESS_JETSON_JS", {})
