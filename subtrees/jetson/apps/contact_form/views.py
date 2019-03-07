# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _
from django.conf import settings

from base_libs.utils.misc import get_installed
from base_libs.utils.user import get_user_title

from jetson.apps.contact_form.models import ContactFormCategory

ContactForm = get_installed('contact_form.forms.ContactForm')


@never_cache
def process_contact_form(
    request,
    slug=None,
    template_name='contact_form/contact_form.html',
    **kwargs
):
    """
    Displays the contact form
    """
    if not ContactFormCategory.site_objects.count():
        raise Http404, "Contact form is not configured."
    try:
        cat = ContactFormCategory.site_objects.get(slug=slug)
    except:
        cat = None

    if request.method == 'POST':
        data = request.POST.copy()
        form = ContactForm(data)

        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('%salldone/' % request.path)
    else:
        form = ContactForm()
        if cat and 'contact_form_category' in form.fields:
            form.fields['contact_form_category'].initial = cat.id
        if request.user.is_authenticated():
            form.fields['sender_name'].initial = get_user_title(request.user)
            form.fields['sender_email'].initial = getattr(
                request.user, "email", ""
            )
    return render_to_response(
        template_name,
        {
            'form': form,
        },
        context_instance=RequestContext(request),
    )
