# -*- coding: UTF-8 -*-
from threading import local

from django.conf import settings

_thread_locals = local()


def get_current_user(forced_user=None):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = forced_user or getattr(_thread_locals, "user", None)
    return (None, user)[isinstance(user, User)]


def set_current_user(user):
    _thread_locals.user = user


def get_current_language():
    # TODO: refactor or eliminate this function
    from django.utils import translation

    lang = getattr(
        _thread_locals,
        "language",
        (translation.get_language() or settings.LANGUAGE_CODE)[:2],
    )
    return lang in dict(settings.LANGUAGES).keys() and lang or settings.LANGUAGE_CODE


def set_current_language(language_code):
    from django.utils import translation

    translation.activate(language_code)
    ### _thread_locals.language = language_code


class ThreadLocalsMiddleware(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""

    def process_request(self, request):
        set_current_user(request.user)

    def process_response(self, request, response):
        return response
