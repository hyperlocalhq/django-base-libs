# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import SlugMixin

from jetson.apps.i18n.models import Language
from filebrowser.fields import FileBrowseField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from base_libs.middleware.threadlocals import get_current_language
from base_libs.utils.misc import get_translation

from museumsportal.apps.museums.models import Museum
from museumsportal.apps.exhibitions.models import Exhibition
from museumsportal.apps.events.models import Event
from museumsportal.apps.workshops.models import Workshop

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('trashed', _("Trashed")),
)


class ShopProductType(MPTTModel, SlugMixin()):
    parent = TreeForeignKey('self', blank=True, null=True)
    title = MultilingualCharField(_('Title'), max_length=255)
    
    objects = TreeManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

        
class ShopProductCategory(SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=255)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        
        
class ShopProductManager(models.Manager):
    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if not user.is_authenticated():
            return self.get_queryset().none()
        if user.has_perm("shop.change_shopproduct"):
            return self.get_queryset().exclude(status="trashed")
        product_ids = map(int, PerObjectGroup.objects.filter(
            content_type__app_label="shop",
            content_type__model="shopproduct",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True))

        museum_ids = map(int, PerObjectGroup.objects.filter(
            content_type__app_label="museums",
            content_type__model="museum",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True))

        return self.get_queryset().filter(
            models.Q(pk__in=product_ids) | models.Q(museums__id__in=museum_ids)
        ).exclude(status="trashed").distinct()

    def featured_published(self):
        return self.filter(status="published", is_featured=True)
        
class ShopProduct(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_("Name"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    image = FileBrowseField(_('Image'), max_length=255, directory="shop/", extensions=['.jpg', '.jpeg', '.gif', '.png'])
    price = models.DecimalField(_(u"Price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    link = models.URLField(_('Order link'), max_length=255)
    product_categories = models.ManyToManyField(ShopProductCategory, verbose_name=_("Categories"), blank=True)
    product_types = TreeManyToManyField(ShopProductType, verbose_name=_("Types"), blank=True)
    languages = models.ManyToManyField(Language, verbose_name=_("Languages"), blank=True, limit_choices_to={'display': True})
    museums = models.ManyToManyField(Museum, verbose_name=_("Related Museums"), blank=True)
    exhibitions = models.ManyToManyField(Exhibition, verbose_name=_("Related Exhibitions"), blank=True)
    events = models.ManyToManyField(Event, verbose_name=_("Related Events"), blank=True)
    workshops = models.ManyToManyField(Workshop, verbose_name=_("Related Workshops"), blank=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_for_children = models.BooleanField(_('For children'), default=False)
    is_new = models.BooleanField(_('New'), default=False)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")
    
    objects = ShopProductManager()
    
    row_level_permissions = True

    def __unicode__(self):
        return self.title
        
    def get_url_path(self):
        try:
            path = reverse("shop_product_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_languages(self):
        langs = []
        for lang in self.languages.all():
            langs.append(lang.get_name())
        return langs

    def get_similar_published_products(self):
        category_ids = [cat.pk for cat in self.product_categories.all()]
        language = get_current_language()
        if category_ids:
            return ShopProduct.objects.filter(
                product_categories__id__in=category_ids,
                status="published",
            ).exclude(pk=self.pk).distinct().order_by('title_%s' % language)
        return ShopProduct.objects.none()

    def get_related_museums(self):
        if not hasattr(self, '_cached_related_museums'):
            self._cached_related_museums = self.museums.filter(
                status="published",
            )
        return self._cached_related_museums

    def get_related_exhibitions(self):
        if not hasattr(self, '_cached_related_exhibitions'):
            self._cached_related_exhibitions = self.exhibitions.filter(
                status="published",
            )
        return self._cached_related_exhibitions

    def get_related_events(self):
        if not hasattr(self, '_cached_related_events'):
            self._cached_related_events = self.events.filter(
                status="published",
            )
        return self._cached_related_events

    def get_related_workshops(self):
        if not hasattr(self, '_cached_related_workshops'):
            self._cached_related_workshops = self.workshops.filter(
                status="published",
            )
        return self._cached_related_workshops

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(ShopProduct),
            )
        except:
            role = PerObjectGroup(
                sysname="owners",
            )
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(role, "title_%s" % lang_code, get_translation("Owners", language=lang_code))
            role.content_object = self
            role.save()

            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self,
                owner=role,
            )

        if not role.users.filter(pk=user.pk).count():
            role.users.add(user)

    def remove_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(ShopProduct),
            )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()

    def get_owners(self):
        from django.contrib.auth.models import User
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            owners_ids = list(PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(ShopProduct),
            ).users.values_list("id", flat=True))
        except:
            owners_ids = []

        for museum in self.museums.all():
            try:
                owners_ids += list(PerObjectGroup.objects.get(
                    sysname__startswith="owners",
                    object_id=museum.pk,
                    content_type=ContentType.objects.get_for_model(Museum),
                ).users.values_list("id", flat=True))
            except:
                pass

        return User.objects.filter(id__in=owners_ids).distinct()

    def get_next_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return ShopProduct.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
                **{
                    '{}__gt'.format(field_name): getattr(self, field_name)
                }
            ).order_by(field_name)[0]
        except:
            return None

    def get_previous_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return ShopProduct.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
                **{
                    '{}__lt'.format(field_name): getattr(self, field_name)
                }
            ).order_by('-{}'.format(field_name))[0]
        except:
            return None
