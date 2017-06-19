# -*- coding: UTF-8 -*-
from django.db import models
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader

Rating = models.get_model("ratings", "Rating")

register = template.Library()

def do_obj_rating(parser, token):
    """ Prints the rating widget
    using the default "generic/rating.html" template or a custom one
    
    Usage::
        
        {% obj_rating for <object> %}
        
    Examples::
        
        {% obj_rating for object %}
        {% obj_rating for project %}
        {% obj_rating for user %}
        
    """
    try:
        tag_name, for_str, obj_to_rate, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            # split_contents() knows not to split quoted strings.
            tag_name, for_str, obj_to_rate = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r for <object> %%}" % (token.contents[0], token.contents[0])
    return ObjectRating(obj_to_rate, template_path)

class ObjectRating(template.Node):
    count = 0
    def __init__(self, obj_to_rate, template_path):
        self.obj_to_rate = obj_to_rate
        self.counter = self.__class__.count 
        self.__class__.count += 1
        self.template_path = template_path
    def render(self, context):
        obj_to_rate = template.resolve_variable(self.obj_to_rate, context)
        ct = ContentType.objects.get_for_model(obj_to_rate)
        
        is_not_rated_by_user = not Rating.objects.filter(
            user=context['request'].user,
            content_type=ct,
            object_id=obj_to_rate.pk,
            ).count()
        
        object_ratings = Rating.get_object_rating(obj_to_rate)
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""

        c = context
        c.push()
        c['object'] = obj_to_rate
        c['counter'] = self.counter
        c['content_type_id'] = ct.pk
        c['is_not_rated_by_user'] = is_not_rated_by_user
        c.update(object_ratings)
        output = loader.render_to_string(template_path or "generic/ratings.html", c)
        c.pop()
        return output

register.tag('obj_rating', do_obj_rating)
