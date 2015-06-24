# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

def patch_contenttypes():
    # Patch ContentType model
    #def contenttype_unicode(self):
    #    return u"%s | %s" % (self.app_label, self.name) 
    #ContentType.__unicode__ = contenttype_unicode
    ContentType._meta.ordering = ("app_label", "name")
    
patch_contenttypes()
