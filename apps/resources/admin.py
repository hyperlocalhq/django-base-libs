# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings

from filebrowser.settings import URL_FILEBROWSER_MEDIA

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from jetson.apps.utils.models import XFieldList

from ccb.apps.resources.models import Medium
from ccb.apps.resources.models import DocumentType
from ccb.apps.resources.models import Document

class DocumentTypeOptions(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title']
    
    fieldsets = [(None, {'fields': ('parent',)}),]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}),]
    
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

class MediumOptions(ExtendedModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}),]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}

class DocumentOptions(admin.ModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    list_display = XFieldList(['title_', 'document_type', 'url_link', 'status', 'is_featured'])
    list_filter = ('document_type', 'medium', 'status', 'is_featured', 'creative_sectors', 'context_categories')
    search_fields = XFieldList(['title_'])

admin.site.register(Medium, MediumOptions)
admin.site.register(DocumentType, DocumentTypeOptions)
admin.site.register(Document, DocumentOptions)

