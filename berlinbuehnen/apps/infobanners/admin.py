# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import PublishingMixinAdminOptions

from .models import InfoBanner

class InfoBannerAdmin(ExtendedModelAdmin):
    save_on_top = True
    list_display = ["sysname", "get_content", "token", 'is_published']
    search_fields = ["sysname", "content_de", "content_en"]
    ordering = ["sysname",]
    
    fieldsets = get_admin_lang_section(_("Contents"), ["content"])
    fieldsets += [
        (None, {'fields': ("sysname",)}),
    ]
    fieldsets += PublishingMixinAdminOptions.fieldsets

    def get_content(self, obj):
        return obj.get_rendered_content()
    get_content.short_description = _("Content")
    get_content.allow_tags = True

admin.site.register(InfoBanner, InfoBannerAdmin)

