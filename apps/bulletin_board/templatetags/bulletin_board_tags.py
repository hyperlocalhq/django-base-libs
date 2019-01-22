# -*- coding: UTF-8 -*-
import re
from django import template
from itertools import chain

register = template.Library()


### FILTERS ###


@register.filter
def can_be_changed(val, user):
    return val.can_be_changed(user)
    
@register.filter
def bulletin_type_count(bt, facets={}):
    qs = facets['queryset'].filter(
        bulletin_type=bt,
        ).distinct()
    
    return qs.count()
    
@register.filter
def bulletin_category_count(cg, facets={}):
    qs = facets['queryset'].filter(
        category__pk=cg.pk,
        ).distinct()
    
    return qs.count()
    
@register.filter
def status_count(bt, facets={}):
    qs = facets['queryset'].filter(
        status=bt,
        ).distinct()
    
    return qs.count()

@register.filter
def merge_with(bulletins, jobs):
    return list(chain(bulletins, jobs))