# -*- coding: UTF-8 -*-

from django import forms
from django.db import models
from django import template
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.admin import helpers
from django.contrib.admin.util import model_ngettext
from django.utils.encoding import force_unicode

import filebrowser.settings as filebrowser_settings

URL_FILEBROWSER_MEDIA = getattr(filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/')
from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

Person = models.get_model("people", "Person")
IndividualType = models.get_model("people", "IndividualType")


class IndividualTypeOptions(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title']

    fieldsets = [(None, {'fields': ('parent',)}), ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}), ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


class PersonOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('user', 'get_first_name', 'get_last_name', 'get_email', 'status')
    list_filter = ('status',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username', 'user__email',)


admin.site.register(IndividualType, IndividualTypeOptions)
admin.site.register(Person, PersonOptions)
