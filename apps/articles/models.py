# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from mptt.fields import TreeManyToManyField

from base_libs.models.models import PublishingMixinPublishedManager
from base_libs.models.models import PublishingMixinDraftManager
from base_libs.models.models import MultiSiteMixin
from base_libs.models.fields import URLField
from jetson.apps.articles.base import *
from jetson.apps.structure.models import Term


### CCB-SPECIFIC ARTICLE ###

class ArticleContentProvider(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    url = URLField(_("URL"), blank=True)

    class Meta:
        verbose_name = _("article-content provider")
        verbose_name_plural = _("article-content providers")
        ordering = ('title',)

    def __unicode__(self):
        return force_unicode(self.title)


class ArticleType(ArticleTypeBase):
    objects = TreeManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            ArticleType.objects.insert_node(self, self.parent)
        super(ArticleType, self).save(*args, **kwargs)


class PublishedArticleAllLanguagesManager(PublishingMixinPublishedManager):
    def get_queryset(self):
        return super(PublishedArticleAllLanguagesManager, self).get_queryset().filter(
            sites=Site.objects.get_current(),
        )

    def featured_news(self):
        return self.filter(is_featured=True).order_by("-creation_date")

    def interviews(self):
        return self.filter(article_type__slug="interviews")

    def non_interviews(self):
        return self.exclude(article_type__slug="interviews")


class PublishedArticleManager(PublishingMixinPublishedManager):
    def get_queryset(self):
        return super(PublishedArticleManager, self).get_queryset().filter(
            sites=Site.objects.get_current(),
            language=get_current_language(),
        )

    def interviews(self):
        return self.filter(article_type__slug="interviews")

    def non_interviews(self):
        return self.exclude(article_type__slug="interviews")


class DraftArticleManager(PublishingMixinDraftManager):
    def get_queryset(self):
        return super(DraftArticleManager, self).get_queryset().filter(
            sites=Site.objects.get_current(),
            language=get_current_language(),
        )


class Article(ArticleBase, MultiSiteMixin):
    creative_sectors = TreeManyToManyField(
        Term,
        verbose_name=_("Creative sectors"),
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'},
        related_name="creative_sector_articles",
        blank=True,
        null=True,
    )

    external_url = URLField(_("External URL"), blank=True,
                            help_text=_("Original location of the article if it was imported."), max_length=512)
    is_excerpt = models.BooleanField(_("Excerpt"), default=False, help_text=_(
        "If this article is an excerpt, the link in the list of articles will lead to the external URL."))

    content_provider = models.ForeignKey(
        ArticleContentProvider,
        verbose_name=_("Content provider"),
        blank=True,
        null=True,
    )

    objects = models.Manager()
    site_published_objects = PublishedArticleManager()
    site_published_objects_all_languages = PublishedArticleAllLanguagesManager()
    site_draft_objects = DraftArticleManager()

    def get_url_path(self):
        """ returns an absolute url with the creative sector slug passed to this method """
        # from django.conf import settings
        return "/news/%s/%s/" % (
            self.published_from.strftime("%Y/%m/%d").lower(),
            self.slug,
        )

    def get_newer_published(self):
        try:
            return Article.published_objects.filter(
                published_from__gt=self.published_from,
                pk__gt=self.pk,
                language=self.language,
            ).order_by("published_from")[0]
        except Exception:
            return None

    def get_older_published(self):
        try:
            return Article.published_objects.filter(
                published_from__lt=self.published_from,
                pk__lt=self.pk,
                language=self.language,
            ).order_by("-published_from")[0]
        except Exception:
            return None
