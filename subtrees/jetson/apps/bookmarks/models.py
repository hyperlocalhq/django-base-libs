# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from base_libs.models.models import CreatorMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_translation

verbose_name = _("Bookmarks")

class Bookmark(CreatorMixin, CreationModificationDateMixin):   
    """
    Lets a user save a bookmark of a page into the website's database
    """
    title = models.CharField(_("title"), max_length=80)
    url_path = models.CharField(_("URL"), max_length=255) #we do not use an URLField here, because we only save the "relative path"
    
    class Meta:
        ordering = ["creation_date"]
        verbose_name = _("bookmark")
        verbose_name_plural = _("bookmarks")
        
    def __unicode__(self):
        return force_unicode(self.url_path)
        
    def get_log_message(self, language=None, action=None):
        """
        Gets a message for a specific action which will be logged for history """
        history_models = models.get_app("history")
        message = ""
        if action in (history_models.A_ADDITION, history_models.A_CHANGE):
            message = get_translation("%(user)s set reminder for %(url_path)s.", language=language) % {
                'user': force_unicode(self.creator.username),
                'url_path': force_unicode(self.url_path),
                }
        elif action==history_models.A_DELETION:
            message = get_translation("%(user)s's reminder for %(url_path)s was removed.", language=language) % {
                'user': force_unicode(self.creator.username),
                'url_path': force_unicode(self.url_path),
                }
        return message

