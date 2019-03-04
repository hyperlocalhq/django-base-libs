# -*- coding: UTF-8 -*-
from django.apps import AppConfig, apps


class MessagingConfig(AppConfig):
    name = 'jetson.apps.messaging'

    def ready(self):
        if apps.is_installed("actstream"):
            from actstream import registry
            registry.register(self.get_model('InternalMessage'))
