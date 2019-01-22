# -*- coding: UTF-8 -*-
from django.template import loader
from django import template

from ..models import InfoBanner

register = template.Library()


def do_infobanner(parser, token):
    try:
        tag_name, sysname, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            tag_name, sysname = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "{0} tag requires a following syntax: {% {0} <sysname> [using <template_path>] %}".format(token.contents[0])
    return InfoBannerRenderer(sysname, template_path)


class InfoBannerRenderer(template.Node):
    """ {% infobanner <sysname> [using <template_path>] %} """
    def __init__(self, sysname, template_path):
        self.sysname = sysname
        self.template_path = template_path

    def render(self, context):
        try:
            sysname = template.resolve_variable(self.sysname, context)
        except:
            return ""
            
        banner, created = InfoBanner.objects.get_or_create(
            sysname=sysname,
        )
        if not banner.content or not banner.is_published():
            return ""
        
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""

        context_vars = context
        context_vars.push()
        cookie_variable = "infobanner_{}_hidden".format(banner.token)
        cookies = context['request'].COOKIES
        context_vars['show_banner'] = cookie_variable not in cookies
        context_vars['cookie_variable'] = cookie_variable
        context_vars['content'] = banner.get_rendered_content()
        output = loader.render_to_string(template_path or "infobanners/infobanner.html", context_vars)
        context_vars.pop()
        return output

register.tag('infobanner', do_infobanner)

