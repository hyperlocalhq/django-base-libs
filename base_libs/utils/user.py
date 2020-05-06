# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.encoding import force_unicode


def get_user_title(user):
    """ Returns user's first and last name or username or nickname """
    profile = getattr(user, "profile", None)
    if profile:
        return force_unicode(profile)
    return "{} {}".format(user.first_name, user.last_name).strip() or user.username
