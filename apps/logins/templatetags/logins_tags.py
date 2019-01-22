# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django import template
from django.utils.timezone import now

register = template.Library()

from ..models import LoginAction, WelcomeMessage


@register.inclusion_tag('logins/includes/welcome_message.html')
def show_welcome_message(user):
    welcome_message = None
    if user.is_authenticated():
        login_action_qs = LoginAction.objects.filter(user=user).order_by('-login_date')
        welcome_message_qs = WelcomeMessage.published_objects.all()

        # let's find the appropriate condition for the welcome messages
        if login_action_qs.count() == 1:
            welcome_message_qs = welcome_message_qs.filter(condition=WelcomeMessage.CONDITION_FIRST_LOGIN)
        elif login_action_qs.count() >= 2 and (now() - login_action_qs[1].login_date).days > 30:
            welcome_message_qs = welcome_message_qs.filter(condition=WelcomeMessage.CONDITION_AFTER_1_MONTH)
        else:
            welcome_message_qs = welcome_message_qs.filter(condition=WelcomeMessage.CONDITION_OTHER_LOGINS)

        try:
            welcome_message = welcome_message_qs.order_by('?')[0]
        except IndexError:
            pass

    return {
        'welcome_message': welcome_message,
    }