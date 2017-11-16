# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.utils.encoding import force_unicode, smart_unicode, smart_str
from django.conf import settings
from django.dispatch import Signal
from django.utils.translation import ugettext, get_language, activate
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_text_list

from base_libs.models.models import ObjectRelationMixin
from base_libs.models.fields import MultilingualPlainTextField
from base_libs.middleware import get_current_user, get_current_language
from base_libs.utils.misc import get_translation

from jetson.apps.history.default_settings import *

verbose_name = _("History")

ACTION_CHOICES = (
    (A_UNDEFINED, _("Undefined")),
    (A_ADDITION, _("Add")),
    (A_READ, _("Read")),
    (A_CHANGE, _("Change")),
    (A_DELETION, _("Delete")),
    # custom activities depend on each app and model separately
    # i.e. it might be sending an email for mailing.EmailMessage
    #      or exporting a pdf out of flatpages.FlatPage
    (A_CUSTOM1, _("Custom #1")),
    (A_CUSTOM2, _("Custom #2")),
    (A_CUSTOM3, _("Custom #3")),
)

SCOPE_CHOICES = (
    (AS_SYSTEM, _("System")),   # shown only to administrators
    (AS_PRIVATE, _("Private")), # shown only to the related user
    (AS_PUBLIC, _("Public")),   # shown to everyone
)

class ExtendedLogEntryManager(models.Manager):
    def log_action(self, user=None, content_object=None, action_flag=A_UNDEFINED, scope=AS_SYSTEM, **kwargs):
        if not user.pk:  # if the user has just been deleted, skip this logging
            return
        e = self.model(
            user=user,
            action_flag=action_flag,
            object_repr=force_unicode(content_object)[:200],
            scope=scope,
        )
        for lang_code, lang_name in settings.LANGUAGES:
            setattr(e, "change_message_%s" % lang_code, kwargs['change_message_%s' % lang_code])
        if content_object.pk:  # if the object hasn't just been deleted
            e.content_object=content_object
        e.save()

    def import_from_log_entries(self):
        from django.contrib.admin.models import LogEntry
        for item in LogEntry.objects.all():
            e = self.model(
                action_time=item.action_time,
                user=item.user,
                content_type=item.content_type,
                object_id=item.object_id,
                object_repr=item.object_repr,
                action_flag=item.action_flag,
                )
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(e, "change_message_%s" % lang_code, item.change_message)
            e.save()
        LogEntry.objects.all().delete()

    def list_out(self):
        import re
        def format_message(message):
            result = message[:46]
            message = message[46:]
            message = re.sub(
                r"(.{1,45})",
                r"\n               |              | \1",
                message,
                )
            return (result + message).strip()
        entries = self.all().order_by("action_time")
        for el in entries:
            print "%s | %12s | %s" % (
                smart_str(el.action_time)[5:],
                smart_str(el.user.username).ljust(12)[:12],
                format_message(smart_str(el.get_change_message())),
                )

class ExtendedLogEntry(ObjectRelationMixin()):
    action_time = models.DateTimeField(_('action time'), auto_now=True)
    user = models.ForeignKey(User)
    object_repr = models.CharField(_('object repr'), max_length=200)
    action_flag = models.PositiveSmallIntegerField(_('action'), choices=ACTION_CHOICES, default=A_UNDEFINED)
    change_message = MultilingualPlainTextField(_('change message'), blank=True)
    scope = models.PositiveSmallIntegerField(_('scope'), choices=SCOPE_CHOICES, default=AS_SYSTEM)
    objects = ExtendedLogEntryManager()
    
    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-action_time',)

    def __repr__(self):
        return smart_unicode(self.action_time)

    def get_change_message(self, language=None):
        language = language or get_current_language()
        return force_unicode(getattr(self, "change_message_%s" % language, "") or self.change_message)

    def is_addition(self):
        return self.action_flag == A_ADDITION

    def is_change(self):
        return self.action_flag == A_CHANGE

    def is_deletion(self):
        return self.action_flag == A_DELETION

    def get_edited_object(self):
        """Returns the edited object represented by this log entry"""
        return self.content_object

    def get_admin_url(self):
        """
        Returns the admin URL to edit the object represented by this log entry.
        This is relative to the Django admin index page.
        """
        return u"%s/%s/%s/" % (self.content_type.app_label, self.content_type.model, self.object_id)

def get_change_message(old_obj, updated_obj, language=None):
    current_lang = get_current_language()
    activate(language or "en")
    change_message = []
    added, changed, deleted = [], [], []
    
    for f in old_obj._meta.fields:
        if f.primary_key or type(f).__name__.startswith("Multilingual"):
            continue
        field_changed = (getattr(old_obj, f.name) != getattr(updated_obj, f.name))
        if field_changed:
            if getattr(old_obj, f.name) in (None, ""):
                added.append(ugettext(f.verbose_name))
            elif getattr(updated_obj, f.name) in (None, ""):
                deleted.append(ugettext(f.verbose_name))
            else:
                changed.append(ugettext(f.verbose_name))
    if added:
        change_message.append(
            ugettext("Added %s.") % get_text_list(
                added,
                ugettext("and")))
    if changed:
        change_message.append(
            ugettext("Changed %s.") % get_text_list(
                changed,
                ugettext("and")))
    if deleted:
        change_message.append(
            ugettext("Deleted %s.") % get_text_list(
                deleted,
                ugettext("and")))
    change_message = " ".join(change_message)
    if not change_message:
        change_message = ugettext("No fields or some multiple-choice field changed.")
        
    activate(current_lang)
    return change_message

def pre_save_handler(sender, instance, signal, user=None, *args, **kwargs):
    str_model = "%s.%s" % (sender._meta.app_label, sender.__name__.lower())
    if str_model in TRACKED_MODELS:
        if not user:
            user = get_current_user()
            if not(user and user.is_authenticated()):
                user = None
            if not user and isinstance(instance, User):
                user = instance
        if user:
            if instance.pk:
                if A_CHANGE in TRACKED_MODELS[str_model]:
                    try:
                        old_record = sender.objects.get(pk=instance.pk)
                    except:
                        instance._is_new = True
                        return
                    # set default values for change_message and change_message_(*), where (*) is two letter language code for all installed languages other than English
                    named = dict([
                        (
                            "change_message_" + lang[:2],
                            get_change_message(old_record, instance, language=lang[:2])
                        )
                        for lang in dict(settings.LANGUAGES)
                        ])
                    # update change_message and change_message_(*) if get_log_message exists
                    if hasattr(instance, "get_log_message"):
                        for lang in dict(settings.LANGUAGES):
                            lang = lang[:2]
                            message = instance.get_log_message(
                                language=lang,
                                action=A_CHANGE,
                                )
                            if message:
                                named["change_message_" + lang] = message
                    ExtendedLogEntry.objects.log_action(
                        user=user,
                        content_object=old_record,
                        action_flag=A_CHANGE,
                        scope=TRACKED_MODELS[str_model][A_CHANGE],
                        **named
                        )
            else:
                instance._is_new = True

def post_save_handler(sender, instance, signal, user=None, *args, **kwargs):
    str_model = "%s.%s" % (sender._meta.app_label, sender.__name__.lower())
    if str_model in TRACKED_MODELS:
        if not user:
            user = get_current_user()
            if not(user and user.is_authenticated()):
                user = None
        if user:
            if getattr(instance, "_is_new", False) and hasattr(instance, "__unicode__"):
                if A_ADDITION in TRACKED_MODELS[str_model]:
                    # point system
                    points = 0
                    if sender.__name__ in ["Comment", "Rating"]:
                        points = 1
                    elif sender.__name__.endswith("Contribution"):
                        points = 2
                    elif sender.__name__ in ["FundedProject"]:
                        points = 3
                    # set default values for change_message and change_message_(*), where (*) is two letter language code for all installed languages other than English
                    named = dict([
                        (
                            "change_message_" + lang[:2],
                            get_translation("%(obj)s created.", language=lang[:2]) % {
                                'obj': force_unicode(instance),
                                }
                        )
                        for lang in dict(settings.LANGUAGES)
                        ])
                    # update change_message and change_message_(*) if get_log_message exists
                    if hasattr(instance, "get_log_message"):
                        for lang in dict(settings.LANGUAGES):
                            lang = lang[:2]
                            message = instance.get_log_message(
                                language=lang,
                                action=A_ADDITION,
                                )
                            if message:
                                named["change_message_" + lang] = message
                    ExtendedLogEntry.objects.log_action(
                        user=user,
                        content_object=instance,
                        action_flag=A_ADDITION,
                        scope=TRACKED_MODELS[str_model][A_ADDITION],
                        **named
                        )
                    del instance._is_new

def pre_delete_handler(sender, instance, signal, user=None, *args, **kwargs):
    str_model = "%s.%s" % (sender._meta.app_label, sender.__name__.lower())
    if str_model in TRACKED_MODELS:
        if A_DELETION in TRACKED_MODELS[str_model]:
            if not user:
                user = get_current_user()
                if not(user and user.is_authenticated()):
                    user = None
            if user:
                # set default values for change_message and change_message_(*), where (*) is two letter language code for all installed languages other than English
                named = dict([
                    (
                        "change_message_" + lang[:2],
                        get_translation("%(obj)s removed.", language=lang[:2]) % {
                            'obj': force_unicode(instance),
                            }
                    )
                    for lang in dict(settings.LANGUAGES)
                    ])
                # update change_message and change_message_(*) if get_log_message exists
                if hasattr(instance, "get_log_message"):
                    for lang in dict(settings.LANGUAGES):
                        lang = lang[:2]
                        message = instance.get_log_message(
                            language=lang,
                            action=A_DELETION,
                            )
                        if message:
                            named["change_message_" + lang] = message
                ExtendedLogEntry.objects.log_action(
                    user=user,
                    content_object=instance,
                    action_flag=A_DELETION,
                    scope=TRACKED_MODELS[str_model][A_DELETION],
                    **named
                    )

def read_handler(sender, instance, signal, user=None, *args, **kwargs):
    str_model = "%s.%s" % (sender._meta.app_label, sender.__name__.lower())
    if str_model in TRACKED_MODELS:
        if A_READ in TRACKED_MODELS[str_model]:
            if not user:
                user = get_current_user()
                if not(user and user.is_authenticated()):
                    user = None
            if user:
                # set default values for change_message and change_message_(*), where (*) is two letter language code for all installed languages other than English
                named = dict([
                    (
                        "change_message_" + lang[:2],
                        get_translation("%(obj)s seen.", language=lang[:2]) % {
                            'obj': force_unicode(instance),
                            }
                    )
                    for lang in dict(settings.LANGUAGES)
                    ])
                # update change_message and change_message_(*) if get_log_message exists
                if hasattr(instance, "get_log_message"):
                    for lang in dict(settings.LANGUAGES):
                        lang = lang[:2]
                        message = instance.get_log_message(
                            language=lang,
                            action=A_READ,
                            )
                        if message:
                            named["change_message_" + lang] = message
                ExtendedLogEntry.objects.log_action(
                    user=user,
                    content_object=instance,
                    action_flag=A_READ,
                    scope=TRACKED_MODELS[str_model][A_READ],
                    **named
                    )

def custom_action_handler_1(sender, instance, signal, user=None, *args, **kwargs):
    str_model = "%s.%s" % (sender._meta.app_label, sender.__name__.lower())
    if str_model in TRACKED_MODELS:
        if A_CUSTOM1 in TRACKED_MODELS[str_model]:
            if not user:
                user = get_current_user()
                if not(user and user.is_authenticated()):
                    user = None
            if user:
                # set default values for change_message and change_message_(*), where (*) is two letter language code for all installed languages other than English
                named = dict([
                    ("change_message_" + lang[:2], "")
                    for lang in dict(settings.LANGUAGES)
                    ])
                # update change_message and change_message_(*) if get_log_message exists
                if hasattr(instance, "get_log_message"):
                    for lang in dict(settings.LANGUAGES):
                        lang = lang[:2]
                        message = instance.get_log_message(
                            language=lang,
                            action=A_CUSTOM1,
                            )
                        if message:
                            named["change_message_" + lang] = message
                ExtendedLogEntry.objects.log_action(
                    user=user,
                    content_object=instance,
                    action_flag=A_CUSTOM1,
                    scope=TRACKED_MODELS[str_model][A_CUSTOM1],
                    **named
                    )

def custom_action_handler_2(sender, instance, signal, user=None, *args, **kwargs):
    str_model = "%s.%s" % (sender._meta.app_label, sender.__name__.lower())
    if str_model in TRACKED_MODELS:
        if A_CUSTOM2 in TRACKED_MODELS[str_model]:
            if not user:
                user = get_current_user()
                if not(user and user.is_authenticated()):
                    user = None
            if user:
                # set default values for change_message and change_message_(*), where (*) is two letter language code for all installed languages other than English
                named = dict([
                    ("change_message_" + lang[:2], "")
                    for lang in dict(settings.LANGUAGES)
                    ])
                # update change_message and change_message_(*) if get_log_message exists
                if hasattr(instance, "get_log_message"):
                    for lang in dict(settings.LANGUAGES):
                        lang = lang[:2]
                        message = instance.get_log_message(
                            language=lang,
                            action=A_CUSTOM2,
                            )
                        if message:
                            named["change_message_" + lang] = message
                ExtendedLogEntry.objects.log_action(
                    user=user,
                    content_object=instance,
                    action_flag=A_CUSTOM2,
                    scope=TRACKED_MODELS[str_model][A_CUSTOM2],
                    **named
                    )

def custom_action_handler_3(sender, instance, signal, user=None, *args, **kwargs):
    str_model = "%s.%s" % (sender._meta.app_label, sender.__name__.lower())
    if str_model in TRACKED_MODELS:
        if A_CUSTOM3 in TRACKED_MODELS[str_model]:
            if not user:
                user = get_current_user()
                if not(user and user.is_authenticated()):
                    user = None
            if user:
                # set default values for change_message and change_message_(*), where (*) is two letter language code for all installed languages other than English
                named = dict([
                    ("change_message_" + lang[:2], "")
                    for lang in dict(settings.LANGUAGES)
                    ])
                # update change_message and change_message_(*) if get_log_message exists
                if hasattr(instance, "get_log_message"):
                    for lang in dict(settings.LANGUAGES):
                        lang = lang[:2]
                        message = instance.get_log_message(
                            language=lang,
                            action=A_CUSTOM3,
                            )
                        if message:
                            named["change_message_" + lang] = message
                ExtendedLogEntry.objects.log_action(
                    user=user,
                    content_object=instance,
                    action_flag=A_CUSTOM3,
                    scope=TRACKED_MODELS[str_model][A_CUSTOM3],
                    **named
                    )

read_signal = Signal()
custom_action_signal_1 = Signal()
custom_action_signal_2 = Signal()
custom_action_signal_3 = Signal()

signals.pre_save.connect(pre_save_handler)
signals.post_save.connect(post_save_handler)
signals.pre_delete.connect(pre_delete_handler)

read_signal.connect(read_handler)
custom_action_signal_1.connect(custom_action_handler_1)
custom_action_signal_2.connect(custom_action_handler_2)
custom_action_signal_3.connect(custom_action_handler_3)

