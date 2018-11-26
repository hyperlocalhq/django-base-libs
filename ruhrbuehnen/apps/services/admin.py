# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

from .models import Banner


class BannerAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = [
        "title", "subtitle", "creation_date", "modified_date", "header_bg_color"
    ]
    list_filter = ["creation_date", "modified_date"]

    fieldsets = get_admin_lang_section(
        _("Title"), ["title", "subtitle", "short_description"]
    )
    fieldsets += [
        (_("Details"), {
            'fields': ("header_bg_color", "header_icon")
        }),
    ]


admin.site.register(Banner, BannerAdmin)
