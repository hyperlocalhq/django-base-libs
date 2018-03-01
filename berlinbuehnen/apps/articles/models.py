# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.articles.base import *
from jetson.apps.articles.base import ArticleManager as ArticleManagerBase

from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED

from cms.models import CMSPlugin

class ArticleType(ArticleTypeBase):
    objects = TreeManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            ArticleType.objects.insert_node(self, self.parent)
        super(ArticleType, self).save(*args, **kwargs)

class ArticleCategory(MPTTModel, CreationModificationDateMixin, UrlMixin, SlugMixin()):
    sort_order = models.IntegerField(
        _("sort order"), 
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
       'self',
       related_name="child_set",
       blank=True,
       null=True,
    )
    title = MultilingualCharField(_('title'), max_length=512)
    
    objects = TreeManager()
    
    class Meta:
        verbose_name = _('Article Category')
        verbose_name_plural = _('Article Categories')
        ordering = ["tree_id", "lft"]
        
    class MPTTMeta:
        order_insertion_by = ['sort_order']
    
    def __unicode__(self):
        return force_unicode(self.title)
    __unicode__.admin_order_field = 'path'
    
    def get_url_path(self):
        return "%s/" % self.slug

    def save(self, *args, **kwargs):
        if not self.pk:
            ArticleCategory.objects.insert_node(self, self.parent)
        super(ArticleCategory, self).save(*args, **kwargs)


class ArticleManager(ArticleManagerBase):
    def latest_published(self):
        lang_code = get_current_language()
        return super(ArticleManager, self).latest_published().filter(
            models.Q(language__in=(None, u'')) | models.Q(language=lang_code)
        )

    def for_newsletter(self):
        return self.filter(
            status=STATUS_CODE_PUBLISHED,
            newsletter=True
        )


class Article(ArticleBase):
    category = TreeForeignKey("articles.ArticleCategory", verbose_name=_("Category"), blank=True, null=True)
    short_title = models.CharField(_('short title'), max_length=255, blank=True, default="")
    
    newsletter = models.BooleanField(_("Show in newsletter"), default=False)

    objects = ArticleManager()

class ArticleSelection(CMSPlugin):
    article = models.ForeignKey("articles.Article")
    
    def __unicode__(self):
        return self.article.title
