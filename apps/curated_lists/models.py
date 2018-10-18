# -*- coding: UTF-8 -*-
from hashids import Hashids

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language, activate
from django.utils.text import force_text
from django.conf import settings
from django.core.urlresolvers import reverse
from mptt.fields import TreeManyToManyField

from base_libs.middleware import get_current_user
from filebrowser.fields import FileBrowseField

from base_libs.models.models import CreationModificationDateMixin, SlugMixin, ObjectRelationMixin, UrlMixin
from base_libs.models.fields import MultilingualCharField, MultilingualTextField

verbose_name = _("Curated Lists")

PRIVACY_CHOICES = (
    ("private", _("Private")),
    ("public", _("Public")),
)

limit_owner_content_type_choices_to = (
    models.Q(app_label="institutions", model="institution") |
    models.Q(app_label="people", model="person")
)


class CuratedListManager(models.Manager):
    def get_by_token(self, token):
        hashids = Hashids(min_length=6)

        try:
            curated_list_id = hashids.decode(token)[0]
        except IndexError:
            return None

        try:
            curated_list = self.get_queryset().filter(pk=curated_list_id)[0]
        except IndexError:
            return None

        return curated_list


class CuratedList(
        CreationModificationDateMixin,
        SlugMixin(unique=False),
        UrlMixin,
    ):
    title = MultilingualCharField(_("Title"), max_length=255)
    description = MultilingualTextField(_("Description"), blank=True)
    image = FileBrowseField(_('Image'), max_length=255, directory="curated_lists/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    image_author = models.CharField(_("Image Credits"), max_length=100, blank=True)

    sort_order = models.IntegerField(_("Sort order"), blank=True, default=0)
    categories = TreeManyToManyField(
        "structure.Category",
        verbose_name=_("categories"),
        blank=True
    )
    privacy = models.CharField(_("Privacy"), max_length=20, choices=PRIVACY_CHOICES, default="public")
    is_featured = models.BooleanField(_("Featured"), default=False)

    objects = CuratedListManager()

    class Meta:
        verbose_name = _("Curated List")
        verbose_name_plural = _("Curated Lists")
        ordering = ["sort_order"]

    def __unicode__(self):
        return self.title

    def get_token(self):
        if not self.pk:
            return ""
        hashids = Hashids(min_length=6)
        return hashids.encode(self.pk)

    def get_url_path(self):
        if not self.pk:
            return ""
        token = self.get_token()
        try:
            path = reverse("curated_list_detail", kwargs={'token': token})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def get_item_count(self):
        return self.listitem_set.count()

    def get_next_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return CuratedList.objects.filter(
                ~models.Q(pk=self.pk),
                is_featured=True,
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
            return CuratedList.objects.filter(
                ~models.Q(pk=self.pk),
                is_featured=True,
                **{
                    '{}__lt'.format(field_name): getattr(self, field_name)
                }
            ).order_by('-{}'.format(field_name))[0]
        except:
            return None

    def is_editable(self, user=None):
        if user is None:
            # get current user from the local thread
            user = get_current_user()
        if not user.is_authenticated():
            # anonymous users can't edit curated lists
            return False
        if user.is_staff:
            # staff users always can edit curated lists
            return True
        if not user.groups.filter(name="Curators").exists():
            # non-staff user should belong to a "Curators" group in order to edit curated lists
            return False
        for owner in self.listowner_set.exclude(owner_content_type=None).prefetch_related('owner_content_type'):
            if owner.owner_content_type.model.lower() == "person":
                if owner.owner_content_object and user.profile == owner.owner_content_object:
                    # if the owner is a person of the current user, let them edit curated list
                    return True
            elif owner.owner_content_type.model.lower() == "institution":
                if owner.owner_content_object and user.profile in owner.owner_content_object.get_owners():
                    # if the owner of the curated list is in the owners of related institution, let them edit the list
                    return True
        return False


class ListOwner(
        CreationModificationDateMixin,
        ObjectRelationMixin(
            prefix="owner",
            prefix_verbose=_("Owner"),
            limit_content_type_choices_to=limit_owner_content_type_choices_to
        ),
    ):
    curated_list = models.ForeignKey(CuratedList, verbose_name=_("Curated list"), on_delete=models.CASCADE)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)

    representation = MultilingualCharField(_("Representation"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("List Owner")
        verbose_name_plural = _("List Owners")
        ordering = ["creation_date"]

    def __unicode__(self):
        return self.representation

    def save(self, *args, **kwargs):
        current_language = get_language()
        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            if self.owner_content_object:
                setattr(self, 'representation_{}'.format(lang_code), force_text(self.owner_content_object))
            else:
                setattr(self, 'representation_{}'.format(lang_code), '{} {}'.format(self.first_name, self.last_name))
        activate(current_language)
        super(ListOwner, self).save(*args, **kwargs)


limit_item_content_type_choices_to = (
    models.Q(app_label="institutions", model="institution") |
    models.Q(app_label="people", model="person") |
    models.Q(app_label="media_gallery", model="mediagallery")
)


class ListItem(CreationModificationDateMixin, ObjectRelationMixin(limit_content_type_choices_to=limit_item_content_type_choices_to), UrlMixin):
    curated_list = models.ForeignKey(CuratedList, verbose_name=_("Curated list"), on_delete=models.CASCADE)
    representation = MultilingualCharField(_("Representation"), max_length=255, blank=True)
    sort_order = models.IntegerField(_("Sort order"), blank=True, default=0)

    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("List Item")
        verbose_name_plural = _("List Items")
        ordering = ["sort_order"]

    def __unicode__(self):
        return self.representation

    def get_url_path(self):
        if self.content_object:
            return self.content_object.get_url_path()
        return ""

    def save(self, *args, **kwargs):
        current_language = get_language()
        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            setattr(self, 'representation_{}'.format(lang_code), force_text(self.content_object))
        activate(current_language)
        super(ListItem, self).save(*args, **kwargs)
