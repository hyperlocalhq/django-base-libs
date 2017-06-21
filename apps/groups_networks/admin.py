# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import filebrowser.settings as filebrowser_settings

URL_FILEBROWSER_MEDIA = getattr(filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/')
from base_libs.admin.tree_editor import TreeEditor
from base_libs.admin import ExtendedStackedInline
from base_libs.models.admin import get_admin_lang_section

from kb.apps.groups_networks.models import GroupType, PersonGroup, GroupMembership


class GroupTypeOptions(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title']

    fieldsets = [(None, {'fields': ('parent',)}), ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [(None, {'fields': ('slug',)}), ]

    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


class GroupMembership_Inline(ExtendedStackedInline):
    model = GroupMembership
    list_display = ('user', 'person_group', 'role', 'title', 'activation')
    list_filter = ('person_group', 'role')
    allow_add = True
    extra = 1

    fieldsets = [
        (_("Main"), {'fields': ("user", "role"), 'classes': ["collapse open"]}),
    ]
    fieldsets += get_admin_lang_section(None, ['title'])
    fieldsets += [
        (_("Details"), {'fields': ("inviter", "is_accepted", "is_blocked", "is_contact_person", "confirmer"),
                        'classes': ["collapse open"]}),
    ]
    raw_id_fields = ("user", "inviter", "confirmer")
    autocomplete_lookup_fields = {
        'fk': ["user", "inviter", "confirmer"],
    }


class PersonGroupOptions(admin.ModelAdmin):
    list_display = ('title', 'title2', 'group_type', 'access_type', 'preferred_language', 'status')
    search_fields = ["title", "title2"]
    list_filter = ('creation_date', 'group_type', 'status', 'preferred_language')
    save_on_top = True
    prepopulated_fields = {'slug': ("title",)}
    filter_horizontal = ('creative_sectors',)
    filter_vertical = ('context_categories',)
    inlines = [GroupMembership_Inline]
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'], ],
    }
    raw_id_fields = ("organizing_institution",)
    autocomplete_lookup_fields = {
        'fk': ["organizing_institution"],
    }


admin.site.register(GroupType, GroupTypeOptions)
admin.site.register(PersonGroup, PersonGroupOptions)
