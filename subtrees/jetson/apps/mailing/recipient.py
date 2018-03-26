# -*- coding: UTF-8 -*-
from django.conf import settings

from base_libs.utils.crypt import cryptString
from base_libs.utils.user import get_user_title

class Recipient(object):
    _counter = 0
    def _generate_id(self):
        type(self)._counter += 1
        return "inc_%d" % type(self)._counter
        
    def __init__(
        self,
        id=None,
        user=None,
        name="", # name shown in the recipient address
        email="", # email of the recipient
        display_name="", # name shown in a list
        slug="",
        first_name="",
        last_name="",
        url="", # url of the recipient's page
        ):
        self.url = url
        self.link = ""
        self.user = user
        if user:
            self.id = unicode(user.id)
            self.name = name or get_user_title(user)
            self.email = email or user.email
            self.slug = slug or user.username
            self.first_name = first_name or user.first_name
            self.last_name = last_name or user.last_name
            if not self.url:
                profile = getattr(user, "profile", None)
                if profile:
                    self.url = profile.get_absolute_url()
                
        else:
            self.id = id and unicode(id) or self._generate_id()
            self.name = name
            self.email = email
            self.slug = slug
            self.first_name = first_name
            self.last_name = last_name
        if self.url:
            self.link = '<a href="%s">%s</a>' % (self.url, self.name)
        self.display_name = display_name or self.name
    
    def __unicode__(self):
        if self.name is None:
            return "(%s)" % self.email
        else:
            return "%s (%s)" % (self.name, self.email)
        
    def __str__(self):
        return unicode(self).decode("utf-8")
        
    def __repr__(self):
        return '<%s "%s">' % (type(self).__name__, unicode(self))
    
    def get_placeholders(self, placeholders=None, language="en"):
        """
        sets up the current recipients placeholders
        The keys used here are the "sysname" values from
        the EmailTemplatePlaceholder Model.
        These values must not be changed!!!
        
        language:     some of the recipient_placeholders depend on the language
                      (e.g. "salutation")
        """
        if not placeholders:
            placeholders = {}
        placeholders['recipient_salutation'] = self.get_salutation(language=language)
        
        placeholders['recipient_firstname'] = self.first_name
        placeholders['recipient_lastname'] = self.last_name
        placeholders['recipient_name'] = self.name
        placeholders['recipient_email'] = self.email
        placeholders['recipient_encrypted_email'] = cryptString(self.email)
        placeholders['recipient_slug'] = self.slug
        placeholders['recipient_url'] = self.url
        placeholders['recipient_link'] = self.link
        return placeholders
    
    def get_salutation(self, language="en"):
        """
        returns salutation depending on the following properties:
        If self.user is not None, the salutation is returned from the
        underlying Person model. If no salutation is returned, a default one 
        is returned.
        If self.user is none, but the name given, some default salutation is returned.
        
        language:            the preferred language ("de" or "en")
        """
        if self.user and getattr(self.user, "profile", None):
            person = self.user.profile
            if language == 'de':
                return person.get_salutation(language) or "Hallo %s %s!" %(self.user.first_name, self.user.last_name)
            else:
                return person.get_salutation(language) or "Hello %s %s!" %(self.user.first_name, self.user.last_name)
        else:
            if self.name:
                if language == 'de':
                    return "Hallo %s!" % self.name
                else:
                    return "Hello %s!" % self.name
            else:
                if language == 'de':
                    return "Hallo!"
                else:
                    return "Hello!"
