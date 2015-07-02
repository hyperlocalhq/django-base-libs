# -*- coding: UTF-8 -*-
from django.db import models
from django.db.models.loading import get_model, load_app
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context
from django.conf import settings

app = models.get_app("groups_networks")
GroupMembership, PersonGroup, PG_ROLE_PERMISSIONS = (
    app.GroupMembership, app.PersonGroup, app.PG_ROLE_PERMISSIONS,
    )

Institution = models.get_model("institutions", "Institution")

register = template.Library()

### TEMPLATE TAGS ###

def do_adding_group_membership(parser, token):
    """ Prints the widget for adding object to confirmed contacts
    using the default "groups_networks/group_membership.html" template or a custom one
    Object might be of type ContextItem related to Person, Person, or User.
    
    Usage::
        
        {% adding_group_membership at <object> [using <template_path>] %}
        
    Examples::
        
        {% adding_group_membership at context_item %}
        {% adding_group_membership at group using "membership_at_affinity_group.html" %}
        {% adding_group_membership with object %}
        
    """
    try:
        tag_name, str_at, obj_to_add, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            # split_contents() knows not to split quoted strings.
            tag_name, str_at, obj_to_add = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r at <object> [using <template_path>] %%}" % (token[0], token[0])
    return ObjectAddingGroupMembership(obj_to_add, template_path)

class ObjectAddingGroupMembership(template.Node):
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
            
        ct = ContentType.objects.get_for_model(obj_to_add)
        
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
        
        user=context['request'].user
            
        c = context
        c.push()
        c['group'] = obj_to_add
        output = loader.render_to_string(
            template_path or "groups_networks/group_membership.html",
            c,
            )
        c.pop()
        return output
        

register.tag('adding_group_membership', do_adding_group_membership)

### TEMPLATE FILTERS ###

def is_member_request_acceptable(group, obj):
    if type(obj).__name__ == "ContextItem":
        obj = obj.content_object
    if type(obj).__name__ == "Person":
        obj = obj.user
    return group.is_member_request_acceptable(obj)
is_member_request_acceptable = register.filter(is_member_request_acceptable)   

def is_member_request_denyable(group, obj):
    if type(obj).__name__ == "ContextItem":
        obj = obj.content_object
    if type(obj).__name__ == "Person":
        obj = obj.user
    return group.is_member_request_denyable(obj)
is_member_request_denyable = register.filter(is_member_request_denyable)   

def is_member_removable(group, obj):
    if type(obj).__name__ == "ContextItem":
        obj = obj.content_object
    if type(obj).__name__ == "Person":
        obj = obj.user
    return group.is_member_removable(obj)
is_member_removable = register.filter(is_member_removable)   

def is_member_invitation_cancelable(group, obj):
    if type(obj).__name__ == "ContextItem":
        obj = obj.content_object
    if type(obj).__name__ == "Person":
        obj = obj.user
    return group.is_member_invitation_cancelable(obj)
is_member_invitation_cancelable = register.filter(is_member_invitation_cancelable)   


