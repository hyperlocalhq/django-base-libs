# -*- coding: UTF-8 -*-
from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings

class ExtendedDjangoTestSuiteRunner(DjangoTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        settings.LANGUAGE_CODE = "en"
        settings.SITE_ID = 1
        super(ExtendedDjangoTestSuiteRunner, self).setup_test_environment(**kwargs)
    
