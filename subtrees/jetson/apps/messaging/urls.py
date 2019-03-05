# -*- coding: UTF-8 -*-
import os

from django.conf.urls import *

urlpatterns = patterns(
    'jetson.apps.messaging.views',
    url(
        r"^((?P<box>inbox|drafts|sent|deleted)/)?$",
        "messages_list",
        name="messages_list"
    ),
    url(r"^message/(?P<pk>[^/]+)/$", "view_message"),
    url(r"^message/(?P<pk>[^/]+)/reply/$", "reply_message"),
    url(r"^message/(?P<pk>[^/]+)/delete/$", "delete_message"),
    url(r"^message/(?P<pk>[^/]+)/forward/$", "forward_message"),
    url(r"^message/(?P<pk>[^/]+)/send_draft/$", "send_draft_message"),
    url(r"^new/$", "new_message"),
    url(r"^json/$", "json_change_message"),
)
