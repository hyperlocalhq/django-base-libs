# -*- coding: UTF-8 -*-
from django.db import models
from django import template
from django.template import loader

from base_libs.middleware import get_current_user

Bookmark = models.get_model("bookmarks", "Bookmark")

register = template.Library()

def do_bookmarks(parser, token):
    """
    This will output the bookmarks section. 
    By default it uses the template generic/bookmarks.html,
    but optionally you can set some custom template.

    Usage::

        {% bookmarks [using <template_path>] %}
    """
    bits = token.split_contents()
    try:
        template_path = ""
        if "using" in bits:
            template_path = bits[2]
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r [using <template_path>] %%}" % token.contents[0]
    return Bookmarks(template_path)

class Bookmarks(template.Node):
    def __init__(self, template_path):
        self.template_path = template_path
    def render(self, context):
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
        
        bookmarks = Bookmark.objects.filter(creator = get_current_user())
        context_vars = context
        context_vars.push()
        context_vars['bookmarks'] = bookmarks        
        output = loader.render_to_string(template_path or "generic/bookmarks.html", context_vars)
        context_vars.pop()
        return output

register.tag('bookmarks', do_bookmarks)

