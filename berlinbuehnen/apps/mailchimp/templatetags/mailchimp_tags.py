# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('mailchimp/includes/subscribe.html', takes_context=True)
def subscribe(context):
        
    return {
    }