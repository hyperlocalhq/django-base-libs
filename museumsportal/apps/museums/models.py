# -*- coding: UTF-8 -*-
from datetime import datetime, time

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import OpeningHoursMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import MultilingualPlainTextField
from base_libs.models.fields import ExtendedTextField
from base_libs.models.fields import PositionField
from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_translation

from filebrowser.fields import FileBrowseField

from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

from jetson.apps.utils.models import MONTH_CHOICES


COUNTRY_CHOICES = (
    ('de', _("Germany")),
    ('-', "Other"),
)

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('trashed', _("Trashed")),
)

YEAR_CHOICES = [(i, i) for i in range(datetime.now().year, datetime.now().year+5)]

DAY_CHOICES = [(i, i) for i in range(1, 32)]

TOKENIZATION_SUMMAND = 56436 # used to hide the ids of media files


class MuseumCategory(MPTTModel, CreationModificationDateMixin, SlugMixin()):
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
            MuseumCategory.objects.insert_node(self, self.parent)
        super(MuseumCategory, self).save(*args, **kwargs)


class AccessibilityOption(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('Title'), max_length=200)
    image = FileBrowseField(_('Image'), max_length=255, directory="accessibility/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Accessibility option")
        verbose_name_plural = _("Accessibility options")


class MuseumManager(models.Manager):
    def owned_by(self, user):
        from jetson.apps.permissions.models import PerObjectGroup
        if not user.is_authenticated():
            return self.get_queryset().none()
        if user.has_perm("museums.change_museum"):
            return self.get_queryset().exclude(status="trashed")
        ids = map(int, PerObjectGroup.objects.filter(
            content_type__app_label="museums",
            content_type__model="museum",
            sysname__startswith="owners",
            users=user,
        ).values_list("object_id", flat=True))
        return self.get_queryset().filter(pk__in=ids).exclude(status="trashed")


class Museum(CreationModificationDateMixin, SlugMixin(), UrlMixin):
    parent = models.ForeignKey("self", verbose_name=_("Parent museum"), blank=True, null=True)

    title = MultilingualCharField(_("Name"), max_length=255)
    subtitle = MultilingualCharField(_("Subtitle"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)

    image = FileBrowseField(_('Image'), max_length=255, directory="museums/", extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, editable=False)
    image_caption = MultilingualTextField(_("Image Caption"), max_length=255, blank=True, editable=False)

    categories = TreeManyToManyField(MuseumCategory, verbose_name=_("Categories"),)
    tags = TagAutocompleteField(verbose_name=_("tags"))
    is_for_children = models.BooleanField(_("Special for children"), default=False)

    street_address = models.CharField(_("Street address"), max_length=255)
    street_address2 = models.CharField(_("Street address (second line)"), max_length=255, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=255)
    city = models.CharField(_("City"), default="Berlin", max_length=255)
    country = models.CharField(_("Country"), choices=COUNTRY_CHOICES, default='de', max_length=255)
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)

    phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    fax_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    fax_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    fax_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    email = models.EmailField(_("Email"), max_length=255, blank=True)
    website = URLField("Website", blank=True)
    group_bookings_phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    group_bookings_phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    group_bookings_phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    service_phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    service_phone_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    service_phone_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)

    open_on_mondays = models.BooleanField(_("Open on Mondays"), default=False)

    # prices
    free_entrance = models.BooleanField(_("Free entrance"), default=False)
    admission_price = models.DecimalField(_(u"Admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    admission_price_info = MultilingualTextField(_("Admission price info"), blank=True)
    reduced_price = models.DecimalField(_(u"Reduced admission price (€)"), max_digits=5, decimal_places=2, blank=True, null=True)
    reduced_price_info = MultilingualTextField(_("Reduced admission price info"), blank=True)
    show_family_ticket = models.BooleanField(_("Family ticket"), blank=True)
    show_group_ticket = models.BooleanField(_("Group ticket"), blank=True)
    group_ticket = MultilingualTextField(_("Group ticket"), blank=True)
    show_yearly_ticket = models.BooleanField(_("Yearly ticket"), blank=True)
    member_of_museumspass = models.BooleanField(_("Museumspass Berlin"), default=False)

    # accessibility
    accessibility = MultilingualTextField(_("Accessibility"), blank=True)
    mobidat = MultilingualTextField(_("Mobidat"), blank=True)
    accessibility_options = models.ManyToManyField(AccessibilityOption, verbose_name=_("Accessibility options"), blank=True)

    service_shop = models.BooleanField(_("Museum Shop"), default=False)
    service_restaurant = models.BooleanField(_("Restaurant"), default=False)
    service_cafe = models.BooleanField(_("Cafe"), default=False)
    service_library = models.BooleanField(_("Library"), default=False)
    service_archive = models.BooleanField(_("Archive"), default=False)
    service_diaper_changing_table = models.BooleanField(_("Diaper changing table"), default=False)

    has_audioguide = models.BooleanField(_("Audioguide"), default=False)
    has_audioguide_de = models.BooleanField(_("German"), default=False)
    has_audioguide_en = models.BooleanField(_("English"), default=False)
    has_audioguide_fr = models.BooleanField(_("French"), default=False)
    has_audioguide_it = models.BooleanField(_("Italian"), default=False)
    has_audioguide_sp = models.BooleanField(_("Spanish"), default=False)
    has_audioguide_pl = models.BooleanField(_("Polish"), default=False)
    has_audioguide_tr = models.BooleanField(_("Turkish"), default=False)
    audioguide_other_languages = models.CharField(_("Other languages"), max_length=255, blank=True)
    has_audioguide_for_children = models.BooleanField(_("Audioguide for children"), default=False)
    has_audioguide_for_learning_difficulties = models.BooleanField(_("Audioguide for people with learning difficulties"), default=False)

    participates_in_langenacht = models.BooleanField(_("Participates in Lange Nacht"), default=False)
    participates_in_berlinartweek = models.BooleanField(_("Participates in Berlin Art Week"), default=False)
    participates_in_emop = models.BooleanField(_("Participates in EMOP"), default=False)

    search_keywords = MultilingualPlainTextField(_("Search keywords"), blank=True)

    favorites_count = models.PositiveIntegerField(_("Favorites count"), editable=False, default=0)

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    objects = MuseumManager()

    row_level_permissions = True

    def __unicode__(self):
        return self.title

    def is_museum(self):
        return True

    class Meta:
        ordering = ['title']
        verbose_name = _("Museum")
        verbose_name_plural = _("Museums")

    def get_url_path(self):
        try:
            path = reverse("museum_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def get_services(self):
        services = []
        if self.service_shop:
            services.append(_("Museum Shop"))
        if self.service_restaurant:
            services.append(_("Restaurant"))
        if self.service_cafe:
            services.append(_("Cafe"))
        if self.service_library:
            services.append(_("Library"))
        if self.service_archive:
            services.append(_("Archive"))
        if self.service_diaper_changing_table:
            services.append(_("Diaper changing table"))
        return services

    def get_audioguide_languages(self):
        langs = []
        if self.has_audioguide_de:
            langs.append(_("German"))
        if self.has_audioguide_en:
            langs.append(_("English"))
        if self.has_audioguide_fr:
            langs.append(_("French"))
        if self.has_audioguide_it:
            langs.append(_("Italian"))
        if self.has_audioguide_sp:
            langs.append(_("Spanish"))
        if self.has_audioguide_pl:
            langs.append(_("Polish"))
        if self.has_audioguide_tr:
            langs.append(_("Turkish"))
        if self.audioguide_other_languages:
            langs.extend(self.audioguide_other_languages.split(","))
        return langs

    def get_museums_with_the_same_categories(self):
        categories = list(self.categories.all().values_list("pk", flat=True))
        museums = Museum.objects.filter(
            categories__in=categories,
            status="published",
        ).exclude(pk=self.pk).distinct()
        return museums

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_address(self):
        # Return museum's address. All components separated by comma, all subcomponents separated by space.
        components = []
        for j in ["street_address", "street_address2", ["postal_code", "city"]]:
            if isinstance(j, list):
                subcomponents = []
                for k in j:
                    if getattr(self, k):
                        subcomponents.append(getattr(self, k))
                components.append(" ".join(subcomponents))
            elif getattr(self, j):
                components.append(getattr(self, j))
        return ", ".join(components)
    get_address.short_description = _("Address")

    def is_open_until(self, weekday, closing_time):
        """
        weekday := "mon" | "tue" | "wed" | "thu" | "fri" | "sat" | "sun"
        closing_time := time(hh, mm)
        """
        today = datetime.today()
        if not hasattr(self, "_actual_season"): # let's cache the actual season
            actual_seasons = self.season_set.filter(start__lte=today, end__gte=today)
            self._actual_season = None
            if actual_seasons.count():
                self._actual_season = actual_seasons[0]
        if self._actual_season:
            return closing_time <= (getattr(self._actual_season, "%s_close" % weekday, None) or time(0, 0))
        return False

    # open till 20:00
    def is_open_on_mon_till_20(self):
        return self.is_open_until("mon", time(20, 0))

    def is_open_on_tue_till_20(self):
        return self.is_open_until("tue", time(20, 0))

    def is_open_on_wed_till_20(self):
        return self.is_open_until("wed", time(20, 0))

    def is_open_on_thu_till_20(self):
        return self.is_open_until("thu", time(20, 0))

    def is_open_on_fri_till_20(self):
        return self.is_open_until("fri", time(20, 0))

    def is_open_on_sat_till_20(self):
        return self.is_open_until("sat", time(20, 0))

    def is_open_on_sun_till_20(self):
        return self.is_open_until("sun", time(20, 0))

    # open till 22:00
    def is_open_on_mon_till_22(self):
        return self.is_open_until("mon", time(22, 0))

    def is_open_on_tue_till_22(self):
        return self.is_open_until("tue", time(22, 0))

    def is_open_on_wed_till_22(self):
        return self.is_open_until("wed", time(22, 0))

    def is_open_on_thu_till_22(self):
        return self.is_open_until("thu", time(22, 0))

    def is_open_on_fri_till_22(self):
        return self.is_open_until("fri", time(22, 0))

    def is_open_on_sat_till_22(self):
        return self.is_open_until("sat", time(22, 0))

    def is_open_on_sun_till_22(self):
        return self.is_open_until("sun", time(22, 0))

    def set_owner(self, user):
        ContentType = models.get_model("contenttypes", "ContentType")
        PerObjectGroup = models.get_model("permissions", "PerObjectGroup")
        RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
        try:
            role = PerObjectGroup.objects.get(
                sysname__startswith="owners",
                object_id=self.pk,
                content_type=ContentType.objects.get_for_model(Museum),
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
                content_type=ContentType.objects.get_for_model(Museum),
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
                content_type=ContentType.objects.get_for_model(Museum),
            )
        except:
            return []
        return role.users.all()

    def _get_cover_image(self):
        qs = self.mediafile_set.all()
        if qs.count():
            return qs[0].path
    cover_image = property(_get_cover_image)

    def get_exhibitions(self):
        Exhibition = models.get_model("exhibitions", "Exhibition")
        return Exhibition.objects.filter(
            models.Q(museum=self) | models.Q(organizer__organizing_museum=self)
        ).distinct().order_by("-start")

    def get_published_exhibitions(self):
        return self.get_exhibitions().filter(status="published")

    def get_events(self):
        Event = models.get_model("events", "Event")
        return Event.objects.filter(
            models.Q(museum=self) | models.Q(organizer__organizing_museum=self)
        ).distinct().order_by('closest_event_date', 'closest_event_time')

    def get_published_events(self):
        return self.get_events().filter(status="published")

    def get_workshops(self):
        language = get_current_language()
        Workshop = models.get_model("workshops", "Workshop")
        return Workshop.objects.filter(
            models.Q(museum=self) | models.Q(organizer__organizing_museum=self)
        ).distinct().order_by('closest_workshop_date', 'closest_workshop_time', 'title_%s' % language)

    def get_published_workshops(self):
        return self.get_workshops().filter(status="published")

    def get_twitter_username(self):
        if not hasattr(self, '_twitter_username_cache'):
            self._twitter_username_cache = ""
            import re
            channels = self.socialmediachannel_set.filter(channel_type__iexact="twitter")
            if channels:
                self._twitter_username_cache = re.sub(r'/$', "", re.sub(r'^https?://(www\.)?twitter.com/', "", channels[0].url))
        return self._twitter_username_cache

    def get_current_season(self):
        today = datetime.today().date()
        current_seasons = self.season_set.filter(
            start__lte=today,
            end__gte=today,
        )
        if current_seasons:
            return current_seasons[0]
        return None

    def get_related_products(self):
        if not hasattr(self, '_cached_related_products'):
            self._cached_related_products = self.shopproduct_set.filter(
                status="published",
            ).order_by("-creation_date")
        return self._cached_related_products

    def get_next_item(self):
        lang_code = settings.LANGUAGE_CODE
        field_name = 'title_{}'.format(lang_code)
        try:
            return Museum.objects.filter(
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
            return Museum.objects.filter(
                ~models.Q(pk=self.pk),
                status="published",
                **{
                    '{}__lt'.format(field_name): getattr(self, field_name)
                }
            ).order_by('-{}'.format(field_name))[0]
        except:
            return None


class Season(OpeningHoursMixin):
    museum = models.ForeignKey(Museum)
    title = MultilingualCharField(_('Season title'), max_length=255)
    start = models.DateField(_("Start"))
    end = models.DateField(_("End"))
    last_entry = MultilingualCharField(_("Last entry"), max_length=255, blank=True)

    def __unicode__(self):
        if self.start and self.end:
            return u"%s - %s" % (self.start.strftime('%Y-%m-%d'), self.end.strftime('%Y-%m-%d'))
        return u""

    class Meta:
        ordering = ('start',)
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

    def is_current(self):
        today = datetime.today().date()
        return self.start <= today <= self.end

    def is_open(self, selected_date):
        WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
        if getattr(self, "%s_open" % WEEKDAYS[selected_date.weekday()]):
            return True
        return False


class SpecialOpeningTime(models.Model):
    museum = models.ForeignKey(Museum)
    yyyy = models.PositiveIntegerField(_("Year"), blank=True, null=True, choices=YEAR_CHOICES, help_text=_("Leave this field empty, if the occasion happens every year at the same time."))
    mm = models.PositiveIntegerField(_("Month"), choices=MONTH_CHOICES)
    dd = models.PositiveIntegerField(_("Day"), choices=DAY_CHOICES)

    day_label = MultilingualCharField(_('Day label'), max_length=255, blank=True, help_text=_("e.g. Christmas, Easter, etc."))

    is_closed = models.BooleanField(_("Closed"), default=False)
    is_regular = models.BooleanField(_("Regular Opening hours"), default=False)

    opening = models.TimeField(_('Opens'), blank=True, null=True)
    break_close = models.TimeField(_('Break Starts'), blank=True, null=True)
    break_open = models.TimeField(_('Break Ends'), blank=True, null=True)
    closing = models.TimeField(_('Closes'), blank=True, null=True)

    exceptions = MultilingualTextField(_('Exceptions for working hours'), blank=True)

    def __unicode__(self):
        result = u"%s %s" % (self.get_mm_display(), self.dd)
        if self.yyyy:
            result = u"%s %s" % (self.yyyy, result)
        if self.day_label:
            result += u" - " + self.day_label
        return result

    class Meta:
        ordering = ("yyyy", "mm", "dd")
        verbose_name = _("Special opening time")
        verbose_name_plural = _("Special Opening hours")


class MediaFile(CreationModificationDateMixin):
    museum = models.ForeignKey(Museum, verbose_name=_("Museum"))
    path = FileBrowseField(_('File path'), max_length=255, directory="museums/", help_text=_("A path to a locally stored image, video, or audio file."))
    sort_order = PositionField(_("Sort order"), collection="museum")

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


class SocialMediaChannel(models.Model):
    museum = models.ForeignKey(Museum)
    channel_type = models.CharField(_("Social media type"), max_length=255, help_text=_("e.g. twitter, facebook, etc."))
    url = URLField(_("URL"), max_length=255)

    class Meta:
        ordering = ['channel_type']
        verbose_name = _("Social media channel")
        verbose_name_plural = _("Social media channels")

    def __unicode__(self):
        return self.channel_type
