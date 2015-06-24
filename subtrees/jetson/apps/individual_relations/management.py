# -*- coding: UTF-8 -*-
from django.db.models import signals

try:
    from jetson.apps.notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("individual_relation_requested", "Individual Relation Requested", "someone has invited you to be his friend", default=1)
        notification.create_notice_type("individual_relation_confirmed", "Individual Relation Confirmed", "someone has confirmed you as his friend", default=1)
    
    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"
