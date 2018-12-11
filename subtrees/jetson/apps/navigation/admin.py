# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin.tree_editor import TreeEditor

from jetson.apps.navigation.models import NavigationLink

### Normal Navigation Admin Settings ###


class NavigationLinkOptions(
    TreeEditor,
    ObjectRelationMixinAdminOptions(prefix_verbose=_("Linked Object"))
):
    description = _("Each item can be either a link or a group of links.")
    save_on_top = True
    list_display = [
        'actions_column',
        'indented_short_title',
        'get_link_display',
        'is_shown_for_visitors',
        'is_shown_for_users',
        'sysname',
    ]
    search_fields = ['title', 'link_url', 'sysname']

    list_filter = (
        'site', 'is_shown_for_visitors', 'is_shown_for_users', 'is_group'
    )

    fieldsets = [(None, {'fields': ('site', 'parent')})]
    fieldsets += get_admin_lang_section(_("Title"), ['title'], True)
    fieldsets += [
        (
            _("Link"), {
                'fields': ('content_type', 'object_id', 'link_url'),
                'description':
                    _(
                        "If this item is a link, choose a target object or enter a URL."
                    ),
            }
        )
    ]
    fieldsets += [
        (
            _("Group"), {
                'fields': (
                    'is_group',
                    'is_group_name_shown',
                ),
                'description':
                    _(
                        "If this item is a group of links, check 'Group of links' below."
                    ),
            }
        )
    ]
    fieldsets += get_admin_lang_section(
        _("Description"), ['description'], False
    )
    fieldsets += [
        (
            _("Availability"), {
                'fields':
                    (
                        'is_shown_for_visitors',
                        'is_shown_for_users',
                        'is_login_required',
                        'is_promoted',
                    )
            }
        )
    ]
    fieldsets += [
        (
            _("Advanced"), {
                'fields': ('sysname', 'related_urls'),
                'classes': ('grp-collapse grp-closed', ),
            }
        )
    ]

    def get_link_display(self, obj):
        if obj.content_object:
            return obj.content_object.get_url_path()
        if ("{%" in obj.link_url) or ("{{" in obj.link_url):
            return _("(depends on the context)")
        if obj.link_url:
            return obj.link_url
        if obj.is_group:
            return _("(group of links)")
        return _("(broken link)")

    get_link_display.short_description = _("Link target")


admin.site.register(NavigationLink, NavigationLinkOptions)
