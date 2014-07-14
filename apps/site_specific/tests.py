# -*- coding: UTF-8 -*-
"""
Unit tests for reverse URL lookups.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings

test_data = (
    ('splash_page', [], {}, 200),
    ('jssettings', [], {}, 200),
)

class URLPatternReverse(TestCase):
    urls = settings.ROOT_URLCONF
    fixtures = ("test.json",)

    def test_urlpatterns_and_views(self):
        return
        for name, args, kwargs, status_code in test_data:
            url = reverse(name, args=args, kwargs=kwargs)
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, status_code)
