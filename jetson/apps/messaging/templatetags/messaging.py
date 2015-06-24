# -*- coding: UTF-8 -*-
from django.db import models
from django import template

InternalMessage = models.get_model("messaging", "InternalMessage")

register = template.Library()

### FILTERS ###

def get_new_message_count(request):
    return InternalMessage.objects.filter(
        recipient=request.user,
        is_read=False,
        is_draft=False,
        is_spam=False,
        ).count()
    
register.filter('get_new_message_count', get_new_message_count)
