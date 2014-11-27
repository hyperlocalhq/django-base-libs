# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # needed for south to work
from base_libs.models.fields import PositionField
from base_libs.utils.misc import get_translation

from filebrowser.fields import FileBrowseField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('trashed', _("Trashed")),
)

COPYRIGHT_RESTRICTION_CHOICES = (
    ('general_use', _("Released for general use")),
    ('protected', _("Released for this and own site only"))
)


class LanguageAndSubtitles(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class ProductionCategory(MPTTModel, CreationModificationDateMixin, SlugMixin()):
    parent = TreeForeignKey('self', blank=True, null=True)
    title = MultilingualCharField(_('Title'), max_length=200)

    objects = TreeManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        if not self.pk:
            ProductionCategory.objects.insert_node(self, self.parent)
        super(ProductionCategory, self).save(*args, **kwargs)


class ProductionManager(models.Manager):
    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if user.has_perm("productions.change_production"):
            return self.get_query_set().exclude(status="trashed")
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="productions",
            content_type__model="production",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")


class Production(CreationModificationMixin, UrlMixin, SlugMixin()):
    prefix = MultilingualCharField(_("Title prefix"), max_length=255)
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    original = MultilingualCharField(_("Original title"), max_length=255)
    website = URLField("Production URL", blank=True)

    in_program_of = models.ManyToManyField("locations.Location", verbose_name=_("In program of"), blank=True)
    ensembles = models.ManyToManyField("locations.Location", verbose_name=_("Ensembles"), blank=True)
    play_locations = models.ManyToManyField("locations.Location", verbose_name=_("Play locations"), blank=True)
    play_stages = models.ManyToManyField("locations.Stage", verbose_name=_("Play stages"), blank=True)
    organizers = models.ManyToManyField("locations.Location", verbose_name=_("Organizers"), blank=True)
    in_cooperation_with = models.ManyToManyField("locations.Location", verbose_name=_("In cooperation with"), blank=True)

    categories = TreeManyToManyField(ProductionCategory, verbose_name=_("Categories"), blank=True)

    description = MultilingualTextField(_("Description"), blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    work_info = MultilingualTextField(_("Work info"), blank=True)
    contents = MultilingualTextField(_("Contents"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)

    festivals = models.ManyToManyField("festivals.Festival", verbose_name=_("Festivals"), blank=True)
    language_and_subtitles = models.ForeignKey(LanguageAndSubtitles, verbose_name=_("Language / Subtitles"), blank=True, null=True)

    free_entrance = models.BooleanField(_("Free entrance"))
    price_from = models.DecimalField(_(u"Price from (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    price_till = models.DecimalField(_(u"Price till (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    tickets_website = URLField("Tickets website", blank=True)
    price_information = MultilingualTextField(_("Additional price information"), blank=True)


    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    objects = ProductionManager()

    row_level_permissions = True

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Production")
        verbose_name_plural = _("Productions")

    def get_url_path(self):
        try:
            path = reverse("production_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Production),
            )
        except:
            role = PerObjectGroup(
                sysname="owners",
            )
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(role, "title_%s" % lang_code, get_translation("Owners", language=lang_code))
            role.content_object = self
            role.save()

            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self,
                owner=role,
            )

        if not role.users.filter(pk=user.pk).count():
            role.users.add(user)

    def remove_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Production),
                )
        except:
            return
        role.users.remove(user)
        if not role.users.count():
            role.delete()

    def get_owners(self):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Production),
            )
        except:
            return []
        return role.users.all()


class ProductionVideo(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="location")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk


class ProductionImage(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    path = FileBrowseField(_('File path'), max_length=255, directory="productions/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="location")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk


class ProductionPDF(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    path = FileBrowseField(_('File path'), max_length=255, directory="productions/", extensions=['.pdf'], help_text=_("A path to a locally stored PDF file."))
    sort_order = PositionField(_("Sort order"), collection="location")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("PDF")
        verbose_name_plural = _("PDFs")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk


class ProductionLeadership(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Leadership")
        verbose_name_plural = _("Leaderships")

    def __unicode__(self):
        return unicode(self.person)


class ProductionAuthorship(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    authorship_type = models.ForeignKey('people.AuthorshipType', verbose_name=_('Type'))

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Authorship")
        verbose_name_plural = _("Authorships")

    def __unicode__(self):
        return unicode(self.person)


class ProductionInvolvement(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    involvement_type = models.ForeignKey('people.InvolvementType', verbose_name=_('Type'))
    involvement_role = MultilingualCharField(_('Role'), max_length=255, blank=True)
    involvement_instrument = MultilingualCharField(_('Instrument'), max_length=255, blank=True)

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Involvement")
        verbose_name_plural = _("Involvements")

    def __unicode__(self):
        return unicode(self.person)


class Event(CreationModificationMixin, UrlMixin):
    production = models.ForeignKey(Production, verbose_name=_("Prodution"))
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"), blank=True, null=True)
    start_time = models.TimeField(_("Start time"))
    duration = models.TimeField(_("Duration"))
    pauses = models.PositiveIntegerField(_("Pauses"), default=0)

    class Meta:
        ordering = ["start_date", "start_time"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __unicode__(self):
        return unicode(self.production) + ' ' + self.start_date.strftime('%Y-%m-%d')


class EventVideo(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="location")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk


class EventImage(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    path = FileBrowseField(_('File path'), max_length=255, directory="events/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="location")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk


class EventPDF(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    path = FileBrowseField(_('File path'), max_length=255, directory="events/", extensions=['.pdf'], help_text=_("A path to a locally stored PDF file."))
    sort_order = PositionField(_("Sort order"), collection="location")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("PDF")
        verbose_name_plural = _("PDFs")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk


class EventLeadership(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Leadership")
        verbose_name_plural = _("Leaderships")

    def __unicode__(self):
        return unicode(self.person)


class EventAuthorship(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    authorship_type = models.ForeignKey('people.AuthorshipType', verbose_name=_('Type'))

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Authorship")
        verbose_name_plural = _("Authorships")

    def __unicode__(self):
        return unicode(self.person)


class EventInvolvement(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    involvement_type = models.ForeignKey('people.InvolvementType', verbose_name=_('Type'))
    involvement_role = MultilingualCharField(_('Role'), max_length=255, blank=True)
    involvement_instrument = MultilingualCharField(_('Instrument'), max_length=255, blank=True)

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Involvement")
        verbose_name_plural = _("Involvements")

    def __unicode__(self):
        return unicode(self.person)


