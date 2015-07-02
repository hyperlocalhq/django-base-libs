# -*- coding: UTF-8 -*-
import re
from hashlib import md5

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _

from jetson.apps.email_campaigns.forms import InfoSubscriptionForm
from jetson.apps.configuration.models import SiteSettings

@never_cache
def subscribe_for_info(request, *arguments, **keywords):
    """Displays the info subscription form and handles the subscription action"""
    site_settings = SiteSettings.objects.get_current()
    if request.method=="POST":
        form = InfoSubscriptionForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/subscribe4info/done/')
    else:
        form = InfoSubscriptionForm()
    return render_to_response('email_campaigns/infosubscription.html', {
        'form': form,
        'site_name': Site.objects.get_current().name,
        'login_by_email': site_settings.login_by_email,
    }, context_instance=RequestContext(request))

