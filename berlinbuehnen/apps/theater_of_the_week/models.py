# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.articles.base import *
from jetson.apps.articles.base import ArticleManager as ArticleManagerBase

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
        
        try:
            return reverse("%s:theater_of_the_week_object_detail" % get_current_language(), kwargs=kwargs)
        except:
            return reverse("theater_of_the_week_object_detail", kwargs=kwargs)
            

class TheaterOfTheWeekSelection(CMSPlugin):
    theater_of_the_week = models.ForeignKey("theater_of_the_week.TheaterOfTheWeek")
    
    def __unicode__(self):
        return self.theater_of_the_week.title
