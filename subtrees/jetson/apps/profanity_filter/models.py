# -*- coding: UTF-8 -*-

import re
import sys

from datetime import datetime

from django.db import models
from django.conf import settings

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import smart_str, force_unicode
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import ExtendedTextField
from base_libs.middleware import get_current_user
from base_libs.utils.misc import db_table_exists

verbose_name = _("Profanity filter")

DO_REPLACE = getattr(settings, "PROFANITY_DO_REPLACE", True)

MODELS_TO_CHECK = getattr(settings, "PROFANITY_MODELS_TO_CHECK", ())

MODELS_NOT_TO_CHECK = getattr(
    settings, "PROFANITY_MODELS_NOT_TO_CHECK", (
        "admin.LogEntry",
        "auth.Message",
        "contenttypes.ContentType",
        "notification.LogEntry",
        "history.ExtendedLogEntry",
        "configuration.SiteSettings",
        "configuration.PageSettings",
        "permissions.RowLevelPermission",
        "permissions.PerObjectGroup",
        "structure.Vocabulary",
        "structure.Term",
        "structure.ContextCategory",
        "navigation.NavigationLink",
        "tagging.Tag",
    )
)


class SwearWordManager(models.Manager):
    def get_regex(self):
        words = self.values_list("word", flat=True).order_by("-word")
        r = None
        if words:
            words = [re.escape(w) for w in words]
            pattern = r"\b(" + "|".join(words) + r")\b".lower()
            r = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
        return r


class SwearWord(models.Model):
    word = models.CharField(_("Word to filter out"), max_length=80)

    objects = SwearWordManager()

    class Meta:
        verbose_name = _("swear word")
        verbose_name_plural = _("swear words")
        ordering = ('word', )

    def __unicode__(self):
        return self.word


class SwearingCase(ObjectRelationMixin(), CreationModificationDateMixin):
    user = models.ForeignKey(
        User, blank=True, null=True, verbose_name=_("user")
    )
    used_words = models.TextField(_("used words"))

    class Meta:
        verbose_name = _("swearing case")
        verbose_name_plural = _("swearing cases")
        ordering = ('-creation_date', )

    def __unicode__(self):
        return """%s on %s "%s" """ % (
            self.user or "unknown",
            type(self.content_object).__name__,
            force_unicode(self.content_object),
        )


def filter_swear_words(sender, instance, *args, **kwargs):
    if not isinstance(instance, (SwearWord, SwearingCase)):
        if not db_table_exists(SwearWord) or not db_table_exists(SwearingCase):
            return
        app_model = ".".join((sender._meta.app_label, sender.__name__))
        if (
            (not MODELS_TO_CHECK or app_model in MODELS_TO_CHECK) and
            (not MODELS_NOT_TO_CHECK or app_model not in MODELS_NOT_TO_CHECK)
        ):
            swear_words_regex = SwearWord.objects.get_regex()
            if swear_words_regex:
                found_words = []
                for f in sender._meta.fields:
                    if (
                        type(f) in (
                            models.CharField,
                            models.TextField,
                            ExtendedTextField,
                        ) and "object_id" not in f.name
                    ):
                        value = getattr(instance, f.name) or ""
                        try:
                            matches = swear_words_regex.findall(value)
                        except TypeError as e:
                            value = force_unicode(value)
                            matches = swear_words_regex.findall(value)
                        for m in matches:
                            found_words.append(m)
                        if matches and DO_REPLACE:
                            clean_value = swear_words_regex.sub(
                                (lambda m: m.group(0)[0] + "*" * (len(m.group(0)) - 2) + m.group(0)[-1]),
                                value,
                                )
                            setattr(instance, f.name, clean_value)
                instance._found_swear_words = found_words
                # pk might not exist at this point,
                # so reporting should happen after saving


def report_swearing(sender, instance, created, *args, **kwargs):
    found_words = getattr(instance, "_found_swear_words", [])
    if found_words:
        if not db_table_exists(SwearWord) or not db_table_exists(SwearingCase):
            return
        ct = ContentType.objects.get_for_model(instance)
        cases = SwearingCase.objects.filter(
            user=get_current_user(),
            content_type=ct,
            object_id=instance.pk,
            used_words=", ".join(found_words)
        )
        if cases:
            sc = cases[0]
            cases.delete()  # delete duplicates
            sc.save()  # change modification date
        else:
            SwearingCase.objects.create(
                user=get_current_user(),
                content_type=ct,
                object_id=instance.pk,
                used_words=", ".join(found_words)
            )


models.signals.pre_save.connect(filter_swear_words)
models.signals.post_save.connect(report_swearing)
