# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import smart_str, force_unicode

class Debugger(object):
    """
    A class for debugging system processes. Saves messages to LogEntry
    instances for the superadmin.
    """
    @staticmethod
    def _get_user():
        return User.objects.filter(is_superuser=True)[0]

    @staticmethod
    def log(message=""):
        Debugger._get_user().logentry_set.create(
            change_message=force_unicode(message),
            action_flag=0,
            )
    alert = log
    alert = staticmethod(alert)

    @staticmethod
    def clear():
        Debugger._get_user().logentry_set.filter(action_flag=0).delete()

    @staticmethod
    def list_out():
        entries = Debugger._get_user().logentry_set.filter(
            action_flag=0,
            ).order_by("id")
        for el in entries:
            print "%s | %s" % (
                smart_str(el.action_time),
                smart_str(el.change_message),
                )

