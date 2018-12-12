# -*- coding: utf-8 -*-
from django import template
from django.template import loader

from jetson.apps.forum.models import ForumContainer, Forum, ForumThread, ForumReply
from jetson.apps.forum.forms import ReplyForm

register = template.Library()


class ForumChildListNode(template.Node):
    def __init__(self, lookup_var, var_name):
        self.lookup_var = lookup_var
        self.var_name = var_name

    def render(self, context):
        obj = template.resolve_variable(self.lookup_var, context)

        if isinstance(obj, ForumContainer):
            forum_child_list = Forum.objects.filter(
                container=obj, parent__isnull=True
            )
        else:
            forum_child_list = Forum.objects.filter(parent=obj)

        context[self.var_name] = forum_child_list
        return ''


class ForumThreadListNode(template.Node):
    def __init__(self, forum_lookup_var, var_name):
        self.forum_lookup_var = forum_lookup_var
        self.var_name = var_name

    def render(self, context):
        forum = template.resolve_variable(self.forum_lookup_var, context)
        context[self.var_name] = forum.get_threads()
        return ''


class ForumReplyListNode(template.Node):
    def __init__(self, thread_lookup_var, var_name):
        self.thread_lookup_var = thread_lookup_var
        self.var_name = var_name

    def render(self, context):
        thread = template.resolve_variable(self.thread_lookup_var, context)
        context[self.var_name] = thread.get_replies()
        return ''


class DoGetForumChildList:
    """
    Gets Forum children for the given params and populates
    the template context. 
    Syntax::
        {% get_forum_children for [context_var_containing_forum] as [varname] %}
        to get all the children of a forum or
        {% get_forum_children for [context_var_containing_container] as [varname] %}
        to get the root forums of a container
    Example usage::
        {% get_forum_children for forum as forum_child_list %}
        {% get_forum_children for container as root_forums_list %}
    Remarks: Here either a forum or a container can be set to get all the "children".
        In the first case, these are the child forums of a forum, in the second case,
        the root forums of a container are got. (This is some kind of ducktyping, but
        why not :)?)
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):
        tokens = token.contents.split()
        # Now tokens is a list like this:
        # ['get_forum_children', 'for', 'forum', 'as', 'child_list']
        if not len(tokens) == 5:
            raise template.TemplateSyntaxError, "%r tag requires exactly 5" % tokens[
                0]
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[
                0]

        forum_var_name = tokens[2]
        if tokens[3] != 'as':
            raise template.TemplateSyntaxError, "Third argument in %r must be 'as'" % tokens[
                0]
        return ForumChildListNode(forum_var_name, tokens[4])


class DoGetThreadList:
    """
    Gets Threads for the given forum and populates
    the template context.
    Syntax::
        {% get_threads for [context_var_containing_forum] as [varname] %}
    Example usage::
        {% get_threads for forum as thread_list %}
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):
        tokens = token.contents.split()
        # Now tokens is a list like this:
        # ['get_threads', 'for', 'forum', 'as', 'child_list']
        if not len(tokens) == 5:
            raise template.TemplateSyntaxError, "%r tag requires exactly 5" % tokens[
                0]
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[
                0]

        forum_var_name = tokens[2]
        if tokens[3] != 'as':
            raise template.TemplateSyntaxError, "Third argument in %r must be 'as'" % tokens[
                0]
        return ForumThreadListNode(forum_var_name, tokens[4])


class DoGetReplyList:
    """
    Gets Replies for the given thread and populates
    the template context.
    Syntax::
        {% get_replies for [context_var_containing_thread] as [varname] %}
    Example usage::
        {% get_thread for thread as reply_list %}
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):
        tokens = token.contents.split()
        # Now tokens is a list like this:
        # ['get_replies', 'for', 'thread', 'as', 'reply_list']
        if not len(tokens) == 5:
            raise template.TemplateSyntaxError, "%r tag requires exactly 5" % tokens[
                0]
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[
                0]

        forum_var_name = tokens[2]
        if tokens[3] != 'as':
            raise template.TemplateSyntaxError, "Third argument in %r must be 'as'" % tokens[
                0]
        return ForumReplyListNode(forum_var_name, tokens[4])


register.tag('get_forum_children', DoGetForumChildList())
register.tag('get_thread_list', DoGetThreadList())
register.tag('get_reply_list', DoGetReplyList())
