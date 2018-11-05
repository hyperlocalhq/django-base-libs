# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode

from base_libs.models.models import ObjectRelationMixin
from base_libs.utils.misc import get_translation

verbose_name = _("Recommendations")

class Recommendation(ObjectRelationMixin(is_required=True)):
    """
    Defines that a user recommends an object to everybody
    """
    user = models.ForeignKey(User, verbose_name=_("Recommender"))
    
    class Meta:
        verbose_name = _("recommendation")
        verbose_name_plural = _("recommendations")
        
    def __unicode__(self):
        try:
            content_object = self.content_object
            postfix = ""
        except:
            content_object = None
            postfix = " (broken; id=%s)" % self.id
        return u'%s recommends %s%s' % (
            force_unicode(self.user.username),
            force_unicode(content_object),
            postfix,
            )

    def get_log_message(self, language=None, action=None):
        """
        Gets a message for a specific action which will be logged for history """
        history_models = models.get_app("history")
        message = ""
        if action in (history_models.A_ADDITION, history_models.A_CHANGE):
            message = get_translation("%(user)s recommended %(obj)s.", language=language) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
                }
        elif action==history_models.A_DELETION:
            message = get_translation("%(obj)s was removed from %(user)s's recommendations.", language=language) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
                }
        return message

