# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.admin.tree_editor import TreeEditor
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin

from jetson.apps.location.models import Address, Locality, Geoposition, LocalityType


class Locality_Inline(admin.StackedInline):
    model = Locality
    extra = 0
    max_num = 1


class Geoposition_Inline(admin.StackedInline):
    model = Geoposition
    extra = 0
    max_num = 1


class AddressAdmin(ExtendedModelAdmin):
    inlines = [Locality_Inline, Geoposition_Inline]
    search_fields = ['city', 'street_address', 'street_address2', 'street_address3', 'postal_code']
    save_on_top = True


class LocalityTypeAdmin(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', 'slug']

    fieldsets = [(None, {'fields': ('parent',)}), ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}), ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


admin.site.register(Address, AddressAdmin)
admin.site.register(LocalityType, LocalityTypeAdmin)
