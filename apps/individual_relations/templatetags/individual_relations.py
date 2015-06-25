# -*- coding: UTF-8 -*-
from django.db.models.loading import get_model, load_app
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context
from django.conf import settings

from jetson.apps.individual_relations.models import IndividualRelation

register = template.Library()

### TEMPLATE TAGS ###

def do_adding_individual_relation(parser, token):
    """ Prints the widget for adding object to confirmed contacts
    using the default "individual_relations/individual_relation.html" template or a custom one
    Object might be of type ContextItem related to Person, Person, or User.
    
    Usage::
        
        {% adding_individual_relation with <object> [using <template_path>] %}
        
    Examples::
        
        {% adding_individual_relation with context_item %}
        {% adding_individual_relation with person using "music/individual_relation_song.html" %}
        {% adding_individual_relation with object %}
        
    """
    try:
        tag_name, str_with, obj_to_add, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            # split_contents() knows not to split quoted strings.
            tag_name, str_with, obj_to_add = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r with <object> [using <template_path>] %%}" % (token[0], token[0])
    return ObjectAddingIndividualRelation(obj_to_add, template_path)

class ObjectAddingIndividualRelation(template.Node):
    count = 0
    def __init__(self, obj_to_add, template_path):
        self.obj_to_add = obj_to_add
        self.counter = self.__class__.count 
        self.__class__.count += 1
        self.template_path = template_path
    def render(self, context):
        # get user by current object
        obj_to_add = template.resolve_variable(self.obj_to_add, context)
        if type(obj_to_add).__name__ == "ContextItem":
            obj_to_add = obj_to_add.content_object
        if type(obj_to_add).__name__ == "Person":
            obj_to_add = obj_to_add.user
            
        ct = ContentType.objects.get_for_model(obj_to_add)
        
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
        
        
        status = IndividualRelation.objects.get_status(
            user_1=context['request'].user,
            user_2=obj_to_add,
            )
            
        c = context
        c.push()
        c['user'] = obj_to_add
        c['status'] = status
        output = loader.render_to_string(
            template_path or "individual_relations/individual_relation.html",
            c,
            )
        c.pop()
        return output
        
register.tag('adding_individual_relation', do_adding_individual_relation)
