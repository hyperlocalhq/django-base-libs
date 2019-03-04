from django.template import loader
from django import template

from ccb.apps.metro.models import Tile

register = template.Library()


def do_metro_tile(parser, token):
    try:
        tag_name, sysname, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            tag_name, sysname = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> [using <template_path>] %%}" % \
                                                token.contents[0]
    return MetroTileRenderer(sysname, template_path)


class MetroTileRenderer(template.Node):
    """ {% metro_tile <sysname> [using <template_path>] %} """

    def __init__(self, sysname, template_path):
        self.sysname = sysname
        self.template_path = template_path

    def render(self, context):
        try:
            sysname = template.resolve_variable(self.sysname, context)
        except Exception:
            return ""

        tile, created = Tile.objects.get_or_create(
            sysname=sysname,
        )

        try:
            template_path = template.resolve_variable(self.template_path, context)
        except Exception:
            template_path = ""
        context_vars = context
        context_vars.push()
        context_vars['tile'] = tile
        output = loader.render_to_string(template_path or "metro/tile.html", context_vars)
        context_vars.pop()
        return output


register.tag('metro_tile', do_metro_tile)
