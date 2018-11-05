# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings

from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import UrlMixin
from base_libs.utils.misc import get_translation


class ParentManager(models.Manager):
    def accessible_to(self, user):
        from ruhrbuehnen.apps.locations.models import Location
        if user.has_perm("productions.change_production"):
            return self.get_queryset()

        owned_locations = Location.objects.owned_by(user=user)
        return self.get_queryset().filter(
            models.Q(production__in_program_of__in=owned_locations) |
            models.Q(production__play_locations__in=owned_locations)
        ).exclude(production__status="trashed").distinct()

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        ids = map(int, PerObjectGroup.objects.filter(
            content_type__app_label="multiparts",
            content_type__model="parent",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True))
        return self.get_queryset().filter(pk__in=ids)


class Parent(CreationModificationMixin, UrlMixin):
    production = models.OneToOneField('productions.Production', verbose_name=_("Production"), related_name="multipart")

    row_level_permissions = True

    objects = ParentManager()

    def __unicode__(self):
        return self.production.title

    class Meta:
        ordering = ['production__title']
        verbose_name = _("Multipart production")
        verbose_name_plural = _("Multipart productions")

    def get_url_path(self):
        return self.production.get_url_path()

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Parent),
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
    set_owner.alters_data = True

    def remove_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Parent),
                )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()
    remove_owner.alters_data = True

    def get_owners(self):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Parent),
            )
        except:
            return []
        return role.users.all()

    def is_editable(self, user=None):
        from django.contrib.auth.models import AnonymousUser
        from base_libs.middleware.threadlocals import get_current_user
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            if user.has_perm("multiparts.change_parent", self):
                return True
            # return True when the first editable location is found
            self._is_editable_cache = any((
                location.is_editable()
                for locations in (self.production.in_program_of.all(), self.production.play_locations.all())
                for location in locations
            ))
        return self._is_editable_cache

    def is_deletable(self, user=None):
        return self.is_editable(user=user)


class Part(models.Model):
    parent = models.ForeignKey(Parent, verbose_name=_("Parent"))
    production = models.ForeignKey('productions.Production')
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.production.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
