# -*- coding: UTF-8 -*-
import datetime
import sys

from django.db import models
from django.conf import settings
from django.template.defaultfilters import striptags
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.db.models.query import QuerySet
from django.utils.timezone import now as tz_now

from base_libs.utils.misc import html_to_plain_text
from base_libs.utils.misc import get_installed
from base_libs.models.models import UrlMixin
from base_libs.models.models import SysnameMixin
from base_libs.models.models import CreationDateMixin
from base_libs.models.models import ObjectRelationMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualPlainTextField

# The following won't work, because apps are not yet loaded to the registry at this point:
# EmailTemplate = apps.get_model("mailing", "EmailTemplate")
# so we are retrieving the EmailTemplate by the get_installed() function.
EmailTemplate = get_installed("mailing.models.EmailTemplate")

verbose_name = _("Notification")


class SiteProfileNotAvailable(Exception):
    pass


class NoticeTypeCategory(models.Model):
    title = MultilingualCharField(_('display'), max_length=50)
    is_public = models.BooleanField(
        _('public'),
        help_text=_(
            'is this category displayed in the public notification settings?'
        ),
        default=True
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("notice-type category")
        verbose_name_plural = _("notice-type categories")
        ordering = ("title", )


NOTICE_MEDIA_DEFAULTS_CHOICES = (
    (0, _("Not reported")),
    (1, _("Shown in the website")),
    (2, _("Shown in the website and sent by email")),
)


class NoticeType(
    SysnameMixin(
        help_text=_(
            "should match the slug of an associated EmailTemplate object"
        )
    )
):  #TODO max_length 40 -> 255
    category = models.ForeignKey(
        NoticeTypeCategory, verbose_name=_("Category"), null=True, blank=True
    )
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    display = MultilingualCharField(_('display'), max_length=50)
    description = MultilingualCharField(_('description'), max_length=100)
    message_template = MultilingualPlainTextField(
        _("Message Template"),
        help_text=_(
            "This message will be shown in the website. Accepted template variables: {{ notified_user }}, {{ object }}, and specific extra context."
        )
    )

    # by default only on for media with sensitivity less than or equal to this number
    default = models.IntegerField(
        _('default media'),
        choices=NOTICE_MEDIA_DEFAULTS_CHOICES,
        help_text=_("How will the notices be reported to users by default?")
    )
    is_public = models.BooleanField(
        _('public'),
        help_text=_(
            'is this notice type displayed in the public notification settings?'
        ),
        default=True
    )

    def get_display(self):
        return mark_safe(force_unicode(self.display))

    get_display.short_description = _("Display")

    def get_description(self):
        return mark_safe(force_unicode(self.description))

    get_description.short_description = _("Description")

    def get_message_template(self):
        return mark_safe(force_unicode(self.message_template))

    def __unicode__(self):
        return self.sysname

    class Meta:
        verbose_name = _("notice type")
        verbose_name_plural = _("notice types")
        ordering = (
            "sort_order",
            "category__title",
            "display",
        )


class NoticeEmailTemplate(EmailTemplate):
    pass


# if this gets updated, the create() method below needs to be as well...
NOTICE_MEDIA = (("1", _("Email")), )

# how spam-sensitive is the medium
NOTICE_MEDIA_DEFAULTS = {
    "1": 2  # email
}

NOTICE_FREQUENCY = (
    ('never', _("Don't send notifications")),
    ('immediately', _("Send immediately")),
    ('daily', _("Send in a daily digest")),
    ('weekly', _("Send in a weekly digest")),
)


class NoticeSetting(models.Model):
    """
    Indicates, for a given user, whether to send notifications
    of a given type to a given medium.
    """

    user = models.ForeignKey(User, verbose_name=_('user'))
    notice_type = models.ForeignKey(NoticeType, verbose_name=_('notice type'))
    medium = models.CharField(_('medium'), max_length=1, choices=NOTICE_MEDIA)
    frequency = models.CharField(
        _('sending frequency'), max_length=15, choices=NOTICE_FREQUENCY
    )

    class Meta:
        verbose_name = _("notice setting")
        verbose_name_plural = _("notice settings")


DIGEST_FREQUENCY = (
    ('daily', _("Daily")),
    ('weekly', _("Weekly")),
)


class Digest(CreationDateMixin):
    user = models.ForeignKey(User, verbose_name=_('user'))
    frequency = models.CharField(
        _('frequency'), max_length=15, choices=DIGEST_FREQUENCY
    )
    is_sent = models.BooleanField(_('sent?'), default=False)

    class Meta:
        verbose_name = _("digest")
        verbose_name_plural = _("digests")

    def __unicode__(self):
        return _(u"Notification digest to %s") % self.user

    def send(self):
        from base_libs.utils.misc import get_installed
        Recipient = get_installed("mailing.recipient.Recipient")
        send_email_using_template = get_installed("mailing.views.send_email_using_template")
        # setting default values
        sender_name = ''
        sender_email = settings.DEFAULT_FROM_EMAIL

        notices_html = ""
        for notice in self.digestnotice_set.all():
            notices_html += notice.message

        send_email_using_template(
            recipients_list=[Recipient(user=self.user)],
            email_template_slug="%s_digest" % self.frequency,
            obj_placeholders={
                'notices_html': notices_html,
                'notices_text': html_to_plain_text(notices_html),
            },
            sender_name=sender_name,
            sender_email=sender_email,
            delete_after_sending=True,
        )
        # send
        self.is_sent = True
        self.save()


class DigestNotice(CreationDateMixin):
    digest = models.ForeignKey(Digest, verbose_name=_('digest'))
    message = models.TextField(_('message'))
    notice_type = models.ForeignKey(NoticeType, verbose_name=_('notice type'))

    def __unicode__(self):
        return striptags(self.message)

    class Meta:
        verbose_name = _("notice of a digest")
        verbose_name_plural = _("notices of digests")
        ordering = ['creation_date']


class NoticeManager(models.Manager):
    def notices_for(self, user, archived=False, unseen=None):
        """
        returns Notice objects for the given user.

        If archived=False, it only include notices not archived.
        If archived=True, it returns all notices for that user.

        If unseen=None, it includes all notices.
        If unseen=True, return only unseen notices.
        If unseen=False, return only seen notices.
        """
        if archived:
            qs = self.filter(user=user)
        else:
            qs = self.filter(user=user, archived=archived)
        if unseen is not None:
            qs = qs.filter(unseen=unseen)
        return qs

    def unseen_count_for(self, user):
        """
        returns the number of unseen notices for the given user but does not
        mark them seen
        """
        return self.filter(user=user, unseen=True).count()


class Notice(UrlMixin):

    user = models.ForeignKey(User, verbose_name=_('user'))
    message = models.TextField(_('message'))
    notice_type = models.ForeignKey(NoticeType, verbose_name=_('notice type'))
    added = models.DateTimeField(_('added'), default=tz_now)
    unseen = models.BooleanField(_('unseen'), default=True)
    archived = models.BooleanField(_('archived'), default=False)

    objects = NoticeManager()

    def __unicode__(self):
        return force_unicode(self.message)

    def archive(self):
        self.archived = True
        self.save()

    def is_unseen(self):
        """
        returns value of self.unseen but also changes it to false.

        Use this in a template to mark an unseen notice differently the first
        time it is shown.
        """
        unseen = self.unseen
        if unseen:
            self.unseen = False
            self.save()
        return unseen

    class Meta:
        ordering = ["-added"]
        verbose_name = _("notice")
        verbose_name_plural = _("notices")

    @models.permalink
    def get_absolute_url(self):
        return ("notification_notice", [str(self.pk)])

    @models.permalink
    def get_url_path(self):
        return ("notification_notice", [str(self.pk)])


def create_notice_type(
    sysname,
    display,
    description,
    default=2,
    display_de="",
    description_de="",
    is_public=True
):
    """
    Creates a new NoticeType.

    This is intended to be used by other apps by a post_migrate signal handler.
    """
    try:
        NoticeType.objects.get(sysname=sysname)
    except NoticeType.DoesNotExist:
        nt = NoticeType(
            sysname=sysname,
            default=default,
            is_public=is_public,
        )
        nt.display_en = display
        nt.display_de = display_de
        nt.description_en = description
        nt.description_de = description_de
        nt.save()


def send(
    recipients,
    sysname,
    extra_context=None,
    on_site=True,
    instance=None,
    sender=None,
    sender_name="",
    sender_email=""
):
    """
    This is intended to be how other apps create new notices.

    notification.send(user, 'friends_invite_sent', {
        'spam': 'eggs',
        'foo': 'bar',
    )
    """
    if not getattr(settings, "SEND_NOTIFICATIONS", True):
        return

    if not extra_context:
        extra_context = {}
    from tasks import send_to_user

    # preparing recipients
    if not hasattr(recipients, '__iter__'):
        recipients = [recipients]

    if isinstance(recipients, QuerySet):
        user_ids = recipients.values_list("pk", flat=True)
    else:
        user_ids = [user.pk for user in recipients]

    instance_ct = None
    instance_id = None
    if instance:
        instance_ct = ContentType.objects.get_for_model(instance).pk
        instance_id = instance.pk

    sender_id = None
    if sender:
        sender_id = sender.pk

    for user_id in user_ids:
        print('{} - queueing send_to_user'.format(datetime.datetime.now(), ))
        send_to_user(
            user_id, sysname, extra_context, on_site, instance_ct, instance_id,
            sender_id, sender_name, sender_email
        )


class ObservedItemManager(models.Manager):
    def all_for(self, observed, signal):
        """
        Returns all ObservedItems for an observed object,
        to be sent when a signal is emited.
        """
        content_type = ContentType.objects.get_for_model(observed)
        observed_items = self.filter(
            content_type=content_type, object_id=observed.id, signal=signal
        )
        return observed_items

    def get_for(self, observed, observer, signal):
        content_type = ContentType.objects.get_for_model(observed)
        observed_item = self.get(
            content_type=content_type,
            object_id=observed.id,
            user=observer,
            signal=signal
        )
        return observed_item


class ObservedItem(ObjectRelationMixin(is_required=True)):

    user = models.ForeignKey(User, verbose_name=_('user'))

    notice_type = models.ForeignKey(NoticeType, verbose_name=_('notice type'))

    added = models.DateTimeField(_('added'), default=tz_now)

    # the signal that will be listened to send the notice
    signal = models.CharField(verbose_name=_('signal'), max_length=255)

    objects = ObservedItemManager()

    class Meta:
        ordering = ['-added']
        verbose_name = _('observed item')
        verbose_name_plural = _('observed items')

    def send_notice(self):
        send(
            [self.user], self.notice_type.sysname,
            {'observed': self.content_object}
        )

    send_notice.alters_data = True

    def __unicode__(self):
        return u"%s @ %s" % (
            force_unicode(self.content_object),
            force_unicode(self.user),
        )


def observe(observed, observer, notice_type_sysname, signal='post_save'):
    """
    Create a new ObservedItem.

    To be used by applications to register a user as an observer for some object.
    """
    notice_type = NoticeType.objects.get(sysname=notice_type_sysname)
    observed_item = ObservedItem(
        user=observer,
        content_object=observed,
        notice_type=notice_type,
        signal=signal,
    )
    observed_item.save()
    return observed_item


def stop_observing(observed, observer, signal='post_save'):
    """
    Remove an observed item.
    """
    observed_item = ObservedItem.objects.get_for(observed, observer, signal)
    observed_item.delete()


def send_observation_notices_for(observed, signal='post_save'):
    """
    Send a notice for each registered user about an observed object.
    """
    observed_items = ObservedItem.objects.all_for(observed, signal)
    for observed_item in observed_items:
        observed_item.send_notice()
    return observed_items


def is_observing(observed, observer, signal='post_save'):
    try:
        observed_items = ObservedItem.objects.get_for(
            observed, observer, signal
        )
        return True
    except ObservedItem.DoesNotExist:
        return False
    except ObservedItem.MultipleObjectsReturned:
        return True


def handle_observations(sender, instance, *args, **kw):
    send_observation_notices_for(instance)
