# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
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
    ('protected', _("Released for this and own site only")),
    ('promotional', _("Released for promotional reasons")),
)

TICKET_STATUS_CHOICES = (
    ('tickets_@_box_office', _("Tickets at the box office")),
    ('sold_out', _("Sold out")),
)

EVENT_STATUS_CHOICES = (
    ('takes_place', _("Takes place")),
    ('canceled', _("Canceled")),
)

TOKENIZATION_SUMMAND = 56436 # used to hide the ids of media files

class LanguageAndSubtitles(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Language and Subtitles")
        verbose_name_plural = _("Languages and Subtitles")


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


class ProductionCharacteristics(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Production Characteristics")
        verbose_name_plural = _("Production Characteristics")


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
    prefix = MultilingualCharField(_("Title prefix"), max_length=255, blank=True)
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    original = MultilingualCharField(_("Original title"), max_length=255, blank=True)
    website = URLField(_("Production URL"), blank=True, max_length=255)

    in_program_of = models.ManyToManyField("locations.Location", verbose_name=_("In program of"), blank=True, related_name="program_productions")
    ensembles = models.ManyToManyField("locations.Location", verbose_name=_("Ensembles"), blank=True, related_name="ensembled_productions")
    play_locations = models.ManyToManyField("locations.Location", verbose_name=_("Play locations"), blank=True, related_name="located_productions")
    play_stages = models.ManyToManyField("locations.Stage", verbose_name=_("Play stages"), blank=True)
    organizers = models.ManyToManyField("locations.Location", verbose_name=_("Organizers"), blank=True, related_name="organized_productions")
    in_cooperation_with = models.ManyToManyField("locations.Location", verbose_name=_("In cooperation with"), blank=True, related_name="cooperated_productions")

    organizer_title = models.CharField(_("Organizer title"), max_length=255, blank=True)

    location_title = models.CharField(_("Location title"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    categories = TreeManyToManyField(ProductionCategory, verbose_name=_("Categories"), blank=True)

    description = MultilingualTextField(_("Description"), blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    work_info = MultilingualTextField(_("Work info"), blank=True)
    contents = MultilingualTextField(_("Contents"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)
    credits = MultilingualTextField(_("Credits"), blank=True)

    # text fields for data from the Culturbase import feed
    concert_programm = MultilingualTextField(_("Concert programm"), blank=True)
    supporting_programm = MultilingualTextField(_("Supporting programm"), blank=True)
    remarks = MultilingualTextField(_("Remarks"), blank=True)
    duration_text = MultilingualCharField(_("Duration text"), max_length=255, blank=True)
    subtitles_text = MultilingualCharField(_("Subtitles text"), max_length=255, blank=True)
    age_text = MultilingualCharField(_("Age text"), max_length=255, blank=True)

    festivals = models.ManyToManyField("festivals.Festival", verbose_name=_("Festivals"), blank=True)
    language_and_subtitles = models.ForeignKey(LanguageAndSubtitles, verbose_name=_("Language / Subtitles"), blank=True, null=True)
    related_productions = models.ManyToManyField("self", verbose_name=_("Related productions"), blank=True)

    free_entrance = models.BooleanField(_("Free entrance"))
    price_from = models.DecimalField(_(u"Price from (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    price_till = models.DecimalField(_(u"Price till (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    tickets_website = URLField(_("Tickets website"), blank=True, max_length=255)
    price_information = MultilingualTextField(_("Additional price information"), blank=True)

    characteristics = models.ManyToManyField(ProductionCharacteristics, verbose_name=_("Characteristics"), blank=True)
    age_from = models.PositiveSmallIntegerField(_(u"Age from"), blank=True, null=True)
    age_till = models.PositiveSmallIntegerField(_(u"Age till"), blank=True, null=True)
    edu_offer_website = URLField(_("Educational offer website"), blank=True, max_length=255)

    sponsors = models.ManyToManyField("sponsors.Sponsor", verbose_name=_("Sponsors"), blank=True)

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
        return self.event_set.all()[0].get_url_path()

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


class ProductionSocialMediaChannel(models.Model):
    production = models.ForeignKey(Production)
    channel_type = models.CharField(_("Social media type"), max_length=255, help_text=_("e.g. twitter, facebook, etc."))
    url = URLField(_("URL"), max_length=255)

    class Meta:
        ordering = ['channel_type']
        verbose_name = _("Social media channel")
        verbose_name_plural = _("Social media channels")

    def __unicode__(self):
        return self.channel_type


class ProductionVideo(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    title = MultilingualCharField(_("Title"), max_length=255)
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="production")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __unicode__(self):
        return self.title

    def get_embed(self):
        # TODO: return embed code
        return self.link_or_embed

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProductionLiveStream(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    title = MultilingualCharField(_("Title"), max_length=255)
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="production")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Live Stream")
        verbose_name_plural = _("Live Streams")

    def __unicode__(self):
        return self.title

    def get_embed(self):
        # TODO: return embed code
        return self.link_or_embed

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProductionImage(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    path = FileBrowseField(_('File path'), max_length=255, directory="productions/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="production")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProductionPDF(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    path = FileBrowseField(_('File path'), max_length=255, directory="productions/", extensions=['.pdf'], help_text=_("A path to a locally stored PDF file."))
    sort_order = PositionField(_("Sort order"), collection="production")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("PDF")
        verbose_name_plural = _("PDFs")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class ProductionLeadership(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)
    sort_order = PositionField(_("Sort order"), collection="production", default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Leadership")
        verbose_name_plural = _("Leaderships")

    def __unicode__(self):
        return unicode(self.person)


class ProductionAuthorship(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    authorship_type = models.ForeignKey('people.AuthorshipType', verbose_name=_('Type'))
    sort_order = PositionField(_("Sort order"), collection="production", default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Authorship")
        verbose_name_plural = _("Authorships")

    def __unicode__(self):
        return unicode(self.person)


class ProductionInvolvement(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    involvement_type = models.ForeignKey('people.InvolvementType', verbose_name=_('Type'), blank=True, null=True)
    involvement_role = MultilingualCharField(_('Role'), max_length=255, blank=True)
    involvement_instrument = MultilingualCharField(_('Instrument'), max_length=255, blank=True)
    sort_order = PositionField(_("Sort order"), collection="production", default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = _("Involvement")
        verbose_name_plural = _("Involvements")

    def __unicode__(self):
        return unicode(self.person)


class EventCharacteristics(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Event Characteristics")
        verbose_name_plural = _("Event Characteristics")


class Event(CreationModificationMixin, UrlMixin):
    production = models.ForeignKey(Production, verbose_name=_("Prodution"))
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"), blank=True, null=True)
    start_time = models.TimeField(_("Start time"), blank=True, null=True)
    end_time = models.TimeField(_("End time"), blank=True, null=True)
    duration = models.PositiveIntegerField(_("Duration in seconds"), null=True, blank=True)
    pauses = models.PositiveIntegerField(_("Pauses"), default=0)

    play_locations = models.ManyToManyField("locations.Location", verbose_name=_("Play locations"), blank=True)
    play_stages = models.ManyToManyField("locations.Stage", verbose_name=_("Play stages"), blank=True)

    location_title = models.CharField(_("Location title"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    organizer_title = models.CharField(_("Organizer title"), max_length=255, blank=True)

    description = MultilingualTextField(_("Description"), blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    work_info = MultilingualTextField(_("Work info"), blank=True)
    contents = MultilingualTextField(_("Contents"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)
    credits = MultilingualTextField(_("Credits"), blank=True)

    # text fields for data from the Culturbase import feed
    concert_programm = MultilingualTextField(_("Concert programm"), blank=True)
    supporting_programm = MultilingualTextField(_("Supporting programm"), blank=True)
    remarks = MultilingualTextField(_("Remarks"), blank=True)
    duration_text = MultilingualCharField(_("Duration text"), max_length=255, blank=True)
    subtitles_text = MultilingualCharField(_("Subtitles text"), max_length=255, blank=True)
    age_text = MultilingualCharField(_("Age text"), max_length=255, blank=True)

    event_status = models.CharField(_("Event status"), max_length=20, choices=EVENT_STATUS_CHOICES, blank=True)
    ticket_status = models.CharField(_("Ticket status"), max_length=20, choices=TICKET_STATUS_CHOICES, blank=True)

    free_entrance = models.BooleanField(_("Free entrance"))
    price_from = models.DecimalField(_(u"Price from (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    price_till = models.DecimalField(_(u"Price till (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    tickets_website = URLField(_("Tickets website"), blank=True, max_length=255)
    price_information = MultilingualTextField(_("Additional price information"), blank=True)

    characteristics = models.ManyToManyField(EventCharacteristics, verbose_name=_("Characteristics"), blank=True)
    other_characteristics = MultilingualTextField(_("Other characteristics"), blank=True)

    sponsors = models.ManyToManyField("sponsors.Sponsor", verbose_name=_("Sponsors"), blank=True)

    class Meta:
        ordering = ["start_date", "start_time"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __unicode__(self):
        return unicode(self.production) + ' ' + self.start_date.strftime('%Y-%m-%d')

    def get_url_path(self):
        try:
            path = reverse("event_detail", kwargs={'slug': self.production.slug, 'event_id': self.pk})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def humanized_duration(self):
        from dateutil.relativedelta import relativedelta
        attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
        human_readable = lambda delta: ['%d %s' % (getattr(delta, attr), ugettext(getattr(delta, attr) > 1 and attr or attr[:-1]))
            for attr in attrs if getattr(delta, attr)
        ]
        return u" ".join(human_readable(relativedelta(seconds=self.duration)))

    ### venues ###

    def ev_or_prod_play_locations(self):
        if self.play_locations.exists():
            return self.play_locations.all()
        return self.production.play_locations.all()

    def ev_or_prod_play_stages(self):
        if self.play_stages.exists():
            return self.play_stages.all()
        return self.production.play_stages.all()

    ### text fields ###

    def ev_or_prod_description(self):
        return self.get_rendered_description() or self.production.get_rendered_description()

    def ev_or_prod_teaser(self):
        return self.get_rendered_teaser() or self.production.get_rendered_teaser()

    def ev_or_prod_work_info(self):
        return self.get_rendered_work_info() or self.production.get_rendered_work_info()

    def ev_or_prod_contents(self):
        return self.get_rendered_contents() or self.production.get_rendered_contents()

    def ev_or_prod_press_text(self):
        return self.get_rendered_press_text() or self.production.get_rendered_press_text()

    def ev_or_prod_credits(self):
        return self.get_rendered_credits() or self.production.get_rendered_credits()

    ### Culturebase-specific fields ###

    def ev_or_prod_concert_programm(self):
        return self.get_rendered_concert_programm() or self.production.get_rendered_concert_programm()

    def ev_or_prod_supporting_programm(self):
        return self.get_rendered_supporting_programm() or self.production.get_rendered_supporting_programm()

    def ev_or_prod_remarks(self):
        return self.get_rendered_remarks() or self.production.get_rendered_remarks()

    def ev_or_prod_duration_text(self):
        return self.duration_text or self.production.duration_text

    def ev_or_prod_subtitles_text(self):
        return self.subtitles_text or self.production.subtitles_text

    def ev_or_prod_age_text(self):
        return self.age_text or self.production.age_text

    ### prices ###

    def ev_or_prod_free_entrance(self):
        return self.free_entrance or self.production.free_entrance

    def ev_or_prod_price_from(self):
        return self.price_from or self.production.price_from

    def ev_or_prod_price_till(self):
        return self.price_till or self.production.price_till

    def ev_or_prod_tickets_website(self):
        return self.tickets_website or self.production.tickets_website

    def ev_or_prod_price_information(self):
        return self.get_rendered_price_information() or self.production.get_rendered_price_information()

    ### sponsors ###

    def ev_or_prod_sponsors(self):
        if self.sponsors.exists():
            return self.sponsors.all()
        return self.production.sponsors.all()

    ### media ###

    def ev_or_prod_videos(self):
        if self.eventvideo_set.exists():
            return self.eventvideo_set.all()
        return self.production.productionvideo_set.all()

    def ev_or_prod_images(self):
        if self.eventimage_set.exists():
            return self.eventimage_set.all()
        return self.production.productionimage_set.all()

    def ev_or_prod_pdfs(self):
        if self.eventpdf_set.exists():
            return self.eventpdf_set.all()
        return self.production.productionpdf_set.all()

    ### people ###

    def ev_or_prod_leaderships(self):
        if self.eventleadership_set.exists():
            return self.eventleadership_set.all().order_by('sort_order')
        return self.production.productionleadership_set.all().order_by('sort_order')

    def ev_or_prod_authorships(self):
        if self.eventauthorship_set.exists():
            return self.eventauthorship_set.all().order_by('sort_order')
        return self.production.productionauthorship_set.all().order_by('sort_order')

    def ev_or_prod_involvements(self):
        if self.eventinvolvement_set.exists():
            return self.eventinvolvement_set.all().order_by('sort_order')
        return self.production.productioninvolvement_set.all().order_by('sort_order')


class EventSocialMediaChannel(models.Model):
    event = models.ForeignKey(Event)
    channel_type = models.CharField(_("Social media type"), max_length=255, help_text=_("e.g. twitter, facebook, etc."))
    url = URLField(_("URL"), max_length=255)

    class Meta:
        ordering = ['channel_type']
        verbose_name = _("Social media channel")
        verbose_name_plural = _("Social media channels")

    def __unicode__(self):
        return self.channel_type


class EventVideo(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    title = MultilingualCharField(_("Title"), max_length=255)
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="event")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __unicode__(self):
        return self.title

    def get_embed(self):
        # TODO: return embed code
        return self.link_or_embed

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class EventLiveStream(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    title = MultilingualCharField(_("Title"), max_length=255)
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="event")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Live Stream")
        verbose_name_plural = _("Live Streams")

    def __unicode__(self):
        return self.title

    def get_embed(self):
        # TODO: return embed code
        return self.link_or_embed

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class EventImage(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    path = FileBrowseField(_('File path'), max_length=255, directory="events/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."))
    copyright_restrictions = models.CharField(_('Copyright restrictions'), max_length=20, blank=True, choices=COPYRIGHT_RESTRICTION_CHOICES)
    sort_order = PositionField(_("Sort order"), collection="event")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class EventPDF(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    path = FileBrowseField(_('File path'), max_length=255, directory="events/", extensions=['.pdf'], help_text=_("A path to a locally stored PDF file."))
    sort_order = PositionField(_("Sort order"), collection="event")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("PDF")
        verbose_name_plural = _("PDFs")

    def __unicode__(self):
        if self.path:
            return self.path.path
        return "Missing file (id=%s)" % self.pk

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND


class EventLeadership(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)
    sort_order = PositionField(_("Sort order"), collection="event", default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Leadership")
        verbose_name_plural = _("Leaderships")

    def __unicode__(self):
        return unicode(self.person)


class EventAuthorship(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    authorship_type = models.ForeignKey('people.AuthorshipType', verbose_name=_('Type'))
    sort_order = PositionField(_("Sort order"), collection="event", default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Authorship")
        verbose_name_plural = _("Authorships")

    def __unicode__(self):
        return unicode(self.person)


class EventInvolvement(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"))
    involvement_type = models.ForeignKey('people.InvolvementType', verbose_name=_('Type'), blank=True, null=True)
    involvement_role = MultilingualCharField(_('Role'), max_length=255, blank=True)
    involvement_instrument = MultilingualCharField(_('Instrument'), max_length=255, blank=True)
    sort_order = PositionField(_("Sort order"), collection="event", default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = _("Involvement")
        verbose_name_plural = _("Involvements")

    def __unicode__(self):
        return unicode(self.person)


