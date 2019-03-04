# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Day


def advent_calendar(request):
    qs = Day.objects.all().order_by("?")

    context = {
        'day_list': qs,
    }
    return render(request, "advent_calendar/advent_calendar.html", context)
