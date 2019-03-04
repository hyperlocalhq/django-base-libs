# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.utils.text import force_text

from ..models import Recommendation


class RecommendationModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(RecommendationModelTest, cls).setUpClass()
        cls.instance = Recommendation.objects.create(
            sysname="test",
            widget_template="recommendations/includes/news_of_the_category.html",
        )
    
    @classmethod
    def tearDownClass(cls):
        super(RecommendationModelTest, cls).tearDownClass()
        cls.instance.delete()

    def test_str(self):
        self.assertEqual(
            force_text(self.instance),
            "test",
            "The __str__ value doesn't match",
        )
