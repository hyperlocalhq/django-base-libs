# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from mptt.fields import TreeManyToManyField
from actstream import action
from actstream.models import following, followers

from ccb.apps.events.base import *


### SITE-SPECIFIC EVENT ###

class ExtendedEventManager(EventManager):
    def nearest_published_featured(self):
        return self.nearest().filter(
            status="published",
            is_featured=True,
        ).order_by("-importance", "start").distinct()


class Event(ComplexEventBase):
    fees = MultilingualTextField(_("Fees"), blank=True)

    is_featured = models.BooleanField(_("Featured"), default=False)
    importance = models.IntegerField(_("Importance"), default=0)

    creative_sectors = TreeManyToManyField(
        Term,
        verbose_name=_("Creative sectors"),
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'},
        related_name="creative_industry_events",
        blank=True,
    )
    categories = TreeManyToManyField(
        Category,
        verbose_name=_("categories"),
        blank=True
    )

    objects = ExtendedEventManager()

    def get_creative_sectors(self):
        return self.creative_sectors.all()

    def get_context_categories(self):
        return []

    def get_categories(self):
        return self.categories.all()

    def has_fees(self):
        return bool(self.fees)

    def are_fees_displayed(self, user=None):
        if not hasattr(self, "_are_are_fees_displayed_cache"):
            user = get_current_user(user)
            self._are_are_fees_displayed_cache = bool(
                self.has_fees()
                or (user and user.has_perm("events.change_event", self))
            )
        return self._are_are_fees_displayed_cache

    def is_editable(self, user=None):
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_editable_cache = user.has_perm("events.change_event", self)
        return self._is_editable_cache

    def is_deletable(self, user=None):
        if not hasattr(self, "_is_deletable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_deletable_cache = user.has_perm("events.delete_event", self)
        return self._is_deletable_cache

    def is_public(self):
        return self.status == "published"

    def get_url_path(self):
        try:
            path = reverse("event_detail", kwargs={
                'slug': self.slug,
            })
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    @staticmethod
    def autocomplete_search_fields():
        return ["id__iexact"] + ["title_{}__icontains".format(lang_code) for lang_code, lang_name in settings.LANGUAGES]


class EventTime(ComplexEventTimeBase):
    def closest_start(self):
        now = datetime.now()
        if self.start and self.start < now:
            return now
        return self.start


# Notify appropriate users about new events from contacts and favorite institutions
def event_created(sender, instance, **kwargs):
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

            if instance.organizing_institution:
                institution = instance.organizing_institution
                if institution != instance.venue:
                    institution = instance.venue
                # get users who favorited the institution organizing this event
                # and who haven't received notifications yet
                ci = ContextItem.objects.get_for(
                    institution,
                )
                recipients = followers(institution)
                sent_recipient_pks += [recipient.pk for recipient in recipients]

                notification.send(
                    recipients,
                    "event_by_favorite_institution",
                    {
                        "object_description": instance.description,
                        "object_creator_url": institution.get_url(),
                        "object_creator_title": institution.title,
                        "object_title": unicode(instance.title),
                        "object_url": instance.get_url(),
                    },
                    instance=instance,
                    on_site=False,
                )
                action.send(institution, verb="hosting event", action_object=instance)
            elif instance.organizing_person:
                # get users who favorited the person organizing this event
                # and who haven't received notifications yet
                ci = ContextItem.objects.get_for(
                    instance.organizing_person,
                )
                recipients = [
                    recipient
                    for recipient in followers(instance.organizing_person.user)
                    if recipient.pk not in sent_recipient_pks
                ]
                sent_recipient_pks += [recipient.pk for recipient in recipients]

                notification.send(
                    recipients,
                    "event_by_contact",
                    {
                        "object_description": instance.description,
                        "object_creator_url": instance.organizing_person.get_url(),
                        "object_creator_title": instance.organizing_person.title,
                        "object_title": force_text(instance.get_title()),
                        "object_url": instance.get_url(),
                    },
                    instance=instance,
                    on_site=False,
                )
                action.send(instance.organizing_person.user, verb="organizing event", action_object=instance)
            elif user:
                ci = ContextItem.objects.get_for(
                    user.profile,
                )
                recipients = [
                    recipient
                    for recipient in followers(user)
                    if recipient.pk not in sent_recipient_pks
                ]

                notification.send(
                    recipients,
                    "event_by_contact",
                    {
                        "object_description": instance.description,
                        "object_creator_url": user.profile.get_url(),
                        "object_creator_title": user.profile.title,
                        "object_title": force_text(instance.get_title()),
                        "object_url": instance.get_url(),
                    },
                    instance=instance,
                    on_site=False,
                )
                action.send(user, verb="added event", action_object=instance)


models.signals.post_save.connect(event_created, sender=Event)
