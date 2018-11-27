# -*- coding: UTF-8 -*-
from django.db.models import get_model
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader

Recommendation = get_model("recommendations", "Recommendation")

register = template.Library()


def do_adding2recommendations(parser, token):
    """ Prints the widget for adding object to recommendations
    using the default "generic/recommendation.html" template or a custom one
    
    Usage::
        
        {% adding2recommendations for <object> [using <template_path>] %}
        
    Examples::
        
        {% adding2recommendations for project %}
        {% adding2recommendations for institution %}
        {% adding2recommendations for song using "music/recommendation_song.html" %}
        {% adding2recommendations for object using object_recommendation_template %}
        
    """
    try:
        tag_name, for_str, obj_to_add, str_using, template_path = token.split_contents(
        )
    except ValueError:
        template_path = ""
        try:
            # split_contents() knows not to split quoted strings.
            tag_name, for_str, obj_to_add = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r for <object> %%}" % (
                token.contents[0], token.contents[0]
            )
    return ObjectAdding2Recommendations(obj_to_add, template_path)


class ObjectAdding2Recommendations(template.Node):
    count = 0

    def __init__(self, obj_to_add, template_path):
        self.obj_to_add = obj_to_add
        self.counter = self.__class__.count
        self.__class__.count += 1
        self.template_path = template_path

    def render(self, context):
        obj_to_add = template.resolve_variable(self.obj_to_add, context)
        ct = ContentType.objects.get_for_model(obj_to_add)

        is_not_recommendation_for_user = not Recommendation.objects.filter(
            user=context['request'].user,
            content_type=ct,
            object_id=obj_to_add.id
        ).count()

        try:
            template_path = template.resolve_variable(
                self.template_path, context
            )
        except:
            template_path = ""

        c = context
        c.push()
        c['object'] = obj_to_add
        c['content_type_id'] = ct.id
        c['is_not_recommendation_for_user'] = is_not_recommendation_for_user
        output = loader.render_to_string(
            template_path or "generic/recommendation.html", c
        )
        c.pop()
        return output


register.tag('adding2recommendations', do_adding2recommendations)
