# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


def create_notice_types(app, created_models, verbosity, **kwargs):
    from jetson.apps.notification import models as notification
    notification.create_notice_type(
        "comment_added",
        "Comment Added",
        "a new comment added",
        default=1,
    )


class CommentsConfig(AppConfig):
    name = 'jetson.apps.comments'

    def ready(self):
        from django.db.models import signals
        from jetson.apps.notification import models as notification

        registry.register(self.get_model('Comment'))
        signals.post_migrate.connect(create_notice_types, sender=notification)
