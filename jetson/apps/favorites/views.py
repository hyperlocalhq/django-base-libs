# -*- coding: UTF-8 -*-
from django.db import models
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.shortcuts import render_to_response

from base_libs.middleware import get_current_user
from base_libs.utils.misc import ExtendedJSONEncoder

Favorite = models.get_model("favorites", "Favorite")

from templatetags.favorites import get_favorites_count

def json_set_favorite(request, content_type_id, object_id):
    "Sets the object as a favorite for the current user"
    json = "false"
    if request.user.is_authenticated():
        content_type = ContentType.objects.get(id=content_type_id)
        instance = content_type.get_object_for_this_type(pk=object_id)
        favorite, is_created = Favorite.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            user=request.user,
            )
        if not is_created:
            favorite.delete()
        result = favorite.__dict__
        result = dict([
            (item[0], item[1])
            for item in result.items()
            if not item[0].startswith("_")
            ])
        result['action'] = is_created and "added" or "removed"
        result['count'] = get_favorites_count(instance)
        json = simplejson.dumps(
            result,
            ensure_ascii=False,
            cls=ExtendedJSONEncoder,
            )
    return HttpResponse(json, mimetype='text/javascript; charset=utf-8')
json_set_favorite = never_cache(json_set_favorite)

def favorites(request, **kwargs):
    """ 
    Displays the list of favorite objects
    """
    favorites = Favorite.objects.filter(
        user=get_current_user(),
        )
    return render_to_response(kwargs["template_name"], {
        'object_list': favorites,
    }, context_instance=RequestContext(request))    

