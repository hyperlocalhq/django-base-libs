# -*- coding: UTF-8 -*-

from django.db.models import signals

from jetson.apps.marketplace.management import *

try:
    from jetson.apps.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type(
            "job_offer_by_favorite_institution",
            "New job offer by your favorite institution",
            "one of your favorite institutions published a new job offer",
            default=0,
        )
        notification.create_notice_type(
            "job_offer_by_contact",
            "New job offer by your contact",
            "one of your contacts published a new job offer",
            default=0,
        )

    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"
