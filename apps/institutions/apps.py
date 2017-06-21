# -*- coding: UTF-8 -*-
from jetson.apps.institutions.apps import InstitutionsConfig as BaseInstitutionsConfig
from actstream import registry


class InstitutionsConfig(BaseInstitutionsConfig):
    name = "kb.apps.institutions"

    def ready(self):
        super(InstitutionsConfig, self).ready()
        registry.register(self.get_model('Institution'))
