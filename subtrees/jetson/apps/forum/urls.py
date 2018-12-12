# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.conf import settings

from base_libs.forms.formprocessing import ID_ACTION_NEW
from base_libs.forms.formprocessing import ID_ACTION_EDIT
from base_libs.forms.formprocessing import ID_ACTION_DELETE

from jetson.apps.forum.forms import ForumOptionsForm, ForumForm
from jetson.apps.forum.forms import ThreadForm, ReplyForm
from jetson.apps.forum.views import ForumOptionsFormHandler, ForumFormPreviewHandler
from jetson.apps.forum.views import ThreadFormPreviewHandler, ReplyFormPreviewHandler

urlpatterns = patterns(
    'jetson.apps.forum.views',

    # mind the order of the url-patterns!!!!!

    # display forum overview
    (r'^/?$', 'handle_request'),

    # forum options (only edit)
    (
        r'^apply_forum_options/$',
        ForumOptionsFormHandler(ForumOptionsForm, use_ajax=False), {
            'action': ID_ACTION_EDIT
        }
    ),

    # new forum on the root level
    (
        r'^(?P<action>%s)/$' % ID_ACTION_NEW,
        ForumFormPreviewHandler(ForumForm, use_ajax=False)
    ),

    # displays a forum
    (r'^(?P<forum_slug>[^/]+)/$', 'handle_request'),

    # new forum under a given forum, edit or delete forum
    (
        r'^(?P<forum_slug>[^/]+)/(?P<action>%s|%s|%s)/$' %
        (ID_ACTION_NEW, ID_ACTION_EDIT, ID_ACTION_DELETE),
        ForumFormPreviewHandler(ForumForm, use_ajax=False)
    ),

    # start a new thread (mind the action url here! We must not use 'new' in this case,
    # because the 'new' action is used for creating a new forum under a current forum)
    (
        r'^(?P<forum_slug>[^/]+)/start_thread/$',
        ThreadFormPreviewHandler(ThreadForm, use_ajax=False), {
            'action': ID_ACTION_NEW
        }
    ),

    # displays a thread
    (r'^(?P<forum_slug>[^/]+)/(?P<thread_slug>[^/]+)/$', 'handle_request'),

    # edit or delete thread
    (
        r'^(?P<forum_slug>[^/]+)/(?P<thread_slug>[^/]+)/(?P<action>%s|%s)/$' %
        (ID_ACTION_EDIT, ID_ACTION_DELETE),
        ThreadFormPreviewHandler(ThreadForm, use_ajax=False)
    ),

    # new reply to thread!
    (
        r'^(?P<forum_slug>[^/]+)/(?P<thread_slug>[^/]+)/(?P<action>%s)/$' %
        ID_ACTION_NEW, ReplyFormPreviewHandler(ReplyForm, use_ajax=False)
    ),

    # new reply to a reply, edit or delete reply
    (
        r'^(?P<forum_slug>[^/]+)/(?P<thread_slug>[^/]+)/(?P<reply_slug>[^/]+)/(?P<action>%s|%s|%s)/$'
        % (ID_ACTION_NEW, ID_ACTION_EDIT, ID_ACTION_DELETE),
        ReplyFormPreviewHandler(ReplyForm, use_ajax=False)
    ),
)
