# -*- coding: UTF-8 -*-
from django import template
from django.conf import settings

register = template.Library()

def absolute_url(value, arg):
    return value.get_absolute_url2(arg)

register.filter('absolute_url', absolute_url)
