# -*- coding: UTF-8 -*-
import re
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect


class RequireLoginMiddleware(object):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication.
    
    If an anonymous user requests a page, he/she is redirected to the login
    page set by LOGIN_URL or /accounts/login/ by default.
    """

    def __init__(self):
        self.require_login_path = getattr(
            settings, 'LOGIN_URL', '/accounts/login/'
        )

    def process_request(self, request):
        path = request.path
        if path != self.require_login_path and not request.user.is_authenticated(
        ) and not path.startswith("/admin/") and not path.startswith(
            "/jssettings/"
        ) and not path.startswith("/jsi18n/") and not (
            path.startswith("/project/") and path.endswith("/confirm/")
        ) and not settings.DEBUG:
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect(
                    '%s?goto_next=%s' % (self.require_login_path, request.path)
                )


class AdminScriptUpdateMiddleware(object):
    """ Middleware adding document domain to popup windows with forms after
    submitting data. It is necessary for cross-window scripting. """

    def process_response(self, request, response):
        return response  # temporary problem solving
