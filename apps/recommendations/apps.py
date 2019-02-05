# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RecommendationsConfig(AppConfig):
    name = 'ccb.apps.recommendations'
    verbose_name = _("Recommendations")

    def ready(self):
        pass
