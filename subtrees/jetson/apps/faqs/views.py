# -*- coding: utf-8 -*-
from django.template import loader
from django.http import Http404
from django.conf import settings
from django.contrib.sites.models import Site

from base_libs.views import get_object_from_url
from base_libs.views import get_container
from base_libs.utils.loader import get_template_name_list_for_object
from base_libs.utils.misc import get_or_404

from jetson.apps.utils.views import object_list
from jetson.apps.faqs.models import FaqContainer, FaqCategory
from base_libs.utils.misc import get_website_url


def get_faq_params(
    object_url_part, url_identifier, category_slug=None, **kwargs
):
    """
    gets some parameters. 
    It is used by the view functions and for form processing.
    Returns the parsed and calculated parameters as a 
    dictionary. This later can be used is extra_context
    in the rendered templates or for other purposes.
    """
    root_category = None

    # first of all, object and container stuff!
    (obj, base_template) = get_object_from_url(object_url_part, **kwargs)
    site = None
    if kwargs.has_key('only_for_this_site'):
        if kwargs['only_for_this_site']:
            site = Site.objects.get_current()
    container = get_container(FaqContainer, site, obj, url_identifier)

    if category_slug:
        root_category = get_or_404(FaqCategory, slug=category_slug)

    # we need the path to the root for the breadcrumbs
    category_path = []
    if root_category:
        cat = root_category
        while cat:
            category_path.append(cat)
            cat = cat.parent
    category_path.reverse()

    extra_context = {
        'container': container,
        'object': obj,
        'root_category': root_category,
        'category_path': category_path,
        'base_template': base_template or "faqs/base.html"
    }

    return extra_context


def handle_request(
    request,
    object_url_part,
    url_identifier,
    category_slug=None,
    paginate_by=None,
    page=None,
    allow_empty=True,
    allow_future=False,
    extra_context=None,
    context_processors=None,
    **kwargs
):
    """
    archive of Faq Categories. If a category_slug is given,
    all children of that category will be displayed!

    Context:
        object     The object related to the Faq Categories (or None)
 
    """
    template_object_name = 'category'

    # first of all, get faq parameters from the url parts...
    extra_context = get_faq_params(
        object_url_part, url_identifier, category_slug, **kwargs
    )
    container = extra_context['container']
    root_category = extra_context['root_category']

    # try to resolve FAQ category from slug
    if root_category:
        queryset = FaqCategory.objects.filter(parent=root_category)
    else:
        queryset = FaqCategory.objects.get_roots(container)

    obj = extra_context['object']
    template_name_list = get_template_name_list_for_object("faqs", obj, "faqs")

    return object_list(
        request,
        queryset,
        paginate_by=paginate_by,
        page=page,
        allow_empty=True,
        template_name=template_name_list,
        template_loader=loader,
        extra_context=extra_context,
        context_processors=context_processors,
        template_object_name=template_object_name,
        content_type=None
    )
