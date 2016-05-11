# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode, smart_str
from django.conf import settings
from django.apps import apps
from django.db import IntegrityError
from mptt.fields import TreeForeignKey, TreeManyToManyField
from actstream import action

from base_libs.models.models import UrlMixin
from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import SlugMixin
from base_libs.models import CreationModificationDateMixin
from base_libs.models.query import ExtendedQuerySet
from base_libs.middleware import get_current_language, get_current_user
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from ccb.apps.search.fulltextsearch import SearchQuerySet

verbose_name = _("Site Specific")

### Context Item

class DefaultContextItemModels(tuple):
    def __iter__(self):
        return iter([
            models.get_model("people", "Person"),
            models.get_model("institutions", "Institution"),
            models.get_model("resources", "Document"),
            models.get_model("events", "Event"),
            models.get_model("groups_networks", "PersonGroup"),
        ])


class DefaultMappedItemModels(tuple):
    def __iter__(self):
        return iter([
            models.get_model("people", "IndividualContact"),
            models.get_model("institutions", "InstitutionalContact"),
            models.get_model("events", "Event"),
            models.get_model("marketplace", "JobOffer"),
        ])


CONTEXT_ITEM_MODELS = getattr(
    settings,
    "CONTEXT_ITEM_MODELS",
    DefaultContextItemModels(),
)

MAPPED_ITEM_MODELS = DefaultMappedItemModels()


class ContextItemManager(models.Manager):
    def __init__(self, fields=None):
        if not fields:
            fields = []
        super(ContextItemManager, self).__init__()
        self._search_fields = fields

    def get_queryset(self):
        return ExtendedQuerySet(self.model)

    # def get_queryset(self):
    #     """
    #     fulltext search functionality
    #     """
    #     return SearchQuerySet(self.model, None, self._search_fields)

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'completeness': (
                1,
                _('Completeness (complete first)'),
                ['-completeness', '-creation_date'],
            ),
            'creation_date_desc': (
                2,
                _('Creation date (newest first)'),
                ['-creation_date'],
            ),
            'creation_date_asc': (
                3,
                _('Creation date (oldest first)'),
                ['creation_date'],
            ),
            'alphabetical_asc': (
                4,
                _('Alphabetical (A-Z)'),
                ['title'],
            ),
            'alphabetical_desc': (
                5,
                _('Alphabetical (Z-A)'),
                ['-title'],
            ),
        }
        return sort_order_mapper

    def _get_title_fields(self, prefix=''):
        language = get_current_language()
        if language and language != 'en':
            return ["%stitle_%s" % (prefix, language), "%stitle" % prefix]
        else:
            return ["%stitle" % prefix]

    def search(self, query):
        """
        fulltext search functionality
        """
        return self.get_queryset().search(query)

    def recreate_all(self):
        for item in self.get_queryset():
            if not item.content_object:
                item.delete()
        for Model in CONTEXT_ITEM_MODELS:
            for obj in Model.objects.all():
                self.update_for(obj)

    def get_for(self, obj):
        if not obj:
            return None
        if isinstance(obj, self.model):
            return obj
        ctype = ContentType.objects.get_for_model(obj)
        try:
            return ContextItem.objects.get(
                content_type__pk=ctype.id,
                object_id=obj.id,
            )
        except Exception:
            return self.update_for(obj)

    def update_for(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        try:
            item = self.get(content_type=ctype, object_id=obj.id)
        except Exception:
            item = self.model(content_type=ctype, object_id=obj.id)

        """ 
        creation and modification date should not be 
        automatically generated (as usual), but taken from
        the object. We use this for sorting the whole stuff.
        """
        item.creation_date = obj.creation_date
        item.modified_date = obj.modified_date

        for lang_code, lang_title in settings.LANGUAGES:
            try:
                setattr(
                    item,
                    "title_%s" % lang_code,
                    getattr(obj, "title_%s" % lang_code),
                )
                setattr(
                    item,
                    "description_%s" % lang_code,
                    getattr(obj, "description_%s" % lang_code),
                )
            except AttributeError:
                setattr(
                    item,
                    "title_%s" % lang_code,
                    getattr(obj, "title"),
                )
                setattr(
                    item,
                    "description_%s" % lang_code,
                    getattr(obj, "description"),
                )

        item.slug = obj.slug
        item.status = obj.status

        if hasattr(obj, "get_locality_type"):
            item.locality_type = obj.get_locality_type()

        if hasattr(obj, "completeness"):
            item.completeness = obj.completeness

        # now fill in additional fields for search ....

        additional_search_data = []
        if callable(getattr(obj, "get_additional_search_data", None)):
            # adds a list of strings for indexing
            additional_search_data += obj.get_additional_search_data()

        # object types
        # for cat in obj.get_object_types():
        #    for lang_code, lang_title in settings.LANGUAGES:
        #        additional_search_data.append(
        #            getattr(cat, "title_%s" % lang_code),
        #            )

        # context categories
        for cat in obj.get_context_categories():
            for lang_code, lang_title in settings.LANGUAGES:
                additional_search_data.append(
                    getattr(cat, "title_%s" % lang_code),
                )

        # categories
        for cat in obj.get_categories():
            for lang_code, lang_title in settings.LANGUAGES:
                additional_search_data.append(
                    getattr(cat, "title_%s" % lang_code),
                )

        # creative sectors
        for cat in obj.get_creative_sectors():
            for lang_code, lang_title in settings.LANGUAGES:
                additional_search_data.append(
                    getattr(cat, "title_%s" % lang_code),
                )

        # TODO add additional index data here!

        item.additional_search_data = " ".join(additional_search_data)
        item.save()

        # item.object_types.clear()
        # item.object_types.add(*list(obj.get_object_types()))
        item.context_categories.clear()
        context_categories = list(obj.get_context_categories())
        try:
            item.context_categories.add(*context_categories)
        except IntegrityError:
            pass

        item.creative_sectors.clear()
        try:
            item.creative_sectors.add(*list(obj.get_creative_sectors()))
        except IntegrityError:
            pass

        item.categories.clear()
        try:
            item.categories.add(*list(obj.get_categories()))
        except IntegrityError:
            pass

        return item

    def delete_for(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        self.filter(content_type__pk=ctype.id, object_id=obj.id).delete()

    def publish_all(self, models=None, status_sysname="published"):
        if not models:
            models = ['person', 'institution', 'document', 'event', 'persongroup']
        for item in self.filter(content_type__model__in=models):
            item.content_object.status = status_sysname
            item.content_object.save()


ContextItemObjectRelation = ObjectRelationMixin(
    is_required=True,
    limit_content_type_choices_to={
        'model__in': ('person', 'institution', 'document', 'event', 'persongroup'),
    }
)


class ContextItem(CreationModificationDateMixin, ContextItemObjectRelation, UrlMixin, SlugMixin()):
    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)

    creative_sectors = TreeManyToManyField("structure.Term", verbose_name=_("Creative sectors"),
                                           limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'},
                                           related_name="creative_industry_contextitems", blank=True)

    context_categories = TreeManyToManyField("structure.ContextCategory", verbose_name=_("Context categories"),
                                             blank=True)

    categories = TreeManyToManyField(
        "structure.Category",
        verbose_name=_("Categories"),
        blank=True,
    )

    locality_type = TreeForeignKey("location.LocalityType", verbose_name=_("Locality type"), blank=True, null=True, on_delete=models.SET_NULL)

    completeness = models.SmallIntegerField(_("Completeness in %"), default=0)

    status = models.CharField(max_length=20, blank=True)

    # this field is used for storing additional fulltext search data
    additional_search_data = models.TextField(null=True, blank=True)

    """
    The ContextItemManager contains fulltext search capability.
    fulltext search is performed over the given fields!!! 
    Those fields must correspond to a fulltext index from mysql,
    created previously by this statement:
    
    CREATE FULLTEXT INDEX fulltext_system_contextitem on 
    creativeberlin.system_contextitem (title_en, title_de, description_en, description_de)
    """
    _searchable_fields = ['additional_search_data']
    for lang_code, lang_title in settings.LANGUAGES:
        _searchable_fields.append("title_%s" % lang_code)
        _searchable_fields.append("description_%s" % lang_code)

    objects = ContextItemManager(_searchable_fields)

    class Meta:
        verbose_name = _("context item")
        verbose_name_plural = _("context items")
        db_table = "system_contextitem"
        ordering = ['title', 'creation_date']

    def __unicode__(self):
        return force_unicode(self.get_title())

    def __str__(self):
        return smart_str(self.get_title())

    def get_title(self, language=None):
        language = language or get_current_language()
        return (getattr(self, "title_%s" % language, "") or self.title).strip() or ugettext("(Untitled)")

    get_title = lazy(get_title, unicode)
    get_title.short_description = _("Title")
    get_title.admin_order_field = "title"

    def get_description(self, language=None):
        language = language or get_current_language()
        return mark_safe(getattr(self, "description_%s" % language, "") or self.description)

    def get_creative_sectors(self):
        return self.creative_sectors.all()

    # def get_object_types(self):
    #    return self.object_types.all()

    def get_context_categories(self):
        return self.context_categories.all()

    def get_categories(self):
        return self.categories.all()

    def is_person(self):
        return self.content_type.model == "person"

    def is_institution(self):
        return self.content_type.model == "institution"

    def is_document(self):
        return self.content_type.model == "document"

    def is_event(self):
        return self.content_type.model == "event"

    def is_persongroup(self):
        return self.content_type.model == "persongroup"

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def get_url_path(self):
        return self.content_object.get_url_path()

    def get_reviewed(self):
        Comment = apps.get_model("comments", "Comment")
        # here we must take the id of contenttype and the object_id!!!!!!
        nof = Comment.objects.filter(content_type__exact=self.content_type, object_id__exact=self.object_id).count()
        return nof

    def get_saved_by(self):
        from ccb.apps.favorites.models import Favorite
        ct = ContentType.objects.get_for_model(ContextItem)
        nof = Favorite.objects.filter(content_type__exact=ct, object_id__exact=self.id).count()
        return nof

    def get_viewed_by(self):
        return "NOT YET IMPLEMENTED"

    def get_created(self):
        return self.creation_date

    def get_last_updated(self):
        return "NOT YET IMPLEMENTED"


### MappedItem

class MappedItemManager(models.Manager):
    def recreate_all(self):
        for item in self.get_queryset():
            if not item.content_object:
                item.delete()
        for Model in MAPPED_ITEM_MODELS:
            for obj in Model.objects.all():
                self.update_for(obj)

    def update_for(self, obj):
        if obj.is_public and obj.postal_address:
            address_dict = obj.postal_address.get_dict()
            # check the status of the object
            if address_dict['latitude'] and address_dict['longitude']:
                from django.utils.translation import activate
                from django.template import loader
                from django.template.context import Context

                ctype = ContentType.objects.get_for_model(obj)
                try:
                    item = self.get(content_type=ctype, object_id=obj.id)
                except Exception:
                    item = self.model(content_type=ctype, object_id=obj.id)
                item.lat = address_dict['latitude']
                item.lng = address_dict['longitude']

                item.rendered_de = item.rendered_en = unicode(obj)
                # TODO: restore the rendered_individualcontact etc templates if MappedItem is going to be used in the future
                # # use search/indexes for rendering
                # current_language = get_current_language()
                # for lang_code, lang_name in settings.LANGUAGES:
                #     activate(lang_code)
                #     field_name = "rendered_%s" % lang_code
                #     template_name = 'search/indexes/%s/%s_%s.txt' % (
                #         obj._meta.app_label, obj._meta.module_name, field_name)
                #     t = loader.get_template(template_name)
                #     html = t.render(Context({'object': obj}))
                #     setattr(item, field_name, html)
                # activate(current_language)
                try:
                    item.save()
                except Exception:
                    pass
            else:
                self.delete_for(obj)
        else:
            self.delete_for(obj)

    def delete_for(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        self.filter(content_type__pk=ctype.id, object_id=obj.id).delete()


class MappedItem(ObjectRelationMixin(is_required=True)):
    rendered_en = models.TextField()
    rendered_de = models.TextField()
    lat = models.FloatField(_("Latitude"), help_text=_(
        "Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."))
    lng = models.FloatField(_("Longitude"), help_text=_(
        "Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."))

    objects = MappedItemManager()

    class Meta:
        verbose_name = _("mapped item")
        verbose_name_plural = _("mapped items")

    def __unicode__(self):
        return self.pk

    def get_distance(self):
        distance = getattr(self, "distance", 0)
        if distance >= 1:
            return "%1f km" % distance
        else:
            return "%d m" % (distance * 1000)


### Auto-updating / auto-deleting

def update_contextitem(sender, instance, signal, *args, **kwargs):
    """
    sender is a class, not an instance of a class. So, isinstance 
    must not be used here!
    """
    if sender in iter(CONTEXT_ITEM_MODELS):
        ContextItem.objects.update_for(instance)
    if sender in iter(MAPPED_ITEM_MODELS):
        MappedItem.objects.update_for(instance)


def delete_contextitem(sender, instance, signal, *args, **kwargs):
    if sender in iter(CONTEXT_ITEM_MODELS):
        ContextItem.objects.delete_for(instance)
    if sender in iter(MAPPED_ITEM_MODELS):
        MappedItem.objects.delete_for(instance)


models.signals.post_save.connect(update_contextitem)
models.signals.pre_delete.connect(delete_contextitem)

### Visits

class VisitManager(models.Manager):
    def current(self):
        return self.filter(
            last_activity__gt=datetime.now() - timedelta(minutes=2),
        ).distinct()


class Visit(CreationModificationDateMixin):
    user = models.ForeignKey(User, verbose_name=_("User"), null=True, blank=True)
    last_activity = models.DateTimeField(default=datetime.now)
    ip_address = models.IPAddressField(_("IP Address"))
    user_agent = models.CharField(_("User Agent"), max_length=255)
    session_key = models.CharField(_("Session ID"), max_length=255)

    objects = VisitManager()

    class Meta:
        ordering = ("-last_activity",)

    def __unicode__(self):
        return _("%(user)s's visit") % {
            'user': unicode(self.user),
        }

    def update_last_activity(self):
        # change to raw UPDATE
        self.last_activity = datetime.now()
        self.save()

### Claim Request

TIME_OF_DAY_CHOICES = (
    ('morning', _('Morning')),
    ('noon', _('Noon')),
    ('afternoon', _('Afternoon')),
    ('evening', _('Evening'))
)

CLAIM_STATUS = (
    (0, _('Requested')),
    (1, _('Approved')),
    (2, _('Denied'))
)

ObjectRelationForClaimRequest = ObjectRelationMixin(
    is_required=True,
    limit_content_type_choices_to=(
        models.Q(app_label="institutions", model="institution")
        | models.Q(app_label="resources", model="document")
        | models.Q(app_label="events", model="event")
        | models.Q(app_label="groups_networks", model="persongroup")
    ),
)


class ClaimRequest(ObjectRelationForClaimRequest):
    user = models.ForeignKey(User, verbose_name=_("User"), related_name="claimrequest_user")
    name = models.CharField(_('Name'), max_length=80)
    email = models.EmailField(_('Email'))
    phone_country = models.CharField(_("Country Code"), max_length=4, blank=True, null=True)
    phone_area = models.CharField(_("Area Code"), max_length=5, blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)
    best_time_to_call = models.CharField(_("Best Time to Call"), max_length=25, choices=TIME_OF_DAY_CHOICES, blank=True,
                                         null=True)
    role = models.CharField(_('Role'), max_length=80, blank=True, null=True)
    comments = models.TextField(_('Comments'), blank=True, null=True)

    created_date = models.DateTimeField(_("Created"), auto_now_add=True)
    modified_date = models.DateTimeField(_("Modified"), auto_now=True)
    modifier = models.ForeignKey(User, verbose_name=_("Modifier"), related_name="claimrequest_modifier", blank=True,
                                 null=True)

    status = models.IntegerField(_("Status"), choices=CLAIM_STATUS, blank=True, null=True)

    class Meta:
        verbose_name = _("claim")
        verbose_name_plural = _("claims")
        db_table = "system_claimrequest"
        ordering = ('-created_date',)

    def __unicode__(self):
        return u"%s => %s" % (
            not self.content_object and "-------" or self.content_object.get_title(),
            not self.user and "-------" or self.user.username,
        )

    def save(self, *args, **kwargs):
        is_new = not self.id
        if self.id:
            self.modified_date = datetime.now()
            self.modifier = get_current_user()

        super(ClaimRequest, self).save(*args, **kwargs)
        if is_new:
            institution_claimed(type(self), self)

    save.alters_data = True

    # displays related object in admin
    def get_claimed_object(self):
        return u"""
        <a href="%s" onclick="open_new_window(event)">%s</a>
        """ % (
            self.content_object.get_absolute_url(),
            self.content_object,
        )

    get_claimed_object.short_description = _('Claimed Object')
    get_claimed_object.allow_tags = True
    get_claimed_object.admin_order_field = 'content_type'

    def get_claimer(self):
        return u"""
        <a href="%s" onclick="open_new_window(event)">%s</a>
        """ % (
            self.user.profile.get_absolute_url(),
            self.user.profile.get_title(),
        )

    get_claimer.short_description = _('User')
    get_claimer.allow_tags = True
    get_claimer.admin_order_field = 'user'
    # action in admin
    def get_approve_action(self):
        if self.status in [None, 0]:
            action = 'approve'
            action_label = force_unicode(_("Approve"))
            action_icon = "icon-yes.gif"
            return '<a href="%d/%s/"><img src="%simg/admin/%s"/> %s</a>' % (
                self.id,
                action,
                settings.JETSON_MEDIA_URL,
                action_icon,
                action_label,
            )
        else:
            return ""

    get_approve_action.short_description = _('Approve')
    get_approve_action.allow_tags = True
    get_approve_action.admin_order_field = 'status'

    def get_deny_action(self):
        if self.status in [None, 0]:
            action = 'deny'
            action_label = force_unicode(_("Deny"))
            action_icon = "icon-no.gif"
            return '<a href="%d/%s/"><img src="%simg/admin/%s"/> %s</a>' % (
                self.id,
                action,
                settings.JETSON_MEDIA_URL,
                action_icon,
                action_label
            )
        else:
            return ""

    get_deny_action.short_description = _('Deny')
    get_deny_action.allow_tags = True
    get_deny_action.admin_order_field = 'status'


# Notify appropriate users about claim requests
def institution_claimed(sender, instance, **kwargs):
    from django.contrib.sites.models import Site
    from django.contrib.auth.models import User
    from jetson.apps.notification import models as notification

    if instance.email:
        submitter_email = instance.email
    else:
        submitter_email = instance.user.email
    if instance.name:
        submitter_name = instance.name
    else:
        submitter_name = instance.user.profile.get_title()
    if instance.user:
        submitter_url = instance.user.profile.get_absolute_url()
    else:
        submitter_url = "http://%s/admin/site_specific/claimrequest/" % Site.objects.get_current().domain
    recipients = User.objects.filter(is_staff=True, is_active=True)
    notification.send(
        recipients,
        "institution_claimed",
        {
            "object_description": instance.comments,
            "object_creator_url": submitter_url,
            "object_creator_title": submitter_name,
        },
        instance=instance.content_object,
        on_site=False,
    )
    if instance.user:
        action.send(instance.user, verb="claimed", action_object=instance)
