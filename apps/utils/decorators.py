from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

login_required = user_passes_test(
    lambda u: u.is_authenticated(),
    login_url="/login/",
    redirect_field_name="goto_next"
)
login_required.__doc__ = (
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
)
