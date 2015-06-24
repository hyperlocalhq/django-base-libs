# -*- coding: UTF-8 -*-

from django.core.handlers.base import BaseHandler

def _handle_uncaught_exception(self, request, resolver, exc_info):
    """
    Processing for any otherwise uncaught exceptions (those that will
    generate HTTP 500 responses). Can be overridden by subclasses who want
    customised 500 handling.

    Be *very* careful when overriding this because the error could be
    caused by anything, so assuming something like the database is always
    available would be an error.
    """
    from django.conf import settings
    from django.core.mail.message import EmailMessage
    from django.views import debug

    if settings.DEBUG_PROPAGATE_EXCEPTIONS:
        raise

    technical_500_response = debug.technical_500_response(request, *exc_info)

    if settings.DEBUG:
        return technical_500_response

    # When DEBUG is False, send an error message to the admins.
    subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
    
    msg = EmailMessage(
        settings.EMAIL_SUBJECT_PREFIX + subject,
        technical_500_response.content,
        settings.SERVER_EMAIL,
        [a[1] for a in settings.ADMINS],
        )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=True)

    # If Http500 handler is not installed, re-raise last exception
    if resolver.urlconf_module is None:
        raise exc_info[1], None, exc_info[2]
    # Return an HttpResponse that displays a friendly error message.
    callback, param_dict = resolver.resolve500()
    return callback(request, **param_dict)

BaseHandler.handle_uncaught_exception = _handle_uncaught_exception
