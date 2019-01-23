# -*- coding: UTF-8 -*-
from copy import deepcopy
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import get_admin_lang_section

from jetson.apps.permissions.models import PerObjectGroup
from jetson.apps.permissions.models import RowLevelPermission

ObjectRelationAdminMixin = ObjectRelationMixinAdminOptions()
OwnerAdminMixin = ObjectRelationMixinAdminOptions(
    prefix="owner", prefix_verbose=_("Owner")
)


class RowLevelPermissionOptions(ObjectRelationAdminMixin, OwnerAdminMixin):
    save_on_top = True
    list_display = (
        '__unicode__', 'get_owner_content_object_display',
        'get_content_object_display'
    )
    fieldsets = deepcopy(OwnerAdminMixin.fieldsets)
    fieldsets += deepcopy(ObjectRelationAdminMixin.fieldsets)
    fieldsets += [
        (
            _("Permission"), {
                'fields': (
                    'permission',
                    'negative',
                ),
                'classes': ('grp-collapse grp-open', ),
            }
        ),
    ]
    related_lookup_fields = {
        'generic':
            ObjectRelationAdminMixin.related_lookup_fields['generic'] +
            OwnerAdminMixin.related_lookup_fields['generic'],
    }


class PerObjectGroupOptions(ObjectRelationAdminMixin):
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    list_filter = [
        'title',
    ]
    fieldsets = get_admin_lang_section(_("Title"), [
        'title',
    ])
    fieldsets += deepcopy(ObjectRelationAdminMixin.fieldsets)
    fieldsets += [
        (None, {
            'fields': ('sysname', 'users'),
        }),
    ]
    raw_id_fields = ["users"]
    related_lookup_fields = {
        'generic': ObjectRelationAdminMixin.related_lookup_fields['generic'],
        'm2m': ["users"],
    }


admin.site.register(PerObjectGroup, PerObjectGroupOptions)
admin.site.register(RowLevelPermission, RowLevelPermissionOptions)
