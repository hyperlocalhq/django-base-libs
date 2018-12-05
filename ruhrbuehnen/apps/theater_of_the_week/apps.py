# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TheaterOfTheWeekConfig(AppConfig):
    name = 'ruhrbuehnen.apps.theater_of_the_week'
    verbose_name = _("Theaters of the week")
