# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CuratedListsAppConfig(AppConfig):
    name = "kb.apps.curated_lists"
    verbose_name = _("Curated Lists")
