# -*- coding: UTF-8 -*-
from django.db.models import signals

try:
    from jetson.apps.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("institution_claimed", "Institution Claimed",
                                        "someone has claimed an institution/company as his own", default=0)
        notification.create_notice_type("institution_ownership_confirmed", "Institution Ownership Confirmed",
                                        "someone has been confirmed as the owner of an institution/company", default=2)

    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"
