# -*- coding: UTF-8 -*-
from django.db.models import signals

try:
    from jetson.apps.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type(
            "bulletin_by_favorite_institution",
            "New bulletin by your favorite institution",
            "one of your favorite institutions published a new bulletin",
            default=0,
        )
        notification.create_notice_type(
            "bulletin_by_contact",
            "New bulletin by your contact",
            "one of your contacts published a new bulletin",
            default=0,
        )

    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"
