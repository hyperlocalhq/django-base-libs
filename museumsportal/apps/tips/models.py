# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import UrlMixin
from base_libs.models.fields import MultilingualCharField

from filebrowser.fields import FileBrowseField


class TipOfTheDayManager(models.Manager):
    def upcoming(self):
        today = datetime.today()
        return self.filter(day__gte=today).order_by("day")


RelatedObject = ObjectRelationMixin(
    limit_content_type_choices_to={'model__in': ('exhibition', 'event', 'workshop')},
    is_required=True,
)


class TipOfTheDay(CreationModificationMixin, RelatedObject, UrlMixin):
    day = models.DateField(_("Day"), unique=True)
    starting_time = models.TimeField(_("Time"), blank=True, null=True)
    title = MultilingualCharField(_('Title'), max_length=255)
    subtitle = MultilingualCharField(_('Subtitle'), max_length=255, blank=True)
    image = FileBrowseField(_('Image'), max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    location_title = MultilingualCharField(_('Location Title'), max_length=255, blank=True)
    event_type = MultilingualCharField(_('Event Type'), max_length=255, blank=True)

    objects = TipOfTheDayManager()

    class Meta:
        verbose_name = _("Tip of the Day")
        verbose_name_plural = _("Tips of the Day")

    def __unicode__(self):
        try:
            return u"""{} "{}" """.format(self.content_type, self.content_object)
        except:
            return "Broken Tip of the Day"

    def get_url_path(self):
        return self.content_object.get_url_path()