# -*- coding: UTF-8 -*-
import datetime
import random
import re
import urllib
from htmlentitydefs import name2codepoint
from django.db import models
from django import template
from django.conf import settings
from django.template import loader, RequestContext, Template
from django.contrib.contenttypes.models import ContentType
from django.template import defaultfilters
from django.utils.encoding import force_unicode
from django.template.loader import select_template
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines
from django.template.defaultfilters import stringfilter
from base_libs.django_compatibility import force_str

from base_libs.utils.loader import select_template_for_object
from base_libs.utils.user import get_user_title

register = template.Library() 

### TAGS ### 

class IncludeSelectNode(template.Node):
    def __init__(self, case, params):
        self.case = case
        self.params = params

    def render(self, context):
        param_list = []
        # first build a list with resolved vars
        for param in self.params:
            try:
                if param[1] == 1:
                    param_list.append(param[2])
                elif param[1] == 2:
                    param_list.append(template.Variable(param[2]).resolve(context))
            except template.TemplateSyntaxError, e:
                if settings.TEMPLATE_DEBUG:
                    raise
        # the first case (see below)
        t = None
        if self.case == 0:
            try:
                t = select_template(param_list)
            except:
                if settings.TEMPLATE_DEBUG:
                    raise
            return t.render(context) 
        # the second case (see below)
        elif self.case == 1:
            # the param list should look like [<<template>>, <<obj>>, <<app_dir>>]
            try:
                t = select_template_for_object(param_list[0], param_list[1], param_list[2])
            except:
                if settings.TEMPLATE_DEBUG:
                    raise
            return t.render(context) 
        return ""

def do_include_selected(parser, token):
    """
    Loads a template and renders it with the current context.
    Example::
    {% include_selected "template_1.html" "template_2.html" "template_3.html" %}
    {% include_selected "some_include" for obj under "forum" %}
    """
    bits = token.contents.split()
    # well: [some_include, for, obj, under, forum]
    """
    creates a list of tuples for params. Such a tuple consists of three
    entries: 
    1. the index of the param
    2. a code for the type of param with: 
        0 ... reserved word
        1 ... string
        2 ... template var name
    The "case" var is used to distinguish between the two cases
    case=0: {% include_selected "template_1.html" "template_2.html" "template_3.html" %}
    case=1: {% include_selected "some_include" for obj under "forum" %}       
    """
    case = 0
    params = []
    for i in range(1, len(bits)):
        reserved = False
        # check for reserved words
        if (i==2 and bits[i] == "for") or (i==4 and bits[i] == "under"):
            if len(bits) != 6:
                raise template.TemplateSyntaxError, "%r tag takes 4 arguments, there are %d arguments provided." % (bits[0], len(bits)-1)
            if bits[2] != 'for':
                raise template.TemplateSyntaxError, "Second argment in %r tag must be 'for'." % bits[0]
            if bits[4] != 'under':
                raise template.TemplateSyntaxError, "Fourth argment in %r tag must be 'under'." % bits[0]
            case = 1
            reserved = True
        # as string or as template var
        if bits[i][0] in ('"', "'") and bits[i][-1] == bits[i][0]:
            if reserved:
                raise template.TemplateSyntaxError, 'Reserved word %s must not be under "" in %r tag.' % (bits[i], bits[0])
            param =(i, 1, bits[i][1:-1])
        else:
            if reserved:
                param = (i, 0, bits[i])
            else:
                param = (i, 2, bits[i])
        params.append(param) 
    return IncludeSelectNode(case, params)
register.tag('include_selected', do_include_selected)

def do_load_obj(parser, token):
    """
    Loads an object by its application and model names and id
    
    Usage:
        {% load_obj <app_name>.<model_name> <object_id> as <var_name> %}
        
    Example:
        {% load_obj people.Person 3 as person %}
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, appmodel, object_id, str_as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r app.model <object_id> as <var_name> %%}" % (token.contents[0], token.contents[0])
    try:
        appname, modelname = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires application name and model name separated by a dot" % (token.contents[0], token.contents[0])
    model = models.get_model(appname, modelname)
    return LoadObjNode(model, object_id, var_name)

class LoadObjNode(template.Node):
    def __init__(self, model, object_id, var_name):
        self.model = model
        self.object_id = object_id
        self.var_name = var_name
    def render(self, context):
        try:
            object_id = template.resolve_variable(self.object_id, context)
            obj = self.model.objects.get(pk=object_id)
        except ValueError:
            obj = None

        context[self.var_name] = obj
        return ''    

register.tag('load_obj', do_load_obj)

def do_get_all_objects(parser, token):
    """
    Gets a queryset of all objects of the model specified by app and model names

    Usage:
        
        {% get_all_objects app.name as <var_name> %}
        
    Example:
        
        {% get_all_objects people.Person as people %}
        
    """
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, appmodel, str_as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r app.model as <var_name> %%}" % (token.contents[0], token.contents[0])
    try:
        appname, modelname = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires application name and model name separated by a dot" % (token.contents[0], token.contents[0])
    #from django.conf import settings
    model = models.get_model(appname, modelname)
    return GetAllObjectsNode(model, var_name)

class GetAllObjectsNode(template.Node):
    def __init__(self, model, var_name):
        self.model = model
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = self.model.objects.all()
        return ''

register.tag('get_all_objects', do_get_all_objects)

def do_get_latest_published_objects(parser, token):
    """
    Gets a queryset of all objects of the model specified by app and model names

    Usage:
        
        {% get_latest_published_objects app.name <amount> as <var_name> %}
        
    Example:
        
        {% get_latest_published_objects people.Person 3 as people %}
        
    """
    try:
        tag_name, appmodel, amount, str_as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "get_latest_published_objects tag requires a following syntax: {% get_published_objects app.model <amount> as <var_name> %}"
    try:
        appname, modelname = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError, "get_latest_published_objects tag requires application name and model name separated by a dot"
    model = models.get_model(appname, modelname)
    return LatestPublishedObjectsNode(model, amount, var_name)

class LatestPublishedObjectsNode(template.Node):
    def __init__(self, model, amount, var_name):
        self.model = model
        self.amount = amount
        self.var_name = var_name
    def render(self, context):
        if hasattr(self.model._default_manager, "latest_published"):
            qs = self.model._default_manager.latest_published()
        else:
            qs = self.model._default_manager.all()
        amount = template.resolve_variable(self.amount, context)
        context[self.var_name] = qs[:amount]
        return ''

register.tag('get_latest_published_objects', do_get_latest_published_objects)

def do_get_objects(parser, token):
    """
    Gets a queryset of all objects of the model specified by app and model names

    Usage:
        
        {% get_objects [<manager>.]<method> app.name [<amount>] as <var_name> %}
        
    Example:
        
        {% get_objects latest_published people.Person 3 as people %}
        {% get_objects site_objects.all articles.Article 3 as articles %}
        {% get_objects site_objects.all articles.Article as articles %}
        
    """
    amount = None
    try:
        tag_name, manager_method, appmodel, amount, str_as, var_name = token.split_contents()
    except ValueError:
        try:
            tag_name, manager_method, appmodel, str_as, var_name = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "get_objects tag requires a following syntax: {% get_objects <manager_method> app.model <amount> as <var_name> %}"
    try:
        appname, modelname = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError, "get_objects tag requires application name and model name separated by a dot"
    model = models.get_model(appname, modelname)
    return ObjectsNode(model, manager_method, amount, var_name)

class ObjectsNode(template.Node):
    def __init__(self, model, manager_method, amount, var_name):
        self.model = model
        self.manager_method = manager_method
        self.amount = amount
        self.var_name = var_name
    def render(self, context):
        if "." in self.manager_method:
            manager, method = self.manager_method.split(".")
        else:
            manager = "_default_manager"
            method = self.manager_method
            
        qs = getattr(
            getattr(self.model, manager),
            method,
            self.model._default_manager.all,
            )()
        if self.amount:
            amount = template.resolve_variable(self.amount, context)
            context[self.var_name] = qs[:amount]
        else:
            context[self.var_name] = qs
        return ''

register.tag('get_objects', do_get_objects)


def do_call(parser, token):
    """
    Calls a method if it has not attribute alters_data set to True.

    Usage:

        {% call <object>.<method> param1 param2 key1=value1 key2=value2 [as <var_name>] %}

    Example:

        {% call event.get_closest_event_time from_date="2014-01-01" till_date="2014-02-01" as closest_event_time %}

    """
    bits = token.split_contents()
    bits.pop(0)  # tag name
    var_name = ""
    method_args = []
    method_kwargs = {}
    try:
        obj, method_name = bits.pop(0).split(".")
        if bits[-2] == "as":
            var_name = bits.pop(-1)
            bits.pop(-1)  # string "as"
        while bits:
            arg = bits.pop(0)
            if "=" in arg:
                key, value = arg.split("=")
                method_kwargs[key] = value
            else:
                method_args.append(arg)
    except ValueError:
        raise template.TemplateSyntaxError, "call tag requires a following syntax: {% call <object>.<method> param1 param2 key1=value1 key2=value2 [as <var_name>] %}"
    return CallNode(obj, method_name, method_args, method_kwargs, var_name)


class CallNode(template.Node):

    def __init__(self, obj, method_name, method_args, method_kwargs, var_name):
        self.obj = obj
        self.method_name = method_name
        self.method_args = method_args
        self.method_kwargs = method_kwargs
        self.var_name = var_name

    def render(self, context):
        obj = template.resolve_variable(self.obj, context)
        method = getattr(obj, self.method_name)
        if getattr(method, "alters_data", False):
            raise template.TemplateSyntaxError, u"You can't call %s.%s in a template, because it alters data. Call it in the view instead." % (self.obj, self.method_name)

        method_args = [template.resolve_variable(arg, context) for arg in self.method_args]
        method_kwargs = dict([(key, template.resolve_variable(value, context)) for key, value in self.method_kwargs.items()])

        result = method(*method_args, **method_kwargs)

        if self.var_name:
            context[self.var_name] = result
            return ''

        return result

register.tag('call', do_call)


def auto_populated_field_script_fixed(auto_pop_fields, change = False):
    t = []
    for field in auto_pop_fields:
        if change:
            t.append('document.getElementById("id_%s")._changed = true;' % field.name)
        else:
            t.append('document.getElementById("id_%s").onchange = function() { this._changed = true; };' % field.name)

        add_values = ' + " " + '.join(['document.getElementById("id_%s").value' % g for g in field.prepopulate_from])
        for f in field.prepopulate_from:
            t.append('document.getElementById("id_%s").onkeyup = function() {' \
                     ' var e = document.getElementById("id_%s");' \
                     ' if(!e._changed) { e.value = URLify(%s, %s);} }; ' % (
                     f, field.name, add_values, field.maxlength))
    return ''.join(t)
auto_populated_field_script_fixed = register.simple_tag(auto_populated_field_script_fixed)

def do_ifvalue(parser, token, name, negate=False):
    bits = list(token.split_contents())
    if len(bits) != 2 and len(bits) != 4:
        raise template.TemplateSyntaxError, "%r takes one or three arguments" % bits[0]
    tagname, variable = tuple(bits)[:2]
    if len(bits) == 4:
        if bits[2] != "as":
            raise template.TemplateSyntaxError, "%r with three arguments must be 'value as name'" % tagname
        name = bits[3]
    
    end_tag = 'end' + tagname
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    return IfValueNode(variable, name, nodelist_true, nodelist_false, negate)

def ifvalue(parser, token, name="value"):
    """
    Output the contents of the block if the argument is true, assigning
    the value of the argument to a context variable ("value" by default).

    Examples::

        {% ifvalue user.name %}
            {{ value }}
            ...
        {% else %}
            ...
        {% endifvalue %}

        {% ifvalue user.name as username %}
            {{ username }}
            ...
        {% else %}
            ...
        {% endifvalue %}
    """
    return do_ifvalue(parser, token, name, False)
ifvalue = register.tag(ifvalue)

def ifnotvalue(parser, token, name="value"):
    """Output the contents of the block if the argument is false. See ifvalue."""
    return do_ifvalue(parser, token, name, True)
ifnotvalue=register.tag(ifnotvalue)

class IfValueNode(template.Node):
    def __init__(self, var, name, nodelist_true, nodelist_false, negate):
        self.var = var
        self.name = name
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfValueNode>"

    def render(self, context):
        try:
            val = template.resolve_variable(self.var, context)
        except template.VariableDoesNotExist:
            val = None

        context[self.name] = val

        if (self.negate and not val) or (not self.negate and val):
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

def do_parse(parser, token):
    """
    Parses the value as a template and prints it or saves to a variable

    Usage::

        {% parse <template_value> [as <variable>] %}
    
    Examples::

        {% parse object.get_description %}
        {% parse header as header %}
        {% parse "{{ MEDIA_URL }}js/" as js_url %}

    """    
    bits = token.split_contents()
    tag_name = bits.pop(0)
    try:
        template_value = bits.pop(0)
        var_name = None
        if bits:
            bits.pop(0) # remove the word "as"
            var_name = bits.pop(0)
    except ValueError:
        raise template.TemplateSyntaxError, "parse tag requires a following syntax: {% parse <template_value> [as <variable>] %}"
    return ParseNode(template_value, var_name)
    
class ParseNode(template.Node):
    def __init__(self, template_value, var_name):
        self.template_value = template_value
        self.var_name = var_name
    def render(self, context):
        template_value = template.resolve_variable(self.template_value, context)
        t = Template(template_value)
        context_vars = {}
        for d in list(context):
            for var, val in d.items():
                context_vars[var] = val
        result = t.render(RequestContext(context['request'], context_vars))
        if self.var_name:
            context[self.var_name] = result
            return ""
        return result

register.tag('parse', do_parse)

    
def do_include_parsed(parser, token):
    """
    Parses the defined template with the current context variables and also the ones passed to the template tag. The included template might extend some other template.

    Usage::

        {% include_parsed <template_path> [with <value1> as <variable1>[ and <value2> as <variable2>[ and ...]] %}
    
    Examples::

        {% include_parsed "people/item_person.html" %}
        {% include_parsed path with membership.user.get_profile as person and membership.persongroup as persongroup %}

    """    
    bits = token.split_contents()
    tag_name = bits.pop(0)
    try:
        template_path = bits.pop(0)
        extra = [] # a tuple of variables names and values to parse before passing to the template
        if bits:
            bits.pop(0) # remove the word "with"
            while bits:
                val = bits.pop(0)
                bits.pop(0) # remove the word "as"
                var = bits.pop(0)
                extra.append((var, val))
                if bits:
                    bits.pop(0) # remove the word "and"
                    
    except ValueError:
        raise template.TemplateSyntaxError, "include_parsed tag requires a following syntax: {% include_parsed <template_path> [with <value1> as <variable1>[ and <value2> as <variable2>[ and ...]] %}"
    return ParsedIncludeNode(tag_name, template_path, extra)

class ParsedIncludeNode(template.Node):
    def __init__(self, tag_name, template_path, extra):
        self.tag_name = tag_name
        self.template_path = template_path
        self.extra = extra
    def render(self, context):
        template_path = template.resolve_variable(self.template_path, context)
        context_vars = {}
        for d in list(context):
            for var, val in d.items():
                context_vars[var] = val
        for var, val in self.extra:
            context_vars[var] = template.resolve_variable(val, context)
        return loader.render_to_string(template_path, context_vars)

register.tag('include_parsed', do_include_parsed)

"""
Decorator to facilitate template tag creation
"""
def easy_tag(func):
    """deal with the repetitive parts of parsing template tags"""
    def inner(parser, token):
        #print token
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % token.split_contents()[0])
    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner



class AppendGetNode(template.Node):
    def __init__(self, dict, no_path=False):
        self.dict_pairs = {}
        for pair in dict.split(','):
            pair = pair.split('=')
            self.dict_pairs[pair[0]] = template.Variable(pair[1])
        self.no_path = no_path
            
    def render(self, context):
        get = context['request'].GET.copy()

        for key in self.dict_pairs:
            get[key] = self.dict_pairs[key].resolve(context)
        
        path = not self.no_path and context['request'].META['PATH_INFO'] or ""
        
        #print "&".join(["%s=%s" % (key, value) for (key, value) in get.items() if value])
        
        if len(get):
            path += "?%s" % "&".join(["%s=%s" % (key, value) for (key, value) in get.items() if value])
        
        
        return path

@register.tag()
@easy_tag
def append_to_get(_tag_name, dict, no_path=False):
    return AppendGetNode(dict, no_path)


@register.simple_tag(takes_context=True)
def modify_query(context, *params_to_remove, **params_to_change):
    """ Renders a link with modified current query parameters """
    query_params = []
    for key, value_list in context['request'].GET._iterlists():
        if not key in params_to_remove:
            # don't add key-value pairs for params to change
            if key in params_to_change:
                query_params.append((key, params_to_change[key]))
                params_to_change.pop(key)
            else:
                # leave existing parameters as they were if not mentioned in the params_to_change
                for value in value_list:
                    query_params.append((key, value))
    # attach new params
    for key, value in params_to_change.items():
        query_params.append((key, value))
    query_string = u""
    if len(query_params):
        query_string += u"?%s" % urllib.urlencode([
            (key, force_str(value)) for (key, value) in query_params if value
        ]).replace("&", "&amp;")
    return query_string


@register.simple_tag(takes_context=True)
def add_to_query(context, *params_to_remove, **params_to_add):
    """ Renders a link with modified current query parameters """
    query_params = []
    # go through current query params..
    for key, value_list in context['request'].GET._iterlists():
        if not key in params_to_remove:
            # don't add key-value pairs which already exist in the query
            if key in params_to_add and unicode(params_to_add[key]) in value_list:
                params_to_add.pop(key)
            for value in value_list:
                query_params.append((key, value))
    # add the rest key-value pairs
    for key, value in params_to_add.items():
        query_params.append((key, value))
    # empty values will be removed
    query_string = u""
    if len(query_params):
        query_string += u"?%s" % urllib.urlencode([
            (key, force_str(value)) for (key, value) in query_params if value
        ]).replace("&", "&amp;")
    return query_string


@register.simple_tag(takes_context=True)
def remove_from_query(context, *args, **kwargs):
    """ Renders a link with modified current query parameters """
    query_params = []
    # go through current query params..
    for key, value_list in context['request'].GET._iterlists():
        # skip keys mentioned in the args
        if not key in args:
            for value in value_list:
                # skip key-value pairs mentioned in kwargs
                if not (key in kwargs and value == unicode(kwargs[key])):
                    query_params.append((key, value))
    # empty values will be removed
    query_string = u""
    if len(query_params):
        query_string += u"?%s" % urllib.urlencode([
            (key, force_str(value)) for (key, value) in query_params if value
        ]).replace("&", "&amp;")
    return query_string




class IncludeNode(template.Node):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        try:
            # Loading the template and rendering it
            template_name = template.resolve_variable(self.template_name, context)
            included_template = template.loader.get_template(
                    template_name).render(context)
        except template.TemplateDoesNotExist:
            included_template = ''
        return included_template


@register.tag
def try_to_include(parser, token):
    """Usage: {% try_to_include "head.html" %}

    This will fail silently if the template doesn't exist. If it does, it will
    be rendered with the current context."""
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires a single argument" % token.contents.split()[0]

    return IncludeNode(template_name)    


class TranslatedURL(template.Node):
    def __init__(self, lang_code):
        self.lang_code = lang_code

    def render(self, context):
        import sys
        from django.core.urlresolvers import reverse
        from django.core.urlresolvers import resolve
        from django.utils import translation
        lang_code = template.resolve_variable(self.lang_code, context)

        try:
            view = resolve(context['request'].path)
        except:
            return "/%s/" % lang_code

        request_lang_code = translation.get_language()
        translation.activate(lang_code)

        try:
            url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        except:  # if there are any errors resolving the view in another language, fallback to the trasnalted start page
            url = "/%s/" % lang_code

        translation.activate(request_lang_code)
        return url

@register.tag(name="translate_url")
def do_translate_url(parser, token):
    lang_code = token.split_contents()[1]
    return TranslatedURL(lang_code)


### FILTERS ### 


@register.filter
def dayssince(value):
    """Returns number of days between today and value."""
    today = datetime.date.today()
    diff  = today - value
    if diff.days > 1:
        return '%s days ago' % diff.days
    elif diff.days == 1:
        return 'yesterday'
    elif diff.days == 0:
        return 'today'
    else:
        # Date is in the future; return formatted date.
        return value.strftime("%B %d, %Y")


@register.filter
def in_list(value,arg):
    """
    Returns True if value is in list
    
    Example:
        {% if item|in_list:list %}
        in list
        {% else %}
        not in list
        {% endif %}

    """
    return value in arg


@register.filter(is_safe=True)
def mark_first_and_last(value, tag):
    """
    Marks the first tag found with css class "first-child"
    and the last tag found with css class "last-child"
    Example:
    {% filter mark_first_and_last:"li" %}
        <ul>
            <li>A</li>
            <li>B</li>
            <li>C</li>
            <li class="d">D</li>
        </ul>
    {% endfilter %}
    will be rendered as:
        <ul>
            <li class="first-child">A</li>
            <li>B</li>
            <li>C</li>
            <li class="d last-child">D</li>
        </ul>
    """
    tag_regex = re.compile(r'(<' + re.escape(tag) + r')([^>]*)(>)')
    class_regex = re.compile(r'class=([\'"])(.*?)\1')
    parts = tag_regex.split(value)
    # "<p class="a">A</p><p>B</p>" -> 
    # ['', '<p', ' class="a"', '>A</p>', '<p', '', '>','B</p>']
    if len(parts) > 1:
        if class_regex.search(parts[2]):
            parts[2] = class_regex.sub(r'class=\1\2 first-child\1', parts[2])
        else:
            parts[2] += ' class="first-child"'
        if class_regex.search(parts[-3]):
            parts[-3] = class_regex.sub(r'class=\1\2 last-child\1', parts[-3])
        else:
            parts[-3] += ' class="last-child"'
        value = "".join(parts)
    return value


media_file_regex = re.compile(r'<object .+?</object>|<(img|embed) [^>]+>')


@register.filter(is_safe=True)
@stringfilter
def get_first_media(content):
    """ Returns the first image or flash file from the html content """
    m = media_file_regex.search(content)
    media_tag = ""
    if m:
        media_tag = m.group()
    return media_tag


image_file_regex = re.compile(r'<(img) [^>]+>')


@register.filter(is_safe=True)
@stringfilter
def get_first_image(content):
    """ Returns the first image or flash file from the html content """
    m = image_file_regex.search(content)
    media_tag = ""
    if m:
        media_tag = m.group()
    return media_tag


media_src_regex = re.compile(r'src=(["\'])([^\1]+?)\1')    


@register.filter(is_safe=True)
def get_media_src(media_file):
    """ Returns the first image or flash file from the html content """
    m = media_src_regex.search(media_file)
    media_src = ""
    if m:
        media_src = m.group(2)
    return media_src


@register.filter
def content_type_id(value):
    """
    Returns the content_type_id of an object or None, if the object does not exist
    """
    if value is None:
        return None
    
    try:
        ct = ContentType.objects.get_for_model(value)
        return ct.id
    except:
        return None        


@register.filter
def remainder_eq_zero(value, divisor):
    
    """Returns True, if the remainder of the division value/divisor equals 0,
       false otherwise.
    """
    return value % divisor == 0


@register.filter
def remainder_eq_minus1(value, divisor):
    
    """Returns True, if the remainder of the division value/divisor equals -1,
       that is (divisor -1), false otherwise.
    """
    # You are right, Aidas: Python does not the same like C does
    # In algebraic words, divisor-1 and -1 is the same in an
	# algebraic group modulo divisor....
    return value % divisor == divisor - 1


@register.filter
def dict_value(dict, key):
    """ returns the value of a dictionary key ...
    """
    try:
        return dict[key]
    except:
        return None


@register.filter
def encode_string(value):
    """
    Encode a string into it's equivalent html entity.

    The tag will randomly choose to represent the character as a hex digit or
    decimal digit.
   
    Use {{ obj.name|encode_string }}
    
    {{ "person"|encode_string }} Becomes something like:
    &#112;&#101;&#x72;&#x73;&#x6f;&#110;
    """
    e_string = "" 
    for a in value:
        type = random.randint(0,1)
        if type:
            en = "&#x%x;" % ord(a)
        else:
            en = "&#%d;" % ord(a)
        e_string += en 
    return e_string


entity_re = re.compile(
    "&(#?)([Xx]?)(\d+|[A-Fa-f0-9]+|%s);" % '|'.join(name2codepoint)
    )

entity_no_escape_chars_re = re.compile(
    r"&(#?)([Xx]?)((?!39;)(\d+|[A-Fa-f0-9]+)|%s);" % '|'.join(
        [k for k in name2codepoint if k not in ('amp', 'lt', 'gt', 'quot')]
        )
    )


@register.filter
def decode_entities(html, decode_all=False):
    """ 
    Replaces HTML entities with unicode equivalents. 
    Ampersands, quotes and carets are not replaced by default. 
    """ 
    def _replace_entity(m): 
        entity = m.group(3)
        if m.group(1) == '#': 
            val = int(entity, m.group(2) == '' and 10 or 16) 
        else: 
            val = name2codepoint[entity] 
        return unichr(val) 
    regexp = decode_all and entity_re or entity_no_escape_chars_re 
    return regexp.sub(_replace_entity, force_unicode(html)) 


@register.filter
def remove_empty_lists(html):
    """ returns the value without empty <ul></ul> and <ol></ol> ...
    """
    pattern = re.compile(r'<[uo]l[^>]*>\s*</[uo]l>')
    html = pattern.sub("", html)
    return html


@register.filter(is_safe=True, needs_autoescape=False)
def disarm_user_input(html):
    """ 
    Returns html without posible harm
    """
    import bleach
    if "</p>" not in html:
        html = defaultfilters.linebreaks(html)
    html = bleach.clean(
        html,
        tags=[u'a', u'abbr', u'acronym', u'b', u'blockquote', u'br', u'code', u'em', u'i', u'iframe' u'img', u'li', u'ol', u'p', u'strong', u'ul'],
        attributes={
            u'*': [u'class'],
            u'a': [u'href', u'title'],
            u'acronym': [u'title'],
            u'abbr': [u'title'],
            u'img': [u'src', u'alt'],
            u'iframe': [u'src', u'width', u'height'],
        },
        styles=[],
        protocols=[u'http', u'https', u'mailto', u'data'],
        strip=True,
        strip_comments=True,
    )
    html = bleach.linkify(html)
    html = mark_safe(html)
    return html


@register.filter(is_safe=True, needs_autoescape=False)
def disarm_admin_input(html):
    """
    Returns html without posible harm
    """
    import bleach
    if "</p>" not in html:
        html = defaultfilters.linebreaks(html)
    html = bleach.clean(
        html,
        tags=[u'a', u'abbr', u'acronym', u'b', u'blockquote', u'br', u'code', u'em', u'i', u'iframe', u'img', u'li', u'ol', u'p', u'strong', u'ul'],
        attributes={
            u'*': [u'class', u'style'],
            u'a': [u'href', u'title'],
            u'acronym': [u'title'],
            u'abbr': [u'title'],
            u'img': [u'src', 'alt'],
        },
        styles=[u'color', u'font-family', u'font-size'],
        protocols=[u'http', u'https', u'mailto', u'data'],
        strip=True,
        strip_comments=True,
    )
    html = bleach.linkify(html)
    html = mark_safe(html)
    return html


@register.filter
def humanize_url(url, letter_count):
    letter_count = int(letter_count)
    re_start = re.compile(r'^https?://')
    re_end = re.compile(r'/$')
    url = re_end.sub("", re_start.sub("", url))
    if len(url) > letter_count:
        url = url[:letter_count - 1] + u"…"
    return url


@register.filter
def truncated_multiply(value, arg):
    """
    Multiplies the arg with the value and returns 
    the rounded ("integered") value as string.
    """
    return int(value * arg)


register.filter('get_user_title', get_user_title)


@register.filter
@stringfilter
def cssclass(value, arg):
    """
    Replace the attribute css class for Field 'value' with 'arg'.
    """
    attrs = value.field.widget.attrs
    if 'class' in attrs:
        orig = attrs['class']
    else:
        orig = None

    attrs['class'] = arg
    rendered = str(value)

    if not orig:
        del attrs['class']

    return rendered


@register.filter
def in_group(user, groups):
    """Returns a boolean if the user is in the given group, or comma-separated
    list of groups.

    Usage::

        {% if user|in_group:"Friends" %}
        ...
        {% endif %}

    or::

        {% if user|in_group:"Friends,Enemies" %}
        ...
        {% endif %}

    """
    group_list = force_unicode(groups).split(',')
    return bool(user.groups.filter(name__in=group_list).values('name'))


@register.filter(is_safe=True)
@stringfilter
def remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))


@register.filter
@stringfilter
def better_slugify(value):
    from base_libs.utils.betterslugify import better_slugify as utils_better_slugify
    return utils_better_slugify(value)


@register.filter
@stringfilter
def convert_umlauts(value):
    from base_libs.utils.betterslugify import better_slugify as utils_better_slugify
    return utils_better_slugify(value, remove_stopwords=False, slugify=False)
