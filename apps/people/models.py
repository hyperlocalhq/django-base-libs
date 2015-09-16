# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

from jetson.apps.people.base import *

### SITE-SPECIFIC PERSON ###

class PersonManagerExtended(PersonManager):
    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'creation_date_desc': (
                1,
                _('Sign-up date (newest first)'),
                ['-user__date_joined'],
            ),
            'alphabetical_asc': (
                2,
                _('Alphabetical (A-Z)'),
                ['user__last_name'],
            ),
            'completeness_desc': (
                3,
                _('Completeness (complete first)'),
                ['-completeness', '-user__date_joined'],
            ),
        }
        return sort_order_mapper

    def latest_published_with_avatars(self):
        return self.latest_published().exclude(image="")


class Person(PersonBase):
    creative_sectors = TreeManyToManyField(
        Term,
        verbose_name=_("Creative sectors"),
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'},
        related_name="creative_industry_people",
        blank=True,
    )
    completeness = models.SmallIntegerField(_("Completeness in %"), default=0)

    objects = PersonManagerExtended()

    def get_creative_sectors(self):
        return self.creative_sectors.all()

    def is_deletable(self, user=None):
        if not hasattr(self, "_is_deletable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_deletable_cache = user.has_perm("people.delete_person", self)
        return self._is_deletable_cache

    def calculate_completeness(self):
        progress = 0
        if self.user.first_name and self.user.last_name:
            progress += 25
        if self.image:
            progress += 25
        if self.description:
            progress += 25
        if self.individualcontact_set.count():
            progress += 25
        self.completeness = progress


class IndividualContact(IndividualContactBase):
    def is_public(self):
        return self.person.status == "published"
