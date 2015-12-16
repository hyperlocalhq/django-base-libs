# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import operator

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from datetime import datetime

from filebrowser.fields import FileBrowseField

from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import UrlMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import PositionField
from base_libs.middleware import get_current_language

from mptt.fields import TreeForeignKey, TreeManyToManyField


TYPE_CHOICES = (
    ('searching', _("Searching")),
    ('offering', _("Offering")),
)

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
)

TOKENIZATION_SUMMAND = 75623 # used to hide the ids of bulletins


class BulletinCategory(SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=200)
    sort_order = PositionField(_("Sort order")) 
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Bulletin Category")
        verbose_name_plural = _("Bulletin Categories")
        ordering = ("sort_order", )


class PublishedBulletinManager(models.Manager):
    def get_queryset(self):
        conditions = []
        now = datetime.now()
        conditions.append(models.Q(
            published_from=None,
            published_till=None,
        ))
        conditions.append(models.Q(
            published_from__lt=now,
            published_till=None,
        ))
        conditions.append(models.Q(
            published_from=None,
            published_till__gt=now,
        ))
        conditions.append(models.Q(
            published_from__lt=now,
            published_till__gt=now,
        ))
        return super(PublishedBulletinManager, self).get_queryset().filter(
            reduce(operator.or_, conditions),
        ).filter(status="published")

class ExpiredBulletinManager(models.Manager):
    def update_status(self):
        conditions = []
        now = datetime.now()
        conditions.append(models.Q(
            published_from=None,
            published_till=None,
        ))
        conditions.append(models.Q(
            published_from__lt=now,
            published_till=None,
        ))
        conditions.append(models.Q(
            published_from=None,
            published_till__gt=now,
        ))
        conditions.append(models.Q(
            published_from__lt=now,
            published_till__gt=now,
        ))
        self.get_queryset().exclude(
            reduce(operator.or_, conditions),
        ).exclude(status="draft").update(status="expired")


class Bulletin(CreationModificationMixin, UrlMixin):
    bulletin_type = models.CharField(_("Type"), max_length=20, choices=TYPE_CHOICES)
    bulletin_category = models.ForeignKey(BulletinCategory, verbose_name=_("Bulletin category"))
    
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), max_length=300)

    institution = models.ForeignKey("institutions.Institution", blank=True, null=True)
    institution_title = models.CharField(_("Institution title"), max_length=255, blank=True)
    institution_url = models.URLField(_("Institution URL"), max_length=255, blank=True)
    contact_person = models.CharField(_("Contact person"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=200, blank=True)
    email = models.CharField(_("Email"), max_length=254, blank=True)

    image = FileBrowseField(_("Image"), max_length=255, directory="bulletin_board/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    image_description = models.TextField(_('Image Description'), blank=True, default="")

    source_url = models.URLField(_("Source URL"), max_length=255, blank=True)

    categories = TreeManyToManyField(
        "structure.Category",
        verbose_name=_("Categories"),
        related_name="creative_industry_bulletin",
        blank=True,
    )
        
    locality_type = TreeForeignKey(
        "location.LocalityType",
        verbose_name=_("Locality type"),
        blank=True,
        null=True, 
        related_name="locality_bulletin"
    )

    published_from = models.DateTimeField(
        _("publishing date"), 
        null=True,
        blank=True,
        help_text=_("If not provided and the status is set to 'published', the entry will be published immediately."),
    )
    published_till = models.DateTimeField(
        _("published until"), 
        null=True,
        blank=True,
        help_text=_("If not provided and the status is set to 'published', the entry will be published forever."),
    )
 
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="published")

    objects = models.Manager()
    published_objects = PublishedBulletinManager()
    expired_objects = ExpiredBulletinManager()

    class Meta:
        verbose_name = _("Bulletin")
        verbose_name_plural = _("Bulletins")
        ordering = ("-creation_date",)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.published_from:
            self.published_from = datetime.now()
        super(Bulletin, self).save(*args, **kwargs)
    save.alters_data = True
        
    def get_title(self, language=None):
        language = language or get_current_language()
        return getattr(self, "title_%s" % language, "") or self.title
    get_title = lazy(get_title, unicode)
    
    def get_slug(self):
        return self.slug
    
    def get_description(self, language=None):
        language = language or get_current_language()
        return mark_safe(getattr(self, "description_%s" % language, "") or self.description)
    
    def get_type(self):
        for key, name in TYPE_CHOICES:
            if key == self.bulletin_type:
                return _(name)
        return ''

    def get_url_path(self):
        try:
            path = reverse("bulletin_detail", kwargs={'token': self.get_token()})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def is_published(self):
        return bool(Bulletin.published_objects.filter(pk=self.pk))

    def is_draft(self):
        return self.status == "draft"        

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND

    def can_be_changed(self, user):
        return user.has_perm("bulletin_board.change_bulletin", self) or user.is_authenticated() and self.creator == user
