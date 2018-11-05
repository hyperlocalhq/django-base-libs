# -*- coding: UTF-8 -*-
from jetson.apps.tracker.apps import TrackerConfig as BaseTrackerConfig
from actstream import registry


def create_notice_types(app, created_models, verbosity, **kwargs):
    from jetson.apps.notification import models as notification
    notification.create_notice_type(
        "ticket_reported",
        "Ticket Reported",
        "a new ticket has been reported",
        default=0,
    )


class TrackerConfig(BaseTrackerConfig):
    name = 'ccb.apps.tracker'

    def ready(self):
        from django.db.models import signals
        from jetson.apps.notification import models as notification

        super(TrackerConfig, self).ready()
        registry.register(self.get_model('Ticket'))
        signals.post_migrate.connect(create_notice_types, sender=notification)
