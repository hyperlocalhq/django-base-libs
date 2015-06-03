# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from base_libs.admin import ExtendedModelAdmin

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from jetson.apps.utils.models import XFieldList

Document = models.get_model("resources", "Document")

class DocumentOptions(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = XFieldList(['title_', 'creation_date', 'status'])
    list_filter = ('creation_date', 'status')
    search_fields = XFieldList(['title_'])

admin.site.register(Document, DocumentOptions)

