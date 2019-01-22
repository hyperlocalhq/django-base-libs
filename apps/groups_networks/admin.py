# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'filebrowser/'
)
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

GroupType = models.get_model("groups_networks", "GroupType")
PersonGroup = models.get_model("groups_networks", "PersonGroup")
GroupMembership = models.get_model("groups_networks", "GroupMembership")


class GroupTypeOptions(TreeEditor):
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


class GroupMembership_Inline(ExtendedStackedInline):
    model = GroupMembership
    list_display = ('user', 'person_group', 'role', 'title', 'activation')
    list_filter = ('person_group', 'role')
    allow_add = True
    extra = 0

    fieldsets = [
        (
            _("Main"), {
                'fields': ("user", "role"),
                'classes': ["grp-collapse grp-open"]
            }
        ),
    ]
    fieldsets += get_admin_lang_section(None, ['title'])
    fieldsets += [
        (
            _("Details"), {
                'fields':
                    (
                        "inviter", "is_accepted", "is_blocked",
                        "is_contact_person", "confirmer"
                    ),
                'classes': ["grp-collapse grp-open"]
            }
        ),
    ]
    raw_id_fields = ("user", "inviter", "confirmer")
    autocomplete_lookup_fields = {
        'fk': ["user", "inviter", "confirmer"],
    }


class PersonGroupOptions(ExtendedModelAdmin):
    list_display = (
        'title', 'title2', 'group_type', 'access_type', 'preferred_language',
        'status'
    )
    search_fields = ["title", "title2"]
    list_filter = (
        'creation_date', 'group_type', 'status', 'preferred_language'
    )
    save_on_top = True
    fieldsets = [
        (
            _("Main"), {
                'fields':
                    ("content_type", "object_id", "title", "title2", "slug"),
                'classes': ["grp-collapse grp-open"]
            }
        ),
        (
            _("Details"), {
                'fields':
                    ("organizing_institution", "preferred_language", "image"),
                'classes': ["grp-collapse grp-closed"]
            }
        ),
        (
            _("Configuration"), {
                'fields':
                    (
                        "group_type",
                        "access_type",
                        "is_by_invitation",
                        "is_by_confirmation",
                    ),
                'classes': ["grp-collapse grp-closed"]
            }
        ),
    ]
    fieldsets += get_admin_lang_section(
        _("Description"), [
            'description',
        ], False
    )
    fieldsets += [
        (
            _("Categories"), {
                'fields': ("context_categories", ),
                'classes': ["grp-collapse grp-closed"]
            }
        ),
        (
            _("Status"), {
                'fields': ("status", ),
                'classes': ["grp-collapse grp-closed"]
            }
        ),
    ]

    prepopulated_fields = {'slug': ("title", )}
    filter_vertical = ('context_categories', )
    inlines = [GroupMembership_Inline]
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'], ],
    }
    raw_id_fields = ("organizing_institution", )
    autocomplete_lookup_fields = {
        'fk': ["organizing_institution"],
    }


admin.site.register(GroupType, GroupTypeOptions)
admin.site.register(PersonGroup, PersonGroupOptions)
