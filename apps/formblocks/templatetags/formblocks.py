from django.conf import settings
from django.db.models import get_model
from django.template import loader, Template, Context
from django import template

from ccb.apps.formblocks.models import FormBlock

register = template.Library()


def do_formblocks(parser, token):
    try:
        tag_name, fieldset_id, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            tag_name, fieldset_id = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <fieldset_id> [using <template_path>] %%}" % token.contents[
                0]
    return FormBlocksRenderer(fieldset_id, template_path)


class FormBlocksRenderer(template.Node):
    """ {% formblocks <fieldset_id> [using <template_path>] %} """

    def __init__(self, fieldset_id, template_path):
        self.fieldset_id = fieldset_id
        self.template_path = template_path

    def render(self, context):
        try:
            fieldset_id = template.resolve_variable(self.fieldset_id, context)
        except:
            return ""


        #infoblock, created = InfoBlock.site_objects.get_or_create(
        #    sysname=fieldset_id,
        #)
        #if not infoblock.title and not infoblock.content or not infoblock.is_published(
        #):
        #    return ""

        formblocks = FormBlock.objects.filter(sysname__startswith=fieldset_id)

        try:
            template_path = template.resolve_variable(
                self.template_path, context
            )
        except:
            template_path = ""

        context_vars = context
        context_vars.push()
        context_vars['formblocks'] = formblocks

        output = loader.render_to_string(
            template_path or "blocks/formblocks.html", context_vars
        )
        context_vars.pop()
        return output


register.tag('formblocks', do_formblocks)
