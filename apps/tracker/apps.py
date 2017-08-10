# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


class TrackerConfig(AppConfig):
    name = 'jetson.apps.tracker'

    def ready(self):
        registry.register(self.get_model('Ticket'))

