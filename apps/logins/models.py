# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from base_libs.models import CreationDateMixin
from base_libs.models import CreationModificationMixin
from base_libs.models import PublishingMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField


class LoginActionManager(models.Manager):
    def collect_logins_from_users(self):
        User = get_user_model()
        counter = 0
        for user in User.objects.exclude(last_login=None):
            login_action, created = LoginAction.objects.get_or_create(
                login_date=user.last_login,
                user=user,
            )
            counter += 1
        return counter


class LoginAction(models.Model):
    login_date = models.DateTimeField(_("Login date"), default=now, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE, editable=False)
    user_agent = models.TextField(_("User Agent"), blank=True, editable=False)

    objects = LoginActionManager()

    class Meta:
        verbose_name = _("Login Action")
        verbose_name_plural = _("Login Actions")
        ordering = ['-login_date']

    def __unicode__(self):
        return "{timestamp} {username}".format(
            timestamp=self.login_date.strftime('%Y-%m-%d %H:%M:%S'),
            username=self.user.username,
        )


class WelcomeMessage(CreationModificationMixin, PublishingMixin):
    CONDITION_FIRST_LOGIN = 'f'
    CONDITION_AFTER_1_MONTH = 'm'
    CONDITION_OTHER_LOGINS = 'o'

    CONDITION_CHOICES = (
        (CONDITION_FIRST_LOGIN, _("First login")),
        (CONDITION_AFTER_1_MONTH, _("Login after 1 month of inactivity")),
        (CONDITION_OTHER_LOGINS, _("Other logins")),
    )
    title = MultilingualCharField(_("Title"), max_length=512)
    content = MultilingualTextField(_("Content"))
    condition = models.CharField(_("Condition"), max_length=1, choices=CONDITION_CHOICES, db_index=True)

    class Meta:
        verbose_name = _("Welcome Message")
        verbose_name_plural = _("Welcome Messages")
        ordering = ['title']

    def __unicode__(self):
        return self.title
