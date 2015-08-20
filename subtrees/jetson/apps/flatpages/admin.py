# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.db import models

from base_libs.models.admin import get_admin_lang_section
from base_libs.models.admin import ContentBaseMixinAdminOptions
from base_libs.models.admin import PublishingMixinAdminOptions

from filebrowser.settings import URL_FILEBROWSER_MEDIA

FlatPage = models.get_model("flatpages", "FlatPage")

class FlatPageOptions(ContentBaseMixinAdminOptions):
    list_filter = ('sites', 'template_name')
    search_fieldsets = ['url', 'title']
    list_display = ['id', 'title', 'url', 'template_name', 'is_published' ]
    list_display_links = ('id', 'title')
    ordering = ( 'title', 'template_name', 'url')
    search_fields = ('title',)

    image_fields = ['image'] + get_admin_lang_section(
        _("Image Properties"),
        ['image_title', 'image_description'],
        default_expanded=False,
        )

    fieldsets = get_admin_lang_section(
        _("Content"),
        ['title', 'short_title', 'content'],
        )
    fieldsets += [
        (None, {
            'fields': ('url', 'sites',),
            }),
        ]
    fieldsets += PublishingMixinAdminOptions.fieldsets
    
    fieldsets += [
        (_("Image"), {
            'classes': ("grp-collapse grp-closed",),                                             
            'fields': image_fields,
            }),
        ]
        
    fieldsets += [
        (_("Advanced"), {
            'classes': ("grp-collapse grp-closed",),                                             
            'fields': ('template_name', 'enable_comments', 'registration_required'),
            }),
        ]
    
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )

admin.site.register(FlatPage, FlatPageOptions)

