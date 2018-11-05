# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.models.admin import get_admin_lang_section
from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.admin import ExtendedModelAdmin, ExtendedStackedInline

from jetson.apps.structure.models import Category
from .models import CuratedList, ListOwner, ListItem


class ListItemInline(ExtendedStackedInline):
    model = ListItem
    extra = 0
    sortable_field_name = "sort_order"
    fieldsets = (
        ObjectRelationMixinAdminOptions().fieldsets +
        get_admin_lang_section(_("Title and Description"), ['title', 'description']) + [
            (None, {'fields': ['sort_order']}),
        ]
    )
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }


class ListOwnerInline(admin.StackedInline):
    model = ListOwner
    extra = 0
    fieldsets = ObjectRelationMixinAdminOptions(prefix="owner").fieldsets
    autocomplete_lookup_fields = {
        'generic': [['owner_content_type', 'owner_object_id']],
    }

class TopLevelCategoryListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Categories')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            (cat.pk, cat.title)
            for cat in Category.objects.filter(level=0)
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            cat = get_object_or_404(Category, pk=self.value())
            return queryset.filter(categories__tree_id=cat.tree_id)



class CuratedListAdmin(ExtendedModelAdmin):
    list_display = ['title', 'get_list_owners', 'get_list_item_count', 'privacy', 'is_featured', 'sort_order']
    list_editable = ['privacy', 'is_featured', 'sort_order']
    list_filter = ['privacy', 'is_featured', TopLevelCategoryListFilter]

    fieldsets = get_admin_lang_section(_("Title and Description"), ['title', 'description']) + [
        (None, {'fields': ['slug', 'image', 'categories']}),
        (_("Publishing"), {'fields': ['privacy', 'is_featured', 'sort_order']}),
    ]

    prepopulated_fields = {'slug': ('title_{}'.format(settings.LANGUAGE_CODE),)}
    filter_horizontal = ['categories']
    inlines = [ListOwnerInline, ListItemInline]

    def get_list_owners(self, obj):
        return ',<br />'.join([force_text(owner.owner_content_object) for owner in obj.listowner_set.all()])
    get_list_owners.short_description = _("Owners")
    get_list_owners.allow_tags = True

    def get_list_item_count(self, obj):
        return obj.listitem_set.count()
    get_list_item_count.short_description = _("List Items")


admin.site.register(CuratedList, CuratedListAdmin)