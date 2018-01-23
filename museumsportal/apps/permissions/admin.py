# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm
from base_libs.models.admin import get_admin_lang_section

from museumsportal.apps.permissions.models import PerObjectGroup
from museumsportal.apps.permissions.models import RowLevelPermission

class RowLevelPermissionAdminForm(ObjectRelationMixinAdminForm(), ObjectRelationMixinAdminForm(prefix="owner")):
    pass

class RowLevelPermissionOptions(ObjectRelationMixinAdminOptions(), ObjectRelationMixinAdminOptions(prefix="owner", prefix_verbose=_("Owner"))):
    form = RowLevelPermissionAdminForm
    save_on_top = True
    list_display = ('__unicode__', 'get_owner_content_object_display', 'get_content_object_display')
    fieldsets = ObjectRelationMixinAdminOptions(prefix="owner", prefix_verbose=_("Owner")).fieldsets
    fieldsets += ObjectRelationMixinAdminOptions().fieldsets
    fieldsets += [
        (_("Permission"), {
            'fields': ('permission', 'negative',),
            'classes': ('grp-collapse grp-open',),
            }),
        ]

class PerObjectGroupAdminForm(ObjectRelationMixinAdminForm()):
    pass

class PerObjectGroupOptions(ObjectRelationMixinAdminOptions()):
    form = PerObjectGroupAdminForm
    save_on_top = True
    list_display = ('__unicode__', 'get_content_object_display')
    list_filter = ['title',]
    fieldsets = get_admin_lang_section(
        _("Title"),
        ['title',],
        )
    fieldsets += ObjectRelationMixinAdminOptions().fieldsets
    fieldsets += [
        (None, {
            'fields': ('sysname', 'users'),
            }),
        ]
    filter_horizontal = ("users",)
    

admin.site.register(PerObjectGroup, PerObjectGroupOptions)
admin.site.register(RowLevelPermission, RowLevelPermissionOptions)

