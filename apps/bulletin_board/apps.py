# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


class BulletinBoardConfig(AppConfig):
    name = 'ccb.apps.bulletin_board'

    def ready(self):
        registry.register(self.get_model('Bulletin'))

