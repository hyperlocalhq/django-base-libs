# -*- coding: utf-8 -*-

from django import template
from django.template import loader

from jetson.apps.email_campaigns.forms import InfoSubscriptionForm

register = template.Library()

### TEMPLATE TAGS ###

def do_subscription_form(parser, token):
    """
    Loads a newsletter subscription form
    
    Usage:
        {% newsletter_subscription_form %}
        
    """
    return InfoSubscriptionFormNode()

class InfoSubscriptionFormNode(template.Node):
    def render(self, context):
        context.push()
        context['form'] = InfoSubscriptionForm()
        rendered = loader.render_to_string(
            "email_campaigns/includes/newsletter_subscription_form.html",
            {},
            context,
            )
        context.pop()
        return rendered 

register.tag('subscription_form', do_subscription_form)
