# -*- coding: UTF-8 -*-
from django.db import models

from base_libs.middleware import get_current_language

Museum = models.get_model("museums", "Museum")


def get_published_museums(search):
    from django.db.models.functions import Lower
    language = get_current_language()
    if not search or len(search) < 1:
        return []
    request_specific_field_name = 'title_{}'.format(language)
    queryset = Museum.objects.filter(status="published").annotate(title_uni=models.Case(
        models.When(then=models.F('title_de'), **{request_specific_field_name: ''}),
        default=models.F(request_specific_field_name),
        output_field=models.CharField(),
    ))
    if search != "all":
        queryset = queryset.filter(title_uni__icontains=search.lower()).order_by(Lower("title_uni"))
    queryset = queryset.order_by(Lower("title_uni"))
    return queryset

