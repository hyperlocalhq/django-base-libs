# -*- coding: UTF-8 -*-
from django.db.models import signals

try:
    from jetson.apps.notification import models as notification
    
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("institution_added", "New Institution Added", "someone has added a new institution/company", default=0)
    
    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"
