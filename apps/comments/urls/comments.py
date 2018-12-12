from django.conf.urls import *

urlpatterns = patterns(
    'jetson.apps.comments.views',
    (r'^post/$', 'comments.post_comment'),
    (r'^posted/$', 'comments.comment_was_posted'),
    (r'^karma/vote/(?P<comment_id>\d+)/(?P<vote>up|down)/$', 'karma.vote'),
    (r'^flag/(?P<comment_id>\d+)/$', 'userflags.flag'),
    (r'^flag/(?P<comment_id>\d+)/done/$', 'userflags.flag_done'),
    (r'^delete/(?P<comment_id>\d+)/$', 'userflags.delete'),
    (r'^delete/(?P<comment_id>\d+)/done/$', 'userflags.delete_done'),
)
