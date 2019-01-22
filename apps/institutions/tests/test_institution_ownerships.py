# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.test import SimpleTestCase


class InstitutionOwnershipTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        from django.contrib.auth import get_user_model
        from django.apps import apps
        from base_libs.middleware.threadlocals import set_current_user
        Institution = apps.get_model("institutions", "Institution")
        User = get_user_model()

        super(InstitutionOwnershipTest, cls).setUpClass()

        cls.institution = Institution(title="Demo Institution")
        cls.institution.save()
        cls.user1 = User.objects.create_user(username="demo1", email="demo1@example.com", password="demo1")
        cls.user2 = User.objects.create_user(username="demo2", email="demo2@example.com", password="demo2")
        set_current_user(cls.user1)

    @classmethod
    def tearDownClass(cls):
        super(InstitutionOwnershipTest, cls).tearDownClass()
        if hasattr(cls, "institution"):
            cls.institution.delete()
        if hasattr(cls, "user1"):
            cls.user1.delete()
        if hasattr(cls, "user2"):
            cls.user2.delete()

    def test_institution_ownership(self):
        self.assertEquals(len(self.institution.get_owners()), 0)
        self.institution.set_owner(self.user1.profile)
        self.institution.set_owner(self.user2.profile)
        self.assertEquals(len(self.institution.get_owners()), 2)
        self.institution.remove_owner(self.user1.profile)
        self.institution.remove_owner(self.user2.profile)
        self.assertEquals(len(self.institution.get_owners()), 0)
