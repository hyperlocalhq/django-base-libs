# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.media_gallery.base import *
from jetson.apps.media_gallery.base import MediaGalleryManager as MediaGalleryManagerBase
from base_libs.models import PublishingMixin

### CCB MEDIA GALLERY ###

LANDING_PAGE_CHOICES = (
    ("first_album", _("First album")),
    ("album_list", _("List of albums")),
    ("custom_image", _("Custom image")),
)

class PortfolioSettingsManager(models.Manager):
    def get_for_object(self, obj):
        try:  # get existing settings for the object
            p_settings = self.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk,
            )
        except Exception:  # or take unsaved default
            p_settings = PortfolioSettings()
            p_settings.content_object = obj
        return p_settings


class PortfolioSettings(ObjectRelationMixin(is_required=True, limit_content_type_choices_to={
    'model__in': ['person', 'institution', 'event']}), CreationModificationDateMixin):
    content_object_repr = MultilingualCharField(_("Content object representation"), max_length=100, blank=True,
                                                default="",
                                                help_text=_("Used for search and ordering in administration."),
                                                editable=False)
    content_object_id = models.CharField(_("Content object ID combo"), max_length=100, blank=True, default="",
                                         help_text=_("Used for grouping the sortable galleries."), editable=False)

    landing_page = models.CharField(_("Landing page"), choices=LANDING_PAGE_CHOICES, default="first_album",
                                    max_length=20)
    landing_page_image = FileBrowseField(_('Landing page image'), max_length=255, blank=True,
                                         help_text=_("A path to a custom landing page image."))

    objects = PortfolioSettingsManager()

    class Meta:
        verbose_name = _("Portfolio Settings")
        verbose_name_plural = _("Portfolio Settings")

    def __unicode__(self):
        value = ugettext("Broken portfolio settings")
        if self.content_object:
            value = ugettext("Portfolio settings for %(content_type)s %(object)s") % {
                'content_type': force_unicode(self.content_type).lower(),
                'object': self.content_object,
            }
        return value

    def save(self, **kwargs):
        if self.content_object:
            self.content_object_id = "%s|%s" % (self.content_type.pk, self.object_id)
            current_lang = get_current_language()
            for lang_code, lang_name in settings.LANGUAGES:
                activate_language(lang_code)
                setattr(
                    self,
                    "content_object_repr_%s" % lang_code,
                    unicode(self.content_object)[:100]
                )
            activate_language(current_lang)
        else:
            self.content_object_id = ""
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(self, "content_object_repr_%s" % lang_code, "")

        super(PortfolioSettings, self).save(**kwargs)

    save.alters_data = True


class Section(ObjectRelationMixin(is_required=True,
                                  limit_content_type_choices_to={'model__in': ['person', 'institution', 'event']}),
              CreationModificationDateMixin):
    title = MultilingualCharField(_("Title"), max_length=100, blank=True)
    content_object_repr = MultilingualCharField(_("Content object representation"), max_length=100, blank=True,
                                                default="",
                                                help_text=_("Used for search and ordering in administration."),
                                                editable=False)
    content_object_id = models.CharField(_("Content object ID combo"), max_length=100, blank=True, default="",
                                         help_text=_("Used for grouping the sortable galleries."), editable=False)
    sort_order = PositionField(_("Sort order"), collection="content_object_id")
    show_title = models.BooleanField(_("Show title"), default=False)

    class Meta:
        verbose_name = _("Portfolio Section")
        verbose_name_plural = _("Portfolio Sections")

    def __unicode__(self):
        value = ugettext("Broken gallery section")
        if self.content_object:
            value = ugettext("%(title)s @ %(content_type)s %(object)s") % {
                'title': self.title or "Unnamed gallery section",
                'content_type': force_unicode(self.content_type).lower(),
                'object': self.content_object,
            }
        return value

    def save(self, **kwargs):
        if self.content_object:
            self.content_object_id = "%s|%s" % (self.content_type.pk, self.object_id)
            current_lang = get_current_language()
            for lang_code, lang_name in settings.LANGUAGES:
                activate_language(lang_code)
                setattr(
                    self,
                    "content_object_repr_%s" % lang_code,
                    unicode(self.content_object)[:100]
                )
            activate_language(current_lang)
        else:
            self.content_object_id = ""
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(self, "content_object_repr_%s" % lang_code, "")

        super(Section, self).save(**kwargs)

    save.alters_data = True

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None


class MediaGalleryManager(MediaGalleryManagerBase):
    def newest_featured(self):
        return self.featured().order_by("-creation_date")


class MediaGallery(MediaGalleryBase, PublishingMixin):
    section = models.ForeignKey(Section, verbose_name=_("Section"), blank=True, null=True)

    objects = MediaGalleryManager()

    def __unicode__(self):
        value = ugettext("Global gallery")
        if self.content_object:
            value = ugettext("Gallery of %(object)s") % {
                'object': self.content_object,
            }
        return value

    def get_url_path(self):
        if self.content_object:
            return "%s%s/album/%s/" % (
                self.content_object.get_url_path(),
                URL_ID_PORTFOLIO,
                self.get_token(),
            )
        return ""


class MediaFile(MediaFileBase):
    pass
