# -*- coding: UTF-8 -*-
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from jetson.apps.articles.base import *
from jetson.apps.articles.base import ArticleManager as ArticleManagerBase

from base_libs.models.fields import PositionField

from cms.models import CMSPlugin


class TheaterOfTheWeekManager(ArticleManagerBase):
    def latest_published(self):
        lang_code = get_current_language()
        return super(TheaterOfTheWeekManager, self).latest_published().filter(
            models.Q(language__in=(None, u'')) | models.Q(language=lang_code)
        )


class TheaterOfTheWeek(ArticleBase):
    theater = models.ForeignKey("locations.Location")
    short_title = models.CharField(_('short title'), max_length=255, blank=True, default="")

    objects = TheaterOfTheWeekManager()

    class Meta:
        ordering = ['title']
        verbose_name = _("Theater of the week")
        verbose_name_plural = _("Theaters of the week")
        
    def get_url_path(self):
        kwargs = {
            'theater_of_the_week_slug': self.slug,
            'year': str(self.published_from.year),
            'month': str(self.published_from.month),
            'day': str(self.published_from.day),
        }
        return reverse("theater_of_the_week_object_detail", kwargs=kwargs)

    @cached_property
    def get_related_productions(self):
        return [rel.production for rel in self.theateroftheweekproduction_set.all()]


class TheaterOfTheWeekProduction(CreationModificationDateMixin):
    theater = models.ForeignKey(TheaterOfTheWeek, verbose_name=_("Theater of the week"), on_delete=models.CASCADE)
    production = models.ForeignKey('productions.Production', verbose_name=_("Production"), on_delete=models.CASCADE)
    sort_order = PositionField(_("Sort order"), collection="theater")

    class Meta:
        ordering = ['theater', 'sort_order']
        verbose_name = _("Production for Theater of the week")
        verbose_name_plural = _("Productions for Theaters of the week")


class TheaterOfTheWeekSelection(CMSPlugin):
    theater_of_the_week = models.ForeignKey("theater_of_the_week.TheaterOfTheWeek")
    
    def __unicode__(self):
        return self.theater_of_the_week.title
