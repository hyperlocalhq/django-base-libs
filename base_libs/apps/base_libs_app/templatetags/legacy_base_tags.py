# -*- coding: UTF-8 -*-
from base_libs.django_compatibility import force_str
from django import template
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

register = template.Library()

"""
Decorator to facilitate template tag creation
"""


def easy_tag(func):
    """deal with the repetitive parts of parsing template tags"""

    def inner(parser, token):
        # print token
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError(
                'Bad arguments for tag "%s"' % token.split_contents()[0]
            )

    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner


class AppendGetNode(template.Node):
    def __init__(self, dict, no_path=False):
        self.dict_pairs = {}
        for pair in dict.split(","):
            pair = pair.split("=")
            self.dict_pairs[pair[0]] = template.Variable(pair[1])
        self.no_path = no_path

    def render(self, context):
        get = context["request"].GET.copy()

        for key in self.dict_pairs:
            get[key] = self.dict_pairs[key].resolve(context)

        path = not self.no_path and context["request"].META["PATH_INFO"] or ""

        # print "&".join(["%s=%s" % (key, value) for (key, value) in get.items() if value])

        if len(get):
            path += "?%s" % "&".join(
                ["%s=%s" % (key, value) for (key, value) in get.items() if value]
            )

        return path


@register.tag()
@easy_tag
def append_to_get(_tag_name, dict, no_path=False):
    return AppendGetNode(dict, no_path)


def construct_query_string(context, query_params):
    # empty values will be removed
    query_string = context["request"].path
    if len(query_params):
        encoded_params = urlencode(
            [(key, force_str(value)) for (key, value) in query_params if value]
        ).replace("&", "&amp;")
        query_string += "?" + encoded_params
    return mark_safe(query_string)


@register.simple_tag(takes_context=True)
def modify_query(context, *params_to_remove, **params_to_change):
    """Renders a link with modified current query parameters"""
    query_params = []
    for key, value_list in context["request"].GET.lists():
        if not key in params_to_remove:
            # don't add key-value pairs for params_to_remove
            if key in params_to_change:
                # update values for keys in params_to_change
                query_params.append((key, params_to_change[key]))
                params_to_change.pop(key)
            else:
                # leave existing parameters as they were
                # if not mentioned in the params_to_change
                for value in value_list:
                    query_params.append((key, value))
                    # attach new params
    for key, value in params_to_change.items():
        query_params.append((key, value))
    return construct_query_string(context, query_params)


@register.simple_tag(takes_context=True)
def add_to_query(context, *params_to_remove, **params_to_add):
    """Renders a link with modified current query parameters"""
    query_params = []
    # go through current query params..
    for key, value_list in context["request"].GET.lists():
        if key not in params_to_remove:
            # don't add key-value pairs which already
            # exist in the query
            if key in params_to_add and params_to_add[key] in value_list:
                params_to_add.pop(key)
            for value in value_list:
                query_params.append((key, value))
    # add the rest key-value pairs
    for key, value in params_to_add.items():
        query_params.append((key, value))
    return construct_query_string(context, query_params)


@register.simple_tag(takes_context=True)
def remove_from_query(context, *args, **kwargs):
    """Renders a link with modified current query parameters"""
    query_params = []
    # go through current query params..
    for key, value_list in context["request"].GET.lists():
        # skip keys mentioned in the args
        if key not in args:
            for value in value_list:
                # skip key-value pairs mentioned in kwargs
                if not (key in kwargs and str(value) == str(kwargs[key])):
                    query_params.append((key, value))
    return construct_query_string(context, query_params)

