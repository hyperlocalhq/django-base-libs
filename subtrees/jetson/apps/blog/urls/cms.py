# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from base_libs.forms.formprocessing import ID_ACTION_NEW
from base_libs.forms.formprocessing import ID_ACTION_EDIT
from base_libs.forms.formprocessing import ID_ACTION_DELETE
from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED

from jetson.apps.blog.forms import BlogPostForm
from jetson.apps.blog.views.cms import BlogPostFormPreviewHandler
from jetson.apps.blog.feeds import RssFeed, AtomFeed

all_dict = dict(
    status=STATUS_CODE_PUBLISHED,
    only_for_this_site=True,
)

drafts_dict = dict(
    status=STATUS_CODE_DRAFT,
    only_for_this_site=True,
)

feed_dict = dict(
    rss=RssFeed,
    atom=AtomFeed,
    only_for_this_site=True,
)

urlpatterns = patterns(
    'jetson.apps.blog.views.cms',

    # mind the order of the url-patterns!!!!!

    # display blog overview
    (r'^all/$', 'handle_request', all_dict),

    # drafts
    (r'^drafts/$', 'handle_request', drafts_dict),

    # public posts
    (r'^/?$', 'handle_request', all_dict),

    # date-based by year
    (r'^(?P<year>\d{4})/$', 'handle_request', all_dict),

    # date-based by month
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'handle_request', all_dict),

    # date-based by day
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'handle_request', all_dict),

    # post detail
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/$',
     'handle_request', all_dict),

    # tag based
    url(r'^tag/(?P<tag>[^/]+)/$', 'handle_request', all_dict, name="blog_posts_by_tag"),

    # syndication feeds
    (r'^feeds/(?P<feed_type>rss|atom)/$', 'blog_feed', feed_dict),

    # new post
    (r'^(?P<action>%s)/$' % ID_ACTION_NEW, BlogPostFormPreviewHandler(BlogPostForm, use_ajax=False),
     all_dict),

    # edit or delete post
    (
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/(?P<action>%s|%s)/$' % (
            ID_ACTION_EDIT, ID_ACTION_DELETE), BlogPostFormPreviewHandler(BlogPostForm, use_ajax=False),
        all_dict),

    # comments TODO has to be reworked when new comment app is available in django 1.1
    (
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/comments/add/$',
        'blog_post_comment', {'use_ajax': False}),
    (
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/comments/add_ajax/$',
        'blog_post_comment', {'use_ajax': True}),

    # comment modification (accept, refuse, mark_as_spam)
    (r'^helper/comment/(?P<comment_id>\d+)/(?P<action>refuse|accept|mark_as_spam)/$',
     'blog_modify_comment', {'use_popup': True}),
    (
        r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post_slug>[0-9A-Za-z-_]+)/comment/(?P<comment_id>\d+)/(?P<action>refuse|accept|mark_as_spam)/$',
        'blog_modify_comment', {'use_popup': False}),
)
