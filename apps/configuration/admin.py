from django.contrib import admin

from ccb.apps.configuration.models import SiteSettings


class SiteSettingsOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('get_site_name', '__unicode__',)


admin.site.register(SiteSettings, SiteSettingsOptions)
