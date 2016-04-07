from django.conf import settings
from django.db.models import get_model, Q
from django.template import loader, Template, Context
from django import template
from datetime import datetime

from berlinbuehnen.apps.slideshows.models import Slideshow

register = template.Library()


def do_slideshow(parser, token):
    try:
        tag_name, sysname, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            tag_name, sysname = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> [using <template_path>] %%}" % token.contents[0]
    return SlideshowRenderer(sysname, template_path)


class SlideshowRenderer(template.Node):
    """ {% slideshow <sysname> [using <template_path>] %} """
    def __init__(self, sysname, template_path):
        self.sysname = sysname
        self.template_path = template_path
    def render(self, context):
        try:
            sysname = template.resolve_variable(self.sysname, context)
        except:
            return ""
            
        slideshow, created = Slideshow.objects.get_or_create(
            sysname=sysname,
            )
        
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
            
        now = datetime.today()
        slides = slideshow.slide_set.filter(Q(published_from__lte = now) | Q(published_from__isnull = True), Q(published_till__gt = now) | Q(published_till__isnull = True)).order_by("sort_order")
            
        context_vars = context
        context_vars.push()
        context_vars['slides'] = slides
        output = loader.render_to_string(template_path or "slideshows/top_slideshow.html", context_vars)
        context_vars.pop()
        return output

register.tag('top_slideshow', do_slideshow)

