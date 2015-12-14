# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


class MessagingConfig(AppConfig):
    name = 'jetson.apps.messaging'

    def ready(self):
        registry.register(self.get_model('InternalMessage'))

