# -*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from base_libs.models.models import ContentBaseMixin
from base_libs.models.models import UrlMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField  # needed for south to work

from filebrowser.fields import FileBrowseField

verbose_name = _("Flatpages")


class FlatPageBase(ContentBaseMixin, UrlMixin):
    url = models.CharField(
        _('URL'),
        max_length=100,
        help_text=_(
            "All that goes after '/', for example: 'about/contact/'. Make sure to have trailing slash."
        ),
        blank=True
    )

    image = FileBrowseField(
        _('image'),
        max_length=255,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
        blank=True
    )
    image_title = MultilingualCharField(
        _('image title'), max_length=50, blank=True
    )
    image_description = MultilingualTextField(
        _('image description'), blank=True
    )

    enable_comments = models.BooleanField(_('enable comments'), default=False)
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            "Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'."
        )
    )
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_(
            "If this is checked, only logged-in users will be able to view the page."
        ),
        default=False
    )

    class Meta:
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url', )
        abstract = True

    def __unicode__(self):
        return "%s -- %s" % (self.url, force_unicode(self.get_title()))

    def get_title(self):
        return self.title

    def get_content(self):
        return mark_safe(self.content)

    def get_absolute_url(self):
        return self.get_url_path()

    def get_url_path(self):
        return "/%s" % self.url
