# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin.tree_editor import TreeEditor

import filebrowser.settings as filebrowser_settings

URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/'
)
from jetson.apps.structure.models import Vocabulary
from jetson.apps.structure.models import Term
from jetson.apps.structure.models import ContextCategory
from jetson.apps.structure.models import Category


class VocabularyOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = [
        'title', 'sysname', 'hierarchy', 'link_add_term', 'link_change_terms'
    ]

    fieldsets = get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', )
        }),
    ]
    fieldsets += get_admin_lang_section(_("Body"), ['body'])
    fieldsets += [
        (None, {
            'fields': (
                'image',
                'hierarchy',
            )
        }),
    ]

    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class TermOptions(TreeEditor):
    save_on_top = True
    list_display = [
        'actions_column', 'indented_short_title', 'vocabulary', 'sysname'
    ]
    list_filter = ('vocabulary', )

    fieldsets = [
        (None, {
            'fields': ('vocabulary', 'parent')
        }),
    ]
    fieldsets += get_admin_lang_section(_("Title"), ['title'])
    fieldsets += [
        (None, {
            'fields': ('slug', )
        }),
    ]
    fieldsets += get_admin_lang_section(_("Body"), ['body'])
    fieldsets += [
        (None, {
            'fields': ('image', )
        }),
    ]

    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class ContextCategoryOptions(TreeEditor):
    save_on_top = True
    list_display = [
        'actions_column', 'indented_short_title', 'is_applied4person',
        'is_applied4institution', 'is_applied4document', 'is_applied4event',
        'is_applied4persongroup'
    ]
    # list_filter = ['parent','is_applied4person', 'is_applied4institution', 'is_applied4document', 'is_applied4event', 'is_applied4persongroup']
    list_filter = [
        'is_applied4person', 'is_applied4institution', 'is_applied4document',
        'is_applied4event', 'is_applied4persongroup'
    ]

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
    fieldsets += get_admin_lang_section(_("Body"), ['body'])
    fieldsets += [
        (None, {
            'fields': ('image', )
        }),
    ]
    fieldsets += [
        (
            'Related', {
                'classes': ('grp-collapse grp-closed', 'float-checkbox'),
                'fields':
                    (
                        (
                            'is_applied4person', 'is_applied4institution',
                            'is_applied4document'
                        ),
                        ('is_applied4event', 'is_applied4persongroup'),
                    )
            }
        ),
    ]

    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class CategoryOptions(TreeEditor):
    save_on_top = True
    list_display = ['actions_column', 'indented_short_title', 'slug']

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


admin.site.register(Vocabulary, VocabularyOptions)
admin.site.register(Term, TermOptions)
admin.site.register(ContextCategory, ContextCategoryOptions)
admin.site.register(Category, CategoryOptions)
