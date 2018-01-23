# -*- coding: UTF-8 -*-

from jetson.apps.articles.admin import *
from django.utils.translation import ugettext_lazy as _

ArticleCategory = models.get_model("articles", "ArticleCategory")

class ArticleCategoryOptions(TreeEditor):
    save_on_top = True
    search_fields = ('title',)    
    list_display = ['actions_column', 'indented_short_title',]
    list_filter = ("creation_date",)
 
    fieldsets = [(None, {'fields': ('slug',)}),]
    fieldsets += get_admin_lang_section(_("Contents"), ['title',])
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,),}


admin.site.register(ArticleCategory, ArticleCategoryOptions)

admin.site.unregister(Article)

class ArticleOptions(ExtendedModelAdmin):
    class Media:
        js = (
            "%sjs/AddFileBrowser.js" % URL_FILEBROWSER_MEDIA,
            )
    save_on_top = True
    
    list_display = ['id', 'title', 'author', 'status', 'published_from', 'published_till', 'views', 'article_type', 'language']
    list_display_links = ['title']
    list_filter = ('published_from', 'published_till', 'status', 'is_featured', 'article_type', 'language')
    search_fields = ('title', 'description', 'content', 'author__username')
    
    fieldsets = []
    if ARTICLES_HAVE_TYPES:
        fieldsets += [(None, {'fields': ('article_type',)}),]
    fieldsets += [(_("Article"), {'fields': ('title', 'subtitle', 'short_title', 'content', 'description', 'category', 'language')})]
    fieldsets += [(None, {'fields': ('slug', 'is_featured')}),]
    fieldsets += [(_('Additional Content'), {
        'classes': ("collapse open",),
        'fields': ['image', (_("Description"), {'fields':['image_title', 'image_description']})]
    }),]
    fieldsets += [(_('Publish Status'), {
        'fields': ('author', 'status', 'published_from', 'published_till',),
        'classes': ("collapse open",),
        }),
    ]

    prepopulated_fields = {"slug": ("title",),}

admin.site.register(Article, ArticleOptions)
