# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin

Person = models.get_model("people", "Person")

class PersonOptions(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = ('user', 'get_first_name', 'get_last_name', 'get_email', 'status')
    list_filter = ('status',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username', 'user__email',)

admin.site.register(Person, PersonOptions)

