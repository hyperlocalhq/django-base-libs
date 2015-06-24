# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.utils import translation
from django.conf import settings

from threading import local

_thread_locals = local()

def get_current_user(forced_user=None):
    user = forced_user or getattr(_thread_locals, 'user', None)
    return (None, user)[isinstance(user, User)] 

def set_current_user(user):
    _thread_locals.user = user

def get_current_language():
    lang = getattr(_thread_locals, 'language', translation.get_language()[:2])
    return lang in dict(settings.LANGUAGES).keys() and lang or settings.LANGUAGE_CODE

def set_current_language(language_code):
    translation.activate(language_code)
    ### _thread_locals.language = language_code

class ThreadLocalsMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        set_current_user(request.user)
    def process_response(self, request, response):
        return response

