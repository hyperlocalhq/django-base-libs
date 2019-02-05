# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


def create_notice_types(app, created_models, verbosity, **kwargs):
    from jetson.apps.notification import models as notification
    notification.create_notice_type(
        "event_by_favorite_institution",
        "New event by your favorite institution",
        "one of your favorite institutions published a new event",
        default=0,
    )
    notification.create_notice_type(
        "event_by_contact",
        "New event by your contact",
        "one of your contacts published a new event",
        default=0,
    )


class EventsConfig(AppConfig):
    name = 'ccb.apps.events'

    def ready(self):
        from django.db.models import signals
        from jetson.apps.notification import models as notification

        registry.register(self.get_model('Event'))
        signals.post_migrate.connect(create_notice_types, sender=notification)
