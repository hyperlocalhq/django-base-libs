# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode

from base_libs.models.models import ObjectRelationMixin
from base_libs.utils.misc import get_translation

from settings import *

verbose_name = _("Priorities")

class Priority(ObjectRelationMixin(is_required=True)):
    """
    Lets a user define of which priority the chosen object is
    """
    user = models.ForeignKey(User, verbose_name=_("Priority Setter"))
    
    priority = models.SmallIntegerField(_('Priority'), choices=PRIORITY_CHOICES)
    
    class Meta:
        verbose_name = _("priority")
        verbose_name_plural = _("priorities")
        
    def __unicode__(self):
        try:
            content_object = self.content_object
            postfix = ""
        except:
            content_object = None
            postfix = " (broken; id=%s)" % self.id
        return u'%s  is evaluated by %s%s' % (
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
            message = get_translation("%(user)s set priority for %(obj)s.", language=language) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
                }
        elif action==history_models.A_DELETION:
            message = get_translation("%(obj)s's priority by %(user)s was removed.", language=language) % {
                'user': force_unicode(self.user.username),
                'obj': force_unicode(self.content_object),
                }
        return message

