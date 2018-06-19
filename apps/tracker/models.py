# -*- coding: UTF-8 -*-
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import urlize
from actstream import action

from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models import SlugMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_website_url

verbose_name = _("Tracker")

STATUS_CODES = (
    (1, _("Open")),
    (2, _("Working")),
    (3, _("Closed")),
    (4, _("Rejected")),
)

PRIORITY_CODES = (
    (1, _("Now")),
    (2, _("Soon")),
    (3, _("Someday")),
)

PROJECTS = list(enumerate(settings.INSTALLED_APPS))


class Concern(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Concern")
        verbose_name_plural = _("Concerns")


class Ticket(ObjectRelationMixin()):
    submitted_date = models.DateTimeField(_("submitted Date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified Date"), blank=True, null=True, editable=False)

    # one of the fields, submitter_name and submitter is mandatory. If a user is logged in,
    # submitter is filled in as the logged in user, otherwise, the "submitter" must provide a 
    # name (see the save method below).  
    submitter = models.ForeignKey(
        User, blank=True, null=True, verbose_name=_("submitter"),
        related_name="ticket_submitter", on_delete=models.SET_NULL,
    )
    submitter_name = models.CharField(_("submitter name"), max_length=80)
    submitter_email = models.EmailField(_("submitter email"))

    modifier = models.ForeignKey(
        User, blank=True, null=True, verbose_name=_("modifier"),
        related_name="ticket_modifier", on_delete=models.SET_NULL,
    )

    description = models.TextField(_("description"))
    client_info = models.TextField(_("client info"))
    status = models.IntegerField(_("status"), default=1, choices=STATUS_CODES)
    priority = models.IntegerField(_("priority"), default=1, choices=PRIORITY_CODES)

    url = URLField(_("related object's URL"), blank=True, null=True, max_length=255)

    concern = models.ForeignKey(Concern, verbose_name=_("concern"))

    class Meta:
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")
        ordering = ('-submitted_date',)

    def __unicode__(self):
        return self.description

    # begin remove_that_when_subclassing_is_supported        
    def save(self, *args, **kwargs):
        # This is a new object, set the submitter and the creation date ...
        created = not self.id
        if not self.id:
            self.submitter = get_current_user()
            # fill in user name and email
            if self.submitter is not None:
                self.submitter_name = self.submitter.first_name + ' ' + self.submitter.last_name
                if len(self.submitter_name) < 2:
                    self.submitter_name = self.submitter.username
                self.submitter_email = self.submitter.email
                # TODO: Here we must apply a listener (signal) to listen to
                # changes on relating user objects. If a user's name or email
                # changes, the value here for submitter_name and email_address
                # must also change. If a user is deleted, everything should
                # stay as is.    
        else:
            self.modified_date = datetime.now()
            self.modifier = get_current_user()

        super(Ticket, self).save(*args, **kwargs)

        ticket_reported(sender=Ticket, instance=self, created=created)

    # end remove_that_when_subclassing_is_supported
    save.alters_data = True


class TicketModifications(models.Model):
    """ Change History of a Ticket """
    ticket = models.ForeignKey(Ticket, verbose_name=_("ticket"), related_name="ticket_modification")
    modified_date = models.DateTimeField(_("modified Date"), editable=False)
    modifier = models.ForeignKey(User, verbose_name=_("modifier"), editable=False,
                                 related_name="ticket_modification_modifier")

    modification = models.TextField(_("modification"))
    status = models.IntegerField(_("status"), default=1, choices=STATUS_CODES)
    priority = models.IntegerField(_("priority"), default=1, choices=PRIORITY_CODES)

    class Meta:
        verbose_name = _("ticket history")
        verbose_name_plural = _("ticket history")
        ordering = ('modified_date',)

    def __unicode__(self):
        return self.modification

    def save(self, *args, **kwargs):
        # This is a new object, set the submitter and the creation date ...
        self.modified_date = datetime.now()
        self.modifier = get_current_user()

        # change the ticket values ....
        self.ticket.status = self.status
        self.ticket.priority = self.priority
        self.ticket.save()

        super(TicketModifications, self).save(*args, **kwargs)

    save.alters_data = True


# Notify appropriate users about new tickets
def ticket_reported(sender, instance, **kwargs):
    from django.contrib.sites.models import Site
    from django.contrib.auth.models import User
    from jetson.apps.notification import models as notification

    if 'created' in kwargs:
        if kwargs['created']:
            ticket_url = "%sadmin/tracker/ticket/%s/" % (
                get_website_url(),
                instance.pk,
            )
            if instance.submitter_email:
                submitter_email = instance.submitter_email
            else:
                submitter_email = instance.submitter.email
            if instance.submitter_name:
                submitter_name = instance.submitter_name
            else:
                submitter_name = instance.submitter.profile.get_title()
            if instance.submitter:
                submitter_url = instance.submitter.profile.get_url()
            else:
                submitter_url = ticket_url
            '''
            recipients = set(ns.user
                for ns in notification.NoticeSetting.objects.filter(
                notice_type__sysname="ticket_reported",
                send=True,
                medium="1",
                ))
            '''
            recipients = User.objects.filter(is_staff=True, is_active=True)
            # '''
            notification.send(
                recipients,
                "ticket_reported",
                {
                    "object_description": urlize(instance.description),
                    "object_creator_url": submitter_url,
                    "object_creator_title": submitter_name,
                    "object_title": instance.concern.get_title(),
                    "object_url": ticket_url,
                },
                instance=instance,
                on_site=False,
            )
            if instance.submitter:
                action.send(instance.submitter, verb="reported ticket", action_object=instance)

# models.signals.post_save.connect(ticket_reported, sender=Ticket)
