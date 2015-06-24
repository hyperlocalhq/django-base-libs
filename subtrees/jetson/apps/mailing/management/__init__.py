# -*- coding: UTF-8 -*-
from django.db.models import signals
from django.db import models

try:
    notification = models.get_app("notification")
    if notification:
        def create_notice_types(app, created_models, verbosity, **kwargs):
            notification.create_notice_type("message_received", "Message Received", "someone has written a message to you", default=1)
        
        signals.post_syncdb.connect(create_notice_types, sender=notification)
except:
    print "Skipping creation of NoticeTypes as notification app not found"
