# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

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
    categories = TreeManyToManyField(
        Category,
        verbose_name=_("categories"),
        blank=True
    )
    completeness = models.SmallIntegerField(_("Completeness in %"), default=0)

    photo_author = models.CharField(_("Photo Credits"), max_length=100, blank=True)

    objects = PersonManagerExtended()

    def get_url_path(self):
        try:
            path = reverse("member_detail", kwargs={'slug': self.user.username})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def get_creative_sectors(self):
        return self.creative_sectors.all()

    def get_categories(self):
        return self.categories.all()

    def is_editable(self, user=None):
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_editable_cache = user.has_perm("people.change_person", self)
        return self._is_editable_cache

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

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "user__username__icontains", "user__first_name__icontains", "user__last_name__icontains",)

    def is_curator(self):
        return self.user.groups.filter(name="Curators").exists()

    def get_containing_curated_lists(self):
        from django.contrib.contenttypes.models import ContentType
        from ccb.apps.curated_lists.models import CuratedList
        ct = ContentType.objects.get_for_model(self)
        return CuratedList.objects.filter(
            privacy="public",
            listitem__content_type=ct,
            listitem__object_id=self.pk,
        )


class IndividualContact(IndividualContactBase):
    def is_public(self):
        return self.person.status == "published"
