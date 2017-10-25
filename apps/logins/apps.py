# -*- coding: UTF-8 -*-
from django.apps import AppConfig


class LoginsConfig(AppConfig):
    name = "ccb.apps.logins"

    def ready(self):
        super(LoginsConfig, self).ready()
