# -*- coding: UTF-8 -*-
from django.apps import AppConfig, apps


class TrackerConfig(AppConfig):
    name = 'jetson.apps.tracker'

    def ready(self):
        if apps.is_installed("actstream"):
            from actstream import registry
            registry.register(self.get_model('Ticket'))
