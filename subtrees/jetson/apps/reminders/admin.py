# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin

from base_libs.models.admin import ObjectRelationMixinAdminOptions

Reminder = models.get_model("reminders", "Reminder")


class ReminderOptions(ObjectRelationMixinAdminOptions()):
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    fieldsets = []


admin.site.register(Reminder, ReminderOptions)
