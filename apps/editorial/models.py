# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.fields import ExtendedTextField

from cms.models import CMSPlugin

class QuestionAnswer(CMSPlugin):
    question = models.CharField(_('question'), max_length=255)
    answer = ExtendedTextField(_('answer'), max_length=16384)

    class Meta:
        verbose_name = _('Question and Answer')
        verbose_name_plural = _('Questions and Answers')

    def __unicode__(self):
        return self.question
