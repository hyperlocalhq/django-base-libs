# -*- coding: UTF-8 -*-
import calendar
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import dateformat
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.encoding import force_unicode
from django.utils.text import capfirst
from tagging_autocomplete.models import TagAutocompleteField
from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey

from base_libs.models.models import UrlMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import OpeningHoursMixin
from base_libs.models import SlugMixin
from base_libs.utils.misc import get_unique_value
from base_libs.utils.misc import is_installed
from base_libs.utils.betterslugify import better_slugify
from base_libs.middleware import get_current_language, get_current_user
from base_libs.models.query import ExtendedQuerySet
from base_libs.models.fields import URLField
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from filebrowser.fields import FileBrowseField
from tagging.models import Tag
from jetson.apps.structure.models import Term
from jetson.apps.structure.models import Category
from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType, EmailType, URLType, IMType
from jetson.apps.optionset.models import get_default_phonetype_for_phone
from jetson.apps.optionset.models import get_default_phonetype_for_fax
from jetson.apps.optionset.models import get_default_phonetype_for_mobile
from jetson.apps.utils.models import MONTH_CHOICES
from jetson.apps.image_mods.models import FileManager

DATE_FORMAT = get_format('DATE_FORMAT')
DATETIME_FORMAT = get_format('DATETIME_FORMAT')
TIME_FORMAT = get_format('TIME_FORMAT')
MONTH_DAY_FORMAT = get_format('MONTH_DAY_FORMAT')
YEAR_MONTH_FORMAT = get_format('YEAR_MONTH_FORMAT')

verbose_name = _("Events")

### Event class ###

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    ('import', _("Imported")),
    ('expired', _("Expired")),
)

YEAR_CHOICES = [(i, i) for i in range(1997, datetime.now().year + 10)]

DAY_CHOICES = [(i, i) for i in range(1, 32)]

HOUR_CHOICES = [(i, i) for i in range(0, 24)]

MINUTE_CHOICES = [(i, "%02d" % i) for i in range(0, 60)]

URL_ID_EVENT = getattr(settings, "URL_ID_EVENT", "event")
URL_ID_EVENTS = getattr(settings, "URL_ID_EVENTS", "events")
DEFAULT_LOGO_4_EVENT = getattr(
    settings,
    "DEFAULT_LOGO_4_EVENT",
    "%ssite/img/website/placeholder/event.png" % settings.STATIC_URL,
)
DEFAULT_FORM_LOGO_4_EVENT = getattr(
    settings,
    "DEFAULT_FORM_LOGO_4_EVENT",
    "%ssite/img/website/placeholder/event_f.png" % settings.STATIC_URL,
)
DEFAULT_SMALL_LOGO_4_EVENT = getattr(
    settings,
    "DEFAULT_SMALL_LOGO_4_EVENT",
    "%ssite/img/website/placeholder/event_s.png" % settings.STATIC_URL,
)

SECURITY_SUMMAND = getattr(settings, "EVENT_SECURITY_SUMMAND", 7654102)

### Event class ###

def get_default_url_type():
    try:
        return URLType.objects.get(slug="homepage").id
    except Exception:
        return None


class EventTimeLabel(CreationModificationDateMixin, SlugMixin()):
    title = MultilingualCharField(_('title'), max_length=200)
    sort_order = models.IntegerField(_("Sort Order"), default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['sort_order']
        verbose_name = _("Event-time Label")
        verbose_name_plural = _("Event-time Labels")


class EventManager(models.Manager):
    """
    for comments, see institutions.InstitutionManager
    """

    def get_queryset(self):
        return ExtendedQuerySet(self.model)

    def _get_title_fields(self, prefix=''):
        language = get_current_language()
        if language and language != 'en':
            return ["%stitle_%s" % (prefix, language), "%stitle" % prefix]
        else:
            return ["%stitle" % prefix]

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'start_date_asc': (
                1,
                _('Start date'),
                ['start', ],
            ),
            'creation_date_desc': (
                2,
                _('Creation date'),
                ['-creation_date'],
            ),
            'alphabetical_asc': (
                3,
                _('Alphabetical'),
                self._get_title_fields(),
            ),
        }
        return sort_order_mapper

    def latest_published(self):
        return self.filter(
            status="published",
        ).order_by("-creation_date")

    def published_featured(self):
        return self.filter(
            is_featured=True,
            status="published",
        ).order_by("-creation_date")

    def update_current(self):
        queryset = self.nearest()
        # update start and end of the Event model by resaving
        for obj in queryset:
            obj.save()

    def update_expired(self):
        queryset = self.past().exclude(
            status="expired",
        )
        for obj in queryset:
            obj.status = "expired"
            obj.save()

    def nearest(self, timestamp=datetime.now):
        """ Currently happening and future events """
        if callable(timestamp):
            timestamp = timestamp()
        return self.filter(
            eventtime__end__gte=timestamp,
        ).distinct()

    def past(self, timestamp=datetime.now):
        """ Past events """
        if callable(timestamp):
            timestamp = timestamp()
        return self.filter(
            end__lt=timestamp,
        ).distinct()

    def current(self, timestamp=datetime.now):
        """ Currently happening events """
        if callable(timestamp):
            timestamp = timestamp()
        return self.filter(
            eventtime__start__lte=timestamp,
            eventtime__end__gte=timestamp,
        ).distinct()

    def future(self, timestamp=datetime.now):
        """ Future events """
        if callable(timestamp):
            timestamp = timestamp()
        return self.filter(
            eventtime__start__gt=timestamp,
        ).distinct()

    def nearest_published(self):
        return self.nearest().filter(
            status="published",
        )


class EventBase(CreationModificationMixin, UrlMixin):
    """
    The base class for the event. Wherever event is located - jetson or site-specific project - it should be in an app called "events" and it should be called "Event"
    """

    title = MultilingualCharField(_("Title"), max_length=255)
    slug = models.CharField(
        _("Slug for URIs"),
        max_length=255,
        db_index=True
    )
    description = MultilingualTextField(_("Description"), blank=True)
    image = FileBrowseField(_('Image'), max_length=200, directory="%s/" % URL_ID_EVENTS,
                            extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'], blank=True)

    start = models.DateTimeField(_("Start"), editable=False, null=True, blank=True)
    end = models.DateTimeField(_("End"), editable=False, null=True, blank=True)

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    row_level_permissions = True

    objects = EventManager()

    class Meta:
        abstract = True
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['title', 'creation_date']

    def __unicode__(self):
        return force_unicode(self.get_title())

    def is_event(self):
        return True

    def get_url_path(self):

        return "/%s/%s/" % (URL_ID_EVENT, self.slug)

    def get_title(self, language=None):
        language = language or get_current_language()
        return getattr(self, "title_%s" % language, "") or self.title

    get_title = lazy(get_title, unicode)

    def get_slug(self):
        return self.slug

    def get_description(self, language=None):
        language = language or get_current_language()
        description = getattr(self, "description_%s" % language, "")
        if not description:
            try:
                description = self.description
            except KeyError:
                description = ''
        return mark_safe(description)

    def save(self, *args, **kwargs):
        from jetson.apps.permissions.models import RowLevelPermission

        if not self.slug:
            self.slug = self.title
        self.slug = get_unique_value(type(self), better_slugify(self.slug), separator="-", instance_pk=self.id)
        if not self.title_de:
            self.title_de = self.title_en

        nearest_occurrence = self.get_nearest_occurrence()
        if nearest_occurrence:
            self.start = nearest_occurrence.start
            self.end = nearest_occurrence.end

        super(EventBase, self).save(*args, **kwargs)

        if self.creator and not self.creator.has_perm("events.change_event", self):
            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self,
                owner=self.creator,
            )

    save.alters_data = True

    def delete(self, *args, **kwargs):
        FileManager.delete_file(self.get_filebrowser_dir())
        super(EventBase, self).delete(*args, **kwargs)

    delete.alters_data = True

    def has_start_date(self):
        return bool(self.start)

    def get_start_date(self):
        return self.start

    get_start_date.short_description = _("Start Date")
    get_start_date.admin_order_field = 'start'

    def get_start_date_string(self):
        start_date = self.get_start_date()
        if not start_date:
            return ""
        date_format = get_format('DATE_FORMAT')
        datetime_format = get_format('DATETIME_FORMAT')
        time_format = get_format('TIME_FORMAT')
        return capfirst(dateformat.format(start_date, datetime_format))

    get_start_date_string.short_description = _("Start Date")
    get_start_date_string.admin_order_field = 'start'

    def has_end_date(self):
        return bool(self.end)

    def get_end_date(self):
        return self.end

    get_end_date.short_description = _("End Date")
    get_end_date.admin_order_field = 'end'

    def get_end_date_string(self):
        end_date = self.get_end_date()
        if not end_date:
            return ""
        date_format = get_format('DATE_FORMAT')
        datetime_format = get_format('DATETIME_FORMAT')
        time_format = get_format('TIME_FORMAT')
        return capfirst(dateformat.format(end_date, datetime_format))

    get_end_date_string.short_description = _("End Date")
    get_end_date_string.admin_order_field = 'end'

    def get_start_time_string(self):
        start_date = self.get_start_date()
        date_format = get_format('DATE_FORMAT')
        datetime_format = get_format('DATETIME_FORMAT')
        time_format = get_format('TIME_FORMAT')
        return capfirst(dateformat.format(start_date, time_format))

    get_start_time_string.short_description = _("Start Time")
    get_start_time_string.admin_order_field = 'start_hh'

    def get_end_time_string(self):
        end_date = self.get_end_date()
        date_format = get_format('DATE_FORMAT')
        datetime_format = get_format('DATETIME_FORMAT')
        time_format = get_format('TIME_FORMAT')
        return capfirst(dateformat.format(end_date, time_format))

    get_end_time_string.short_description = _("End Time")
    get_end_time_string.admin_order_field = 'end_hh'

    def get_filebrowser_dir(self):
        return "%s/%s/" % (
            URL_ID_EVENTS,
            self.slug,
        )

    def get_nearest_occurrence(self, timestamp=datetime.now):
        """ returns current or closest future or closest past event time """
        if callable(timestamp):
            timestamp = timestamp()

        event_times = self.eventtime_set.filter(
            end__gte=timestamp,
        )

        if not event_times:
            event_times = self.eventtime_set.order_by("-end")

        if event_times:
            return event_times[0]

        return None
        
    def get_past_occurrences(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.eventtime_set.filter(end__lt=timestamp)

    def get_future_occurrences(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.eventtime_set.filter(start__gt=timestamp)
        
    def get_unexpired_occurences(self, timestamp=datetime.now):
        """ returns all current and future event times """
        if callable(timestamp):
            timestamp = timestamp()

        event_times = self.eventtime_set.filter(
            end__gte=timestamp,
        )
        
        return event_times

    def is_happening(self, timestamp=datetime.now):
        if callable(timestamp):
            timestamp = timestamp()
        return self.start <= timestamp <= self.end

    def has_multiple_occurrences(self):
        return self.eventtime_set.count() > 1


class EventType(MPTTModel, SlugMixin()):
    sort_order = models.IntegerField(
        _("sort order"),
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
        'self',
        # related_name="%(class)s_children",
        related_name="child_set",
        blank=True,
        null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)

    objects = TreeManager()

    class Meta:
        verbose_name = _("event type")
        verbose_name_plural = _("event types")
        ordering = ["tree_id", "lft"]

    # noinspection PyClassHasNoInit
    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return self.title

    def get_title(self, prefix="", postfix=""):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            EventType.objects.insert_node(self, self.parent)
        super(EventType, self).save(*args, **kwargs)


class ComplexEventBase(EventBase, OpeningHoursMixin):
    """
    The base class for the complex event. Wherever event is located - jetson or site-specific project - it should be in an app called "events" and it should be called "Event"
    """

    event_type = TreeForeignKey(EventType, verbose_name=_("Event type"), related_name="type_events", )

    venue_title = models.CharField(_("Title"), max_length=255, blank=True)
    if is_installed("institutions.models"):
        venue = models.ForeignKey(
            "institutions.Institution",
            verbose_name=_("Venue"),
            blank=True,
            null=True,
            related_name="events_happened",
        )
        venue.south_field_triple = lambda: (
            "django.db.models.fields.related.ForeignKey",
            ["orm['institutions.Institution']"],
            dict(
                blank="True",
                null="True",
                related_name='"events_happened"',
            ))

    postal_address = models.ForeignKey(Address, verbose_name=_("Postal Address"), related_name="address_events",
                                       null=True, blank=True)

    if is_installed("institutions.models"):
        organizing_institution = models.ForeignKey(
            "institutions.Institution",
            verbose_name=_("Organizing institution"),
            blank=True,
            null=True,
        )
        organizing_institution.south_field_triple = lambda: (
            "django.db.models.fields.related.ForeignKey",
            ["orm['institutions.Institution']"],
            dict(
                blank="True",
                null="True",
            ))

    if is_installed("people.models"):
        organizing_person = models.ForeignKey(
            "people.Person",
            verbose_name=_("Organizing person"),
            blank=True,
            null=True,
            related_name="events_organized",
        )
        organizing_person.south_field_triple = lambda: (
            "django.db.models.fields.related.ForeignKey",
            ["orm['people.Person']"],
            dict(
                blank="True",
                null="True",
                related_name='"events_organized"',
            ))

    organizer_title = models.TextField(_("Organizer"), blank=True, null=True)
    organizer_url_link = URLField(_("Organizer URL"), blank=True, null=True)

    additional_info = MultilingualTextField(_("Additional Info"), blank=True)


    # PHONES

    phone0_type = models.ForeignKey(PhoneType, verbose_name=_("Phone Type"), blank=True, null=True,
                                    related_name='events0', default=get_default_phonetype_for_phone)
    phone0_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone0_area = models.CharField(_("Area Code"), max_length=6, blank=True, default="30")
    phone0_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    is_phone0_default = models.BooleanField(_("Default?"), default=True)
    is_phone0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    phone1_type = models.ForeignKey(PhoneType, verbose_name=_("Phone Type"), blank=True, null=True,
                                    related_name='events1', default=get_default_phonetype_for_fax)
    phone1_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone1_area = models.CharField(_("Area Code"), max_length=6, blank=True, default="30")
    phone1_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    is_phone1_default = models.BooleanField(_("Default?"), default=False)
    is_phone1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    phone2_type = models.ForeignKey(PhoneType, verbose_name=_("Phone Type"), blank=True, null=True,
                                    related_name='events2', default=get_default_phonetype_for_mobile)
    phone2_country = models.CharField(_("Country Code"), max_length=4, blank=True, default="49")
    phone2_area = models.CharField(_("Area Code"), max_length=6, blank=True)
    phone2_number = models.CharField(_("Subscriber Number and Extension"), max_length=25, blank=True)
    is_phone2_default = models.BooleanField(_("Default?"), default=False)
    is_phone2_on_hold = models.BooleanField(_("On Hold?"), default=False)


    # WEBSITES

    url0_type = models.ForeignKey(URLType, verbose_name=_("URL Type"), blank=True, null=True, related_name='events0', on_delete=models.SET_NULL)
    url0_link = URLField(_("URL"), blank=True)
    is_url0_default = models.BooleanField(_("Default?"), default=True)
    is_url0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    url1_type = models.ForeignKey(URLType, verbose_name=_("URL Type"), blank=True, null=True, related_name='events1', on_delete=models.SET_NULL)
    url1_link = URLField(_("URL"), blank=True)
    is_url1_default = models.BooleanField(_("Default?"), default=False)
    is_url1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    url2_type = models.ForeignKey(URLType, verbose_name=_("URL Type"), blank=True, null=True, related_name='events2', on_delete=models.SET_NULL)
    url2_link = URLField(_("URL"), blank=True)
    is_url2_default = models.BooleanField(_("Default?"), default=False)
    is_url2_on_hold = models.BooleanField(_("On Hold?"), default=False)


    # INSTANT MESSENGERS

    im0_type = models.ForeignKey(IMType, verbose_name=_("IM Type"), blank=True, null=True, related_name='events0', on_delete=models.SET_NULL)
    im0_address = models.CharField(_("Instant Messenger"), blank=True, max_length=255)
    is_im0_default = models.BooleanField(_("Default?"), default=True)
    is_im0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    im1_type = models.ForeignKey(IMType, verbose_name=_("IM Type"), blank=True, null=True, related_name='events1', on_delete=models.SET_NULL)
    im1_address = models.CharField(_("Instant Messenger"), blank=True, max_length=255)
    is_im1_default = models.BooleanField(_("Default?"), default=False)
    is_im1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    im2_type = models.ForeignKey(IMType, verbose_name=_("IM Type"), blank=True, null=True, related_name='events2', on_delete=models.SET_NULL)
    im2_address = models.CharField(_("Instant Messenger"), blank=True, max_length=255)
    is_im2_default = models.BooleanField(_("Default?"), default=False)
    is_im2_on_hold = models.BooleanField(_("On Hold?"), default=False)


    # EMAILS

    email0_type = models.ForeignKey(EmailType, verbose_name=_("Email Type"), blank=True, null=True,
                                    related_name='events0', on_delete=models.SET_NULL)
    email0_address = models.CharField(_("Email Address"), blank=True, max_length=255)
    is_email0_default = models.BooleanField(_("Default?"), default=True)
    is_email0_on_hold = models.BooleanField(_("On Hold?"), default=False)

    email1_type = models.ForeignKey(EmailType, verbose_name=_("Email Type"), blank=True, null=True,
                                    related_name='events1', on_delete=models.SET_NULL)
    email1_address = models.CharField(_("Email Address"), blank=True, max_length=255)
    is_email1_default = models.BooleanField(_("Default?"), default=False)
    is_email1_on_hold = models.BooleanField(_("On Hold?"), default=False)

    email2_type = models.ForeignKey(EmailType, verbose_name=_("Email Type"), blank=True, null=True,
                                    related_name='events2', on_delete=models.SET_NULL)
    email2_address = models.CharField(_("Email Address"), blank=True, max_length=255)
    is_email2_default = models.BooleanField(_("Default?"), default=False)
    is_email2_on_hold = models.BooleanField(_("On Hold?"), default=False)

    related_events = models.ManyToManyField("self", blank=True, symmetrical=True)

    tags = TagAutocompleteField(verbose_name=_("tags"))

    objects = EventManager()

    class Meta:
        abstract = True
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ['title', 'creation_date']

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def has_maps(self):
        return bool(self.postal_address)

    def has_photos(self):
        return False

    def has_videos(self):
        return False

    def get_label(self, language=None):
        language = language or get_current_language()
        return getattr(self, "label_%s" % language, "") or self.label

    def get_additional_info(self, language=None):
        language = language or get_current_language()
        return getattr(self, "additional_info_%s" % language, "") or self.additional_info

    def save(self, *args, **kwargs):
        from jetson.apps.permissions.models import RowLevelPermission

        is_new = not self.id

        super(ComplexEventBase, self).save(*args, **kwargs)

        if is_new:
            if self.creator and not self.creator.has_perm("events.change_event", self):
                RowLevelPermission.objects.create_default_row_permissions(
                    model_instance=self,
                    owner=self.creator,
                )
            if self.organizing_person and not self.organizing_person.user.has_perm("events.change_event", self):
                RowLevelPermission.objects.create_default_row_permissions(
                    model_instance=self,
                    owner=self.organizing_person.user,
                )
            if self.organizing_institution:
                for role in self.organizing_institution.get_representatives():
                    RowLevelPermission.objects.create_default_row_permissions(
                        model_instance=self,
                        owner=role,
                    )

    save.alters_data = True

    def get_locality_type(self):
        from jetson.apps.location.models import LocalityType
        try:
            postal_address = self.postal_address
            if postal_address.country.iso2_code != "DE":
                return LocalityType.objects.get(
                    slug="international",
                )
            elif postal_address.city.lower() != "berlin":
                return LocalityType.objects.get(
                    slug="national",
                )
            else:
                import re
                from jetson.apps.location.data import POSTAL_CODE_2_DISTRICT

                locality = postal_address.get_locality()
                regional = LocalityType.objects.get(
                    slug="regional",
                )
                p = re.compile('[^\d]*')  # remove non numbers
                postal_code = p.sub("", postal_address.postal_code)

                district = ""
                if locality and locality.district:
                    district = locality.district
                elif postal_code in POSTAL_CODE_2_DISTRICT:
                    district = POSTAL_CODE_2_DISTRICT[postal_code]
                if district:
                    d = {}
                    for lang_code, lang_verbose in settings.LANGUAGES:
                        d["title_%s" % lang_code] = district
                    term, created = LocalityType.objects.get_or_create(
                        slug=better_slugify(district),
                        parent=regional,
                        defaults=d,
                    )
                    return term
                else:
                    return regional
        except Exception:
            return self.venue and self.venue.get_locality_type() or None

    def get_object_types(self):
        return self.event_type and [self.event_type] or []

    def get_contacts(self):
        if self.get_postal_address() or self.get_phones() or self.get_urls() or self.get_ims() or self.get_emails():
            l = [self]
            return l
        if self.venue:
            return self.venue.get_contacts()

        return None

    def get_postal_address(self):
        return self.postal_address

    def get_phones(self):
        if not hasattr(self, '_phones_cache'):
            self._phones_cache = [{
                                      "type": getattr(self, "phone%d_type" % pos),
                                      "country": getattr(self, "phone%d_country" % pos),
                                      "area": getattr(self, "phone%d_area" % pos),
                                      "number": getattr(self, "phone%d_number" % pos),
                                      "is_default": getattr(self, "is_phone%d_default" % pos),
                                      "is_on_hold": getattr(self, "is_phone%d_on_hold" % pos),
                                  } for pos in range(3) if getattr(self, "phone%d_number" % pos) and not getattr(self,
                                                                                                                 "is_phone%d_on_hold" % pos)]
            self._phones_cache.sort(lambda p1, p2: cmp(p2['is_default'], p1['is_default']))
        return self._phones_cache

    def get_urls(self):
        if not hasattr(self, '_urls_cache'):
            self._urls_cache = [{
                                    "type": getattr(self, "url%d_type" % pos),
                                    "link": getattr(self, "url%d_link" % pos),
                                    "is_default": getattr(self, "is_url%d_default" % pos),
                                    "is_on_hold": getattr(self, "is_url%d_on_hold" % pos),
                                } for pos in range(3) if
                                getattr(self, "url%d_link" % pos) and not getattr(self, "is_url%d_on_hold" % pos)]
            self._urls_cache.sort(lambda p1, p2: cmp(p2['is_default'], p1['is_default']))

        return self._urls_cache

    def get_ims(self):
        if not hasattr(self, '_ims_cache'):
            self._ims_cache = [{
                                   "type": getattr(self, "im%d_type" % pos),
                                   "address": getattr(self, "im%d_address" % pos),
                                   "is_default": getattr(self, "is_im%d_default" % pos),
                                   "is_on_hold": getattr(self, "is_im%d_on_hold" % pos),
                               } for pos in range(3) if
                               getattr(self, "im%d_address" % pos) and not getattr(self, "is_im%d_on_hold" % pos)]
            self._ims_cache.sort(lambda p1, p2: cmp(p2['is_default'], p1['is_default']))

        return self._ims_cache

    def get_emails(self):
        if not hasattr(self, '_emails_cache'):
            self._emails_cache = [{
                                      "type": getattr(self, "email%d_type" % pos),
                                      "address": getattr(self, "email%d_address" % pos),
                                      "address_protected": getattr(self, "email%d_address" % pos).replace("@", _(
                                          " (at) ")).replace(".", _(" (dot) ")),
                                      "is_default": getattr(self, "is_email%d_default" % pos),
                                      "is_on_hold": getattr(self, "is_email%d_on_hold" % pos),
                                  } for pos in range(3) if getattr(self, "email%d_address" % pos) and not getattr(self,
                                                                                                                  "is_email%d_on_hold" % pos)]
            self._emails_cache.sort(lambda p1, p2: cmp(p2['is_default'], p1['is_default']))

        return self._emails_cache

    def is_participation_addable(self, user=None):
        user = get_current_user(user)
        return True

    def is_participation_removable(self, user=None):
        user = get_current_user(user)
        return False

    def is_claimable(self, user=None):
        user = get_current_user(user)
        return True

    def are_contacts_displayed(self, user=None):
        if not hasattr(self, "_are_contacts_displayed_cache"):
            user = get_current_user(user)
            self._are_contacts_displayed_cache = bool(
                self.postal_address
                or (user and user.has_perm("events.change_event", self))
            )
        return self._are_contacts_displayed_cache

    def are_opening_hours_displayed(self, user=None):
        if not hasattr(self, "_are_opening_hours_displayed_cache"):
            user = get_current_user(user)
            self._are_opening_hours_displayed_cache = bool(
                self.has_opening_hours()
                or (user and user.has_perm("events.change_event", self))
            )
        return self._are_opening_hours_displayed_cache

    def get_additional_search_data(self):
        """ used by ContextItemManager """
        search_data = []
        # add urls
        for url in self.get_urls():
            search_data.append(url["link"])
        search_data.append(self.tags)
        if self.organizing_institution:
            search_data.append(force_unicode(self.organizing_institution))
        if self.venue:
            search_data.append(force_unicode(self.venue))
        if self.organizing_person:
            search_data.append(force_unicode(self.organizing_person))
        return search_data


class EventTimeBase(models.Model):
    """
    The base class for the event time. Wherever event time is located - jetson or site-specific project - it should be in an app called "events" and it should be called "EventTime"
    """

    event = models.ForeignKey("events.Event", verbose_name=_("Event"))

    start_yyyy = models.IntegerField(_("Start Year"), choices=YEAR_CHOICES, default=datetime.now().year)
    start_mm = models.SmallIntegerField(_("Start Month"), blank=True, null=True, choices=MONTH_CHOICES)
    start_dd = models.SmallIntegerField(_("Start Day"), blank=True, null=True, choices=DAY_CHOICES)
    start_hh = models.SmallIntegerField(_("Start Hour"), blank=True, null=True, choices=HOUR_CHOICES)
    start_ii = models.SmallIntegerField(_("Start Minute"), blank=True, null=True, choices=MINUTE_CHOICES)
    start = models.DateTimeField(_("Start"), editable=False)

    end_yyyy = models.IntegerField(_("End Year"), choices=YEAR_CHOICES, blank=True, null=True, )
    end_mm = models.SmallIntegerField(_("End Month"), blank=True, null=True, choices=MONTH_CHOICES)
    end_dd = models.SmallIntegerField(_("End Day"), blank=True, null=True, choices=DAY_CHOICES)
    end_hh = models.SmallIntegerField(_("End Hour"), blank=True, null=True, choices=HOUR_CHOICES)
    end_ii = models.SmallIntegerField(_("End Minute"), blank=True, null=True, choices=MINUTE_CHOICES)
    end = models.DateTimeField(_("Start"), editable=False)

    is_all_day = models.BooleanField(_("All Day Event"), default=False)

    class Meta:
        abstract = True
        verbose_name = _("event time")
        verbose_name_plural = _("event times")
        ordering = ('start',)

    def __unicode__(self):
        return "%s - %s" % (
            self.start.strftime("%Y-%m-%d %H:%M"),
            self.end.strftime("%Y-%m-%d %H:%M"),
        )

    def save(self, *args, **kwargs):
        self.start = datetime(
            int(self.start_yyyy),
            int(self.start_mm or 1),
            int(self.start_dd or 1),
            int(self.start_hh or 0),
            int(self.start_ii or 0),
        )

        end_hh = self.end_hh
        if end_hh in ("", None):
            end_hh = (self.start_hh, 23)[self.start_hh in ("", None)]

        end_ii = self.end_ii
        if end_ii in ("", None):
            end_ii = (self.start_ii, 59)[self.start_ii in ("", None)]

        self.end = datetime(
            int(self.end_yyyy or self.start_yyyy),
            int(self.end_mm or self.start_mm or 12),
            int(self.end_dd or self.start_dd or calendar.monthrange(
                int(self.end_yyyy or self.start_yyyy),
                int(self.end_mm or self.start_mm or 12),
            )[1]),
            int(end_hh),
            int(end_ii),
        )

        super(EventTimeBase, self).save(*args, **kwargs)
        # update the event
        self.event.save()

    save.alters_data = True

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


class ComplexEventTimeBase(EventTimeBase):
    label = models.ForeignKey(
        EventTimeLabel,
        verbose_name=_("Label"),
        related_name="label_event_types",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        verbose_name = _("event time")
        verbose_name_plural = _("event times")
        ordering = ('start',)
