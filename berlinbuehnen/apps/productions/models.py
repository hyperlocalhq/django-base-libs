# -*- coding: UTF-8 -*-

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.timezone import now as tz_now

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualURLField
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # needed for south to work
from base_libs.models.fields import PositionField
from base_libs.utils.misc import get_translation
from base_libs.middleware.threadlocals import get_current_language
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify


from filebrowser.fields import FileBrowseField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('expired', _("Expired")),
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
    ('trashed', _("Trashed")),
)

TOKENIZATION_SUMMAND = 56436  # used to hide the ids of media files

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
    parent = TreeForeignKey('self', blank=True, null=True, related_name="children")
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
    def accessible_to(self, user):
        from berlinbuehnen.apps.locations.models import Location
        if user.has_perm("productions.change_production"):
            return self.get_query_set().exclude(status="trashed")

        owned_production_ids = self.owned_by(user=user).values_list("pk", flat=True)

        owned_locations = Location.objects.owned_by(user=user)
        return self.get_query_set().filter(
            models.Q(
                models.Q(in_program_of__in=owned_locations) |
                models.Q(play_locations__in=owned_locations)
            ) |
            models.Q(pk__in=owned_production_ids)
        ).exclude(status="trashed").distinct()

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="productions",
            content_type__model="production",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")

    def for_newsletter(self):
        return self.filter(
            status="published",
            newsletter=True
        ).order_by('start_date', 'start_time')


class Production(CreationModificationMixin, UrlMixin, SlugMixin()):
    prefix = MultilingualCharField(_("Title prefix"), max_length=255, blank=True)
    title = MultilingualCharField(_("Title"), max_length=255, db_index=True)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    original = MultilingualCharField(_("Original title"), max_length=255, blank=True)
    website = MultilingualURLField(_("Production URL"), blank=True, max_length=255)

    in_program_of = models.ManyToManyField("locations.Location", verbose_name=_("In the programme of"), blank=True, related_name="program_productions")
    play_locations = models.ManyToManyField("locations.Location", verbose_name=_("Theaters"), blank=True, related_name="located_productions")
    play_stages = models.ManyToManyField("locations.Stage", verbose_name=_("Stages"), blank=True)

    ensembles = models.CharField(_("Ensembles"), blank=True, max_length=255)
    organizers = models.CharField(_("Organizers"), blank=True, max_length=255)
    in_cooperation_with = models.CharField(_("In cooperation with"), blank=True, max_length=255)

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
    concert_program = MultilingualTextField(_("Concert program"), blank=True)
    supporting_program = MultilingualTextField(_("Supporting program"), blank=True)
    remarks = MultilingualTextField(_("Remarks"), blank=True)
    duration_text = MultilingualCharField(_("Duration text"), max_length=255, blank=True)
    subtitles_text = MultilingualCharField(_("Subtitles text"), max_length=255, blank=True)
    age_text = MultilingualCharField(_("Age text"), max_length=255, blank=True)

    festivals = models.ManyToManyField("festivals.Festival", verbose_name=_("Festivals"), blank=True)
    language_and_subtitles = models.ForeignKey(LanguageAndSubtitles, verbose_name=_("Language / Subtitles"), blank=True, null=True)
    related_productions = models.ManyToManyField("self", verbose_name=_("Related productions"), blank=True)

    free_entrance = models.BooleanField(_("Free entrance"))
    price_from = models.DecimalField(_(u"Price from (€). Seperate cents by a point."), max_digits=5, decimal_places=2, blank=True, null=True)
    price_till = models.DecimalField(_(u"Price till (€). Seperate cents by a point."), max_digits=5, decimal_places=2, blank=True, null=True)
    tickets_website = URLField(_("Tickets website"), blank=True, max_length=255)
    price_information = MultilingualTextField(_("Additional price information"), blank=True)

    characteristics = models.ManyToManyField(ProductionCharacteristics, verbose_name=_("Characteristics"), blank=True)
    other_characteristics = MultilingualTextField(_("Other characteristics"), blank=True)
    age_from = models.PositiveSmallIntegerField(_(u"Age from"), blank=True, null=True)
    age_till = models.PositiveSmallIntegerField(_(u"Age till"), blank=True, null=True)
    edu_offer_website = URLField(_("Educational offer website"), blank=True, max_length=255)

    sponsors = models.ManyToManyField("sponsors.Sponsor", verbose_name=_("Sponsors"), blank=True)

    show_among_others = models.BooleanField(_("Show among others"), default=True, help_text=_("Should this production be shown in event details among other productions at the same venue?"))
    no_overwriting = models.BooleanField(_("Do not overwrite by the next import"))
    classiccard = models.BooleanField(_("Intended for ClassicCard holders"), default=False)
    newsletter = models.BooleanField(_("Show in newsletter"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    start_date = models.DateField(_("Actual start date"), blank=True, null=True, editable=False)
    start_time = models.TimeField(_("Actual start time"), blank=True, null=True, editable=False)

    import_source = models.ForeignKey('external_services.Service', editable=False, blank=True, null=True)

    objects = ProductionManager()

    row_level_permissions = True

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _("Production")
        verbose_name_plural = _("Productions")

    def get_url_path(self):
        events = self.event_set.exclude(event_status="trashed")
        if events:
            return events[0].get_url_path()
        return reverse('production_detail', kwargs={'slug': self.slug})

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
    set_owner.alters_data = True

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
    remove_owner.alters_data = True

    def get_owners(self):
        if not hasattr(self, "_owners"):
            ContentType = models.get_model("contenttypes", "ContentType")
            PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
            try:
                role = PerObjectGroup.objects.get(
                    sysname__startswith="owners",
                    object_id=self.pk,
                    content_type=ContentType.objects.get_for_model(Production),
                )
            except:
                self._owners = []
            else:
                self._owners = role.users.all()
        return self._owners

    def update_actual_date_and_time(self):
        event = self.get_nearest_occurrence()
        make_expired = False
        if event:
            Production.objects.filter(pk=self.pk).update(
                start_date=event.start_date,
                start_time=event.start_time,
            )
            now = tz_now()
            if self.status != "expired" and ((event.end_date is None and event.start_date < now.date()) or (event.end_date is not None and event.end_date < now.date())):
                make_expired = True
        elif self.status == "published":
            make_expired = True
        if make_expired:
            Production.objects.filter(pk=self.pk).update(
                status="expired",
            )
    update_actual_date_and_time.alters_data = True

    def get_nearest_occurrence(self, timestamp=tz_now):
        """ returns current or closest future or closest past event time """
        if callable(timestamp):
            timestamp = timestamp()

        event_times = self.event_set.exclude(event_status="trashed").filter(
            models.Q(end_date__gte=timestamp.date()) | models.Q(end_date=None, start_date__gte=timestamp.date()),
        )

        if not event_times:
            event_times = self.event_set.exclude(event_status="trashed").order_by("-end_date")

        if event_times:
            return event_times[0]

        return None

    def get_upcoming_occurrences(self, timestamp=tz_now):
        """ returns current or closest future or closest past event time """
        if callable(timestamp):
            timestamp = timestamp()

        event_times = self.event_set.exclude(event_status="trashed").filter(
            models.Q(end_date__gte=timestamp.date()) | models.Q(end_date=None, start_date__gte=timestamp.date()),
        )

        return event_times

    def get_past_occurrences(self, timestamp=tz_now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.event_set.exclude(event_status="trashed").filter(end_date__lt=timestamp.date())

    def get_future_occurrences(self, timestamp=tz_now):
        if callable(timestamp):
            timestamp = timestamp()

        now_date = timestamp.date()
        now_time = timestamp.time()
        events = list(self.event_set.exclude(event_status="trashed").filter(start_date__gte=now_date).order_by('start_date'))

        while len(events) and events[0].start_date == now_date and events[0].start_time < now_time:
            del events[0]

        return events

    def fix_categories(self):
        # for all children categories of this production add the parent category to the database
        for child_cat in self.categories.filter(level=1):
            self.categories.add(child_cat.parent)
    fix_categories.alters_data = True

    def get_categories(self):
        # get the categories of this production and of its parts if this production is a multipart
        categories = ProductionCategory.objects.filter(
            production__pk__in=[self.pk] + [part.production_id for part in self.get_parts()]
        )
        return categories

    def get_import_source(self):
        if not hasattr(self, "_import_source"):
            ObjectMapper = models.get_model("external_services", "ObjectMapper")
            ContentType = models.get_model("contenttypes", "ContentType")
            mappers = ObjectMapper.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                object_id=self.pk,
            )
            self._import_source = ""
            if mappers:
                self._import_source = mappers[0].service.title.replace(' Productions', '')
        return self._import_source
    get_import_source.short_description = _("Import Source")

    def _get_first_image(self):
        if not hasattr(self, '_first_image_cache'):
            self._first_image_cache = None
            qs = self.productionimage_set.all()
            if qs.count():
                self._first_image_cache = qs[0]
        return self._first_image_cache
    first_image = property(_get_first_image)

    def is_multipart(self):
        try:
            return bool(self.multipart)
        except:
            return False

    def get_parts(self):
        try:
            return self.multipart.part_set.all()
        except:
            return []

    def has_parts_leaderships(self):
        multiparts = self.get_parts()
        if multiparts:
            for part in multiparts:
                if part.production.get_leaderships().exists():
                    return True
        return False

    def get_leaderships(self):
        return self.productionleadership_set.all().order_by('sort_order')

    def has_parts_involvements(self):
        multiparts = self.get_parts()
        if multiparts:
            for part in multiparts:
                if part.production.get_involvements().exists():
                    return True
        return False

    def get_involvements(self):
        return self.productioninvolvement_set.all().order_by('sort_order')

    def has_parts_authorships(self):
        multiparts = self.get_parts()
        if multiparts:
            for part in multiparts:
                if part.production.get_authorships().exists():
                    return True
        return False

    def get_authorships(self):
        return self.productionauthorship_set.all().order_by('sort_order')

    def has_parts_videos(self):
        multiparts = self.get_parts()
        if multiparts:
            for part in multiparts:
                if part.production.get_videos().exists():
                    return True
        return False

    def get_videos(self):
        return self.productionvideo_set.all()

    def has_parts_images(self):
        multiparts = self.get_parts()
        if multiparts:
            for part in multiparts:
                if part.production.get_images().exists():
                    return True
        return False

    def get_images(self):
        return self.productionimage_set.all()

    def duplicate(self, new_values={}):
        import os
        from distutils.dir_util import copy_tree
        from filebrowser.models import FileDescription
        # copy the model
        source_prod = self
        target_prod = Production.objects.get(pk=self.pk)
        target_prod.pk = None

        for key, value in new_values.items():
            setattr(target_prod, key, value)

        target_prod.slug = get_unique_value(Production, better_slugify(target_prod.title_de))
        target_prod.start_date = None
        target_prod.start_time = None
        target_prod.creation_date = None
        target_prod.modified_date = None
        target_prod.status = "draft"
        target_prod.save()
        # add m2m relationships
        target_prod.in_program_of = source_prod.in_program_of.all()
        target_prod.play_locations = source_prod.play_locations.all()
        target_prod.play_stages = source_prod.play_stages.all()
        target_prod.categories = source_prod.categories.all()
        target_prod.festivals = source_prod.festivals.all()
        target_prod.related_productions = source_prod.related_productions.all()
        target_prod.sponsors = source_prod.sponsors.all()
        # copy media directory
        source_media_dir = "productions/%s" % source_prod.slug
        target_media_dir = "productions/%s" % target_prod.slug
        abs_source_media_path = os.path.join(settings.MEDIA_ROOT, source_media_dir)
        abs_target_media_path = os.path.join(settings.MEDIA_ROOT, target_media_dir)
        if os.path.exists(abs_source_media_path):
            copy_tree(abs_source_media_path, abs_target_media_path)
        for file_desc in FileDescription.objects.filter(file_path__startswith=source_media_dir):
            file_desc.pk = None
            file_desc.file_path = file_desc.file_path.path.replace(source_media_dir, target_media_dir)
            file_desc.save()
        # add m2o relationships
        for social_media in source_prod.productionsocialmediachannel_set.all():
            social_media.pk = None
            social_media.production = target_prod
            social_media.save()
        for video in source_prod.productionvideo_set.all():
            video.pk = None
            video.production = target_prod
            video.save()
        for livestream in source_prod.productionlivestream_set.all():
            livestream.pk = None
            livestream.production = target_prod
            livestream.save()
        for image in source_prod.productionimage_set.all():
            image.pk = None
            image.path = image.path.path.replace(source_media_dir, target_media_dir)
            image.production = target_prod
            image.save()
        for pdf in source_prod.productionpdf_set.all():
            pdf.pk = None
            pdf.path = pdf.path.path.replace(source_media_dir, target_media_dir)
            pdf.production = target_prod
            pdf.save()
        for member in source_prod.productionleadership_set.all():
            member.pk = None
            member.production = target_prod
            member.save()
        for member in source_prod.productionauthorship_set.all():
            member.pk = None
            member.production = target_prod
            member.save()
        for member in source_prod.productioninvolvement_set.all():
            member.pk = None
            member.production = target_prod
            member.save()
        # set ownership
        for owner in source_prod.get_owners():
            target_prod.set_owner(owner)
        return target_prod
    duplicate.alters_data = True

    def is_editable(self, user=None):
        from django.contrib.auth.models import AnonymousUser
        from base_libs.middleware.threadlocals import get_current_user
        if not hasattr(self, "_is_editable_cache"):
            # return True when user has permissions to edit this production or the first editable location is found
            user = get_current_user(user) or AnonymousUser()
            self._is_editable_cache = user.has_perm("productions.change_production", self) or any((
                location.is_editable()
                for locations in (self.in_program_of.all(), self.play_locations.all())
                for location in locations
            ))
        return self._is_editable_cache

    def is_deletable(self, user=None):
        return self.is_editable(user=user)

    def get_next_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return Production.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
                **{
                    '{}__gt'.format(field_name): getattr(self, field_name)
                }
            ).order_by(field_name)[0]
        except:
            return None

    def get_previous_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return Production.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
                **{
                    '{}__lt'.format(field_name): getattr(self, field_name)
                }
            ).order_by('-{}'.format(field_name))[0]
        except:
            return None


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

    def get_class(self):
        social = self.channel_type.lower()
        if social == "google+":
            return u"googleplus"
        return social


class ProductionVideo(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    title = MultilingualCharField(_("Title"), max_length=255)
    link_or_embed = models.TextField(verbose_name=_("Link or embed code"))
    sort_order = PositionField(_("Sort order"), collection="production")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Video/Audio")
        verbose_name_plural = _("Videos/Audios")

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
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)
    #sort_order = PositionField(_("Sort order"), collection="production", default=0)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    imported_sort_order = models.IntegerField(_("Imported sort order"), default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Leadership")
        verbose_name_plural = _("Leaderships")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        lang_code = get_current_language()
        return getattr(self, 'function_%s' % lang_code, '')


class ProductionAuthorship(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    authorship_type = models.ForeignKey('people.AuthorshipType', verbose_name=_('Type'))
    work_title = models.CharField(_("Work title"), max_length=255, blank=True)
    #sort_order = PositionField(_("Sort order"), collection="production", default=0)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    imported_sort_order = models.IntegerField(_("Imported sort order"), default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Authorship")
        verbose_name_plural = _("Authorships")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        lang_code = get_current_language()
        return getattr(self.authorship_type, 'title_%s' % lang_code, '')


class ProductionInvolvement(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    involvement_type = models.ForeignKey('people.InvolvementType', verbose_name=_('Type'), blank=True, null=True)
    another_type = MultilingualCharField(_("Another type"), max_length=255, blank=True)
    involvement_role = MultilingualCharField(_('Role'), max_length=255, blank=True)
    involvement_instrument = MultilingualCharField(_('Instrument'), max_length=255, blank=True)
    #sort_order = PositionField(_("Sort order"), collection="production", default=0)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    imported_sort_order = models.IntegerField(_("Imported sort order"), default=0)

    class Meta:
        index_together = [
            ['production', 'sort_order']
        ]
        ordering = ["sort_order"]
        verbose_name = _("Involvement")
        verbose_name_plural = _("Involvements")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        lang_code = get_current_language()
        if self.involvement_type:
            return getattr(self.involvement_type, 'title_%s' % lang_code)
        return getattr(self, 'another_type_%s' % lang_code, '') or getattr(self, 'involvement_role_%s' % lang_code, '') or getattr(self, 'involvement_instrument_%s' % lang_code, '')


class EventCharacteristics(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)
    show_as_main_category= models.BooleanField(_("Show as main category"))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Event Characteristics")
        verbose_name_plural = _("Event Characteristics")


class EventManager(models.Manager):
    def published_upcoming(self, timestamp=tz_now):
        if callable(timestamp):
            timestamp = timestamp()

        qs = self.filter(
            models.Q(end_date__gte=timestamp.date()) |
            models.Q(end_date=None, start_date__gte=timestamp.date()),
            production__status="published",
        )

        today = datetime.today()
        qs = qs.exclude(
            start_date__exact=today,
            start_time__lt=today,
        ).distinct()

        return qs


class Event(CreationModificationMixin, UrlMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"))
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"), blank=True, null=True)
    start_time = models.TimeField(_("Start time"), blank=True, null=True)
    end_time = models.TimeField(_("End time"), blank=True, null=True)
    duration = models.PositiveIntegerField(_("Duration in seconds"), null=True, blank=True)
    pauses = models.PositiveIntegerField(_("Pauses"), blank=True, null=True)

    play_locations = models.ManyToManyField("locations.Location", verbose_name=_("Theaters"), blank=True)
    play_stages = models.ManyToManyField("locations.Stage", verbose_name=_("Stages"), blank=True)

    location_title = models.CharField(_("Location title"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    organizers = models.CharField(_("Organizers"), max_length=255, blank=True)

    description = MultilingualTextField(_("Description"), blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    work_info = MultilingualTextField(_("Work info"), blank=True)
    contents = MultilingualTextField(_("Contents"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)
    credits = MultilingualTextField(_("Credits"), blank=True)

    # text fields for data from the Culturbase import feed
    concert_program = MultilingualTextField(_("Concert program"), blank=True)
    supporting_program = MultilingualTextField(_("Supporting program"), blank=True)
    remarks = MultilingualTextField(_("Remarks"), blank=True)
    duration_text = MultilingualCharField(_("Duration text"), max_length=255, blank=True)
    subtitles_text = MultilingualCharField(_("Subtitles text"), max_length=255, blank=True)
    age_text = MultilingualCharField(_("Age text"), max_length=255, blank=True)

    event_status = models.CharField(_("Event status"), max_length=20, choices=EVENT_STATUS_CHOICES, blank=True)
    ticket_status = models.CharField(_("Ticket status"), max_length=20, choices=TICKET_STATUS_CHOICES, blank=True)

    language_and_subtitles = models.ForeignKey(LanguageAndSubtitles, verbose_name=_("Language / Subtitles"), blank=True, null=True)

    free_entrance = models.BooleanField(_("Free entrance"))
    price_from = models.DecimalField(_(u"Price from (€). Seperate cents by a point."), max_digits=5, decimal_places=2, blank=True, null=True)
    price_till = models.DecimalField(_(u"Price till (€). Seperate cents by a point."), max_digits=5, decimal_places=2, blank=True, null=True)
    tickets_website = URLField(_("Tickets website"), blank=True, max_length=255)
    price_information = MultilingualTextField(_("Additional price information"), blank=True)

    characteristics = models.ManyToManyField(EventCharacteristics, verbose_name=_("Characteristics"), blank=True)
    other_characteristics = MultilingualTextField(_("Other characteristics"), blank=True)

    sponsors = models.ManyToManyField("sponsors.Sponsor", verbose_name=_("Sponsors"), blank=True)

    classiccard = models.BooleanField(_("Intended for ClassicCard holders"), default=False)

    objects = EventManager()

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
        if not self.duration:
            return u''
        attrs = (
            ('years', ugettext('year'), ugettext('years')),
            ('months', ugettext('month'), ugettext('months')),
            ('days', ugettext('day'), ugettext('days')),
            ('hours', ugettext('hour'), ugettext('hours')),
            ('minutes', ugettext('minute'), ugettext('minutes')),
            ('seconds', ugettext('second'), ugettext('seconds')),
        )
        human_readable = lambda delta: [
            '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and plural or singular)
            for attr, singular, plural in attrs if getattr(delta, attr)
        ]
        return u' '.join(human_readable(relativedelta(seconds=self.duration)))

    ### venues ###

    def ev_or_prod_play_locations(self):
        if self.pk and self.play_locations.exists():
            return self.play_locations.all()
        return self.production.play_locations.all()

    def ev_or_prod_play_stages(self):
        if self.pk and self.play_stages.exists():
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

    def ev_or_prod_concert_program(self):
        return self.get_rendered_concert_program() or self.production.get_rendered_concert_program()

    def ev_or_prod_supporting_program(self):
        return self.get_rendered_supporting_program() or self.production.get_rendered_supporting_program()

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
        if not hasattr(self, "_ev_or_prod_sponsors_cache"):
            if self.pk and self.eventsponsor_set.exists():
                sponsors = self.eventsponsor_set.all()
            else:
                sponsors = self.production.productionsponsor_set.all()

            final = []
            for sponsor in sponsors:
                if sponsor.image or sponsor.title:
                    final.append(sponsor)

            self._ev_or_prod_sponsors_cache = final

        return self._ev_or_prod_sponsors_cache

    ### media ###

    def ev_or_prod_videos(self):
        if self.pk and self.eventvideo_set.exists():
            return self.eventvideo_set.all()
        return self.production.productionvideo_set.all()

    def ev_or_prod_images(self):
        if self.pk and self.eventimage_set.exists():
            return self.eventimage_set.all()
        return self.production.productionimage_set.all()

    def ev_or_prod_pdfs(self):
        if self.pk and self.eventpdf_set.exists():
            return self.eventpdf_set.all()
        return self.production.productionpdf_set.all()

    def ev_or_prod_social_media(self):
        if self.pk and self.eventsocialmediachannel_set.exists():
            return self.eventsocialmediachannel_set.all()
        return self.production.productionsocialmediachannel_set.all()

    ### people ###

    def ev_or_prod_leaderships(self):
        lang_code = get_current_language()
        if self.pk and self.eventleadership_set.exists():
            # return self.eventleadership_set.all().order_by('function_%s' % lang_code, 'sort_order')
            return self.eventleadership_set.all().order_by('sort_order')
        #return self.production.productionleadership_set.all().order_by('function_%s' % lang_code, 'sort_order')
        return self.production.productionleadership_set.all().order_by('sort_order')

    def ev_or_prod_authorships(self):
        lang_code = get_current_language()
        if self.pk and self.eventauthorship_set.exists():
            # return self.eventauthorship_set.all().order_by('authorship_type__title_%s' % lang_code, 'sort_order')
            return self.eventauthorship_set.all().order_by('sort_order')
        # return self.production.productionauthorship_set.all().order_by('authorship_type__title_%s' % lang_code, 'sort_order')
        return self.production.productionauthorship_set.all().order_by('sort_order')

    def ev_or_prod_involvements(self):
        lang_code = get_current_language()
        if self.pk and self.eventinvolvement_set.exists():
            # return self.eventinvolvement_set.all().order_by('involvement_type__title_%s' % lang_code, 'involvement_role_%s' % lang_code, 'involvement_instrument_%s' % lang_code, 'sort_order')
            return self.eventinvolvement_set.all().order_by('sort_order')
        # return self.production.productioninvolvement_set.all().order_by('involvement_type__title_%s' % lang_code, 'involvement_role_%s' % lang_code, 'involvement_instrument_%s' % lang_code, 'sort_order')
        return self.production.productioninvolvement_set.all().order_by('sort_order')

    def ev_or_prod_language_and_subtitles(self):
        return self.language_and_subtitles or self.production.language_and_subtitles

    def _get_first_image(self):
        if not hasattr(self, '_first_image_cache'):
            self._first_image_cache = None
            qs = self.ev_or_prod_images()
            if qs.count():
                self._first_image_cache = qs[0]
        return self._first_image_cache
    first_image = property(_get_first_image)

    ### special text ###

    def get_special_text(self):
        if not self.pk:
            return u""
        ch = self.characteristics.filter(slug="premiere")
        if ch:
            return ch[0].title
        return u""

    def is_canceled(self):
        return self.event_status == 'canceled'

    def get_festivals(self):
        return self.production.festivals.filter(status="published")

    def get_previous_item(self):
        return self.production.get_previous_item()

    def get_next_item(self):
        return self.production.get_next_item()


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

    def get_class(self):
        social = self.channel_type.lower()
        if social == "google+":
            return u"googleplus"
        return social


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
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    function = MultilingualCharField(_('Function'), max_length=255, blank=True)
    #sort_order = PositionField(_("Sort order"), collection="event", default=0)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    imported_sort_order = models.IntegerField(_("Imported sort order"), default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Leadership")
        verbose_name_plural = _("Leaderships")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        lang_code = get_current_language()
        return getattr(self, 'function_%s' % lang_code, '')


class EventAuthorship(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    authorship_type = models.ForeignKey('people.AuthorshipType', verbose_name=_('Type'))
    work_title = models.CharField(_("Work title"), max_length=255, blank=True)
    #sort_order = PositionField(_("Sort order"), collection="event", default=0)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    imported_sort_order = models.IntegerField(_("Imported sort order"), default=0)

    class Meta:
        ordering = ["person__last_name", "person__first_name"]
        verbose_name = _("Authorship")
        verbose_name_plural = _("Authorships")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        lang_code = get_current_language()
        return getattr(self.authorship_type, 'title_%s' % lang_code, '')


class EventInvolvement(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    person = models.ForeignKey('people.Person', verbose_name=_("Person"), blank=True, null=True)
    involvement_type = models.ForeignKey('people.InvolvementType', verbose_name=_('Type'), blank=True, null=True)
    another_type = MultilingualCharField(_("Another type"), max_length=255, blank=True)
    involvement_role = MultilingualCharField(_('Role'), max_length=255, blank=True)
    involvement_instrument = MultilingualCharField(_('Instrument'), max_length=255, blank=True)
    #sort_order = PositionField(_("Sort order"), collection="event", default=0)
    sort_order = models.IntegerField(_("Sort order"), default=0)
    imported_sort_order = models.IntegerField(_("Imported sort order"), default=0)

    class Meta:
        index_together = [
            ['event', 'sort_order']
        ]
        ordering = ["sort_order"]
        verbose_name = _("Involvement")
        verbose_name_plural = _("Involvements")

    def __unicode__(self):
        return unicode(self.person)

    def get_function(self):
        lang_code = get_current_language()
        if self.involvement_type:
            return getattr(self.involvement_type, 'title_%s' % lang_code)
        return getattr(self, 'another_type_%s' % lang_code, '') or getattr(self, 'involvement_role_%s' % lang_code, '') or getattr(self, 'involvement_instrument_%s' % lang_code, '')


class ProductionSponsor(CreationModificationDateMixin):
    production = models.ForeignKey(Production, verbose_name=_("Production"), on_delete=models.CASCADE)
    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    image = FileBrowseField(_("Image"), max_length=255, directory="productions/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."), blank=True)
    website = URLField(_("Website"), blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __unicode__(self):
        return self.title or (self.image and self.image.filename) or self.pk


class EventSponsor(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.CASCADE)
    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    image = FileBrowseField(_("Image"), max_length=255, directory="events/", extensions=['.jpg', '.jpeg', '.gif', '.png'], help_text=_("A path to a locally stored image."), blank=True)
    website = URLField(_("Website"), blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")

    def __unicode__(self):
        return self.title or (self.image and self.image.filename) or self.pk
