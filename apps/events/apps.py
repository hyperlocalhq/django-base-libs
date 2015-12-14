# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


class EventConfig(AppConfig):
    name = 'ccb.apps.events'

    def ready(self):
        registry.register(self.get_model('Event'))

