from django.utils.encoding import force_str


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
            request.META["AUTH_USER"] = force_str(request.user.username)
        else:
            request.META["AUTH_USER"] = "Anonymous User"
