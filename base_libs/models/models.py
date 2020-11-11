# -*- coding: UTF-8 -*-
import operator
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:
    from urlparse import urlparse, urlunparse

try:
    reduce  # Python 2
except NameError:
    from functools import reduce  # Python 3

import six
from django.conf import settings
from django.contrib.auth.models import User

try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey  #  Django 1.8

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import signals
from django.db.models.fields import NOT_PROVIDED
from django.template.defaultfilters import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _

try:
    from django.utils.timezone import now as tz_now
except ImportError:
    from datetime.datetime import now as tz_now

from babel.numbers import format_currency

from base_libs.models.fields import MultilingualProxy
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.signals import strip_whitespaces_from_charfields
from base_libs.utils.betterslugify import better_slugify

from base_libs.middleware import get_current_user
from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_unique_value
from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED
from base_libs.utils.text_utils import string_concat


class BaseModel(models.Model):
    """
    Abstract class for the base model. 
    Just provides some useful methods
    """

    class Meta:
        abstract = True

    def get_content_type(self):
        """returns the contenttype for the object"""
        return ContentType.objects.get_for_model(self)

    def save(self, *args, **kwargs):
        if not self.pk:
            kwargs["force_insert"] = True
        super(BaseModel, self).save(*args, **kwargs)


class CreationDateMixin(BaseModel):
    """
    Abstract base class with a creation date
    """

    creation_date = models.DateTimeField(_("creation date"), editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creation_date = tz_now()
        else:
            """
            there are some strange creation_date entries in the dump.
            To ensure that we have a creation data always, we add this one
            """
            if not self.creation_date:
                self.creation_date = tz_now()

        super(CreationDateMixin, self).save(*args, **kwargs)
        # TODO: maybe should be changed to self.save_base(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class ModifiedDateMixin(BaseModel):
    """
    Abstract base class with a modified date
    """

    modified_date = models.DateTimeField(_("modified date"), null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.pk:
            self.modified_date = tz_now()
        super(ModifiedDateMixin, self).save(*args, **kwargs)
        # TODO: maybe should be changed to self.save_base(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreationModificationDateMixin(CreationDateMixin, ModifiedDateMixin):
    """
    Abstract base class with a creation date and modification date
    """

    class Meta:
        abstract = True


class CreatorMixin(BaseModel):
    """
    Abstract base class with a "creator" Field
    """

    creator = models.ForeignKey(
        User,
        verbose_name=_("creator"),
        related_name="%(class)s_creator",
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = get_current_user()
        super(CreatorMixin, self).save(*args, **kwargs)
        # TODO: maybe should be changed to self.save_base(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class ModifierMixin(BaseModel):
    """
    Abstract base class with a "modifier" Field
    """

    modifier = models.ForeignKey(
        User,
        verbose_name=_("modifier"),
        related_name="%(class)s_modifier",
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )

    def save(self, *args, **kwargs):
        if self.pk:
            self.modifier = get_current_user()
        super(ModifierMixin, self).save(*args, **kwargs)
        # TODO: maybe should be changed to self.save_base(*args, **kwargs)

    save.alters_data = True

    class Meta:
        abstract = True


class CreatorModifierMixin(CreatorMixin, ModifierMixin):
    """
    Abstract base class with a creator and a modifier
    """

    class Meta:
        abstract = True


class CreationModificationMixin(
    CreatorMixin, CreationDateMixin, ModifierMixin, ModifiedDateMixin
):
    """
    Abstract base class with a creator and a modifier 
    as well as creation date and modifcation date
    """

    class Meta:
        abstract = True


class PublishingMixinDraftManager(models.Manager):
    def get_queryset(self):
        return (
            super(PublishingMixinDraftManager, self,)
            .get_queryset()
            .filter(status__exact=STATUS_CODE_DRAFT)
        )


class PublishingMixinPublishedManager(models.Manager):
    def get_queryset(self):
        conditions = []
        now = tz_now()
        conditions.append(models.Q(published_from=None, published_till=None,))
        conditions.append(models.Q(published_from__lte=now, published_till=None,))
        conditions.append(models.Q(published_from=None, published_till__gt=now,))
        conditions.append(models.Q(published_from__lte=now, published_till__gt=now,))
        return (
            super(PublishingMixinPublishedManager, self,)
            .get_queryset()
            .filter(reduce(operator.or_, conditions),)
            .filter(status__exact=STATUS_CODE_PUBLISHED)
        )


class PublishingMixin(BaseModel):
    """
    Abstract base class with publishing start and end dates.
    """

    STATUS_CHOICES = getattr(
        settings,
        "PUBLISHING_STATUS_CHOICES",
        ((STATUS_CODE_DRAFT, _("Draft")), (STATUS_CODE_PUBLISHED, _("Published")),),
    )

    author = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=_("author"),
        related_name="%(class)s_author",
        help_text=_("If you do not select an author, you will be the author!"),
        on_delete=models.SET_NULL,
    )

    published_from = models.DateTimeField(
        _("publishing date"),
        null=True,
        blank=True,
        help_text=_(
            "If not provided and the status is set to 'published', the entry will be published immediately."
        ),
    )
    published_till = models.DateTimeField(
        _("published until"),
        null=True,
        blank=True,
        help_text=_(
            "If not provided and the status is set to 'published', the entry will be published forever."
        ),
    )

    status = models.SmallIntegerField(
        _("status"), choices=STATUS_CHOICES, default=STATUS_CODE_DRAFT,
    )

    objects = models.Manager()
    published_objects = PublishingMixinPublishedManager()
    draft_objects = PublishingMixinDraftManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.author:
            self.author = get_current_user()

        # publishing date save logic.
        if not self.published_from:
            self.published_from = tz_now()

        super(PublishingMixin, self).save(*args, **kwargs)
        # TODO: maybe should be changed to self.save_base(*args, **kwargs)

    save.alters_data = True

    def is_published(self):
        return bool(type(self).published_objects.filter(pk=self.pk))

    is_published.boolean = True
    is_published.short_description = _("Published")

    def is_draft(self):
        return self.status == STATUS_CODE_DRAFT

    is_draft.boolean = True
    is_draft.short_description = _("Draft")


class ViewsMixin(BaseModel):
    """
    Abstract base class with a "views" field
    """

    views = models.IntegerField(_("views"), default=0, editable=False)

    def increase_views(self):
        """
        Update the views count without resaving the whole instance.
          * pre_save and post_save signals are not trigerred
          * save() method is not called
          * modification dates are not changed
        """
        type(self)._default_manager.filter(
            pk=self.pk,
        ).update(views=models.F("views") + 1)

    increase_views.alters_data = True

    class Meta:
        abstract = True


class UrlMixin(models.Model):
    """
    A replacement for get_absolute_url()
    Models extending this mixin should have either get_url or get_url_path implemented.
    http://code.djangoproject.com/wiki/ReplacingGetAbsoluteUrl
    """

    def get_url(self):
        if hasattr(self.get_url_path, "dont_recurse"):
            raise NotImplementedError("Neither get_url_path() nor get_url() methods are defined for the {model} model.".format(model=type(self).__name__))
        try:
            path = self.get_url_path()
        except NotImplementedError:
            raise
        protocol = getattr(settings, "PROTOCOL", "http")
        domain = Site.objects.get_current().domain
        port = getattr(settings, "PORT", "")
        if port:
            assert port.startswith(":"), "The PORT setting must have a preceeding ':'."
        return "%s://%s%s%s" % (protocol, domain, port, path)

    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, "dont_recurse"):
            raise NotImplementedError("Neither get_url_path() nor get_url() methods are defined for the {model} model.".format(model=type(self).__name__))
        try:
            url = self.get_url()
        except NotImplementedError:
            raise
        bits = urlparse(url)
        return urlunparse(("", "") + bits[2:])

    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url_path()

    class Meta:
        abstract = True


class CommentsMixin(BaseModel):
    """
    Abstract base class for comment handling
    """

    comments_allowed = models.BooleanField(_("allow comments"), default=True)
    comments_close_date = models.DateTimeField(
        _("close comments"), blank=True, null=True
    )

    class Meta:
        abstract = True


def ObjectRelationMixin(
    prefix=None,
    prefix_verbose=None,
    add_related_name=False,
    limit_content_type_choices_to=None,
    limit_object_choices_to=None,
    is_required=False,
):
    """
    returns a mixin class for generic foreign keys using 
    "Content type - object Id" with dynamic field names. 
    This function is just a class generator
    
    Parameters:
    prefix : a prefix, which is added in front of the fields
    prefix_verbose :    a verbose name of the prefix, used to 
                        generate a title for the field column
                        of the content object in the Admin.
    add_related_name :  a boolean value indicating, that a 
                        related name for the generated content
                        type foreign key should be added. This
                        value should be true, if you use more 
                        than one ObjectRelationMixin in your model.

    The model fields are created like this:
    
    <<prefix>>_content_type :   Field name for the "content type"
    <<prefix>>_object_id :      Field name for the "object Id"
    <<prefix>>_content_object : Field name for the "content object"
    
    """
    if not limit_object_choices_to:
        limit_object_choices_to = {}
    if not limit_content_type_choices_to:
        limit_content_type_choices_to = {}
    if prefix:
        p = "%s_" % prefix
    else:
        p = ""

    content_type_field = "%scontent_type" % p
    object_id_field = "%sobject_id" % p
    content_object_field = "%scontent_object" % p
    admin_content_object_name = _("Content Object")
    admin_content_type_name = _("Related object's type (model)")
    if prefix_verbose:
        admin_content_object_name = string_concat(
            prefix_verbose, " ", _("Content Object")
        )
        admin_content_type_name = string_concat(prefix_verbose, _("'s type (model)"))

    class ModelWithObjectRelation(BaseModel):
        class Meta:
            abstract = True

    if add_related_name:
        if not prefix:
            raise FieldError(
                "if add_related_name is set to True, a prefix must be given"
            )
        related_name = prefix
    else:
        related_name = None

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=admin_content_type_name,
        related_name=related_name,
        blank=not is_required,
        null=not is_required,
        help_text=_(
            "Please select the type (model) for the relation, you want to build."
        ),
        limit_choices_to=limit_content_type_choices_to,
        on_delete=models.CASCADE,
    )

    object_id = models.CharField(
        (prefix_verbose and prefix_verbose or _("Related object")),
        blank=not is_required,
        null=False,
        help_text=_("Please select the related object."),
        max_length=255,
        default="",
    )
    object_id.limit_choices_to = limit_object_choices_to
    # can be retrieved by MyModel._meta.get_field("object_id").limit_choices_to
    content_object = GenericForeignKey(
        ct_field=content_type_field, fk_field=object_id_field,
    )

    ModelWithObjectRelation.add_to_class(content_type_field, content_type)
    ModelWithObjectRelation.add_to_class(object_id_field, object_id)
    ModelWithObjectRelation.add_to_class(content_object_field, content_object)

    "add methods: for the methods, we can use setattr(ModelWithObjectRelation, ..., ...)"
    # setattr(ModelWithObjectRelation, 'get_%s' % content_object_field, get_content_object)
    return ModelWithObjectRelation


class SingleSiteMixinManager(models.Manager):
    def get_queryset(self):
        return (
            super(SingleSiteMixinManager, self)
            .get_queryset()
            .filter(models.Q(site=None) | models.Q(site=Site.objects.get_current()))
        )


class SingleSiteMixin(BaseModel):
    site = models.ForeignKey(
        Site,
        verbose_name=_("Site"),
        blank=True,
        null=True,
        help_text=_("Restrict this object only for the selected site"),
        on_delete=models.SET_NULL,
    )

    objects = models.Manager()
    site_objects = SingleSiteMixinManager()

    def get_site(self):
        """used for display in the admin"""
        if not self.site:
            return _("All")
        return self.site.name

    get_site.short_description = _("Site")

    class Meta:
        abstract = True


class MultiSiteMixinManager(models.Manager):
    def get_queryset(self):
        return (
            super(MultiSiteMixinManager, self)
            .get_queryset()
            .filter(sites=Site.objects.get_current(),)
        )


class MultiSiteMixin(BaseModel):
    sites = models.ManyToManyField(
        Site,
        verbose_name=_("Site"),
        help_text=_("Restrict this object only for the selected site"),
    )

    objects = models.Manager()
    site_objects = MultiSiteMixinManager()

    class Meta:
        abstract = True


class SingleSiteContainerMixin(ObjectRelationMixin(), SingleSiteMixin, UrlMixin):
    """
    Abstract base class for "Single Site Containers". 
    These are Containers, where you can specify no or one site.
    """

    sysname = models.CharField(
        _("URL identifier"),
        max_length=255,
        help_text=_(
            "Please specify an additional URL identifier for the container here. The provided name must be the last part of the calling url, which wants to access the container. For example, if you have a FAQ-Container and you want to use the url 'http://www.example.com/gettinghelp/faqs/', the URL identifier must be 'faqs'. For different URL identifiers, you can create multiple containers for the same related object and site. Note, that the site, the related object and the URL identifier must be unique together."
        ),
    )

    @classmethod
    def is_single_site_container(cls):
        """
        we need that at some places in views to look for the 
        appropriate container (SingleSite or MultiSite)
        """
        return True

    # interface method from UrlMixin, required!!!
    def get_url_path(self):
        prefix = "/"
        rel_obj = self.content_object
        if rel_obj and hasattr(rel_obj, "get_url_path"):
            prefix = rel_obj.get_url_path()
        return "%s%s/" % (prefix, self.sysname)

    def create_for_current_site(self):
        self.site = Site.objects.get_current()
        self.save()

    def create_for_site(self, site):
        self.site = site
        self.save()

    class Meta:
        abstract = True


class MultiSiteContainerMixinManager(models.Manager):
    """
    A manager for MultiSiteContainerMixin abstract class below.
    
    Attention:
    see the remarks on HierarchyMixinManager!!!!
    """

    _join_cache = {}

    def contribute_to_class(self, model, name):
        # TODO: Use weakref because of possible memory leak / circular reference.
        self.model = model
        setattr(model, name, models.manager.ManagerDescriptor(self))
        if (
            not getattr(model, "objects", None)
            or self.creation_counter < model.objects.creation_counter
        ):
            model.objects = self

    def add_site(self, site):
        """
        adds a site to all entries (if it is not already in)
        """
        for item in self.all():
            if not (site in item.sites.all()):
                item.sites.add(site)

    def remove_site(self, site):
        """
        removes a site from all entries
        """
        for item in self.all():
            if site in item.sites.all():
                item.sites.remove(site)

    def add_all_sites(self):
        """
        adds a site to all entries (if it is not already in)
        """
        for item in self.all():
            for site in Site.objects.all():
                if not (site in item.sites.all()):
                    item.sites.add(site)

    def clear_all_except(self, site=None):
        """
        removes all sites except the given one from all entries
        if site is None, all sites will be removed!
        """
        if site:
            sites = Site.objects.exclude(id__exact=site.id)
        else:
            sites = Site.objects.all()

        for item in self.all():
            for s in sites:
                if s in item.sites.all():
                    item.sites.remove(s)


class MultiSiteContainerMixin(ObjectRelationMixin(), UrlMixin):
    """
    Abstract base class for "Multi Site Containers". 
    These are Containers, where you can specify 0..n sites.
    """

    sites = models.ManyToManyField(
        Site,
        verbose_name=_("Sites"),
        blank=True,
        help_text=_(
            "Please select some sites, this container relates to. If you do not select any site, the container applies to all sites."
        ),
    )

    sysname = models.CharField(
        _("URL Identifier"),
        max_length=255,
        help_text=_(
            "Please specify an additional URL identifier for the container here. The provided name must be the last part of the calling url, which wants to access the container. For example, if you have a FAQ-Container and you want to use the url 'http://www.example.com/gettinghelp/faqs/', the URL identifier must be 'faqs'. For different URL identifiers, you can create multiple containers for the same related object and site. Note, that the site, the related object and the URL identifier must be unique together."
        ),
    )

    objects = models.Manager()
    container = MultiSiteContainerMixinManager()

    def get_sites(self):
        """used for display in the admin"""
        if len(self.sites.all()) == 0:
            return _("All")
        sites = ""
        for item in self.sites.all():
            sites = sites + str(item.name) + "<br />"
        return sites

    get_sites.short_description = _("Sites")
    get_sites.allow_tags = True

    # get_sites.admin_order_field = sites

    @classmethod
    def is_single_site_container(cls):
        """
        we need that at some places in views to look for the 
        appropriate container (SingleSite or MultiSite)
        """
        return False

    # interface method from UrlMixin, required!!!
    def get_url_path(self):
        prefix = "/"
        rel_obj = self.content_object
        if rel_obj and hasattr(rel_obj, "get_url_path"):
            prefix = rel_obj.get_url_path()
        return "%s%s/" % (prefix, self.sysname)

    class Meta:
        abstract = True

    def create_for_current_site(self):
        self.save()
        self.sites.add(Site.objects.get_current())

    def create_for_site(self, site):
        self.save()
        self.sites.add(site)


class RootDoesNotExist(Exception):
    pass


class HierarchyMixinManager(models.Manager):
    """
    A manager for HierarchyMixin abstract class below.
    """

    def get_roots(self):
        roots = self.get_queryset().filter(parent__isnull=True)
        if roots.count() > 0:
            return roots
        else:
            raise RootDoesNotExist(ugettext(
                "Roots Node does not exist. Please create one."
            ))

    def update_paths(self):
        """
        recalculates all paths and commit changes to the database
        """
        for item in self.all():
            item.path = item.get_path()
            item.save()

    def rebuild_paths(self):
        """
        rebuild paths for Tree structures
        """
        counter = 0
        for item in self.order_by("path"):
            item.sort_order = counter
            counter += 1
            item.save()


def _sort_order_coding(sort_order):
    """
    encodes the sort_order to a sortable string with the
    following options: the string encoding of numbers from
    -16^6/2 to +16^6/2 is well sorted like the number itself.
    A range from -16^6/2 to +^16^6/2 should be sufficient!!! 
    """
    return "%06x" % (0x800000 + sort_order)


class HierarchyMixin(BaseModel):
    """
    A base class for hierarchies
    """

    sort_order = models.IntegerField(_("sort order"), blank=True, editable=False,)
    parent = models.ForeignKey(
        "self",
        # related_name="%(class)s_children",
        related_name="child_set",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    path = models.CharField(_("path"), max_length=8192, null=True, editable=False)

    objects = models.Manager()
    tree = HierarchyMixinManager()

    def short_str(self):
        """
        may be overriden with a shorter representation of str
        """
        return self.__str__()

    def is_hierarchical(self):
        """ just determines, if the model behind is hierarchical data """
        return True

    def is_leaf(self):
        return not self.has_children()

    def get_children(self):
        return self._default_manager.filter(parent=self).order_by("path")

    def has_children(self):
        return self.get_children().count() > 0

    def get_descendants(self):
        return (
            self._default_manager.filter(path__startswith=self.path)
            .exclude(pk=self.pk)
            .order_by("path")
        )

    def get_root(self):
        parent = self.parent
        if not parent:
            return self
        else:
            root = None
            while parent:
                root = parent
                parent = parent.parent
            return root

    def get_level(self):
        return self.path.count("/") - 1

    # can be overwritten!
    def get_path(self):
        """
        calculates internal representation of the 'path' field
        """
        path = ""
        child = self
        parent = self.parent
        root = self
        while parent:
            path = "%s_%s/%s" % (
                str(parent.pk),
                _sort_order_coding(child.sort_order),
                path,
            )
            if not parent.parent:
                root = parent
            child = parent
            parent = parent.parent

        path = "%s/%s" % (_sort_order_coding(root.sort_order), path)
        return path

    # can be overwritten!
    def get_verbose_path(self):
        """
        returns a verbose representation of the path
        """
        path = ""
        parent = self
        while parent:
            path = "%s<p>%s</p>" % (parent, path)
            parent = parent.parent
        return path

    def save(self, *args, **kwargs):
        if self.sort_order is None:
            # get the largest sort_order from the model
            item_with_max_sort_order = self.__class__._default_manager.order_by(
                "-sort_order"
            )[:1]
            if item_with_max_sort_order:
                self.sort_order = item_with_max_sort_order[0].sort_order + 1
            else:
                self.sort_order = 1
        self.path = self.get_path()
        super(HierarchyMixin, self).save()
        # TODO: maybe should be changed to self.save_base(*args, **kwargs)
        # the descendants's path must be saved too!
        for child in self.get_children():
            child.save(*args, **kwargs)

    save.alters_data = True

    class Meta:
        ordering = ["path", "sort_order"]
        abstract = True


def SlugMixin(
    name="slug",
    prepopulate_from=("title",),
    proposal="",
    separator="-",
    verbose_name=_("Slug for URIs"),
    max_length=255,
    unique=True,
    unique_for=(),
    **slug_mixin_kwargs
):
    """
    returns a mixin class for a slug field used for URLs. 
    This function is just a class generator
    
    Parameters:
    name:               name of the slug field.
    prepopulate_from:   a tuple of field names to prepopulate from if name is
                        empty.
    separator:          a symbol to separate different parts of the slug.
    proposal:           a string or a callable taking model instance as 
                        a parameter and returning a string with a proposed value
    unique_for:         defines the tuple of fields for which the slug should be
                        unique
    The other parameters are as for a models.SlugField().
    """

    slug_field = models.SlugField(
        verbose_name=verbose_name,
        max_length=max_length,
        unique=unique and not unique_for,
        **slug_mixin_kwargs
    )

    class ModelWithSlug(BaseModel):
        def save(self, *args, **kwargs):
            slug_field = self._meta.get_field(name)
            # PYTHON BUG? callable() doesn't recognize variables from outer scope
            _proposal = proposal
            if callable(_proposal):
                _proposal = _proposal(self)
            slug_proposal = getattr(self, name, None) or _proposal
            if not slug_field.blank or slug_proposal:
                if not slug_proposal or slug_field.default == slug_proposal:
                    slug_proposal = (
                        separator.join(
                            [getattr(self, fname, "") for fname in prepopulate_from]
                        )
                        or slug_field.default
                    )
                if isinstance(slug_proposal, six.string_types):
                    slug_proposal = better_slugify(
                        slug_proposal, remove_stopwords=False
                    ).replace("-", separator,)[: slug_field.max_length - 5]
                slug = slug_proposal
                if slug_field.unique or unique_for:
                    qs = type(self)
                    if unique_for:
                        qs_filter = {}
                        for field_name in unique_for:
                            qs_filter[field_name] = getattr(self, field_name)
                        qs = qs._default_manager.filter(**qs_filter)
                    slug = get_unique_value(
                        model=qs,
                        proposal=slug_proposal,
                        field_name=name,
                        instance_pk=self.pk,
                        separator=separator,
                    )
                setattr(self, name, slug)
            super(ModelWithSlug, self).save(*args, **kwargs)

        save.alters_data = True

        class Meta:
            abstract = True

    ModelWithSlug.add_to_class(name, slug_field)

    return ModelWithSlug


def SysnameMixin(**sysname_mixin_kwargs):
    """
    returns a mixin class for a slug field used for views and templates. 
    This function is just a class generator
    
    All parameters are as for the SlugMixin().
    """
    sysname_params = {
        "name": "sysname",
        "separator": "_",
        "verbose_name": _("Sysname"),
        "help_text": _("Do not change this value!"),
    }
    sysname_params.update(sysname_mixin_kwargs)

    class ModelWithSysname(SlugMixin(**sysname_params)):
        class Meta:
            abstract = True

    return ModelWithSysname


def MultilingualSlugMixin(
    name="slug",
    prepopulate_from=("title",),
    proposal="",
    separator="-",
    verbose_name=_("Slug for URIs"),
    max_length=255,
    unique=True,
    unique_for=(),
    **kwargs
):
    """
    returns a mixin class for a slug field used for URLs. 
    This function is just a class generator
    
    Parameters:
    name:               name of the slug field.
    prepopulate_from:   a tuple of field names to prepopulate from if name is
                        empty.
    separator:          a symbol to separate different parts of the slug.
    proposal:           a string or a callable taking model instance as 
                        a parameter and returning a string with a proposed value
    unique_for:         defines the tuple of fields for which the slug should be
                        unique
    The other parameters are as for a models.SlugField().
    """
    _blank = False
    if "blank" in kwargs:
        _blank = kwargs.pop("blank")

    class ModelWithMultilingualSlug(BaseModel):
        def save(self, *args, **kwargs):
            for lang_code, lang_name in settings.LANGUAGES:
                slug_field = self._meta.get_field("%s_%s" % (name, lang_code))
                # PYTHON BUG? callable() doesn't recognize variables from outer scope
                _proposal = proposal
                if callable(_proposal):
                    _proposal = _proposal(self)
                slug = ""
                slug_proposal = getattr(self, "%s_%s" % (name, lang_code), _proposal)
                if not slug_field.blank or slug_proposal or prepopulate_from:
                    if not slug_proposal or slug_field.default == slug_proposal:
                        slug_proposal = separator.join(
                            [
                                getattr(self, "%s_%s" % (fname, lang_code), "")
                                for fname in prepopulate_from
                            ]
                        )
                        if slug_field.default != NOT_PROVIDED:
                            slug_proposal = slug_proposal or slug_field.default
                    slug_proposal = better_slugify(
                        slug_proposal, remove_stopwords=False
                    ).replace("-", separator,)[: slug_field.max_length - 5]
                    slug = slug_proposal
                    if slug_field.unique or unique_for:
                        qs = type(self)
                        if unique_for:
                            qs_filter = {}
                            for field_name in unique_for:
                                qs_filter[field_name] = getattr(self, field_name)
                            qs = qs._default_manager.filter(**qs_filter)
                        slug = get_unique_value(
                            model=qs,
                            proposal=slug_proposal,
                            field_name="%s_%s" % (name, lang_code),
                            instance_pk=self.pk,
                            separator=separator,
                        )
                setattr(self, "%s_%s" % (name, lang_code), slug)
            super(ModelWithMultilingualSlug, self).save(*args, **kwargs)

        save.alters_data = True

        class Meta:
            abstract = True

    # localized fields
    for lang_code, lang_name in settings.LANGUAGES:
        if lang_code == settings.LANGUAGE_CODE:
            blank = _blank
        else:
            blank = True
        slug_field = models.SlugField(
            verbose_name=verbose_name,
            max_length=max_length,
            unique=unique and not unique_for,
            blank=blank,
            **kwargs
        )
        ModelWithMultilingualSlug.add_to_class("%s_%s" % (name, lang_code), slug_field)

    # dummy field
    # TODO: remove?
    kwargs["editable"] = False
    kwargs["null"] = True
    kwargs["blank"] = _blank
    slug_field = models.SlugField(
        verbose_name=verbose_name,
        max_length=max_length,
        unique=unique and not unique_for,
        **kwargs
    )
    ModelWithMultilingualSlug.add_to_class(name, slug_field)

    setattr(ModelWithMultilingualSlug, name, MultilingualProxy(slug_field))

    return ModelWithMultilingualSlug


class ContentBaseMixinDraftManager(PublishingMixinDraftManager):
    def get_queryset(self):
        return (
            super(ContentBaseMixinDraftManager, self)
            .get_queryset()
            .filter(sites=Site.objects.get_current(),)
        )


class ContentBaseMixinPublishedManager(PublishingMixinPublishedManager):
    def get_queryset(self):
        return (
            super(ContentBaseMixinPublishedManager, self)
            .get_queryset()
            .filter(sites=Site.objects.get_current(),)
        )


class ContentBaseMixin(MultiSiteMixin, CreationModificationMixin, PublishingMixin):
    """
    Abstract base class for any "Content"
    """

    title = MultilingualCharField(_("title"), max_length=255)
    subtitle = MultilingualCharField(_("subtitle"), max_length=255, blank=True)
    short_title = MultilingualCharField(_("short title"), max_length=32, blank=True)
    content = MultilingualTextField(_("content"), blank=True)

    objects = models.Manager()
    site_published_objects = ContentBaseMixinPublishedManager()
    site_draft_objects = ContentBaseMixinDraftManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title

    def get_content(self):
        return mark_safe(self.content)

    get_content.short_description = _("Content")


class MetaTagsMixin(BaseModel):
    """
    Abstract base class for meta tags in the <head> section
    """

    meta_keywords = MultilingualCharField(
        _("Keywords"),
        max_length=255,
        blank=True,
        help_text=_("Separate keywords by comma."),
    )
    meta_description = MultilingualCharField(
        _("Description"), max_length=255, blank=True
    )
    meta_author = models.CharField(_("Author"), max_length=255, blank=True)
    meta_copyright = models.CharField(_("Copyright"), max_length=255, blank=True)

    class Meta:
        abstract = True

    def get_meta_keywords(self, language=None):
        language = language or get_current_language()
        meta_tag = ""
        meta_keywords = getattr(self, "meta_keywords_%s" % language)
        if meta_keywords:
            meta_tag = u"""<meta name="keywords" lang="%s" content="%s" />\n""" % (
                language,
                escape(meta_keywords),
            )
        return mark_safe(meta_tag)

    def get_meta_description(self, language=None):
        language = language or get_current_language()
        meta_tag = ""
        meta_description = getattr(self, "meta_description_%s" % language)
        if meta_description:
            meta_tag = u"""<meta name="description" lang="%s" content="%s" />\n""" % (
                language,
                escape(meta_description),
            )
        return mark_safe(meta_tag)

    def get_meta_author(self):
        meta_tag = ""
        if self.meta_author:
            meta_tag = u"""<meta name="author" content="%s" />\n""" % escape(
                self.meta_author
            )
        return mark_safe(meta_tag)

    def get_meta_copyright(self):
        meta_tag = ""
        if self.meta_copyright:
            meta_tag = u"""<meta name="copyright" content="%s" />\n""" % escape(
                self.meta_copyright
            )
        return mark_safe(meta_tag)

    def get_meta_tags(self, language=None):
        return mark_safe(
            "".join(
                (
                    self.get_meta_keywords(language=language),
                    self.get_meta_description(language=language),
                    self.get_meta_author(),
                    self.get_meta_copyright(),
                )
            )
        )


class SEOMixin(MetaTagsMixin):
    """
    Abstract base class for title and meta tags in the <head> section
    """

    page_title = MultilingualCharField(_("page title"), max_length=255, blank=True)

    class Meta:
        abstract = True


class OpeningHoursMixin(BaseModel):
    is_appointment_based = models.BooleanField(
        _("Visiting by Appointment"), default=False
    )

    mon_open = models.TimeField(_("Opens on Monday"), blank=True, null=True)
    mon_break_close = models.TimeField(
        _("Break Starts on Monday"), blank=True, null=True
    )
    mon_break_open = models.TimeField(_("Break Ends on Monday"), blank=True, null=True)
    mon_close = models.TimeField(_("Closes on Monday"), blank=True, null=True)

    tue_open = models.TimeField(_("Opens on Tuesday"), blank=True, null=True)
    tue_break_close = models.TimeField(
        _("Break Starts on Tuesday"), blank=True, null=True
    )
    tue_break_open = models.TimeField(_("Break Ends on Tuesday"), blank=True, null=True)
    tue_close = models.TimeField(_("Closes on Tuesday"), blank=True, null=True)

    wed_open = models.TimeField(_("Opens on Wednesday"), blank=True, null=True)
    wed_break_close = models.TimeField(
        _("Break Starts on Wednesday"), blank=True, null=True
    )
    wed_break_open = models.TimeField(
        _("Break Ends on Wednesday"), blank=True, null=True
    )
    wed_close = models.TimeField(_("Closes on Wednesday"), blank=True, null=True)

    thu_open = models.TimeField(_("Opens on Thursday"), blank=True, null=True)
    thu_break_close = models.TimeField(
        _("Break Starts on Thursday"), blank=True, null=True
    )
    thu_break_open = models.TimeField(
        _("Break Ends on Thursday"), blank=True, null=True
    )
    thu_close = models.TimeField(_("Closes on Thursday"), blank=True, null=True)

    fri_open = models.TimeField(_("Opens on Friday"), blank=True, null=True)
    fri_break_close = models.TimeField(
        _("Break Starts on Friday"), blank=True, null=True
    )
    fri_break_open = models.TimeField(_("Break Ends on Friday"), blank=True, null=True)
    fri_close = models.TimeField(_("Closes on Friday"), blank=True, null=True)

    sat_open = models.TimeField(_("Opens on Saturday"), blank=True, null=True)
    sat_break_close = models.TimeField(
        _("Break Starts on Saturday"), blank=True, null=True
    )
    sat_break_open = models.TimeField(
        _("Break Ends on Saturday"), blank=True, null=True
    )
    sat_close = models.TimeField(_("Closes on Saturday"), blank=True, null=True)

    sun_open = models.TimeField(_("Opens on Sunday"), blank=True, null=True)
    sun_break_close = models.TimeField(
        _("Break Starts on Sunday"), blank=True, null=True
    )
    sun_break_open = models.TimeField(_("Break Ends on Sunday"), blank=True, null=True)
    sun_close = models.TimeField(_("Closes on Sunday"), blank=True, null=True)

    exceptions = MultilingualTextField(_("Exceptions for working hours"), blank=True)

    class Meta:
        abstract = True

    def has_opening_hours(self, skip_exceptions=False):
        success = bool(
            self.mon_open
            or self.tue_open
            or self.wed_open
            or self.thu_open
            or self.fri_open
            or self.sat_open
            or self.sun_open
        )
        if skip_exceptions:
            return success
        else:
            return success or self.exceptions

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
        if self.has_opening_hours(skip_exceptions=True):
            for key, val in WEEKDAYS:
                times.append(
                    {
                        "weekday": val,
                        "open": getattr(self, "%s_open" % key),
                        "break_close": getattr(self, "%s_break_close" % key),
                        "break_open": getattr(self, "%s_break_open" % key),
                        "close": getattr(self, "%s_close" % key),
                        "times": "-".join(
                            (
                                str(getattr(self, "%s_open" % key)),
                                str(getattr(self, "%s_break_close" % key)),
                                str(getattr(self, "%s_break_open" % key)),
                                str(getattr(self, "%s_close" % key)),
                            )
                        ),
                    }
                )
        return times


def FeesMixin(count=2,):
    """
    returns a mixin class for fee-related fields
    
    Parameters:
    
        count: the number of fees to create

    """

    _fees_count = count

    def has_fees(self):
        for i in range(_fees_count):
            if getattr(self, "fee%s_label" % i) and getattr(self, "fee%s_amount" % i):
                return True
        return False

    def get_fees(self, language=None):
        language = language or get_current_language()
        fees = []
        for i in range(_fees_count):
            label = getattr(self, "fee%d_label_%s" % (i, language), "") or getattr(
                self, "fee%d_label" % i, ""
            )
            amount = getattr(self, "fee%d_amount" % i)
            if label and amount is not None:
                fees.append(
                    {
                        "label": label,
                        "amount": format_currency(amount, "EUR", locale=language),
                    }
                )
        return fees

    class ModelWithFees(BaseModel):
        class Meta:
            abstract = True

    for index in range(count):
        fee_label_field = MultilingualCharField(
            _("Fee Label"), blank=True, max_length=40,
        )

        fee_amount_field = models.FloatField(_("Fee Amount"), blank=True, null=True,)

        ModelWithFees.add_to_class("fee%s_label" % index, fee_label_field)
        ModelWithFees.add_to_class("fee%s_amount" % index, fee_amount_field)

    registration_required_field = models.BooleanField(
        _("Registration Required"), default=False,
    )

    ModelWithFees.add_to_class("is_registration_required", registration_required_field)

    ModelWithFees.add_to_class("has_fees", has_fees)
    ModelWithFees.add_to_class("get_fees", get_fees)

    return ModelWithFees


### SIGNALS ###

signals.pre_save.connect(strip_whitespaces_from_charfields)
