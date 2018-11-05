# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.fields import ExtendedTextField
from base_libs.models.fields import URLField

from filebrowser.fields import FileBrowseField

from mptt.fields import TreeForeignKey, TreeManyToManyField

from cms.models import CMSPlugin

class QuestionAnswer(CMSPlugin):
    question = models.CharField(_('question'), max_length=255)
    answer = ExtendedTextField(_('answer'), max_length=16384)

    class Meta:
        verbose_name = _('Question and Answer')
        verbose_name_plural = _('Questions and Answers')

    def __unicode__(self):
        return self.question


class Document(CMSPlugin):
    title = models.CharField(_('Title'), max_length=255)
    description = ExtendedTextField(_('Description'), blank=True)

    publisher_title = models.CharField(_('Publisher Title'), max_length=255, blank=True)
    publisher_url = URLField(_('Publisher URL'), blank=True)
    pdf_upload = FileBrowseField(_("PDF Upload"), max_length=255, directory="standortinformationen/", extensions=['.pdf'], blank=True)
    pdf_url = URLField(_('PDF URL'), blank=True)

    image = FileBrowseField(_("Image"), max_length=255, directory="standortinformationen/", extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True)
    categories = TreeManyToManyField(
        "structure.Category",
        verbose_name=_("Categories"),
        related_name="creative_industry_document_plugins",
        blank=True,
    )

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def __unicode__(self):
        return self.title
