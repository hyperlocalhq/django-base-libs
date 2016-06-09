# -*- coding: utf-8 -*-
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.context_processors import prev_next_processor

from .models import Location


def location_list_map(request):
    qs = Location.objects.filter(status="published")

    extra_context = {}

    return object_list(
        request,
        queryset=qs,
        template_name="museumssummer/location_list_map.html",
        paginate_by=200,
        extra_context=extra_context,
        httpstate_prefix="location_list_map",
        context_processors=(prev_next_processor,),
    )


def location_detail_ajax(request, slug):
    qs = Location.objects.filter(status="published")
    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="museumssummer/location_detail_ajax_map.html",
        context_processors=(prev_next_processor,),
    )
