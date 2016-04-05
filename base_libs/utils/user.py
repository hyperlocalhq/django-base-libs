# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.encoding import force_unicode

def get_user_title(user):
    """ Returns user's first and last name or username or nickname """
    try:
        return force_unicode(user.profile)
    except:
        return force_unicode(user)
