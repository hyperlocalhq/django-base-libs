# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


class PeopleConfig(AppConfig):
    name = 'ccb.apps.people'

    def ready(self):
        registry.register(self.get_model('Person'))
