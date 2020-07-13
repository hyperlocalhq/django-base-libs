# -*- coding: UTF-8 -*-
try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_unicode as force_text


def get_user_title(user):
    """ Returns user's first and last name or username or nickname """
    profile = getattr(user, "profile", None)
    if profile:
        return force_text(profile)
    return user.get_full_name() or user.username
