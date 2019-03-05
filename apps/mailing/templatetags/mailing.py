from django.db.models import get_model
from django import template
from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from jetson.apps.mailing.models import EmailTemplate

register = template.Library()


def get_email_templates(parser, token):
    """ Prints the "select email template" widget
    
    Usage::
        
        {% email_templates <<on_change_function>>%}
        
    Examples::
        
        {% email_templates on_change_function %}
        
    """
    try:
        tag_name, on_change_function = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <<on_change_function>>%%}" % (
            token.contents[0], token.contents[0]
        )
    return EmailTemplateWidget(on_change_function)


class EmailTemplateWidget(template.Node):
    def __init__(self, on_change_function):
        self.on_change_function = on_change_function

    def render(self, context):
        on_change_function = template.resolve_variable(
            self.on_change_function, context
        )
        email_templates = EmailTemplate.objects.all()

        html = [
            '<select onchange="%s">' % on_change_function,
            '<option selected="selected" value="">-------</option>',
            '<option value="*">%s</option>' % _("No Template")
        ]
        for email_template in email_templates:
            html.append(
                '<option value="%s">%s</option>' %
                (email_template.slug, email_template.name)
            )
        html.append('</select>')
        return "".join(html)


register.tag('email_templates', get_email_templates)
