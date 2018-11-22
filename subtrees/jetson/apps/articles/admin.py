# -*- coding: UTF-8 -*-
from django import forms
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.models import PublishingMixinAdminOptions
from base_libs.utils.misc import get_installed
from base_libs.admin.tree_editor import TreeEditor

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/'
)
ArticleType = models.get_model("articles", "ArticleType")
Article = models.get_model("articles", "Article")

ARTICLES_HAVE_TYPES = get_installed("articles.settings.ARTICLES_HAVE_TYPES")


class ArticleTypeOptions(TreeEditor):
    save_on_top = True
    search_fields = ('title', )
    list_display = ['indented_short_title', 'actions_column']
    list_filter = ("creation_date", )

    fieldsets = [
        (None, {
            'fields': ('slug', )
        }),
    ]
    fieldsets += get_admin_lang_section(_("Contents"), [
        'title',
    ])
    prepopulated_fields = {
        "slug": ("title_%s" % settings.LANGUAGE_CODE, ),
    }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        if ARTICLES_HAVE_TYPES:
            self.fields['article_type'].required = True


class ArticleOptions(ExtendedModelAdmin):
    form = ArticleForm
    save_on_top = True

    list_display = [
        'id', 'title', 'author', 'status', 'published_from', 'published_till',
        'views', 'article_type', 'language'
    ]
    list_display_links = ['title']
    list_filter = (
        'published_from', 'published_till', 'status', 'is_featured',
        'article_type', 'language'
    )
    search_fields = ('title', 'description', 'content', 'author__username')

    fieldsets = []
    if ARTICLES_HAVE_TYPES:
        fieldsets += [
            (None, {
                'fields': ('article_type', )
            }),
        ]
    fieldsets += [
        (
            _("Article"), {
                'fields':
                    ('title', 'subtitle', 'content', 'description', 'language')
            }
        )
    ]
    fieldsets += [
        (None, {
            'fields': ('slug', 'is_featured')
        }),
    ]
    fieldsets += PublishingMixinAdminOptions.fieldsets
    fieldsets += [
        (
            _('Additional Content'), {
                'classes': ("grp-collapse grp-closed", ),
                'fields':
                    [
                        'image',
                        (
                            _("Description"), {
                                'fields': ['image_title', 'image_description']
                            }
                        )
                    ]
            }
        ),
    ]
    prepopulated_fields = {
        "slug": ("title", ),
    }


if ARTICLES_HAVE_TYPES:
    admin.site.register(ArticleType, ArticleTypeOptions)
admin.site.register(Article, ArticleOptions)
