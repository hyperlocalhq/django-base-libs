# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.encoding import force_unicode

def get_user_title(user):
    """ Returns user's first and last name or username or nickname """
    if getattr(settings, 'AUTH_PROFILE_MODULE', False):
        return force_unicode(user.get_profile())
    return ("%s %s" % (user.first_name, user.last_name)).strip() or user.username

