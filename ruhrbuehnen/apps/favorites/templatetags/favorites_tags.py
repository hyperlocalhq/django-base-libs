# -*- coding: UTF-8 -*-
from django.db import models
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader

Favorite = models.get_model("favorites", "Favorite")

register = template.Library()

### TAGS ###


def do_adding2favorites(parser, token):
    """ Prints the widget for adding object to favorites
    using the default "generic/favorite.html" template or a custom one
    
    Usage::
        
        {% adding2favorites for <object> [using <template_path>] %}
        
    Examples::
        
        {% adding2favorites for project %}
        {% adding2favorites for institution %}
        {% adding2favorites for song using "music/favorite_song.html" %}
        {% adding2favorites for object using object_favorite_template %}
        
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
    return ObjectAdding2Favorites(obj_to_add, template_path)


class ObjectAdding2Favorites(template.Node):
    count = 0

    def __init__(self, obj_to_add, template_path):
        self.obj_to_add = obj_to_add
        self.counter = self.__class__.count
        self.__class__.count += 1
        self.template_path = template_path

    def render(self, context):
        obj_to_add = template.resolve_variable(self.obj_to_add, context)
        ct = ContentType.objects.get_for_model(obj_to_add)

        is_not_favorite_for_user = not Favorite.objects.filter(
            user=context['request'].user,
            content_type=ct,
            object_id=obj_to_add.pk,
        )

        try:
            template_path = template.resolve_variable(
                self.template_path, context
            )
        except:
            template_path = ""

        c = context
        c.push()
        c['object'] = obj_to_add
        c['content_type_id'] = ct.pk
        c['is_not_favorite_for_user'] = is_not_favorite_for_user
        output = loader.render_to_string(
            template_path or "favorites/includes/favorite.html", c
        )
        c.pop()
        return output


register.tag('adding2favorites', do_adding2favorites)


def do_login2favorites(parser, token):

    try:
        tag_name, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
    return ObjectLogin2Favorites(template_path)


class ObjectLogin2Favorites(template.Node):
    count = 0

    def __init__(self, template_path):
        self.counter = self.__class__.count
        self.__class__.count += 1
        self.template_path = template_path

    def render(self, context):

        try:
            template_path = template.resolve_variable(
                self.template_path, context
            )
        except:
            template_path = ""

        c = context
        c.push()
        output = loader.render_to_string(
            template_path or "favorites/includes/favorite_login.html", c
        )
        c.pop()
        return output


register.tag('login2favorites', do_login2favorites)

### FILTERS ###


def get_favorites_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    count = Favorite.objects.filter(
        content_type=ct,
        object_id=obj.pk,
    ).count()
    return count


register.filter('get_favorites_count', get_favorites_count)
