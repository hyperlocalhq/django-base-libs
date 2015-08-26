# -*- coding: UTF-8 -*-
from django import forms
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.models import PublishingMixinAdminOptions
from base_libs.utils.misc import get_installed
from base_libs.admin.tree_editor import TreeEditor
import filebrowser.settings as filebrowser_settings

URL_FILEBROWSER_MEDIA = getattr(filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/')
Article = models.get_model("articles", "Article")
ArticleType = models.get_model("articles", "ArticleType")
ArticleContentProvider = models.get_model("articles", "ArticleContentProvider")
ArticleImportSource = models.get_model("external_services", "ArticleImportSource")

ARTICLES_HAVE_TYPES = get_installed("articles.settings.ARTICLES_HAVE_TYPES")


class ArticleTypeOptions(TreeEditor):
    save_on_top = True
    search_fields = ('title',)
    list_display = ['actions_column', 'indented_short_title']
    list_filter = ("creation_date",)

    fieldsets = [(None, {'fields': ('parent', 'slug',)}), ]
    fieldsets += get_admin_lang_section(_("Contents"), ['title', ])
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['article_type'].required = True
        self.fields['language'].required = True


class ArticleOptions(ExtendedModelAdmin):
    form = ArticleForm

    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
        )

    save_on_top = True

    list_display = ['id', 'title', 'author', 'status', 'published_from', 'published_till', 'views', 'article_type',
                    'language']
    list_display_links = ['title']
    list_filter = (
        'sites', 'content_provider', 'published_from', 'published_till', 'status', 'is_featured', 'article_type',
        'language')
    search_fields = ('title', 'description', 'content', 'author__username')

    fieldsets = [(None, {'fields': ('article_type', 'creative_sectors')}), ]
    fieldsets += [(_("Article"), {'fields': ['title', 'subtitle', 'content', 'description', 'language']})]
    fieldsets += [(None, {'fields': ('slug', 'sites', 'is_featured',), }), ]
    fieldsets += [(_('Import'), {'fields': ('content_provider', 'external_url', 'is_excerpt')}), ]
    fieldsets += PublishingMixinAdminOptions.fieldsets
    fieldsets += [(
        _('Additional Content'),
        {
            'classes': ("collapse closed",),
            'fields': [
                'image',
                (
                    _("Description"),
                    {
                        'fields': [
                            'image_title',
                            'image_description'
                        ]
                    }
                )
            ],
        }
    )]

    prepopulated_fields = {"slug": ("title",), }


class ArticleImportSource_Inline(ExtendedStackedInline):
    model = ArticleImportSource
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'sysname', 'content_provider', 'are_excerpts')
        }),
        (_("Defaults"), {
            'fields': ('default_sites', 'default_creative_sectors', 'default_status')
        }),
    )


class ArticleContentProviderOptions(ExtendedModelAdmin):
    list_display = ['title', 'url']
    fieldsets = [(None, {'fields': ('title', 'url')}), ]
    inlines = [ArticleImportSource_Inline]


if ARTICLES_HAVE_TYPES:
    admin.site.register(ArticleType, ArticleTypeOptions)
admin.site.register(Article, ArticleOptions)
admin.site.register(ArticleContentProvider, ArticleContentProviderOptions)
