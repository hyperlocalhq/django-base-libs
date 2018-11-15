# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import date as django_date
from django.utils.translation import activate

from tagging_autocomplete.models import TagAutocompleteField

from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import MultilingualPlainTextField
from base_libs.models.fields import PositionField
from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_translation

from jetson.apps.i18n.models import Language
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


class WorkshopType(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ["title_de"]
        verbose_name = _("Type")
        verbose_name_plural = _("Types")


class WorkshopManager(models.Manager):
    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if not user.is_authenticated():
            return self.get_queryset().none()
        if user.has_perm("workshop.change_workshop"):
            return self.get_queryset().exclude(status="trashed")
        ids = map(int, PerObjectGroup.objects.filter(
            content_type__app_label="workshops",
            content_type__model="workshop",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True))
        return self.get_queryset().filter(pk__in=ids).exclude(status="trashed")

    def fix_bookable(self):
        self.filter(
            status="expired",
            has_group_offer=True,
        ).update(status="published")

    def update_expired(self):
        for obj in self.exclude(
            status="expired",
            has_group_offer=True,
        ):
            obj.update_closest_workshop_time()

        self.filter(
            closest_workshop_date__isnull=True,
            has_group_offer=False,
        ).exclude(status="expired").update(status="expired")

        self.filter(
            exhibition__status="expired",
            has_group_offer=True,
        ).exclude(status="expired").update(status="expired")

    def populate_press_text(self):
        for e in self.all():
            for lang_code, lang_name in settings.LANGUAGES:
                if not getattr(e, "press_text_%s" % lang_code):
                    setattr(e, "press_text_%s" % lang_code, getattr(e, "description_%s" % lang_code))
                    setattr(e, "press_text_%s_markup_type" % lang_code, getattr(e, "description_%s_markup_type" % lang_code))
            e.save()


class Workshop(CreationModificationMixin, UrlMixin, SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    workshop_type = MultilingualCharField(_("Type"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)
    website = MultilingualCharField(_("Website"), max_length=255, blank=True)
    image = FileBrowseField(_('Image'), max_length=200, directory="workshops/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, editable=False)
    types = models.ManyToManyField(WorkshopType, verbose_name=_("Types"))
    description_locked = models.BooleanField(_("Description locked"), help_text=_("When checked, press text won't be copied automatically to description."), default=False)
    
    pdf_document_de = FileBrowseField(_('PDF Document in German'), max_length=255, directory="exhibitions/", extensions=['.pdf'], blank=True)
    pdf_document_en = FileBrowseField(_('PDF Document in English'), max_length=255, directory="exhibitions/", extensions=['.pdf'], blank=True)

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    tags = TagAutocompleteField(verbose_name=_("tags"))
    languages = models.ManyToManyField(Language, verbose_name=_("Languages"), blank=True, limit_choices_to={'display': True})
    other_languages = models.CharField(_("Other languages"), max_length=255, blank=True)
    
    has_group_offer = models.BooleanField(_("Has bookable group offer"), default=False)
    is_for_preschool = models.BooleanField(_("Special for preschool children (up to 5 years)"), default=False)
    is_for_primary_school = models.BooleanField(_("Special for children of primary school age (6-12 years)"), default=False)
    is_for_youth = models.BooleanField(_("Special for youth (aged 13 years)"), default=False)
    is_for_families = models.BooleanField(_("Special for families"), default=False)
    is_for_wheelchaired = models.BooleanField(_("Special for people in wheelchairs"), default=False)
    is_for_deaf = models.BooleanField(_("Special for deaf people"), default=False)
    is_for_blind = models.BooleanField(_("Special for blind people"), default=False)
    is_for_learning_difficulties = models.BooleanField(_("Special for people with learning difficulties"), default=False)
    is_for_dementia_sufferers = models.BooleanField(_("Special for sufferers of dementia"), default=False)

    museum = models.ForeignKey(Museum, verbose_name=_("Museum"), blank=True, null=True)
    location_name = models.CharField(_("Location name"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255, blank=True)    
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)
    exhibition = models.ForeignKey(Exhibition, verbose_name=_("Related exhibition"), blank=True, null=True)

    free_admission = models.BooleanField(_("Free admission"), default=False)
    meeting_place = MultilingualCharField(_("Meeting place"), max_length=255, blank=True)
    admission_price = models.DecimalField(_(u"Admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    admission_price_info = MultilingualTextField(_("Admission price info"), blank=True)
    reduced_price = models.DecimalField(_(u"Reduced admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    booking_info = MultilingualTextField(_("Booking info"), blank=True)
    shop_link = MultilingualCharField(_("Buy ticket"), max_length=255, blank=True, help_text=_("A link to an external ticket shop"))

    closest_workshop_date = models.DateField(_("Workshop date"), editable=False, blank=True, null=True)
    closest_workshop_time = models.TimeField(_("Workshop start time"), editable=False, blank=True, null=True)

    search_keywords = MultilingualPlainTextField(_("Search keywords"), blank=True)

    favorites_count = models.PositiveIntegerField(_("Favorites count"), editable=False, default=0)

    objects = WorkshopManager()

    row_level_permissions = True

    class Meta:
        verbose_name = _("workshop")
        verbose_name_plural = _("workshops")
        ordering = ['title', 'creation_date']
        
    def __unicode__(self):
        return self.title

    def is_workshop(self):
        return True

    def get_other_workshops(self):
        if not self.museum:
            return []
        return self.museum.workshop_set.filter(status="published").exclude(pk=self.pk).order_by("closest_workshop_date", "closest_workshop_time")

    def is_today(self):
        today = date.today()
        return self.workshoptime_set.filter(workshop_date=today)
        
    def is_tomorrow(self):
        today = date.today()
        one_day = timedelta(days=1)
        return self.workshoptime_set.filter(workshop_date=today + one_day).count()
        
    def is_within_days(self, days=0):
        selected_start = date.today()
        selected_end = selected_start + timedelta(days=days)
        return self.workshoptime_set.filter(workshop_date__gte=selected_start, workshop_date__lte=selected_end).count()
        
    def is_within_7_days(self):
        return self.is_within_days(7)
    
    def is_within_30_days(self):
        return self.is_within_days(30)
    
    def get_closest_workshop_time(self, selected_date = 0):
        if selected_date != 0:
            today = selected_date
        else:
            today = date.today()
        qs = self.workshoptime_set.filter(workshop_date__gte=today)
        if qs:
            return qs[0]
        return None

    def update_closest_workshop_time(self):
        workshop_time = self.get_closest_workshop_time()
        if workshop_time:
            Workshop.objects.filter(pk=self.pk).update(
                closest_workshop_date=workshop_time.workshop_date,
                closest_workshop_time=workshop_time.start,
            )
        else:
            Workshop.objects.filter(pk=self.pk).update(
                closest_workshop_date=None,
                closest_workshop_time=None,
            )

    def get_upcoming_workshop_times(self):
        today = date.today()
        return self.workshoptime_set.filter(
            workshop_date__gte=today
        ).order_by("workshop_date", "start")

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Workshop),
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
                content_type=ContentType.objects.get_for_model(Workshop),
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
                content_type=ContentType.objects.get_for_model(Workshop),
            )
        except:
            return []
        return role.users.all()

    def get_url_path(self):
        try:
            path = reverse("workshop_detail", kwargs={'slug': self.slug})
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

    def get_particularities(self):
        particularities = []
        for f in [
            "is_for_preschool",
            "is_for_primary_school",
            "is_for_youth",
            "is_for_families",
            "is_for_wheelchaired",
            "is_for_deaf",
            "is_for_blind",
            "is_for_learning_difficulties",
            "is_for_dementia_sufferers",
        ]:
            if getattr(self, f):
                particularities.append(unicode(self._meta.get_field(f).verbose_name))
        return particularities

    def get_related_products(self):
        if not hasattr(self, '_cached_related_products'):
            self._cached_related_products = self.shopproduct_set.filter(
                status="published",
            ).order_by("-creation_date")
        return self._cached_related_products

    def get_previous_item(self):
        # The previous item will be taken by selecting all previous items ordered descending and getting the first item from the queryset.
        # To order items correctly in the queryset, we attach a sort order column combined of closest workshop date, closest workshop time, and zero-padded primary key
        try:
            current_sort_order = "{:%Y-%m-%d} {:%H:%M:%S}-{:010d}".format(self.closest_workshop_date, self.closest_workshop_time, self.pk)
            return Workshop.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
            ).extra(
                select={
                    'sort_order': "CONCAT(closest_workshop_date, ' ', closest_workshop_time, '-', LPAD(id, 10, '0'))"
                },
                where=["CONCAT(closest_workshop_date, ' ', closest_workshop_time, '-', LPAD(id, 10, '0')) < %s"],
                params=[current_sort_order],
                order_by=['-sort_order'],
            )[0]
        except Exception as e:
            return None

    def get_next_item(self):
        # The next item will be taken by selecting all next items ordered ascending and getting the first item from the queryset.
        # To order items correctly in the queryset, we attach a sort order column combined of closest workshop date, closest workshop time, and zero-padded primary key
        try:
            current_sort_order = "{:%Y-%m-%d} {:%H:%M:%S}-{:010d}".format(self.closest_workshop_date, self.closest_workshop_time, self.pk)
            return Workshop.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
            ).extra(
                select={
                    'sort_order': "CONCAT(closest_workshop_date, ' ', closest_workshop_time, '-', LPAD(id, 10, '0'))"
                },
                where=["CONCAT(closest_workshop_date, ' ', closest_workshop_time, '-', LPAD(id, 10, '0')) > %s"],
                params=[current_sort_order],
                order_by=['sort_order'],
            )[0]
        except Exception as e:
            return None


class WorkshopTime(models.Model):

    workshop = models.ForeignKey(Workshop, verbose_name=_("Workshop"))
    
    workshop_date = models.DateField(_("Workshop date"))
    start = models.TimeField(_("Start time"), null=True, blank=True)
    end = models.TimeField(_("End time"), null=True, blank=True)

    class Meta:
        verbose_name = _("workshop time")
        verbose_name_plural = _("workshop times")
        ordering = ('workshop_date', 'start', )
        
    def __unicode__(self):
        val = self.workshop_date.strftime("%Y-%m-%d")
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
        return int(self.pk) + TOKENIZATION_SUMMAND
        
    def get_humanized_date_en(self):
        current_language = get_current_language()
        activate("en")
        the_date = django_date(self.workshop_date, "jS F Y")
        activate(current_language)
        return the_date

    def get_humanized_date_de(self):
        current_language = get_current_language()
        activate("de")
        the_date = django_date(self.workshop_date, "j. F Y")
        activate(current_language)
        return the_date


class Organizer(models.Model):
    workshop = models.ForeignKey(Workshop, verbose_name=_("Workshop"))
    organizing_museum = models.ForeignKey("museums.Museum", verbose_name=_("Organizing museum"), blank=True, null=True, related_name="workshop_organizer")
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
    workshop = models.ForeignKey(Workshop, verbose_name=_("Workshop"))
    path = FileBrowseField(_('File path'), max_length=500, directory="workshops/", help_text=_("A path to a locally stored image, video, or audio file."))
    sort_order = PositionField(_("Sort order"), collection="workshop")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Media File")
        verbose_name_plural = _("Media Files")
        
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
