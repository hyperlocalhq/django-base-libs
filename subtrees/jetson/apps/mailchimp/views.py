# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.sites.models import Site
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _

from .forms import SubscriptionForm, SimpleSubscriptionForm


@never_cache
def subscribe_for_info(request, *arguments, **keywords):
    """Displays the info subscription form and handles the subscription action"""
    if request.method=="POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('subscribe4info_done')
    else:
        form = SubscriptionForm()
        if request.user.is_authenticated():
            form.fields['first_name'].initial = getattr(request.user, "first_name", "")
            form.fields['last_name'].initial = getattr(request.user, "last_name", "")
            form.fields['email'].initial = getattr(request.user, "email", "")
    return render_to_response('mailchimp/subscription.html', {
        'form': form,
        'site_name': Site.objects.get_current().name,
    }, context_instance=RequestContext(request))


@never_cache
def subscribe_for_info_simplified(request, *arguments, **keywords):
    """Displays the info subscription form and handles the subscription action"""
    if request.method == "POST":
        form = SimpleSubscriptionForm(request.LANGUAGE_CODE, request.POST)
        if form.is_valid():
            result = form.save(request)
            if result['status'] == 400:
                if result['title'] == 'Member Exists':
                    form.add_error('email', _("You have already subscribed to the newsletter with this email."))
                else:
                    form.add_error('email', _("Unknown error. Try to subscribe with another email or try to subscribe to this newsletter later."))
            else:
                return redirect('subscribe_for_info_simplified_done')
    else:
        form = SimpleSubscriptionForm(request.LANGUAGE_CODE)
        if request.user.is_authenticated():
            form.fields['email'].initial = getattr(request.user, "email", "")
    return render_to_response('mailchimp/subscription_simplified.html', {
        'form': form,
        'site_name': Site.objects.get_current().name,
    }, context_instance=RequestContext(request))

