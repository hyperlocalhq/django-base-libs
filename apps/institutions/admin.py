# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.utils.misc import get_related_queryset

Institution = models.get_model("institutions", "Institution")

class InstitutionOptions(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('title', 'slug', 'creation_date', 'status')
    list_filter = ('creation_date', 'status',)
    search_fields = ('title', 'title2', 'slug')
    actions = ["publish"]

    def publish(self, request, queryset):
        for ev in queryset:
            ev.status = "published"
            ev.save()
    publish.short_description = _("Publish selected institutions")


admin.site.register(Institution, InstitutionOptions)

