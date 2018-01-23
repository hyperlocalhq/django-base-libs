# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from base_libs.models.models import CreationModificationMixin

verbose_name = _(u"Internal Links")


class LinkGroup(CreationModificationMixin):
    group_title = models.CharField(verbose_name=_(u'Group title'), max_length=255, blank=True)
    language = models.CharField(_("Language"), choices=settings.LANGUAGES, max_length=5)

    link_1_text = models.CharField(verbose_name=_(u'Link 1 Text'), max_length=255, blank=True)
    link_1_url = models.CharField(verbose_name=_(u'Link 1 URL'), max_length=255, blank=True)

    link_2_text = models.CharField(verbose_name=_(u'Link 2 Text'), max_length=255, blank=True)
    link_2_url = models.CharField(verbose_name=_(u'Link 2 URL'), max_length=255, blank=True)

    link_3_text = models.CharField(verbose_name=_(u'Link 3 Text'), max_length=255, blank=True)
    link_3_url = models.CharField(verbose_name=_(u'Link 3 URL'), max_length=255, blank=True)

    museums = models.ManyToManyField("museums.Museum", verbose_name=_(u"Museums"), blank=True)
    exhibitions = models.ManyToManyField("exhibitions.Exhibition", verbose_name=_(u"Exhibitions"), blank=True)
    events = models.ManyToManyField("events.Event", verbose_name=_(u"Events"), blank=True)
    workshops = models.ManyToManyField("workshops.Workshop", verbose_name=_(u"Guided Tours"), blank=True)

    class Meta:
        verbose_name = _(u"Link Group")
        verbose_name_plural = _(u"Link Groups")

    def __unicode__(self):
        return "%s (%s)" % (self.group_title, self.language)

    def get_links(self):
        if self.link_1_url and self.link_1_text:
            yield {
                'url': self.link_1_url,
                'text': self.link_1_text,
            }
        if self.link_2_url and self.link_2_text:
            yield {
                'url': self.link_2_url,
                'text': self.link_2_text,
            }
        if self.link_3_url and self.link_3_text:
            yield {
                'url': self.link_3_url,
                'text': self.link_3_text,
            }
        return
        yield  # empty generator if conditions above are not met