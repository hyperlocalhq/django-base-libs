# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig, apps


def create_notice_types(app, created_models, verbosity, **kwargs):
    from jetson.apps.notification import models as notification
    notification.create_notice_type(
        "individual_relation_requested",
        "Individual Relation Requested",
        "someone has invited you to be his friend",
        default=1
    )
    notification.create_notice_type(
        "individual_relation_confirmed",
        "Individual Relation Confirmed",
        "someone has confirmed you as his friend",
        default=1
    )


def add_methods_to_person():
    """Additional methods to Person model"""
    Person = apps.get_model("people", "Person")
    IndividualRelation = apps.get_model(
        "individual_relations", "IndividualRelation"
    )
    from base_libs.middleware import get_current_language, get_current_user

    def _get_individual_relation_status(self, user=None):
        if not hasattr(self, "_get_individual_relation_status_cache"):
            user = get_current_user(user)
            status = IndividualRelation.objects.get_status(user, self.user)
            self._get_individual_relation_status_cache = status
        return self._get_individual_relation_status_cache

    def is_contact_addable(self, user=None):
        if not hasattr(self, "_is_contact_addable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_addable_cache = status in (
                "none", "denied", "denying"
            )
        return self._is_contact_addable_cache

    def is_contact_editable(self, user=None):
        if not hasattr(self, "_is_contact_editable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_editable_cache = status == "confirmed"
        return self._is_contact_editable_cache

    def is_contact_removable(self, user=None):
        if not hasattr(self, "_is_contact_removable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_removable_cache = status == "confirmed"
        return self._is_contact_removable_cache

    def is_contact_blockable(self, user=None):
        if not hasattr(self, "_is_contact_blockable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_blockable_cache = status in (
                "invited", "none", "denied", "denying"
            )
        return self._is_contact_blockable_cache

    def is_contact_unblockable(self, user=None):
        if not hasattr(self, "_is_contact_unblockable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_unblockable_cache = status == "blocking"
        return self._is_contact_unblockable_cache

    def is_contact_acceptable(self, user=None):
        if not hasattr(self, "_is_contact_acceptable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_acceptable_cache = status == "invited"
        return self._is_contact_acceptable_cache

    def is_contact_denyable(self, user=None):
        if not hasattr(self, "_is_contact_denyable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_denyable_cache = status == "invited"
        return self._is_contact_denyable_cache

    def is_contact_cancelable(self, user=None):
        if not hasattr(self, "_is_contact_cancelable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_cancelable_cache = status == "inviting"
        return self._is_contact_cancelable_cache

    def is_contactable(self, user=None):
        if not hasattr(self, "_is_contactable_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._is_contactable_cache = bool(
                user and user != self.user and status != "blocked" and
                user.email
            )
        return self._is_contactable_cache

    def is_addable_to_memos(self, user=None):
        if not hasattr(self, "_is_addable_to_memos_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._is_addable_to_memos_cache = user != self.user and status != "blocked"
        return self._is_addable_to_memos_cache

    def is_addable_to_favorites(self, user=None):
        if not hasattr(self, "_is_addable_to_favorites_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._is_addable_to_favorites_cache = user.is_authenticated(
            ) and user != self.user and status != "blocked"
        return self._is_addable_to_favorites_cache

    def are_contacts_displayed(self, user=None):
        # TODO: eliminate ambiguousness of the name "contact"
        if not hasattr(self, "_are_contacts_displayed_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._are_contacts_displayed_cache = bool(
                status != "blocked" and self.get_contacts() and (
                    self.is_address_displayed(user) or
                    self.is_phone_displayed(user) or
                    self.is_fax_displayed(user) or
                    self.is_mobile_displayed(user) or
                    self.is_email_displayed(user) or self.is_im_displayed(user)
                )
            ) or bool(user and user.has_perm("people.change_person", self))
        return self._are_contacts_displayed_cache

    def get_individual_relations(self):
        if not hasattr(self, "_individual_relations_cache"):
            self._individual_relations_cache = self.user.individualrelation_set.all(
            )
        return self._individual_relations_cache

    def get_all_person_invitations(self):
        ir_db_table = IndividualRelation._meta.db_table
        qs = Person.objects.filter(
            user__individualrelation__to_user=self.user
        ).extra(
            select={
                'individualrelation_id': '%s.id' % ir_db_table,
                'individualrelation_timestamp': '%s.timestamp' % ir_db_table,
                'individualrelation_message': '%s.message' % ir_db_table,
                'individualrelation_status': '%s.status' % ir_db_table,
            },
        ).select_related().distinct().order_by('-individualrelation_timestamp')
        return qs

    def get_person_invitation_requests(self, status_filter=None):
        """
        invititaions to an indvivdual relationship you sent
        """
        if not status_filter:
            status_filter = ["invited", "denying"]

        qs = self.get_all_person_invitations()
        qs = qs.filter(
            user__individualrelation__status__in=status_filter,
            # for any reason, it does not work loke this. But WHY??
            #user__to_user__status__in=status_filter,
        )

        return qs

    def get_person_invitation_requested(self, status_filter=None):
        """
        invititaions to an indvivdual relationship which has to be confirmed
        """

        if not status_filter:
            status_filter = ["inviting", "denied"]

        qs = self.get_all_person_invitations()
        qs = qs.filter(
            user__individualrelation__status__in=status_filter,
            # for any reason, it does not work loke this. But WHY??
            #user__to_user__status__in=status_filter,
        )
        return qs

    Person._get_individual_relation_status = _get_individual_relation_status
    Person.is_contact_addable = is_contact_addable
    Person.is_contact_editable = is_contact_editable
    Person.is_contact_removable = is_contact_removable
    Person.is_contact_blockable = is_contact_blockable
    Person.is_contact_unblockable = is_contact_unblockable
    Person.is_contact_acceptable = is_contact_acceptable
    Person.is_contact_denyable = is_contact_denyable
    Person.is_contact_cancelable = is_contact_cancelable
    Person.is_contactable = is_contactable
    Person.is_addable_to_memos = is_addable_to_memos
    Person.is_addable_to_favorites = is_addable_to_favorites
    Person.are_contacts_displayed = are_contacts_displayed
    Person.get_individual_relations = get_individual_relations
    Person.get_all_person_invitations = get_all_person_invitations
    Person.get_person_invitation_requests = get_person_invitation_requests
    Person.get_person_invitation_requested = get_person_invitation_requested


class IndividualRelationsConfig(AppConfig):
    name = 'jetson.apps.individual_relations'

    def ready(self):
        from django.db.models import signals
        from jetson.apps.notification import models as notification
        add_methods_to_person()
        signals.post_migrate.connect(create_notice_types, sender=notification)
