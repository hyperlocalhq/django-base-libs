# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig, apps


class GroupsNetworksConfig(AppConfig):
    name = 'jetson.apps.groups_networks'

    def ready(self):
        add_methods_to_person()
        add_methods_to_institution()


def add_methods_to_person():
    """Additional methods to Person model"""

    Person = apps.get_model("people", "Person")
    Institution = apps.get_model("institutions", "Institution")

    def get_groups(self):
        """
        PersonGroups where the person is a member
        """
        PersonGroup = apps.get_model("groups_networks", "PersonGroup")
        if not hasattr(self, "_groups_cache"):
            self._groups_cache = PersonGroup.objects.filter(
                groupmembership__user=self.user,
            )
        return self._groups_cache

    def get_my_groups(self):
        """
        PersonGroups where the person is "owner"
        """
        PersonGroup = apps.get_model("groups_networks", "PersonGroup")
        if not hasattr(self, "_my_groups_cache"):
            self._my_groups_cache = PersonGroup.objects.filter(
                groupmembership__user=self.user,
                groupmembership__role="owners",
            )
        return self._my_groups_cache

    def get_institutions(self, clear_cache=False):
        """
        Institutions for which a PersonGroup is created and
        where the person is a member.
        """
        if not hasattr(self, "_institutions_cache") or clear_cache:
            institution_ids = map(
                (lambda el: el['object_id']),
                self.get_groups().filter(group_type__slug="institutional", ).
                values("object_id")
            )
            self._institutions_cache = Institution.objects.filter(
                pk__in=institution_ids,
            )
        return self._institutions_cache

    def get_all_group_invitations(self):
        qs = Person.objects.filter(
            user__groupmembership__activation__isnull=True,
        ).extra(
            select={
                'person_group_id':
                    'groups_networks_groupmembership.person_group_id',
                'person_group_title':
                    'groups_networks_groupmembership.title',
                'membership_id':
                    'groups_networks_groupmembership.id',
                'membership_role':
                    'groups_networks_groupmembership.role',
                'membership_title_en':
                    'groups_networks_groupmembership.title_en',
                'membership_title_de':
                    'groups_networks_groupmembership.title_de',
                'membership_inviter_id':
                    'groups_networks_groupmembership.inviter_id',
                'membership_is_accepted':
                    'groups_networks_groupmembership.is_accepted',
                'membership_is_blocked':
                    'groups_networks_groupmembership.is_blocked',
                'membership_confirmer_id':
                    'groups_networks_groupmembership.confirmer_id',
                'membership_timestamp':
                    'groups_networks_groupmembership.timestamp',
                'membership_activation':
                    'groups_networks_groupmembership.activation',
            },
        ).select_related().distinct().order_by('-membership_timestamp')
        return qs

    def get_my_groups_invitations(self):
        my_groups_id_list = [item.id for item in self.get_my_groups()]
        qs = self.get_all_group_invitations()
        qs = qs.filter(
            user__groupmembership__person_group__id__in=my_groups_id_list,
            user__groupmembership__inviter=self.user,
        )
        return qs

    def get_my_groups_requests(self):
        my_groups_id_list = [item.id for item in self.get_my_groups()]
        qs = self.get_all_group_invitations()
        qs = qs.filter(
            user__groupmembership__person_group__id__in=my_groups_id_list,
            user__groupmembership__inviter__isnull=True,
        )
        return qs

    def get_other_groups(self):
        PersonGroup = apps.get_model("groups_networks", "PersonGroup")
        qs = PersonGroup.objects.filter(
            groupmembership__activation__isnull=True,
        ).extra(
            select={
                'membership_id':
                    'groups_networks_groupmembership.id',
                'membership_role':
                    'groups_networks_groupmembership.role',
                'membership_title_en':
                    'groups_networks_groupmembership.title_en',
                'membership_title_de':
                    'groups_networks_groupmembership.title_de',
                'membership_inviter_id':
                    'groups_networks_groupmembership.inviter_id',
                'membership_is_accepted':
                    'groups_networks_groupmembership.is_accepted',
                'membership_is_blocked':
                    'groups_networks_groupmembership.is_blocked',
                'membership_confirmer_id':
                    'groups_networks_groupmembership.confirmer_id',
                'membership_timestamp':
                    'groups_networks_groupmembership.timestamp',
                'membership_activation':
                    'groups_networks_groupmembership.activation',
            },
        ).select_related().distinct().order_by('-membership_timestamp')
        return qs

    def get_other_groups_invitations(self):
        qs = self.get_other_groups()
        qs = qs.filter(
            groupmembership__user=self.user,
        ).exclude(
            groupmembership__inviter__isnull=True,
        )
        return qs

    def get_other_groups_requests(self):
        qs = self.get_other_groups()
        qs = qs.filter(
            groupmembership__user=self.user,
            groupmembership__inviter__isnull=True,
        )
        return qs

    Person.get_groups = get_groups
    Person.get_my_groups = get_my_groups
    Person.get_institutions = get_institutions
    Person.get_all_group_invitations = get_all_group_invitations
    Person.get_my_groups_invitations = get_my_groups_invitations
    Person.get_my_groups_requests = get_my_groups_requests
    Person.get_other_groups = get_other_groups
    Person.get_other_groups_invitations = get_other_groups_invitations
    Person.get_other_groups_requests = get_other_groups_requests


def add_methods_to_institution():
    """Additional methods to Institution model"""

    Institution = apps.get_model("institutions", "Institution")

    from base_libs.utils.misc import get_unique_value
    from base_libs.utils.misc import get_related_queryset
    from base_libs.middleware import get_current_user

    def create_default_group(self):
        PersonGroup = apps.get_model("groups_networks", "PersonGroup")
        group = PersonGroup(
            title=self.title,
            slug=get_unique_value(PersonGroup, self.slug),
            group_type=get_related_queryset(PersonGroup, "group_type").get(
                slug='institutional',
            ),
            access_type="secret",
        )
        group.content_object = self
        group.save()
        return group

    create_default_group.alters_data = True

    def get_groups(self):
        PersonGroup = apps.get_model("groups_networks", "PersonGroup")
        ContentType = apps.get_model("contenttypes", "ContentType")
        if not hasattr(self, "_groups_cache"):
            ct = ContentType.objects.get_for_model(self)
            self._groups_cache = list(
                PersonGroup.objects.filter(
                    content_type__pk=ct.id,
                    object_id=self.id,
                )
            )
        return self._groups_cache

    def get_object_permission_roles(self):
        """
        Returns the default owners of this object for permission manipulation
        """
        groups = self.get_groups()
        if not groups:
            groups = [self.create_default_group()]
        allowed_groups = []
        for person_group in groups:
            allowed_groups.append(
                person_group.perobjectgroup_set.get(
                    sysname__startswith="owners"
                )
            )
            allowed_groups.append(
                person_group.perobjectgroup_set.get(
                    sysname__startswith="moderators"
                )
            )
        return allowed_groups

    def _get_related_group(self):
        groups = self.get_groups()
        if groups:
            return groups[0]
        else:
            return None

    def is_contactable(self, user=None):
        if not hasattr(self, "_is_contactable_cache"):
            user = get_current_user(user)
            group = self._get_related_group()
            contact_dict = self.get_primary_contact()
            self._is_contactable_cache = not (
                group and group.get_owners().filter(user=user)
            ) and contact_dict.get("email0_address", False)
        return self._is_contactable_cache

    def is_email_displayed(self, user=None):
        if not hasattr(self, "_is_email_displayed_cache"):
            user = get_current_user(user)
            #group = self._get_related_group()
            self._is_email_displayed_cache = False
        return self._is_email_displayed_cache

    def is_phone_displayed(self, user=None):
        if not hasattr(self, "_is_phone_displayed_cache"):
            user = get_current_user(user)
            group = self._get_related_group()
            self._is_phone_displayed_cache = True
        return self._is_phone_displayed_cache

    def is_fax_displayed(self, user=None):
        if not hasattr(self, "_is_fax_displayed_cache"):
            user = get_current_user(user)
            group = self._get_related_group()
            self._is_fax_displayed_cache = True
        return self._is_fax_displayed_cache

    def is_mobile_displayed(self, user=None):
        if not hasattr(self, "_is_mobile_displayed_cache"):
            user = get_current_user(user)
            group = self._get_related_group()
            self._is_mobile_displayed_cache = True
        return self._is_mobile_displayed_cache

    Institution.create_default_group = create_default_group
    Institution.get_groups = get_groups
    Institution.get_object_permission_roles = get_object_permission_roles
    Institution._get_related_group = _get_related_group
    Institution.is_contactable = is_contactable
    Institution.is_email_displayed = is_email_displayed
    Institution.is_phone_displayed = is_phone_displayed
    Institution.is_fax_displayed = is_fax_displayed
    Institution.is_mobile_displayed = is_mobile_displayed
