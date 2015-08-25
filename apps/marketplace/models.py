# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser

from base_libs.middleware import get_current_user

from jetson.apps.marketplace.base import *

### SITE-SPECIFIC JOB POSTING ###


class JobOffer(JobOfferBase):
    talent_in_berlin = models.BooleanField(_("Export to www.talent-in-berlin.de"), default=False)

    def get_location_type(self):
        try:
            postal_address = self.postal_address
            if postal_address.country.iso2_code != "DE":
                return Term.objects.get(
                    vocabulary__sysname="basics_locality",
                    sysname="international",
                )
            elif postal_address.city.lower() != "berlin":
                return Term.objects.get(
                    vocabulary__sysname="basics_locality",
                    sysname="national",
                )
            else:
                import re
                from jetson.apps.location.data import POSTAL_CODE_2_DISTRICT

                locality = postal_address.get_locality()
                regional = Term.objects.get(
                    vocabulary__sysname="basics_locality",
                    sysname="regional",
                )
                p = re.compile('[^\d]*')  # remove non numbers
                postal_code = p.sub("", postal_address.postal_code)

                district = ""
                if locality and locality.district:
                    district = locality.district
                elif postal_code in POSTAL_CODE_2_DISTRICT:
                    district = POSTAL_CODE_2_DISTRICT[postal_code]
                if district:
                    d = {}
                    for lang_code, lang_verbose in settings.LANGUAGES:
                        d["title_%s" % lang_code] = district
                    term, created = Term.objects.get_or_create(
                        vocabulary=regional.vocabulary,
                        slug=slugify(district),
                        parent=regional,
                        defaults=d,
                    )
                    return term
                else:
                    return regional
        except:
            return None

    def is_deletable(self, user=None):
        if not hasattr(self, "_is_deletable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_deletable_cache = user.has_perm("marketplace.delete_joboffer", self)
        return self._is_deletable_cache

    def is_public(self):
        return self.status == "published"


# Notify appropriate users about new job offers from contacts and favorite institutions
def job_offer_created(sender, instance, **kwargs):
    from django.contrib.sites.models import Site
    from django.contrib.auth.models import User

    from jetson.apps.notification import models as notification

    from ccb.apps.site_specific.models import ContextItem

    if 'created' in kwargs:
        if kwargs['created']:

            # let's not send duplicate notices to users who marked
            # organizing institution, venue, and organizing person as favorite.
            sent_recipient_pks = []

            if instance.offering_institution:
                # get users who favorited the offering_institution where the job_offer is happening
                # and who haven't received notifications yet
                ci = ContextItem.objects.get_for(
                    instance.offering_institution,
                )
                # get users who favorited the institution organizing this job_offer
                recipients = User.objects.filter(
                    favorite__content_type__app_label="site_specific",
                    favorite__content_type__model="contextitem",
                    favorite__object_id=ci.pk,
                ).exclude(pk__in=sent_recipient_pks)
                sent_recipient_pks += list(recipients.values_list("pk", flat=True))

                notification.send(
                    recipients,
                    "job_offer_by_favorite_institution",
                    {
                        "object_description": instance.description,
                        "object_creator_url": instance.offering_institution.get_url(),
                        "object_creator_title": instance.offering_institution.title,
                        "object_title": instance.position,
                        "object_url": instance.get_url(),
                    },
                    instance=instance,
                    on_site=False,
                )

            if instance.contact_person:
                # get users who favorited the person organizing this job_offer
                # and who haven't received notifications yet
                ci = ContextItem.objects.get_for(
                    instance.contact_person,
                )
                recipients = User.objects.filter(
                    favorite__content_type__app_label="site_specific",
                    favorite__content_type__model="contextitem",
                    favorite__object_id=ci.pk,
                ).exclude(pk__in=sent_recipient_pks)

                notification.send(
                    recipients,
                    "job_offer_by_contact",
                    {
                        "object_description": instance.description,
                        "object_creator_url": instance.contact_person.get_url(),
                        "object_creator_title": instance.contact_person.title,
                        "object_title": instance.position,
                        "object_url": instance.get_url(),
                    },
                    instance=instance,
                    on_site=False,
                )


models.signals.post_save.connect(job_offer_created, sender=JobOffer)
