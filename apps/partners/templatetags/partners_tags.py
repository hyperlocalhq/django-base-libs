# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.db.models import get_model
from django.template import loader, Template, Context
from django import template

PartnerCategory = models.get_model("partners", "PartnerCategory")

register = template.Library()

def partners_category_css(parser, token):
    try:
        tag_name, sysname, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = '"partners/includes/partner_category.css"'
        try:
            tag_name, sysname = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> [using <template_path>] %%}" % token.contents[0]
    return PartnerCategoryRenderer(sysname, template_path)

def partners_category_html(parser, token):
    try:
        tag_name, sysname, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = '"partners/includes/partner_category.html"'
        try:
            tag_name, sysname = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> [using <template_path>] %%}" % token.contents[0]
    return PartnerCategoryRenderer(sysname, template_path)

class PartnerCategoryRenderer(template.Node):
    """ 
    {% partners_category_css <sysname> [using <template_path>] %} 
    {% partners_category_html <sysname> [using <template_path>] %} 
    """
    def __init__(self, sysname, template_path):
        self.sysname = sysname
        self.template_path = template_path
    def render(self, context):
        try:
            sysname = template.resolve_variable(self.sysname, context)
        except:
            return ""
            
        try:
            partner_category = PartnerCategory.objects.get(sysname=sysname)
        except:
            partner_category = PartnerCategory()
            
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
        context_vars = context
        context_vars.push()
        context_vars['partner_category'] = partner_category
        output = loader.render_to_string(template_path or "partners/includes/partner_category.html", context_vars)
        context_vars.pop()
        return output

register.tag('partners_category_css', partners_category_css)
register.tag('partners_category_html', partners_category_html)

