# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from models import Festival
from models import Image


class ImageInline(ExtendedStackedInline):
    model = Image
    extra = 0
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class FestivalAdmin(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )

    fieldsets = get_admin_lang_section(_("Title"), ['title', 'subtitle', 'description',])
    fieldsets += [(None, {'fields': ('slug', )}),]
    fieldsets += [(_("Dates"), {'fields': ('start', 'end', )}),]
    fieldsets += [(_("Contacts"), {'fields': ('website', )}),]
    fieldsets += [(_("Status"), {'fields': ('status',)}),]

    inlines = [ImageInline]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

admin.site.register(Festival, FestivalAdmin)