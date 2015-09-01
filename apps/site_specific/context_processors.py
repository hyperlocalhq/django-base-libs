# -*- coding: UTF-8 -*-

from django.conf import settings

from jetson.apps.structure.models import Term


def site_specific(request=None):
    conditions = {}
    if hasattr(settings, "CREATIVE_SECTOR"):
        conditions["sysname"] = getattr(settings, "CREATIVE_SECTOR", None)
    if request:
        path_bits = request.path[1:].split("/")  # e.g.: ('en', 'creative-sector', 'architecture', '...') or ('creative-sector', 'architecture', '...')
        if path_bits[0] == request.LANGUAGE_CODE:
            path_bits = path_bits[1:]  # e.g.: ('creative-sector', 'architecture', '...')
        if path_bits >= 2 and path_bits[0] == "creative-sector":
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
        except Exception:
            pass
    d = {
        'creative_sector': creative_sector,
    }
    return d
