# -*- coding: UTF-8 -*-
from jetson.apps.tracker.apps import TrackerConfig as BaseTrackerConfig
from actstream import registry


class TrackerConfig(BaseTrackerConfig):
    name = 'ccb.apps.tracker'

    def ready(self):
        registry.register(self.get_model('Ticket'))

