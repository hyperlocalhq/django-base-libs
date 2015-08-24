# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
#from django.contrib.admin.options import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/')
Event = models.get_model("events", "Event")
EventTime = models.get_model("events", "EventTime")

class EventTime_Inline(ExtendedStackedInline):
    model = EventTime
    extra = 1
    verbose_name = _("Time")
    verbose_name_plural = _("Times")

class EventOptions(ExtendedModelAdmin):
    inlines = [EventTime_Inline]
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ['title', 'get_start_date_string', 'get_end_date_string', 'status', 'creation_date']
    list_filter = ('creation_date', 'status')

    fieldsets = get_admin_lang_section(_("Article"), ['title', 'description'])
    fieldsets += [(None, {'fields': ('slug', 'image', 'status')}),]

admin.site.register(Event, EventOptions)

