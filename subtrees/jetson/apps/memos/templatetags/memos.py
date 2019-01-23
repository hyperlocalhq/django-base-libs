# -*- coding: UTF-8 -*-

from django.db.models import get_model
from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context
from django.conf import settings

from jetson.apps.memos.models import MemoCollection, Memo, MEMO_TOKEN_NAME

register = template.Library()

### TAGS ###


def do_adding2memos(parser, token):
    """ Prints the widget for adding object to notelist
    using the default "memos/memo.html" template or a custom one
    
    Usage::
        
        {% adding2memos for <object> [using <template_path>] %}
        
    Examples::
        
        {% adding2memos for project %}
        {% adding2memos for institution %}
        {% adding2memos for song using "music/memoed_song.html" %}
        {% adding2memos for object using object_memo_template %}
        
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
    return ObjectAdding2Memos(obj_to_add, template_path)


class ObjectAdding2Memos(template.Node):
    count = 0

    def __init__(self, obj_to_add, template_path):
        self.obj_to_add = obj_to_add
        self.counter = self.__class__.count
        self.__class__.count += 1
        self.template_path = template_path

    def render(self, context):
        request = context['request']
        obj_to_add = template.resolve_variable(self.obj_to_add, context)
        if not obj_to_add:
            return ""
        ct = ContentType.objects.get_for_model(obj_to_add)
        if not hasattr(self, "memo_collection"):
            if MEMO_TOKEN_NAME in request.COOKIES:
                try:
                    collection = MemoCollection.objects.get(
                        token=request.COOKIES[MEMO_TOKEN_NAME],
                    )
                except MemoCollection.DoesNotExist:
                    collection = None
                self.__class__.memo_collection = collection
        is_not_memoed_by_user = True
        collection = getattr(self, "memo_collection", None)
        if collection and collection.memo_set.filter(
            content_type=ct,
            object_id=obj_to_add._get_pk_val(),
        ):
            is_not_memoed_by_user = False
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
        c['is_not_memoed_by_user'] = is_not_memoed_by_user
        output = loader.render_to_string(template_path or "memos/memo.html", c)
        c.pop()
        return output


register.tag('adding2memos', do_adding2memos)

### FILTERS ###


def get_memo_count(request):
    return Memo.objects.filter(
        collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
    ).count()


register.filter('get_memo_count', get_memo_count)
