# -*- coding: UTF-8 -*-
from django.shortcuts import redirect

from social.pipeline.partial import partial


USER_FIELDS = ['username', 'email']


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('require_email')


@partial
def login_or_registration(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user:
        return
    return redirect('social_connection_link')


def create_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
