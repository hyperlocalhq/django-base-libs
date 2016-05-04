from celery import shared_task

from django.db import models
from django.template import Context
from django.utils.translation import ugettext, get_language, activate
from django.utils.encoding import force_unicode
from django.template import Template
from django.core.urlresolvers import reverse
from django.conf import settings

from jetson.apps.people.functions import get_user_language

from base_libs.utils.misc import get_installed

send_email_using_template = get_installed("mailing.views.send_email_using_template")
Recipient = get_installed("mailing.recipient.Recipient")

def get_notification_setting(user, notice_type, medium):
    """
    Creates or checks notification.NoticeSetting for a user
    """
    notification = models.get_app("notification")
    NoticeSetting = notification.NoticeSetting
    NOTICE_MEDIA_DEFAULTS = notification.NOTICE_MEDIA_DEFAULTS
    settings = NoticeSetting.objects.filter(user=user, notice_type=notice_type, medium=medium)
    if len(settings) == 0:
        if NOTICE_MEDIA_DEFAULTS[medium] <= notice_type.default:
            frequency = "immediately"
        else:
            frequency = "never"
        setting = NoticeSetting(user=user, notice_type=notice_type, medium=medium, frequency=frequency)
        setting.save()
    else:
        setting = settings[0]
        if len(settings) > 1:
            for repeated_setting in settings[1:]:
                repeated_setting.delete()
    return setting

@shared_task
def send_to_user(user_id, sysname, extra_context=None, on_site=True, instance_ct=None, instance_id=None, sender_id=None,
                 sender_name="", sender_email=""):
    """
    Creates a new notice and/or
    sends notification by email or saves notification to a digest.
    
    Called by notification.send()
    """
    if not extra_context:
        extra_context = {}

    ContentType = models.get_model("contenttypes", "ContentType")
    Site = models.get_model("sites", "Site")
    User = models.get_model("auth", "User")
    NoticeType = models.get_model("notification", "NoticeType")
    Notice = models.get_model("notification", "Notice")
    Digest = models.get_model("notification", "Digest")
    
    instance = None
    if instance_ct and instance_id:
        instance = ContentType.objects.get(
            pk=instance_ct,
            ).get_object_for_this_type(pk=instance_id)
        
    sender = None
    if sender_id:
        sender = User.objects.get(pk=sender_id)
        
    user = User.objects.get(pk=user_id)

    notice_type = NoticeType.objects.get(sysname=sysname)

    current_site = Site.objects.get_current()
    notices_url = u"http://%s%s" % (
        current_site.domain,
        reverse("notification_notices"),
    )
    # setting default values
    if not sender and not sender_name:
        sender_name = ''
    if not sender and not sender_email:
        sender_email = settings.DEFAULT_FROM_EMAIL
        
    current_language = get_language()

    # activate language of user to send message translated
    language = get_user_language(user)
    activate(language)

    # update context with user specific translations
    context = Context({
        "notice": ugettext(notice_type.display),
        "notices_url": notices_url,
        "current_site": current_site,
        "notice_type": notice_type,
        "notified_user": user,
        "object": instance,
    })
    context.update(extra_context)

    # get prerendered format messages
    message = Template(notice_type.get_message_template()).render(context)
    if on_site:
        notice = Notice.objects.create(
            user=user,
            message=force_unicode(message),
            notice_type=notice_type,
            )
        
    if user.email: # Email
        notification_setting = get_notification_setting(user, notice_type, "1")
        if notification_setting.frequency == "immediately":
            send_email_using_template(
                recipients_list=[Recipient(user=user)],
                email_template_slug=sysname,
                obj=instance,
                obj_placeholders=extra_context,
                sender=sender,
                sender_name=sender_name,
                sender_email=sender_email,
                delete_after_sending=True,
                send_immediately=True,
            )
        elif notification_setting.frequency in ("daily", "weekly"):
            digest, _created = Digest.objects.get_or_create(
                user=user,
                frequency=notification_setting.frequency,
                is_sent=False,
                )
            digest.digestnotice_set.create(
                message=message,
                notice_type=notice_type,
                )

    # reset environment to original language
    activate(current_language)

