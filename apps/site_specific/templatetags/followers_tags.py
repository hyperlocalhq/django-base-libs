# -*- coding: UTF-8 -*-
from django import template

from actstream.models import following, followers

register = template.Library()

### FILTERS ###

@register.filter
def followers_count(user):
    return len(followers(user))


@register.filter(name="followers")
def list_followers(user):
    return followers(user)


@register.filter
def following_count(user):
    return len(following(user))


@register.filter(name="following")
def list_following(user):
    return following(user)

