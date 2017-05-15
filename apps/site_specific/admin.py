# -*- coding: UTF-8 -*-
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import get_admin_lang_section

from ccb.apps.site_specific.models import ContextItem, ClaimRequest, Visit


class VisitAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ["session_key", "user", "ip_address", "user_agent", "last_activity"]
    readonly_fields = [
        "session_key", "user", "ip_address", "user_agent", "last_activity"
    ]


ObjectRelationAdminMixin = ObjectRelationMixinAdminOptions()


class ContextItemOptions(ObjectRelationAdminMixin):
    list_display = ['get_title', 'content_type', 'slug', 'creation_date', 'status']
    list_filter = ('creation_date', 'status', 'content_type')
    save_on_top = True
    filter_vertical = ('context_categories',)
    search_fields = ["title_de", "title_en", "slug", "description_de", "description_en", "object_id"]

    fieldsets = [
        (_("Related object"), {
            'fields': ("content_type", "object_id"),
            'description': _("The data for context items is automatically filled in from related people, institutions, documents, events, or groups."),
        }),
    ]
    fieldsets += get_admin_lang_section(_("Title and Description"), ['title', 'description'])
    fieldsets += [
        (_("Details"), {'fields': ("slug", "additional_search_data")}),
        (_("Categories"), {'fields': ("creative_sectors", "context_categories", "categories", "locality_type")}),
        (_("Status"), {'fields': ("status",)}),
    ]

    readonly_fields = [
        "content_type", "object_id",
        "slug", "title_de", "title_en",
        "description_de", "description_en",
        "additional_search_data",
        "creative_sectors", "context_categories", "categories",
        "locality_type", "status",
    ]


class ClaimRequestOptions(ObjectRelationAdminMixin):
    save_on_top = True
    list_display = (
        'created_date',
        'get_content_object_display',
        'get_claimer',
        'status',
        'get_approve_action',
        'get_deny_action',
    )
    list_filter = ('status', 'created_date')
    search_fieldsets = ('status', 'user',)
    fieldsets = [(_('Change claim'), {
        'fields': (
            'user',
            'name',
            'email',
            'role',
            'comments',
        ),
    })]
    fieldsets += ObjectRelationAdminMixin.fieldsets
    fieldsets += [(_('Phone'), {'classes': ('one-line',),
        'fields': (
            (
                'phone_country',
                'phone_area',
                'phone_number'
            ),
            'best_time_to_call',
        ),
    })]
    raw_id_fields = ["user"]
    related_lookup_fields = deepcopy(ObjectRelationAdminMixin.related_lookup_fields)
    related_lookup_fields.setdefault('fk', [])
    related_lookup_fields['fk'] += ["user"]




admin.site.register(ContextItem, ContextItemOptions)
admin.site.register(ClaimRequest, ClaimRequestOptions)
admin.site.register(Visit, VisitAdmin)
