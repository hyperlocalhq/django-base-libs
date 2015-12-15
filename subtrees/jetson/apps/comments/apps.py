# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


class CommentsConfig(AppConfig):
    name = 'jetson.apps.comments'

    def ready(self):
        registry.register(self.get_model('Comment'))

