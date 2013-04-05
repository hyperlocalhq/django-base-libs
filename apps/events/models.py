# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

from base_libs.models.models import OpeningHoursMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import PositionField
from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_translation

from jetson.apps.i18n.models import Language
from jetson.apps.utils.models import MONTH_CHOICES
from filebrowser.fields import FileBrowseField

from museumsportal.apps.museums.models import Museum
from museumsportal.apps.exhibitions.models import Exhibition

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('expired', _("Expired")),
    ('trashed', _("Trashed")),
    )

COUNTRY_CHOICES = (
    ('de', _("Germany")),
    ('-', "Other"),
    )

YEAR_CHOICES = [(i,i) for i in range(1997, datetime.now().year+10)]

DAY_CHOICES = [(i,i) for i in range(1, 32)]

HOUR_CHOICES = [(i,i) for i in range(0, 24)]

MINUTE_CHOICES = [(i,"%02d" % i) for i in range(0, 60)]

TOKENIZATION_SUMMAND = 56436 # used to hide the ids of media files

class EventCategory(MPTTModel, SlugMixin()):
    parent = TreeForeignKey(
       'self',
       related_name="child_set",
       blank=True,
       null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)
    
    objects = TreeManager()
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["tree_id", "lft"]
        
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            EventCategory.objects.insert_node(self, self.parent)
        super(EventCategory, self).save(*args, **kwargs)

class EventManager(models.Manager):
    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if user.has_perm("events.change_event"):
            return self.get_query_set().exclude(status="trashed")
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="events",
            content_type__model="event",
            sysname__startswith="owners",
            users=user,
            ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")

    def update_expired(self):
        for obj in self.exclude(
            status="expired",
            ):
            obj.update_closest_event_time()
        self.filter(
            closest_event_date__isnull=True,
            ).exclude(status="expired").update(status="expired")
        
        
class Event(CreationModificationMixin, UrlMixin, SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    event_type = MultilingualCharField(_("Type"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    website = MultilingualCharField(_("Website"), max_length=255, blank=True)
    image = FileBrowseField(_('Image'), max_length=200, directory="events/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, editable=False)
    
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    categories = TreeManyToManyField(EventCategory, verbose_name=_("Categories"))
    tags = TagAutocompleteField(verbose_name=_("tags"))
    languages = models.ManyToManyField(Language, verbose_name=_("Languages"), blank=True, limit_choices_to={'display': True})
    other_languages = models.CharField(_("Other languages"), max_length=255, blank=True)
    suitable_for_children = models.BooleanField(_("Also suitable for children"), blank=True)
    
    museum = models.ForeignKey(Museum, verbose_name=_("Museum"), blank=True, null=True)
    location_name = models.CharField(_("Location name"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    district = models.CharField(_("District"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255, blank=True)    
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)
    exhibition = models.ForeignKey(Exhibition, verbose_name=_("Related exhibition"), blank=True, null=True)

    free_admission = models.BooleanField(_("Free admission"))
    meeting_place = MultilingualCharField(_("Meeting place"), max_length=255, blank=True)
    admission_price = models.DecimalField(_(u"Admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    admission_price_info = MultilingualTextField(_("Admission price info"), blank=True)
    reduced_price = models.DecimalField(_(u"Reduced admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    booking_info = MultilingualTextField(_("Booking info"), blank=True)

    closest_event_date = models.DateField(_("Event date"), editable=False, blank=True, null=True)
    closest_event_time = models.TimeField(_("Event start time"), editable=False, blank=True, null=True)

    objects = EventManager()

    row_level_permissions = True

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['title', 'creation_date']
        
    def __unicode__(self):
        return self.title

    def is_event(self):
        return True

    def get_other_events(self):
        if not self.museum:
            return []
        return self.museum.event_set.filter(status="published").exclude(pk=self.pk)

    def is_today(self):
        today = date.today()
        return self.eventtime_set.filter(event_date=today)
        
    def is_tomorrow(self):
        today = date.today()
        one_day = timedelta(days=1)
        return self.eventtime_set.filter(event_date=today + one_day).count()
        
    def is_within_days(self, days=0):
        selected_start = date.today()
        selected_end = selected_start + timedelta(days=days)
        return self.eventtime_set.filter(event_date__gte=selected_start, event_date__lte=selected_end).count()
        
    def is_within_7_days(self):
        return self.is_within_days(7)
    
    def is_within_30_days(self):
        return self.is_within_days(30)
    
    def get_closest_event_time(self):
        today = date.today()
        qs = self.eventtime_set.filter(event_date__gte=today).order_by("event_date", "start")
        if qs:
            return qs[0]
        return None

    def update_closest_event_time(self):
        event_time = self.get_closest_event_time()
        if event_time:
            Event.objects.filter(pk=self.pk).update(
                closest_event_date=event_time.event_date,
                closest_event_time=event_time.start,
                )
        else:
            Event.objects.filter(pk=self.pk).update(
                closest_event_date=None,
                closest_event_time=None,
                )

    def get_upcoming_event_times(self):
        today = date.today()
        return self.eventtime_set.filter(
            event_date__gte=today
            ).order_by("event_date", "start")

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Event),
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
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Event),
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
                content_type=ContentType.objects.get_for_model(Event),
                )
        except:
            return []
        return role.users.all()

    def get_url_path(self):
        try:
            path = u"/" + get_current_language() + reverse("%s:event_detail" % get_current_language(), kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def get_languages(self):
        langs = []
        for lang in self.languages.all():
            langs.append(lang.get_name())
        if self.other_languages:
            for lang in self.other_languages.split(","):
                langs.append(lang)
        return langs

    def _get_cover_image(self):
        qs = self.mediafile_set.all()
        if qs.count():
            return qs[0].path
    cover_image = property(_get_cover_image)

class EventTime(models.Model):
    
    event = models.ForeignKey(Event, verbose_name=_("Event"))

    event_date = models.DateField(_("Event date"))
    start = models.TimeField(_("Start time"), null=True, blank=True)
    end = models.TimeField(_("End time"), null=True, blank=True)

    class Meta:
        verbose_name = _("event time")
        verbose_name_plural = _("event times")
        ordering = ('event_date', 'start', )
        
    def __unicode__(self):
        val = self.event_date.strftime("%Y-%m-%d")
        if self.start:
            val += " " + self.start.strftime("%H:%M")
        if self.end:
            val += " - " + self.end.strftime("%H:%M")
        return val
        
    def will_happen(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return timestamp < self.start
        
    def is_happening(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.start <= timestamp <= self.end
        
    def has_happened(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.end < timestamp
        
    def is_end_date_defined(self):
        return self.end_yyyy or self.end_mm or self.end_dd
        
    def has_start_time(self):
        return self.start_hh != None
    
    def has_end_time(self):
        return self.end_hh != None
        
    def get_secure_id(self):
        return int(self.pk) + SECURITY_SUMMAND

class Organizer(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    organizing_museum = models.ForeignKey("museums.Museum", verbose_name=_("Organizing museum"), blank=True, null=True, related_name="event_organizer")
    organizer_title = models.CharField(_("Other Organizer"), max_length=255, blank=True)
    organizer_url_link = URLField(_("Organizer URL"), blank=True)
    
    def __unicode__(self):
        if self.organizing_museum:
            return self.organizing_museum.title
        return self.organizer_title
        
    class Meta:
        ordering = ("organizing_museum__title", "organizer_title")
        verbose_name = _("Organizer")
        verbose_name_plural = _("Organizers")

class MediaFile(CreationModificationDateMixin):
    event = models.ForeignKey(Event, verbose_name=_("Event"))
    path = FileBrowseField(_('File path'), max_length=255, directory="events/", help_text=_("A path to a locally stored image, video, or audio file."))
    sort_order = PositionField(_("Sort order"), collection="event")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Media File")
        verbose_name_plural = _("Media Files")
        
    def __unicode__(self):
        return self.path.path

    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    @staticmethod
    def token_to_pk(token):
        return int(token) - TOKENIZATION_SUMMAND
