# -*- coding: UTF-8 -*-
from django.utils import simplejson

from base_libs.utils.misc import ExtendedJSONEncoder
from jetson.apps.i18n.models import Country


def json_country_name(request, country_code):
    try:
        country = Country.objects.get(iso2_code=country_code)
    except Country.DoesNotExist:
        json = ""
    else:
        json = country.get_name()
    json = simplejson.dumps(json, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json, mimetype='text/javascript; charset=utf-8')

