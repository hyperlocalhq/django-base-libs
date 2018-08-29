# -*- coding: UTF-8 -*-
from django.conf.urls import *

# @@@ from atom import Feed

from jetson.apps.notification.views import notices, mark_all_seen, feed_for_user, single, notification_settings

urlpatterns = patterns('',
    url(r'^$', notices, name="notification_notices"),
    url(r'^settings/$', notification_settings, name="notification_settings"),
    url(r'^(\d+)/$', single, name="notification_notice"),
    url(r'^feed/$', feed_for_user, name="notification_feed_for_user"),
    url(r'^mark-all-seen/$', mark_all_seen, name="notification_mark_all_seen"),
)
