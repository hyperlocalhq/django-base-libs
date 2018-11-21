# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode

from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import CreationModificationDateMixin

from base_libs.utils.misc import get_translation

verbose_name = _("Favorites")


class FavoriteManager(models.Manager):
    def is_favorite(self, obj, user):
        return bool(
            self.filter(
                user=user,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
            )
        )

    def update_favorites_counts(self):
        from templatetags.favorites import get_favorites_count
        for favorite in self.get_queryset():
            instance = favorite.content_object
            if hasattr(instance, "favorites_count"):
                favorites_count = get_favorites_count(instance)
                type(instance).objects.filter(pk=instance.pk).update(
                    favorites_count=favorites_count
                )


class Favorite(
    CreationModificationDateMixin, ObjectRelationMixin(is_required=True)
):
    """
    Defines that a user likes an object
    """
    user = models.ForeignKey(User, verbose_name=_("Preferrer"))

    objects = FavoriteManager()

    class Meta:
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")
        ordering = ("-creation_date", )

    def __unicode__(self):
        try:
            content_object = self.content_object
            postfix = ""
        except:
            content_object = None
            postfix = " (broken; id=%s)" % self.id
        return u"%s is favorite for %s%s" % (
            force_unicode(content_object),
            force_unicode(self.user.username),
            postfix,
        )

    def get_log_message(self, language=None, action=None):
        """
        Gets a message for a specific action which will be logged for history """
        history_models = models.get_app("history")
        message = ""
        if action in (history_models.A_ADDITION, history_models.A_CHANGE):
            message = get_translation(
                "%(user)s added %(obj)s to the favorites.", language=language
            ) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
            }
        elif action == history_models.A_DELETION:
            message = get_translation(
                "%(obj)s was removed from %(user)s's favorites.",
                language=language
            ) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
            }
        return message
