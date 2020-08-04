# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class UserTracebackMiddleware(object):
    """
    Adds user to request context during request processing, so that they
    show up in the error emails.
    """

    def process_exception(self, request, exception):
        is_authenticated = (
            request.user.is_authenticated()
            if callable(request.user.is_authenticated)
            else request.user.is_authenticated
        )
        if is_authenticated:
            request.META["AUTH_USER"] = force_text(request.user.username)
        else:
            request.META["AUTH_USER"] = "Anonymous User"
