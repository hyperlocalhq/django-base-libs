from ccb.apps.configuration.models import SiteSettings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class SiteSettingsOptions(admin.ModelAdmin):
    save_on_top = True
    list_display = ('get_site_name','__unicode__',)

admin.site.register(SiteSettings, SiteSettingsOptions)

