# -*- coding: UTF-8 -*-
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.shortcuts import render
from social import exceptions as social_exceptions

class MySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            return render(request, "accounts/500.html", {'error_message': exception})
        # else:
        #     raise exception