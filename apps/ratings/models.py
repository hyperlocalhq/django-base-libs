# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import connection
from django.utils.encoding import force_unicode

from base_libs.models.models import ObjectRelationMixin

from base_libs.utils.misc import get_translation

verbose_name = _("Ratings")


class Rating(ObjectRelationMixin(is_required=True)):
    """
    Enables users to rate different objects by points
    """
    user = models.ForeignKey(User, verbose_name=_("Rater"))

    points = models.IntegerField(_('Rating points'))

    class Meta:
        verbose_name = _("rating")
        verbose_name_plural = _("ratings")
        permissions = (("can_rate", "Can rate"), )

    def __unicode__(self):
        try:
            content_object = self.content_object
            postfix = ""
        except:
            content_object = None
            postfix = " (broken; id=%s)" % self.id
        return u'%s is rated by %s%s' % (
            force_unicode(content_object),
            force_unicode(self.user.username),
            postfix,
        )

    @staticmethod
    def get_object_rating(obj_to_rate):
        ct = ContentType.objects.get_for_model(obj_to_rate)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT AVG(points), COUNT(*) FROM ratings_rating WHERE content_type_id=%d AND object_id=%d"
            % (ct.id, obj_to_rate.id)
        )
        average_points, rating_count = cursor.fetchone()
        return {
            'average_points': float(average_points or 0),
            'average_points_rounded': int(round(average_points or 0)),
            'rating_count': int(rating_count or 0),
        }

    def get_log_message(self, language=None, action=None):
        """
        Gets a message for a specific action which will be logged for history """
        history_models = models.get_app("history")
        message = ""
        if action in (history_models.A_ADDITION, history_models.A_CHANGE):
            message = get_translation(
                "%(user)s rated %(obj)s.", language=language
            ) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
            }
        elif action == history_models.A_DELETION:
            message = get_translation(
                "Rating for %(obj)s by %(user)s was deleted.",
                language=language
            ) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
            }
        return message
