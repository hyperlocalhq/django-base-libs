"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from jetson.apps.profanity_filter.models import SwearWord

class SwearWordTest(TestCase):
    def test_filtering(self):
        """
        Test the filtering of swear words
        """
        SwearWord.objects.get_or_create(word="fuck")
        SwearWord.objects.get_or_create(word="fucking")
        SwearWord.objects.get_or_create(word="shit")
        r = SwearWord.objects.get_regex()
        s = """What the fuCkiNg <strong>SHiT</strong>
        are you doing here?"""
        matches = r.findall(s)
        self.failUnless("fuCkiNg" in matches)
        self.failUnless("SHiT" in matches)
        self.failUnless("fuck" not in matches)
        
