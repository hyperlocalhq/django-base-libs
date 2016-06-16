# -*- coding: utf-8 -*-
from django.contrib import admin
from cms.extensions import TitleExtensionAdmin

from .models import OpenGraph


class OpenGraphAdmin(TitleExtensionAdmin):
    pass

admin.site.register(OpenGraph, OpenGraphAdmin)