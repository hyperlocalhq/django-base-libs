from django.conf import settings
from django.db.models import get_model
from django.template import loader, Template, Context
from django import template

from jetson.apps.blocks.models import InfoBlock

register = template.Library()

def do_infoblock(parser, token):
    try:
        tag_name, sysname, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            tag_name, sysname = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> [using <template_path>] %%}" % token.contents[0]
    return InfoBlockRenderer(sysname, template_path)

class InfoBlockRenderer(template.Node):
    """ {% infoblock <sysname> [using <template_path>] %} """
    def __init__(self, sysname, template_path):
        self.sysname = sysname
        self.template_path = template_path
    def render(self, context):
        try:
            sysname = template.resolve_variable(self.sysname, context)
        except:
            return ""
            
        infoblock, created = InfoBlock.site_objects.get_or_create(
            sysname=sysname,
            )
        if not infoblock.title and not infoblock.content or not infoblock.is_published():
            return ""
        
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
        context_vars = context
        context_vars.push()
        context_vars['title'] = infoblock.title
        context_vars['content'] = Template(
            infoblock.get_rendered_content(),
            ).render(Context(context))
        output = loader.render_to_string(template_path or "blocks/infoblock.html", context_vars)
        context_vars.pop()
        return output

register.tag('infoblock', do_infoblock)

