# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from mptt.fields import TreeManyToManyField
from actstream import action

from jetson.apps.marketplace.base import *


### SITE-SPECIFIC JOB POSTING ###


class JobOffer(JobOfferBase):
    talent_in_berlin = models.BooleanField(_("Export to www.talent-in-berlin.de"), default=False)

    categories = TreeManyToManyField(
        "structure.Category",
        verbose_name=_("Categories"),
        limit_choices_to={'level': 0},
        blank=True,
    )

    def get_locality_type(self):
        from jetson.apps.location.models import LocalityType
        try:
            postal_address = self.postal_address
            if postal_address.country.iso2_code != "DE":
                return LocalityType.objects.get(
                    slug="international",
                )
            elif postal_address.city.lower() != "berlin":
                return LocalityType.objects.get(
                    slug="national",
                )
            else:
                import re
                from jetson.apps.location.data import POSTAL_CODE_2_DISTRICT

                locality = postal_address.get_locality()
                regional = LocalityType.objects.get(
                    slug="regional",
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
                    term, created = LocalityType.objects.get_or_create(
                        slug=slugify(district),
                        parent=regional,
                        defaults=d,
                    )
                    return term
                else:
                    return regional
        except Exception:
            return None

    def is_editable(self, user=None):
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_editable_cache = user.has_perm("marketplace.change_joboffer", self)
        return self._is_editable_cache

    def is_deletable(self, user=None):
        if not hasattr(self, "_is_deletable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_deletable_cache = user.has_perm("marketplace.delete_joboffer", self)
        return self._is_deletable_cache

    def is_public(self):
        return self.status == "published"

    def get_url_path(self):
        try:
            path = reverse("job_offer_detail", kwargs={
                'secure_id': self.get_secure_id(),
            })
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def get_content_provider(self):
        if not hasattr(self, "_content_provider"):
            from django.contrib.contenttypes.models import ContentType
            from jetson.apps.external_services.models import ObjectMapper
            mappers = ObjectMapper.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.pk,
            )
            self._content_provider = None
            if mappers:
                self._content_provider = mappers[0].service
        return self._content_provider

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

            user = get_current_user()
            if user:
                action.send(user, verb="added job offer", action_object=instance)

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
                action.send(instance.offering_institution, verb="looking for", action_object=instance)

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
                action.send(instance.contact_person.user, verb="became contact person for", action_object=instance)


models.signals.post_save.connect(job_offer_created, sender=JobOffer)
