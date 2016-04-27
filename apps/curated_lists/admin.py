# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.models.admin import get_admin_lang_section
from base_libs.models.admin import ObjectRelationMixinAdminOptions

from .models import CuratedList, ListItem


class ListItemInline(admin.StackedInline):
    model = ListItem
    extra = 0
    fieldsets = ObjectRelationMixinAdminOptions().fieldsets + [
        (None, {'fields': ['sort_order']}),
    ]
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }


class CuratedListAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'get_list_item_count', 'privacy', 'sort_order']
    list_editable = ['privacy', 'sort_order']
    list_filter = ['privacy']
    inlines = [ListItemInline]

    fieldsets = get_admin_lang_section(_("Title"), ['title']) + [
        (None, {'fields': ['slug', 'owner', 'privacy', 'sort_order']}),
    ]

    prepopulated_fields = {'slug': ('title_{}'.format(settings.LANGUAGE_CODE),)}

    def get_list_item_count(self, obj):
        return obj.listitem_set.count()
    get_list_item_count.short_description = _("List Items")


admin.site.register(CuratedList, CuratedListAdmin)