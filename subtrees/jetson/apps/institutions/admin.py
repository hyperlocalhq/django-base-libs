# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'filebrowser/'
)
from base_libs.admin import ExtendedModelAdmin
from base_libs.utils.misc import get_related_queryset
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

LegalForm = models.get_model("institutions", "LegalForm")
InstitutionType = models.get_model("institutions", "InstitutionType")
Institution = models.get_model("institutions", "Institution")


class LegalFormOptions(ExtendedModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', 'sort_order')
        }),
    ]
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class InstitutionTypeOptions(TreeEditor):

    save_on_top = True
    list_display = ['actions_column', 'indented_short_title']

    fieldsets = [
        (None, {
            'fields': ('parent', )
        }),
    ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', )
        }),
    ]

    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class InstitutionOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = ('title', 'slug', 'creation_date', 'status')
    list_filter = (
        'creation_date',
        'status',
    )
    search_fields = ('title', 'title2', 'slug')
    actions = ["publish"]

    def publish(self, request, queryset):
        for ev in queryset:
            ev.status = "published"
            ev.save()

    publish.short_description = _("Publish selected institutions")


admin.site.register(InstitutionType, InstitutionTypeOptions)
admin.site.register(Institution, InstitutionOptions)
admin.site.register(LegalForm, LegalFormOptions)
