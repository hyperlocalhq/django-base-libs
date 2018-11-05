# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from base_libs.forms.formprocessing import ID_ACTION_NEW
from base_libs.forms.formprocessing import ID_ACTION_EDIT
from base_libs.forms.formprocessing import ID_ACTION_DELETE
from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED

from ccb.apps.blog.forms import BlogPostForm
from ccb.apps.blog.views import BlogPostFormPreviewHandler
from ccb.apps.blog.feeds import RssFeed, AtomFeed

all_dict = dict(
    status=STATUS_CODE_PUBLISHED,
)

drafts_dict = dict(
    status=STATUS_CODE_DRAFT,
)

feed_dict = dict(
    rss=RssFeed,
    atom=AtomFeed,
)

urlpatterns = patterns(
    'ccb.apps.blog.views',

    # mind the order of the url-patterns!!!!!

    # display blog overview
    url(r'^all/$', 'handle_request', all_dict),

    # drafts
    url(r'^drafts/$', 'handle_request', drafts_dict),

    # public posts
    url(r'^/?$', 'handle_request', all_dict),

    # success pages
    url(r'^created/$', TemplateView.as_view(template_name='blog/post_created.html')),
    url(r'^deleted/$', TemplateView.as_view(template_name='blog/post_deleted.html')),

    # date-based by year
    url(r'^(?P<year>\d{4})/$', 'handle_request', all_dict),

    # date-based by month
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'handle_request', all_dict),

    # date-based by day
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'handle_request', all_dict),

    # post detail
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/$', 'handle_request',
     all_dict),

    # tag based
    url(r'^tag/(?P<tag>[^/]+)/$', 'handle_request', all_dict),

    # syndication feeds
    url(r'^feeds/(?P<feed_type>rss|atom)/$', 'blog_feed', feed_dict),

    # new post
    url(r'^(?P<action>%s)/$' % ID_ACTION_NEW, BlogPostFormPreviewHandler(BlogPostForm, use_ajax=False)),

    # edit or delete post
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/(?P<action>%s|%s)/$' % (
    ID_ACTION_EDIT, ID_ACTION_DELETE), BlogPostFormPreviewHandler(BlogPostForm, use_ajax=False)),

    # comments TODO has to be reworked when new comment app is availabale in django 1.1 
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/comments/add/$',
     'blog_post_comment', {'use_ajax': False}),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/comments/add_ajax/$',
     'blog_post_comment', {'use_ajax': True}),

    # comment modification (accept, refuse, mark_as_spam)
    url(r'^helper/comment/(?P<comment_id>\d+)/(?P<action>refuse|accept|mark_as_spam)/$', 'blog_modify_comment',
     {'use_popup': True}),
    url(
    r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/comment/(?P<comment_id>\d+)/(?P<action>refuse|accept|mark_as_spam)/$',
    'blog_modify_comment', {'use_popup': False}),
)
