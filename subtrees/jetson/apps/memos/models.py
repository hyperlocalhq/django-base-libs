# -*- coding: UTF-8 -*-

import string

from datetime import datetime, timedelta

from random import choice

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.conf import settings
from django.utils.timezone import now as tz_now

from base_libs.models import CreationDateMixin, ObjectRelationMixin

MEMO_TOKEN_NAME = getattr(settings, "MEMO_TOKEN_NAME", "memo_token")
MEMO_COOKIE_AGE = getattr(settings, "MEMO_COOKIE_AGE", timedelta(weeks=12))

verbose_name = _("Memos")

class MemoCollectionManager(models.Manager):
    def get_updated(self, token=None):
        collection = None
        if token:
            try:
                collection = self.get(token=token)
            except:
                pass
        if not collection:
            collection = self.model()
            collection.generate_token()
        collection.expiration = tz_now() + MEMO_COOKIE_AGE
        collection.save()
        return collection

class MemoCollection(CreationDateMixin):
    token = models.CharField(_("Token"), max_length=20, unique=True, help_text=_("Unique generated identifier saved in the cookie at a visitor's computer"))
    expiration = models.DateTimeField(_("Expiration"), help_text=_("Cookie expiration date"))
    
    objects = MemoCollectionManager()
    
    def __unicode__(self):
        return self.token
    
    def memo_count(self):
        return self.memo_set.count()
    memo_count.short_description = _("Memos")
    
    def expiration_display(self):
        return self.expiration.strftime('%a, %d %b %Y %H:%M:%S')
    
    def generate_token(self, length=20, chars=string.letters + string.digits):
        """ Generate a random unique string for a token """
        token = ''.join([choice(chars) for i in range(length)])
        while MemoCollection.objects.filter(token=token):
            token = ''.join([choice(chars) for i in range(length)])
        self.token = token
    
class Memo(CreationDateMixin, ObjectRelationMixin()):
    collection = models.ForeignKey(MemoCollection, verbose_name=_("Collection"),)
    
    class Meta:
        verbose_name = _("memo")
        verbose_name_plural = _("memos")
        
    def __unicode__(self):
        try:
            content_object = self.content_object
            postfix = ""
        except:
            content_object = None
            postfix = " (broken; id=%s)" % self.id
        return u"%s @ %s%s" % (
            force_unicode(content_object),
            force_unicode(self.collection.token),
            postfix,
            )

