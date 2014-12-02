# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section

from models import Sponsor


class SponsorAdmin(ExtendedModelAdmin):

    save_on_top = True
    list_display = ['title', 'icon']

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('image', 'website', 'status')}),]

    def icon(self, obj):
        return """<img alt="" src="%s%s" />""" % (settings.MEDIA_URL, obj.image.path)
    icon.allow_tags = True

admin.site.register(Sponsor, SponsorAdmin)
