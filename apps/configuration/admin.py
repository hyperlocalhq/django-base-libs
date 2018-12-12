# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import MetaTagsMixinAdminOptions

from museumsportal.apps.configuration.models import SiteSettings

class SiteSettingsOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('get_site_name','__unicode__',)
    
    fieldsets = (
        (None, {'fields': ("site", "registration_type", "login_by_email")}),
        )
    
    fieldsets += MetaTagsMixinAdminOptions.fieldsets
    
    fieldsets += (
        (_("Advanced"), {'fields': ("extra_head", "extra_body"), 'classes': ("grp-collapse grp-closed",)}),
        )

admin.site.register(SiteSettings, SiteSettingsOptions)

