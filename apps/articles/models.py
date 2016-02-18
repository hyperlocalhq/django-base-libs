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
    image = FileBrowseField(_("Image"), max_length=255, directory="content_partners/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)

    class Meta:
        verbose_name = _("article-content provider")
        verbose_name_plural = _("article-content providers")
        ordering = ('title',)

    def __unicode__(self):
        return force_unicode(self.title)


class ArticleTypeManager(TreeManager):
    def under_news(self):
        return self.filter(parent__slug="news")

    def under_interviews(self):
        return self.filter(parent__slug="interviews")


class ArticleType(ArticleTypeBase):
    objects = ArticleTypeManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            ArticleType.objects.insert_node(self, self.parent)
        super(ArticleType, self).save(*args, **kwargs)


class PublishedArticleAllLanguagesManager(PublishingMixinPublishedManager):
    def get_queryset(self):
        return super(PublishedArticleAllLanguagesManager, self).get_queryset().filter(
            sites=Site.objects.get_current(),
        )

    def news(self):
        article_type = ArticleType.objects.get(slug="news")
        return self.filter(article_type__tree_id=article_type.tree_id)

    def news_featured_in_newsletter(self):
        return self.news().filter(
            featured_in_newsletter=True,
        ).order_by("-importance_in_newsletter")

    def interviews(self):
        article_type = ArticleType.objects.get(slug="interviews")
        return self.filter(article_type__tree_id=article_type.tree_id)

    def interviews_featured_in_newsletter(self):
        return self.interviews().filter(
            featured_in_newsletter=True,
        ).order_by("-importance_in_newsletter")

    def tenders_and_competitions(self):
        article_type = ArticleType.objects.get(slug="tenders-competitions")
        return self.filter(article_type=article_type)

    def non_interviews(self):
        article_type = ArticleType.objects.get(slug="interviews")
        return self.exclude(article_type__tree_id=article_type.tree_id)


class PublishedArticleManager(PublishingMixinPublishedManager):
    def get_queryset(self):
        return super(PublishedArticleManager, self).get_queryset().filter(
            sites=Site.objects.get_current(),
            language=get_current_language(),
        )

    def news(self):
        article_type = ArticleType.objects.get(slug="news")
        return self.filter(article_type__tree_id=article_type.tree_id)

    def interviews(self):
        article_type = ArticleType.objects.get(slug="interviews")
        return self.filter(article_type__tree_id=article_type.tree_id)

    def non_interviews(self):
        article_type = ArticleType.objects.get(slug="interviews")
        return self.exclude(article_type__tree_id=article_type.tree_id)


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

    orig_published = models.DateTimeField(_("Originally published"), editable=False, blank=True, null=True)

    content_provider = models.ForeignKey(
        ArticleContentProvider,
        verbose_name=_("Content provider"),
        blank=True,
        null=True,
    )

    featured_in_magazine = models.BooleanField(_("Featured in magazine"), default=False)
    importance_in_magazine = models.PositiveIntegerField(_("Importance in magazine"), default=0, help_text=_("The bigger the number, the more up-front it will be shown in the magazine overview"))

    featured_in_newsletter = models.BooleanField(_("Featured in newsletter"), default=False)
    importance_in_newsletter = models.PositiveIntegerField(_("Importance in newsletter"), default=0, help_text=_("The bigger the number, the more up-front it will be shown in the newsletter"))

    objects = models.Manager()
    site_published_objects = PublishedArticleManager()
    site_published_objects_all_languages = PublishedArticleAllLanguagesManager()
    site_draft_objects = DraftArticleManager()

    categories = TreeManyToManyField(
        "structure.Category",
        verbose_name=_("Categories"),
        limit_choices_to={'level': 0},
        blank=True,
    )

    def get_url_path(self):
        article_type = self.article_type.get_root()
        kwargs = {
            'article_slug': self.slug,
            'year': str(self.published_from.year),
            'month': str(self.published_from.month),
            'day': str(self.published_from.day),
        }
        url_path = ""
        try:
            if article_type.slug == "news":
                url_path = reverse("article_object_detail_for_news", kwargs=kwargs)
            elif article_type.slug == "interviews":
                url_path = reverse("article_object_detail_for_interviews", kwargs=kwargs)
        except:
            pass
        return url_path

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

    def get_creative_sectors(self):
        return self.creative_sectors.all()

    def get_context_categories(self):
        return []

    def get_categories(self):
        return self.categories.all()
