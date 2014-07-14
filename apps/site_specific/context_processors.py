# -*- coding: UTF-8 -*-
import re

from django.conf import settings

from jetson.apps.structure.models import Term

def site_specific(request=None):
    conditions = {}
    if hasattr(settings, "CREATIVE_SECTOR"):
        conditions["sysname"] = getattr(settings, "CREATIVE_SECTOR", None)
    if request:
        if 'HTTP_HOST' in request.META:
            bits = request.META['HTTP_HOST'].split('.')
            path_bits = request.path[1:].split("/")
            if path_bits>=2:
                if path_bits[0] == "creative-sector":
                    conditions["slug"] = path_bits[1]
            elif "creative_sector" in request.GET:
                conditions["sysname"] = request.GET["creative_sector"]
    creative_sector = None
    if conditions:
        try:
            creative_sector = Term.objects.get(
                vocabulary__sysname="categories_creativesectors",
                **conditions
                )
        except:
            pass
    d = {
        'creative_sector': creative_sector,
        }
    return d
