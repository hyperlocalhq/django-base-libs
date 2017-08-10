# -*- coding: UTF-8 -*-

from django.templatetags.cache import *
from django.conf import settings
from django.utils.http import urlquote
from django.template.base import resolve_variable

def cache_node_render(self, context):
    key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
    try:
        expire_time = self.expire_time_var.resolve(context)
    except VariableDoesNotExist:
        raise TemplateSyntaxError('"cache" tag got an unknkown variable: %r' % self.expire_time_var.var)
    try:
        expire_time = int(expire_time)
    except (ValueError, TypeError):
        raise TemplateSyntaxError('"cache" tag got a non-integer timeout value: %r' % expire_time)
    # Build a key for this fragment and all vary-on's.
    key = ':'.join([urlquote(resolve_variable(var, context)) for var in self.vary_on])
    args = hashlib.md5(force_bytes(key))
    cache_key = 'template.cache.%s.%s.%s' % (key_prefix, self.fragment_name, args.hexdigest())
    value = cache.get(cache_key)
    if value is None:
        value = self.nodelist.render(context)
        cache.set(cache_key, value, expire_time)
    return value
    
# CacheNode.render = cache_node_render
