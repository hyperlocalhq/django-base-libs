# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models.loading import get_model, load_app
from django.template import loader, Template, Context
from django import template

from jetson.apps.navigation.models import NavigationLink
from base_libs.utils.misc import get_website_url

register = template.Library()

### TAGS ###

def do_find_active_nav_links(parser, token):
    """
    Usage::

        {% find_active_nav_links [under <sysname>] %}

    Example::

        {% find_active_nav_links %}
        {% find_active_nav_links under "public_info" %}
    """
    sysname = ""
    try:
        tag_name, str_under, sysname = token.split_contents()
    except ValueError:
        if not len(token.split_contents()) == 1:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> %%}" % token.contents[0]
    return FindActiveNavLinks(sysname)

class FindActiveNavLinks(template.Node):
    def __init__(self, sysname):
        self.sysname = sysname
    def render(self, context):
        sysname = ""
        if self.sysname:
            sysname = template.resolve_variable(self.sysname, context)
        nav_link = None
        if sysname:
            try:
                nav_link = NavigationLink.site_objects.get(sysname=sysname)
            except:
                pass
        links_checked = NavigationLink.site_objects.all()
        if nav_link:
            links_checked = links_checked.get_ancestors(include_self=True)
        for link in links_checked:
            ActivenessChecker(link).render(context)
        return ""

register.tag('find_active_nav_links', do_find_active_nav_links)

    

def do_children_of(parser, token):
    """
    This will output the children of NavigationLink with the specified sysname. By default it uses the template navigation/children.html, but optionally you can set some custom template.

    Usage::

        {% children_of <sysname> [using <template_path>] %}

    Examples::

        {% children_of "public_info" %}
        {% children_of "profiles" using "navigation/children_of_profiles.html" %}

    """
    try:
        tag_name, sysname, str_using, template_path = token.split_contents()
    except ValueError:
        template_path = ""
        try:
            tag_name, sysname = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> [using <template_path>] %%}" % token.contents[0]
    return ChildrenOfNavLink(sysname, template_path)

class ChildrenOfNavLink(template.Node):
    def __init__(self, sysname, template_path):
        self.sysname = sysname
        self.template_path = template_path
    def render(self, context):
        try:
            sysname = template.resolve_variable(self.sysname, context)
            nav_link = NavigationLink.site_objects.get(sysname=sysname)
        except:
            nav_link = None
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
        context_vars = context
        context_vars.push()
        context_vars['nav_link'] = nav_link
        output = loader.render_to_string(template_path or "navigation/children.html", context_vars)
        context_vars.pop()
        return output

register.tag('children_of', do_children_of)



def do_parse_link(parser, token):
    """
    Parses the template-syntax-based link using current context variables.

    Usage::

        {% parse_link <link> %} # prints raw url
        {% parse_link <link_url> %} # prints raw url
        {% parse_link <link_url> as <raw_url> %} # saves raw url as raw_url

    Examples::

        {% parse_link link as url %}
        {% parse_link link.url %}
        where link.url is "/profile/{{ request.user.username }}/"
        {% parse_link link.url as url %}

    """
    url_variable = None
    try:
        tag_name, link, str_as, url_variable = token.split_contents()
    except:
        try:
            tag_name, link = token.split_contents()
        except ValueError:
            link = ""
    return LinkParser(link, url_variable)

class LinkParser(template.Node):
    def __init__(self, link, url_variable=None):
        self.link = link
        self.url_variable = url_variable
    def render(self, context):
        link = None
        link_url = ""
        try:
            link = template.resolve_variable(self.link, context)
            if isinstance(link, NavigationLink):
                if link.content_object:
                    link_url = link.content_object.get_url_path()
                else:
                    link_url = link.link_url
            else:
                link_url = link
        except:
            pass
        link_url = Template(link_url).render(Context(context)).strip()
        if link_url and link and link.is_login_required and not context['request'].user.is_authenticated():
            link_url = "%s?%s=%s" % (
                settings.LOGIN_URL,
                settings.REDIRECT_FIELD_NAME,
                link_url,
                )
        if self.url_variable:
            context[self.url_variable] = link_url
            return ""
        else:
            return link_url

register.tag('parse_link', do_parse_link)

def do_check_activeness(parser, token):
    """
    returns "active" if the current URL starts with the link.

    Usage::

        {% activeness <link_url> %}
        {% activeness <link_obj> %}
        {% activeness <link_url> as <bool_var> %}
        {% activeness <link_obj> as <bool_var> %}

    Examples::

        {% activeness link.url %}
        {% activeness link %}
        {% activeness "/info/about/" %}
        {% activeness "/info/about/" as is_active %}
        {% activeness "/info/about/" as is_active %}

    """
    activeness_variable=None
    try:
        tag_name, link_url, str_as, activeness_variable = token.split_contents()
    except:
        try:
            tag_name, link_url = token.split_contents()
        except ValueError:
            link_url = ""
    return ActivenessChecker(link_url, activeness_variable)

def do_check_branch_activeness(parser, token):
    activeness_variable=None
    try:
        tag_name, link_url, str_as, activeness_variable = token.split_contents()
    except:
        try:
            tag_name, link_url = token.split_contents()
        except ValueError:
            link_url = ""
    return ActivenessChecker(link_url, activeness_variable, is_branch=True)

class ActivenessChecker(template.Node):
    def __init__(self, link, activeness_variable=None, is_branch=False):
        self.link = link
        self.is_branch = is_branch
        self.activeness_variable = activeness_variable
    def render(self, context):
        request = context['request']
        website_url = get_website_url()
        link = self.link
        related_link_urls = []
        if not isinstance(link, NavigationLink):
            link = template.resolve_variable(link, context)
        if isinstance(link, NavigationLink):
            if link.content_object:
                link_url = link.content_object.get_url_path()
            else:
                link_url = Template(link.link_url).render(Context(context))
            for related in link.get_related_urls():
                rendered = Template(related).render(Context(context))
                if rendered:
                    rendered = rendered.replace(website_url, "/")
                    related_link_urls.append(rendered)
        else:
            link_url = Template(link).render(Context(context))
        link_url = link_url.replace(website_url, "/")
        current_path = request.path
        if request.META['QUERY_STRING']:
            current_path += "?" + request.META['QUERY_STRING']
        if self.is_branch:
            # matching of url branch
            is_active_link = link_url and current_path.startswith(link_url)
        else:
            # strict url matching
            is_active_link = link_url and current_path == link_url
        for related in related_link_urls:
            if current_path.startswith(related):
                is_active_link = True
        if isinstance(link, NavigationLink) and is_active_link:
            '''
            creating a structure of active links like
            request.active_nav_links = {
                'primary-nav': { # the sysname of the root NavigationLink
                    0: 'main-nav', # the sysname of a link at the 0th level
                    1: 'about-us', # the sysname of a link at the 1st level
                    2: 'history', # the sysname of a link at the 2nd level
                    # other levels if available
                    },
                # other menus if they are also active
                }
            '''
            if not hasattr(request, "active_nav_links"):
                request.active_nav_links = {}
            #bits = link.path.split("/")
            #if bits[1]:
            #    root_pk, sort_order = bits[1].split("_")
            #    root_link = NavigationLink.objects.get(pk=root_pk)
            #    request.active_nav_links.setdefault(root_link.sysname, {})
            #    request.active_nav_links[root_link.sysname][link.get_level()] = link.sysname
        if self.activeness_variable:
            context[self.activeness_variable] = is_active_link
            return ""
        else:
            return is_active_link and "active" or ""

register.tag('activeness', do_check_activeness)
register.tag('branch_activeness', do_check_branch_activeness)


def do_adjacent_child_of(parser, token):
    """
    This will output the children of NavigationLink with the specified sysname. By default it uses the templates navigation/next.html and navigation/previous.html, but optionally you can set some custom template.

    Usage::

        {% next_child_of <sysname> [loop] [using <template_path>] %}
        {% previous_child_of <sysname> [loop] [using <template_path>] %}

    Examples::

        {% next_child_of "primary-nav" loop %}
        {% previous_child_of request.active_nav_links.primary-nav.2 using "navigation/next_product.html" %}

    """
    template_path = ""
    loop = False
    bits = token.split_contents()
    tag_name = bits.pop(0)
    if tag_name == "next_child_of":
        direction = "next"
    else:
        direction = "previous"
    try:
        sysname = bits.pop(0)
        assert(len(bits)<=3)
        if len(bits)==1:
            assert(bits[0] == "loop")
            loop = True
        elif len(bits)==2:
            assert(bits[0] == "using")
            template_path = bits[1]
        elif len(bits)==3:
            assert(bits[0] == "loop")
            assert(bits[1] == "using")
            loop = True
            template_path = bits[2]
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires a following syntax: {%% %s <sysname> [loop] [using <template_path>] %%}" % (tag_name, tag_name)
    return ChildOfNavLink(sysname, direction, loop, template_path)

class ChildOfNavLink(template.Node):
    def __init__(self, sysname, direction, loop, template_path):
        self.sysname = sysname
        self.direction = direction
        self.loop = loop
        self.template_path = template_path
    def render(self, context):
        request = context['request']
        if not hasattr(request, "active_nav_links"):
            return ""
        
        try:
            sysname = template.resolve_variable(self.sysname, context)
            parent_link = NavigationLink.site_objects.get(sysname=sysname)
        except:
            return ""
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except:
            template_path = ""
        
        root_link = None
        bits = parent_link.path.split("/")
        if bits[1]:
            root_pk, sort_order = bits[1].split("_")
            root_link = NavigationLink.objects.get(pk=root_pk)
        if not root_link:
            root_link = parent_link
        active_link_sysname = request.active_nav_links.get(root_link.sysname, {}).get(parent_link.get_level() + 1)
        try:
            active_link = NavigationLink.site_objects.get(sysname=active_link_sysname)
        except:
            return ""
        
        nav_link = None
        if request.user.is_authenticated():
            extra = {
                'is_shown_for_users': True,
                }
        else:
            extra = {
                'is_shown_for_visitors': True,
                }
                
        if self.direction == "previous":
            previous_links = NavigationLink.site_objects.filter(
                parent=parent_link,
                sort_order__lt=active_link.sort_order,
                **extra
                ).order_by("-sort_order")
            if previous_links.count():
                nav_link = previous_links[0]
            elif self.loop:
                nav_link = NavigationLink.site_objects.filter(
                parent=parent_link,
                **extra
                ).order_by("-sort_order")[0]
        elif self.direction == "next":
            next_links = NavigationLink.site_objects.filter(
                parent=parent_link,
                sort_order__gt=active_link.sort_order,
                **extra
                ).order_by("sort_order")
            if next_links.count():
                nav_link = next_links[0]
            elif self.loop:
                nav_link = NavigationLink.site_objects.filter(
                parent=parent_link,
                **extra
                ).order_by("sort_order")[0]
        
        context_vars = context
        context_vars.push()
        context_vars['nav_link'] = nav_link
        output = loader.render_to_string(template_path or "navigation/%s.html" % self.direction, context_vars)
        context_vars.pop()
        return output

register.tag('next_child_of', do_adjacent_child_of)
register.tag('previous_child_of', do_adjacent_child_of)

### FILTERS ###

def nav_link_counter(sysname):
    """ returns the counter of the navigation link in the scope of siblings
    """
    nav_link = NavigationLink.site_objects.get(
        sysname=sysname,
        )
    counter = NavigationLink.site_objects.filter(
        parent=nav_link.parent,
        sort_order__lte=nav_link.sort_order,
        ).count()
    return counter
    
register.filter('nav_link_counter', nav_link_counter)

