from django.core.cache import cache
from django.utils.cache import get_cache_key


def expire_page(request, path):
    request.path = path
    request.method = "GET"
    key = get_cache_key(request)
    if key in cache:
        cache.delete(key)
