# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from actstream import registry


class MarketplaceConfig(AppConfig):
    name = 'ccb.apps.marketplace'

    def ready(self):
        registry.register(self.get_model('JobOffer'))

