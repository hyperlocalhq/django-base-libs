# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import PartnerCategory


def partner_list(request):
    qs = PartnerCategory.objects.filter(status="published").order_by('sort_order')

    return render(
        request,
        "partners/partner_list.html",
        {'partner_categories': qs},
    )
