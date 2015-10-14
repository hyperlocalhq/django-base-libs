# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig, apps

class InstitutionsConfig(AppConfig):
    name = 'jetson.apps.institutions'

    def ready(self):
        extend_people_app()

def extend_people_app():
    """
    Person modification
    Modify the people app if it's installed:
    - add institution field to IndividualContact
    - change the method get_additional_search_data for Person
    """
    # if people app is registered before institutions app, this function will be called while initiating InstitutionalContact
    # if people app is registered after institutions app, this function will be called for each model registered after Institution initiation until people app gets registered.
    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    Person = apps.get_model("people", "Person")
    IndividualContact = apps.get_model("people", "IndividualContact")
    Institution = apps.get_model("institutions", "Institution")
    # if people app is installed
    if Person and IndividualContact and Institution:
        # add institution field to IndividualContact
        institution = models.ForeignKey(
            Institution,
            verbose_name=_("Institution"),
            blank=True,
            null=True,
        )
        institution.south_field_triple = lambda: (
            "django.db.models.fields.related.ForeignKey",
            ["orm['institutions.institution']"],
            {
                'blank': repr(institution.blank),
                'null': repr(institution.null),
            })
        IndividualContact.add_to_class(
            "institution",
            institution,
        )
        # modify get_additional_search_data() to recieve institution as well
        def wrapped(func):
            def get_additional_search_data(self):
                search_data = func(self)
                contacts = self.get_contacts()
                if contacts:
                    for contact in contacts:
                        if contact.institution:
                            search_data.append(contact.institution.get_title())
                return search_data
            return get_additional_search_data
        Person.get_additional_search_data = wrapped(Person.get_additional_search_data)

        # modification should be done just once, so disconnecting
        models.signals.class_prepared.disconnect(extend_people_app)
