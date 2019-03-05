# -*- coding: utf-8 -*-
from django.conf import settings
from django import template
from django.utils.translation import ugettext_lazy as _

from cms.utils.moderator import get_cmsplugin_queryset
from cms.utils import get_language_from_request

register = template.Library()


def placeholder_plugins(parser, token):
    error_string = _(
        "The syntax of placeholder_plugins tag is as follows: {% placeholder_plugins <name> as <plugins> %}"
    )
    try:
        # split_contents() knows not to split quoted strings.
        bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(error_string)
    if len(bits) == 4:
        # placeholder_plugins, name, as, plugins
        return PlaceholderNode(bits[1], bits[3])
    else:
        raise template.TemplateSyntaxError(error_string)


class PlaceholderNode(template.Node):
    """
    This template node is used load placeholder plugins.
    
    Syntax:
    {% placeholder_plugins <name> as <plugins> %}
    
    Keyword arguments:
    name -- the name of the placeholder
    plugins -- the name of variable that will get the list of plugins 
    
    e.g.:
    {% placeholder_plugins "content" as content_plugins %}
    {% for plugin in content_plugins %}
        {{ plugin.title }}
    {% endfor %}
    
    """

    def __init__(self, name, plugins_var):
        self.name = name
        self.plugins_var = plugins_var

    def render(self, context):
        if not 'request' in context:
            return ''
        l = get_language_from_request(context['request'])
        request = context['request']

        page = request.current_page
        if page == "dummy":
            return ""

        name = template.resolve_variable(self.name, context)

        plugins = get_cmsplugin_queryset(request).filter(
            language=l,
            placeholder__slot=name,
            placeholder__page=page,
            parent__isnull=True,
        ).order_by('position').select_related()

        context[self.plugins_var
               ] = (  # generator
                   p.get_plugin_instance()[0] for p in plugins
               )

        return ""


register.tag('placeholder_plugins', placeholder_plugins)
