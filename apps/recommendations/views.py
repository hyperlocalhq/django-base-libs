# -*- coding: UTF-8 -*-
import json

from django.db import models
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from base_libs.utils.misc import ExtendedJSONEncoder

Recommendation = models.get_model("recommendations", "Recommendation")


def json_set_recommendation(request, content_type_id, object_id):
    """Sets the object as a recommendation for the current user"""
    json_str = "false"
    if request.user.is_authenticated():
        content_type = ContentType.objects.get(id=content_type_id)
        recommendation, is_created = Recommendation.objects.get_or_create(
            content_type=content_type,
            object_id=object_id,
            user=request.user,
        )
        if not is_created:
            recommendation.delete()
        result = recommendation.__dict__
        result = dict(
            [
                (item[0], item[1])
                for item in result.items() if not item[0].startswith("_")
            ]
        )
        result['action'] = is_created and "added" or "removed"
        json_str = json.dumps(
            result,
            ensure_ascii=False,
            cls=ExtendedJSONEncoder,
        )
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')


json_set_recommendation = never_cache(json_set_recommendation)


def recommendations(request, **kwargs):
    """ 
    Displays the list of recommendation objects
    """
    recommendations = Recommendation.objects.filter(user=get_current_user(), )
    return render_to_response(
        kwargs["template_name"], {
            'object_list': recommendations,
        },
        context_instance=RequestContext(request)
    )
