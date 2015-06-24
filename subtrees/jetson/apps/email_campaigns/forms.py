# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from base_libs.forms import dynamicforms

from base_libs.middleware import get_current_user
from base_libs.forms.fields import SecurityField

from jetson.apps.email_campaigns.models import InfoSubscription
from jetson.apps.email_campaigns.models import MailingList

class InfoSubscriptionForm(dynamicforms.Form):
    name = forms.CharField(
        label=_("Your name"),
        required=True,
        max_length=200,
        )
    email = forms.EmailField(
        label=_("Your email"),
        required=True,
        )
    prevent_spam = SecurityField()
    def save(self, request):
        cleaned = self.cleaned_data
        email = cleaned['email']
        subscriber_name = cleaned['name']
        ip = request.META['REMOTE_ADDR']
        user = get_current_user()
        mailinglist = MailingList.objects.all()[0]
        subscription, created = InfoSubscription.objects.get_or_create(
            ip=ip,
            email=email,
            subscriber=user,
            subscriber_name=subscriber_name,
            mailinglist=mailinglist,
            )
        return subscription

