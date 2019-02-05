# -*- coding: UTF-8 -*-
import datetime, time

from django.template import loader, RequestContext, Template
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.views.decorators.vary import vary_on_headers
from django.utils.cache import patch_vary_headers
from django.views.decorators.cache import cache_control
from django.conf import settings

FlatPage = models.get_model("flatpages", "FlatPage")

DEFAULT_TEMPLATE = 'flatpages/default.html'


@cache_control(must_revalidate=True, max_age=3600)
@vary_on_headers('Cookie', 'Accept-language', 'Content-Language')
def flatpage(request, url):
    """
    Flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if url.startswith("/"):  # ignore the first slash
        url = url[1:]

    if url.startswith(
        request.LANGUAGE_CODE + '/'
    ):  # ignore the language prefix
        url = url[len(request.LANGUAGE_CODE) + 1:]

    qs = FlatPage.site_published_objects.filter(
        url=url,
    ).order_by("-published_from")

    if not qs:
        raise Http404()

    f = qs[0]

    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)
    # parsing template context variables for content
    f.content = Template(f.content).render(RequestContext(request))
    f.content_de = Template(f.content_de).render(RequestContext(request))
    c = RequestContext(request, {
        'flatpage': f,
    })
    response = HttpResponse(t.render(c))
    return response
