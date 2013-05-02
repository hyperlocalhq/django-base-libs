# -*- coding: UTF-8 -*-

from datetime import datetime, date, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse
from django.conf import settings

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import OpeningHoursMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south
from base_libs.models.fields import URLField
from base_libs.models.fields import PositionField
from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_translation

from filebrowser.fields import FileBrowseField

from cms.models import CMSPlugin

from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from jetson.apps.utils.models import MONTH_CHOICES

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])

COUNTRY_CHOICES = (
    ('de', _("Germany")),
    ('-', "Other"),
    )

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('expired', _("Expired")),
    ('import', _("Imported")),
    ('trashed', _("Trashed")),
    ) 

YEAR_CHOICES = [(i,i) for i in range(datetime.now().year, datetime.now().year+5)]

DAY_CHOICES = [(i,i) for i in range(1, 32)]

TOKENIZATION_SUMMAND = 56436 # used to hide the ids of media files

class ExhibitionCategory(MPTTModel, CreationModificationDateMixin, SlugMixin()):
    parent = TreeForeignKey('self', blank=True, null=True)
    title = MultilingualCharField(_('Title'), max_length=200)
    
    objects = TreeManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ["tree_id", "lft"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class ExhibitionManager(models.Manager):
    def newly_opened(self):
        lang_code = get_current_language()
        return self.filter(newly_opened=True, status="published").order_by("-featured", "-start", "title_%s" % lang_code)
        
    def featured(self):
        return self.filter(featured=True, status="published")
        
    def featured_in_magazine(self):
        return self.filter(featured_in_magazine=True, status="published")
        
    def closing_soon(self):
        lang_code = get_current_language()
        return self.filter(closing_soon=True, status="published").order_by("-featured", "end", "title_%s" % lang_code)
    
    def past(self, timestamp=date.today):
        """ Past events """
        if callable(timestamp):
            timestamp = timestamp()
        return self.filter(
            end__lt=timestamp,
            ).distinct()
            
    def update_expired(self):
        queryset = self.past().exclude(
            status="expired",
            )
        for obj in queryset:
            obj.status = "expired"
            obj.save()

    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if user.has_perm("exhibitions.change_exhibition"):
            return self.get_query_set().exclude(status="trashed")
        ids = PerObjectGroup.objects.filter(
            content_type__app_label="exhibitions",
            content_type__model="exhibition",
            sysname__startswith="owners",
            users=user,
            ).values_list("object_id", flat=True)
        return self.get_query_set().filter(pk__in=ids).exclude(status="trashed")

    def populate_press_text(self):
        for e in self.all():
            for lang_code, lang_name in settings.LANGUAGES:
                if not getattr(e, "press_text_%s" % lang_code):
                    setattr(e, "press_text_%s" % lang_code, getattr(e, "description_%s" % lang_code))
                    setattr(e, "press_text_%s_markup_type" % lang_code, getattr(e, "description_%s_markup_type" % lang_code))
            e.save()


class Exhibition(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    museum = models.ForeignKey("museums.Museum", verbose_name=_("Museum"), blank=True, null=True)
    
    title = MultilingualCharField(_("Title"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    teaser = MultilingualTextField(_("Teaser"), blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    press_text = MultilingualTextField(_("Press text"), blank=True)
    website = MultilingualCharField(_("Website"), max_length=255, blank=True)
    catalog = MultilingualTextField(_("Catalog"), blank=True)
    catalog_ordering = MultilingualCharField(_("Catalog ordering possibilities"), max_length=255, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)

    start = models.DateField(_("Start"), blank=True, null=True)
    end = models.DateField(_("End"), blank=True, null=True)
    vernissage = models.DateTimeField(u"Vernissage", blank=True, null=True)
    finissage = models.DateTimeField(u"Finissage", blank=True, null=True)
    exhibition_extended = models.BooleanField(_("Exhibition extended"))
    permanent = models.BooleanField(_("Permanent exhibition"))
    
    image = FileBrowseField(_('Image'), max_length=255, directory="exhibitions/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, editable=False)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True, editable=False)

    location_name = models.CharField(_("Location name"), max_length=255, blank=True)
    street_address = models.CharField(_("Street address"), max_length=255, blank=True)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255, blank=True)
    district = models.CharField(_("District"), max_length=255, blank=True)
    city = models.CharField(_("City"), default="Berlin", max_length=255, blank=True)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255, blank=True)    
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)
    other_locations = MultilingualTextField(_("Other exhibition locations"), blank=True)

    newly_opened = models.BooleanField(_("Newly opened"))
    featured = models.BooleanField(_("Featured"))
    featured_in_magazine = models.BooleanField(_("Featured in Magazine"))
    closing_soon = models.BooleanField(_("Closing soon"))
    
    # prices
    museum_prices = models.BooleanField(_("See prices from museum"))
    free_entrance = models.BooleanField(_("Free entrance"))
    admission_price = models.DecimalField(_(u"Admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    admission_price_info = MultilingualTextField(_("Admission price info"), blank=True)
    reduced_price = models.DecimalField(_(u"Reduced admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    reduced_price_info = MultilingualTextField(_("Reduced admission price info"), blank=True)

    museum_opening_hours = models.BooleanField(_("See opening hours from museum"))

    suitable_for_disabled = models.BooleanField(_("Exhibition suitable for people with disabilities"))
    suitable_for_disabled_info = MultilingualTextField(_("Suitability for people with disabilities info"), blank=True)
    
    categories = TreeManyToManyField(ExhibitionCategory, verbose_name=_("Categories"), blank=True)
    tags = TagAutocompleteField(verbose_name=_("tags"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")
    is_for_children = models.BooleanField(_("Special for children / families / youth"), blank=True)

    objects = ExhibitionManager()
    
    row_level_permissions = True
    
    def __unicode__(self):
        return self.title

    def is_exhibition(self):
        return True
        
    class Meta:
        ordering = ['title']
        verbose_name = _("Exhibition")
        verbose_name_plural = _("Exhibitions")

    def get_url_path(self):
        try:
            path = u"/" + get_current_language() + reverse("%s:exhibition_detail" % get_current_language(), kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def is_newly_open(self):
        today = date.today()
        two_weeks = timedelta(days=14)
        return today - two_weeks <= self.start <= today
        
    def is_closing_soon(self):
        today = date.today()
        two_weeks = timedelta(days=14)
        return today <= self.end <= today + two_weeks
    
    def is_actual(self):
        today = date.today()
        return self.start <= today <= self.end
        
    def is_upcoming(self):
        today = date.today()
        return today < self.start
    
    def is_today(self):
        return self.is_actual()
        
    def is_tomorrow(self):
        today = date.today()
        one_day = timedelta(days=1)
        return self.start <= today + one_day <= self.end
        
    def is_within_days(self, days=0):
        selected_start = date.today()
        selected_end = selected_start + timedelta(days=days)
        conditions = False
        """
        Get events which start date is within the selected range
        -----[--selected range--]----- time ->
                   [-event-]
                          [-event-]
        """
        conditions = conditions or (
            selected_start <= self.start <= selected_end
            )
        """
        .. which started before and will end after the selected range
        -----[-selected range-]------- time ->
           [------event---------]
        """
        conditions = conditions or (
            self.start <= selected_start and selected_end <= self.end
            )
        """
        .. or which end date is within the selected range
        -----[--selected range--]----- time ->
                 [-event-]
          [-event-]
        """
        conditions = conditions or (
            selected_start <= self.end <= selected_end
            )
        return conditions
        
    def is_within_7_days(self):
        return self.is_within_days(7)
    
    def is_within_30_days(self):
        return self.is_within_days(30)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_museum(self):
        if not self.museum:
            return ""
        return self.museum.title

    def get_other_exhibitions(self):
        if not self.museum:
            return []
        return self.museum.exhibition_set.filter(status="published").exclude(pk=self.pk)

    def get_related_published_events(self):
        return self.event_set.filter(status="published").order_by('closest_event_date', 'closest_event_time')

    def get_related_published_workshops(self):
        return self.workshop_set.filter(status="published").order_by('closest_workshop_date', 'closest_workshop_time')

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Exhibition),
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
                content_type=ContentType.objects.get_for_model(Exhibition),
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
                content_type=ContentType.objects.get_for_model(Exhibition),
                )
        except:
            return []
        return role.users.all()

    def _get_cover_image(self):
        qs = self.mediafile_set.all()
        if qs.count():
            return qs[0].path
    cover_image = property(_get_cover_image)

class Organizer(models.Model):
    exhibition = models.ForeignKey(Exhibition)
    organizing_museum = models.ForeignKey("museums.Museum", verbose_name=_("Organizing museum"), blank=True, null=True, related_name="exhibition_organizer")
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

class Season(OpeningHoursMixin):
    exhibition = models.ForeignKey(Exhibition)
    last_entry = MultilingualCharField(_("Last entry"), max_length=255, blank=True)
    is_open_24_7 = models.BooleanField(_("Open 24/7"))
    
    def __unicode__(self):
        return ugettext("Individual Opening Time of the Exhibition")
        
    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")

    def get_opening_hours(self):
        WEEKDAYS = (
            ("mon", _("Monday")),
            ("tue", _("Tuesday")),
            ("wed", _("Wednesday")),
            ("thu", _("Thursday")),
            ("fri", _("Friday")),
            ("sat", _("Saturday")),
            ("sun", _("Sunday")),
        )
        times = []
        for key, val in WEEKDAYS:
            times.append({
                "weekday": val,
                "open": getattr(self, "%s_open" % key),
                "break_close": getattr(self, "%s_break_close" % key),
                "break_open": getattr(self, "%s_break_open" % key),
                "close": getattr(self, "%s_close" % key),
                "times": "-".join((
                    str(getattr(self, "%s_open" % key)),
                    str(getattr(self, "%s_break_close" % key)),
                    str(getattr(self, "%s_break_open" % key)),
                    str(getattr(self, "%s_close" % key))
                )),
            })
        return times

class NewlyOpenedExhibition(CMSPlugin):
    exhibition = models.ForeignKey(Exhibition, limit_choices_to={'newly_opened': True})
    
    def __unicode__(self):
        return self.exhibition.title
        
    class Meta:
        ordering = ['exhibition__title']
        verbose_name = _("Newly opened exhibition")
        verbose_name_plural = _("Newly opened exhibitions")

class MediaFile(CreationModificationDateMixin):
    exhibition = models.ForeignKey(Exhibition, verbose_name=_("Exhibition"))
    path = FileBrowseField(_('File path'), max_length=255, directory="exhibitions/", help_text=_("A path to a locally stored image, video, or audio file."))
    sort_order = PositionField(_("Sort order"), collection="exhibition")

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
