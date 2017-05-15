# -*- coding: UTF-8 -*-
from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.admin import ExtendedModelAdmin
from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import ObjectRelationMixinAdminForm
from base_libs.models.admin import get_admin_lang_section
from ccb.apps.tracker.models import Concern, Ticket, TicketModifications


class ConcernOptions(ExtendedModelAdmin):
    save_on_top = True
    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug', 'sort_order')}), ]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


class TicketModifications_Inline(admin.StackedInline):
    model = TicketModifications
    extra = 0


ObjectRelationAdminMixin = ObjectRelationMixinAdminOptions()


class TicketOptions(ObjectRelationAdminMixin):
    save_on_top = True
    inlines = [TicketModifications_Inline]
    list_display = (
        'concern', 'submitted_date', 'priority', 'get_submitter', 'get_content_object_display', 'status', 'modifier',
    )
    list_filter = ('status', 'concern', 'submitted_date')
    search_fields = ('description', 'concern__title', 'status',)

    fieldsets = deepcopy(ObjectRelationAdminMixin.fieldsets)
    fieldsets += [
        (None, {'fields': (
             'concern', 'description', 'client_info', 'status', 'priority', 'url', 'submitter_name', 'submitter_email',
             'modifier',
        )}),
    ]
    raw_id_fields = ["modifier"]
    related_lookup_fields = deepcopy(ObjectRelationAdminMixin.related_lookup_fields)
    related_lookup_fields.setdefault('fk', [])
    related_lookup_fields['fk'] += ["modifier"]

    def get_submitter(self, obj):
        if obj.submitter:
            return """<a href="/admin/people/person/%d/">%s</a><br />%s""" % (
                obj.submitter.profile.pk,
                obj.submitter_name,
                obj.submitter_email,
            )
        else:
            return "%s<br />%s" % (obj.submitter_name, obj.submitter_email)

    get_submitter.allow_tags = True
    get_submitter.short_description = _("Submitter")


admin.site.register(Concern, ConcernOptions)
admin.site.register(Ticket, TicketOptions)
