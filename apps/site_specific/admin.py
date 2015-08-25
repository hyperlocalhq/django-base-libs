# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm

from ccb.apps.site_specific.models import ContextItem, ClaimRequest, Visit


class VisitAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ["session_key", "user", "ip_address", "user_agent", "last_activity"]


class ContextItemOptions(ObjectRelationMixinAdminOptions()):
    list_display = ['title', 'creation_date', 'status']
    list_filter = ('creation_date', 'status', 'content_type')
    search_fieldsets = ['title', 'description']
    save_on_top = True
    filter_vertical = ('context_categories',)


class ClaimRequestAdminForm(ObjectRelationMixinAdminForm()):
    pass


class ClaimRequestOptions(ObjectRelationMixinAdminOptions()):
    form = ClaimRequestAdminForm
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
    }
                  ), ] + ObjectRelationMixinAdminOptions().fieldsets + [(_('Phone'), {'classes': ('one-line',),
                                                                                      'fields': (
                                                                                          (
                                                                                              'phone_country',
                                                                                              'phone_area',
                                                                                              'phone_number'),
                                                                                          'best_time_to_call',
                                                                                      ),
                                                                                      }
                                                                         ), ]


admin.site.register(ContextItem, ContextItemOptions)
admin.site.register(ClaimRequest, ClaimRequestOptions)
admin.site.register(Visit, VisitAdmin)
