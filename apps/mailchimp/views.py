# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.sites.models import Site
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _

from jetson.apps.mailchimp.forms import SubscriptionForm

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

