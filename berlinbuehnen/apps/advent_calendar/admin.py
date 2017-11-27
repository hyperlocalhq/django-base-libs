# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.admin import ExtendedModelAdmin
from base_libs.models import get_admin_lang_section
from jetson.apps.image_mods.templatetags.image_modifications import modified_path
from .models import Day


class DayAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ["day", "get_preview_image", "get_image", "title", "get_status"]
    search_fields = ["title", "description"]
    fieldsets = [
        (None, {'fields': ["day"]}),
    ]
    fieldsets += [
        (_("Images"), {'fields': ["preview_image", "image"]}),
    ]
    fieldsets += get_admin_lang_section(_("Content"), ['title', 'description',])

    def get_status(self, obj):
        if obj.is_past():
            return _("Opened")
        elif obj.is_present():
            return _("Openable")
        elif obj.is_future():
            return _("Locked")
        return ""
    get_status.short_description = _("Status Today")

    def get_preview_image(self, obj):
        if not obj.preview_image:
            return ""
        return """<img src="{}{}" alt="" width="60" height="60" />""".format(
            settings.MEDIA_URL,
            modified_path(obj.image, "filebrowser_thumbnail")
        )
    get_preview_image.short_description = _("Preview Image")
    get_preview_image.allow_tags = True

    def get_image(self, obj):
        if not obj.image:
            return ""
        return """<img src="{}{}" alt="" width="60" height="60" />""".format(
            settings.MEDIA_URL,
            modified_path(obj.image, "filebrowser_thumbnail")
        )
    get_image.short_description = _("Active Image")
    get_image.allow_tags = True

admin.site.register(Day, DayAdmin)