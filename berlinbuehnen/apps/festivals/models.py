# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # needed for south to work
from base_libs.models.fields import PositionField
from base_libs.utils.misc import get_translation

from filebrowser.fields import FileBrowseField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('expired', _("Expired")),
    ('trashed', _("Trashed")),
)

COPYRIGHT_RESTRICTION_CHOICES = (
    ('general_use', _("Released for general use")),
    ('protected', _("Released for this and own site only"))
)


class FestivalManager(models.Manager):
    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if user.has_perm("festivals.change_festival"):
            return self.get_query_set().exclude(status="trashed")
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="festivals",
            content_type__model="festival",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")


class Festival(CreationModificationMixin, UrlMixin, SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    website = URLField("Website", blank=True)

    start = models.DateField(_("Start date"))
    end = models.DateField(_("End date"))

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    objects = FestivalManager()

    row_level_permissions = True

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Festival")
        verbose_name_plural = _("Festivals")

    def get_url_path(self):
        try:
            path = reverse("festival_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Festival),
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
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Festival),
                )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()

    def get_owners(self):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Festival),
            )
        except:
            return []
        return role.users.all()


class Image(CreationModificationDateMixin):
    festival = models.ForeignKey(Festival, verbose_name=_("Festival"))
    path = FileBrowseField(_('File path'), max_length=255, directory="festivals/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="festival")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk
