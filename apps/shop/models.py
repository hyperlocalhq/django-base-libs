# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import SlugMixin

from jetson.apps.i18n.models import Language
from filebrowser.fields import FileBrowseField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from museumsportal.apps.museums.models import Museum
from museumsportal.apps.exhibitions.models import Exhibition
from museumsportal.apps.events.models import Event
from museumsportal.apps.workshops.models import Workshop


class ShopProductType(MPTTModel, CreationModificationDateMixin, SlugMixin()):
    parent = TreeForeignKey('self', blank=True, null=True)
    title = MultilingualCharField(_('Title'), max_length=255)
    
    objects = TreeManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

        
class ShopProductCategory(models.Model):

    title = MultilingualCharField(_("Title"), max_length=255)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        

class ShopProduct(models.Model):

    title = MultilingualCharField(_("Name"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    image = FileBrowseField(_('Image'), max_length=255, directory="shop/", extensions=['.jpg', '.jpeg', '.gif','.png'])
    price = models.CharField(_('Price'), max_length=10)
    link = models.URLField(_('Order link'), max_length=255)
    product_categories = models.ManyToManyField(ShopProductCategory, verbose_name=_("Categories"), blank=True, null=True)
    product_types = TreeManyToManyField(ShopProductType, verbose_name=_("Types"), blank=True, null=True)
    languages = models.ManyToManyField(Language, verbose_name=_("Languages"), blank=True, limit_choices_to={'display': True}, null=True)
    museums = models.ManyToManyField(Museum, verbose_name=_("Related Museums"), blank=True, null=True)
    exhibitions = models.ManyToManyField(Exhibition, verbose_name=_("Related Exhibitions"), blank=True, null=True)
    events = models.ManyToManyField(Event, verbose_name=_("Related Events"), blank=True, null=True)
    workshops = models.ManyToManyField(Workshop, verbose_name=_("Related Workshops"), blank=True, null=True)
    is_featured = models.BooleanField(_('Featured'), blank=True)
    is_for_children = models.BooleanField(_('Is for children'), blank=True)
    is_new = models.BooleanField(_('New'), blank=True)


    def __unicode__(self):
        return self.title
        
    def get_url_path(self):
        try:
            path = reverse("shop_product", kwargs={'product_id': self.id})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

