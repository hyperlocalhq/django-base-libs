# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig, apps


def create_notice_types(app, created_models, verbosity, **kwargs):
    from jetson.apps.notification import models as notification
    notification.create_notice_type(
        "message_received",
        "Message Received",
        "someone has written a message to you",
        default=1,
    )


class MailingConfig(AppConfig):
    name = 'jetson.apps.mailing'

    def ready(self):
        from django.db.models import signals
        from jetson.apps.notification import models as notification

        signals.post_migrate.connect(create_notice_types, sender=notification)
