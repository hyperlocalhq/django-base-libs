# -*- coding: UTF-8 -*-
from django import template

register = template.Library()

### FILTERS ###

def get_avatar_url(obj, dimensions):
    url = ""
    if hasattr(obj, "get_original_image_rel_path"):
        path = obj.get_original_image_rel_path()
        if path:
            url = "/helper/tmpimage/%s/?path=%s" % (
                dimensions,
                path,
            )
    return url


register.filter('get_avatar_url', get_avatar_url)
