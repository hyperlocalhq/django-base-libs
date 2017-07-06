# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from base_libs.models import SysnameMixin
from base_libs.models import ObjectRelationMixin
from base_libs.models import CreationDateMixin
from base_libs.models.fields import PlainTextModelField

verbose_name = _("External Services")

class Service(SysnameMixin()):
    title = models.CharField(_("Title"), max_length=50)
    url = models.URLField(_("URL"))
    
    api_key = models.CharField(_("API Key"), max_length=200, blank=True, default="")
    user = models.CharField(_("User"), max_length=200, blank=True, default="")
    password = models.CharField(_("Password"), max_length=200, blank=True, default="")
    
    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")
        ordering = ('title',)
        
    def __unicode__(self):
        return force_unicode(self.title)

class ObjectMapper(ObjectRelationMixin(is_required=True)):
    service = models.ForeignKey(Service, verbose_name=_("Service"))
    external_id = models.CharField(_("External ID"), max_length=512)
    
    class Meta:
        verbose_name = _("object mapper")
        verbose_name_plural = _("object mappers")
        ordering = ('external_id',)
        unique_together = (('object_id', 'content_type', 'service'),)

    def __unicode__(self):
        try:
            obj = force_unicode(self.content_object)
        except:
            obj = "[unrepresentable]"
        return u"%(obj)s @ %(service)s" % {
            'obj': obj,
            'service': force_unicode(self.service),
            }

class ServiceActionLog(CreationDateMixin):
    service = models.ForeignKey(Service, verbose_name=_("Service"))
    request = PlainTextModelField(_("Request"), blank=True)
    response = PlainTextModelField(_("Response"), blank=True)
    response_code = models.IntegerField(_("Response Code"), blank=True)
    
    class Meta:
        verbose_name = _("service-action log")
        verbose_name_plural = _("service-action logs")
        ordering = ('-creation_date',)

    def __unicode__(self):
        return force_unicode(self.creation_date)
