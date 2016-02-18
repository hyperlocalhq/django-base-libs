# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from base_libs.models import MultiSiteContainerMixinAdminForm
from base_libs.models import MultiSiteContainerMixinAdminOptions
from base_libs.models import PublishingMixinAdminOptions
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline

from ccb.apps.blog.models import Blog, Post


class Post_Inline(ExtendedStackedInline):
    model = Post
    fieldsets = [
        (None, {
            'fields': ('title', 'slug', 'body', 'tags')
        }),
    ]
    fieldsets += PublishingMixinAdminOptions.fieldsets
    extra = 0
    prepopulated_fields = {'slug': ('title',), }


class BlogAdminForm(MultiSiteContainerMixinAdminForm):
    class Meta:
        model = Blog
        exclude = ()


class BlogOptions(MultiSiteContainerMixinAdminOptions):
    save_on_top = True
    # inlines = [Post_Inline]
    list_display = ('id', 'title', 'get_sites', 'get_content_object_display', 'sysname', 'posts')
    list_display_links = ('id', 'title',)
    list_filter = ("creation_date", "modified_date", "content_type",)
    fieldsets = [
                    (None, {
                        'fields': ('title',)
                    }),
                ] + MultiSiteContainerMixinAdminOptions.fieldsets

    search_fields = ('title',)
    form = BlogAdminForm
    filter_horizontal = ["sites"]

    def posts(self, obj):
        count = obj.post_set.count()
        return '<a href="/admin/blog/post/?blog__id=%d">%s</a>' % (obj.pk, count)

    posts.short_description = _("Posts")
    posts.allow_tags = True


class PostOptions(ExtendedModelAdmin):
    save_on_top = True
    list_display = (
    'title', 'blog', 'author', 'status', 'published_from', 'published_till', 'enable_comment_form', 'views', 'featured_in_magazine', 'importance_in_magazine')
    list_editable = [
        'featured_in_magazine', 'importance_in_magazine',
    ]

    list_filter = ('blog', 'creation_date', 'modified_date',) + PublishingMixinAdminOptions.list_filter
    search_fields = ('blog__title', 'title', 'body', 'author__username')

    fieldsets = [
        (None, {
            'fields': ('blog', 'title', 'slug', 'body', 'enable_comment_form', 'tags')
        }),
    ]
    fieldsets += PublishingMixinAdminOptions.fieldsets
    fieldsets += [(_('Magazine'), {'fields': (
        'featured_in_magazine', 'importance_in_magazine',
    )}), ]

    prepopulated_fields = {'slug': ('title',), }
    raw_id_fields = ("blog",)
    autocomplete_lookup_fields = {
        'fk': ["blog", ],
    }


admin.site.register(Blog, BlogOptions)
admin.site.register(Post, PostOptions)
