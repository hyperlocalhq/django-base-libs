# -*- coding: UTF-8 -*-
from __future__ import unicode_literals


def get_locality_type(postal_code):
    import re
    from base_libs.utils.betterslugify import better_slugify
    from django.apps import apps
    from django.conf import settings
    LocalityType = apps.get_model("location", "LocalityType")
    Geolocation = apps.get_model("geolocation", "Geolocation")

    p = re.compile('[^\d]*')  # remove non numbers
    postal_code = p.sub("", postal_code)

    geos = Geolocation.objects.filter(zip_code=postal_code)

    if geos.count():

        geo = geos[0]

        if geo.region3:
            d = {}
            for lang_code, lang_verbose in settings.LANGUAGES:
                d["title_%s" % lang_code] = geo.region3

            locality_type, created = LocalityType.objects.get_or_create(
                slug=better_slugify(geo.region3),
                defaults=d,
            )
            return locality_type

    return None
