# -*- coding: UTF-8 -*-
from django.core.cache import cache
from django.utils.cache import get_cache_key


def expire_page(request, path):
    request.path = path
    request.method = "GET"
    key = get_cache_key(request)
    if cache.has_key(key):
        cache.delete(key)