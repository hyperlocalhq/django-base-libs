# -*- coding: UTF-8 -*-
import json

from base_libs.utils.misc import ExtendedJSONEncoder
from jetson.apps.i18n.models import Country


def json_country_name(request, country_code):
    try:
        country = Country.objects.get(iso2_code=country_code)
    except Country.DoesNotExist:
        json_data = ""
    else:
        json_data = country.get_name()
    json_data = json.dumps(json_data, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_data, mimetype='text/javascript; charset=utf-8')

