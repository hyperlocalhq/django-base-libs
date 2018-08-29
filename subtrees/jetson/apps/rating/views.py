# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.conf import settings

from base_libs.utils.misc import ExtendedJSONEncoder
from jetson.apps.rating.models import UserRating

def json_set_userrating(request, content_type_id, object_id, score):
    """Sets a vote by user for an object"""
    json_str = "false"
    #if request.user.has_perm("ratings.can_rate"):
    if not request.user.is_anonymous():
        content_type = ContentType.objects.get(id=content_type_id)
        rating, is_created = UserRating.objects.get_or_create(
              content_type=content_type, 
              object_id=object_id, 
              user=request.user, 
              score=score,
        )
        #obj_to_rate = content_type.get_object_for_this_type(pk=object_id)
        #object_ratings = UserRating.get_object_rating(obj_to_rate)
        result = rating.__dict__
        #result.update(object_ratings)
        result = dict([(item[0], item[1]) for item in result.items() if not item[0].startswith("_")])
        json_str = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')

json_set_userrating = never_cache(json_set_userrating)
