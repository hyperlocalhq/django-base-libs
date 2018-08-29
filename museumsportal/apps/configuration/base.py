# -*- coding: UTF-8 -*-
import pickle

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.conf import settings

from base_libs.models.models import MetaTagsMixin
from base_libs.models.fields import PlainTextModelField
from base_libs.models.fields import MultilingualCharField # for south to work

verbose_name = _("Configuration")

ACCOUNT_REGISTRATION_TYPES = (
    ('simple', _("Simple")),
    ('advanced', _("Advanced")),
)

class SiteSettingsManager(models.Manager):
    def get_current(self):
        site = Site.objects.get_current()
        site_settings, created = self.get_or_create(site=site)
        return site_settings
        
class SiteSettingsBase(MetaTagsMixin):
    site = models.OneToOneField(Site, verbose_name=_("Site"), on_delete=models.CASCADE)
    registration_type = models.CharField(_("Registration type"), max_length=10, choices=ACCOUNT_REGISTRATION_TYPES, default="simple")
    login_by_email = models.BooleanField(_("Login by email"))
    
    extra_head = PlainTextModelField(_("Extra head"), help_text=_("Third-party code snippets to be added to the end of the HEAD section."), blank=True)
    extra_body = PlainTextModelField(_("Extra body"), help_text=_("Third-party code snippets to be added to the end of the BODY section."), blank=True)
    
    objects = SiteSettingsManager()
    
    class Meta:
        abstract = True
        verbose_name = _("site settings")
        verbose_name_plural = _("site settings")
        
    def __unicode__(self):
        return force_unicode(self.site)
        
    def get_site_name(self):
        return self.site.name
    get_site_name.short_description = _("Site")

class PageSettingsManager(models.Manager):
    def get_settings_for_page(self, path):
        path_without_root = path[1:]
        ps_list = self.filter(path=path_without_root, site__id=settings.SITE_ID).order_by(["-user"])
        if ps_list:
            return ps_list[0]
        else:
            return PageSettingsBase()

class PageSettingsBase(models.Model):
    """
    Viewing settings for specific pages for individual users or globally
    i.e.
    1. Individual users have personalized blocks for /my-profile/
    2. Different sections have own blocks for section pages 
    """
    site = models.ForeignKey(Site, verbose_name=_("Site"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=_("Viewer"), null=True)
    path = models.CharField(_('Path'), max_length=100, help_text=_("All that goes after '/', for example: 'about/contact/'. Make sure to have trailing slash. Use '*' for all pages."), blank=True)
    pickled_settings = models.TextField(_('Settings'), editable=False)
    row_level_permissions = True
    objects = PageSettingsManager()
    
    class Meta:
        abstract = True
        verbose_name = _('page settings')
        verbose_name_plural = _('page settings')
        unique_together = ('site', 'user')
        ordering = ('path',)
        
    def __unicode__(self):
        return force_unicode("%s -- %s" % (self.path, self.user))

    def _get_settings(self):
        return pickle.loads(self.pickled_settings)
        
    def _set_settings(self, value):
        self.pickled_settings = pickle.dumps(value)
    
    settings = property(_get_settings, _set_settings)
