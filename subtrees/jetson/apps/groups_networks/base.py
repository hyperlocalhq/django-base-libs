# -*- coding: UTF-8 -*-
import os
import re
from datetime import datetime

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import FieldDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.conf import settings
from django.utils.timezone import now as tz_now
from django.apps import AppConfig

from base_libs.middleware import get_current_language
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import get_translation
from base_libs.utils.betterslugify import better_slugify
from base_libs.models.query import ExtendedQuerySet
from base_libs.models.models import UrlMixin
from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import SlugMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField # for south

from filebrowser.fields import FileBrowseField

from jetson.apps.i18n.models import Language
from jetson.apps.structure.models import Term
from jetson.apps.structure.models import ContextCategory
from jetson.apps.permissions.models import RowLevelPermission
from jetson.apps.permissions.models import PerObjectGroup
from jetson.apps.image_mods.models import FileManager

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

verbose_name = _("Groups & Networks")

### PersonGroup class ###

ACCESS_TYPE_CHOICES = (
    ("public", _("Public")),
    ("private", _("Private")),
    ("secret", _("Secret")),
    )

STATUS_CHOICES = (
    ('draft', _("Draft")),
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
    )

PG_PERMISSIONS = (
    ('can_invite',          'Can invite users'),
    ('can_confirm',         'Can confirm memberships'),
    ('can_change_members',  'Can change members'),
    ('can_see_members',     'Can see members'),
    ('can_see_roles',       'Can see roles of each member'),
    )

PG_ROLE_CHOICES = (
    ('owners',      _('Owner')),
    ('moderators',  _('Moderator')),
    ('members',     _('Member')),
    )


PG_ROLE_PERMISSIONS = {
    'owners': (
        'can_change_members',
        'can_invite',
        'can_confirm',
        'can_see_members',
        'can_see_roles',
        'change_persongroup',
        'delete_persongroup',
        ),
    'moderators': (
        'can_invite',
        'can_confirm',
        'can_see_members',
        'can_see_roles',
        ),
    'members': (
        'can_see_members',
        'can_see_roles',
        ),
    }

URL_ID_PERSONGROUP = getattr(settings, "URL_ID_PERSONGROUP", "group")
URL_ID_PERSONGROUPS = getattr(settings, "URL_ID_PERSONGROUPS", "groups")
DEFAULT_LOGO_4_PERSONGROUP = getattr(
    settings,
    "DEFAULT_LOGO_4_PERSONGROUP",
    "%simg/website/placeholder/persongroup.png" % settings.MEDIA_URL,
    )
DEFAULT_FORM_LOGO_4_PERSONGROUP = getattr(
    settings,
    "DEFAULT_FORM_LOGO_4_PERSONGROUP",
    "%simg/website/placeholder/persongroup_f.png" % settings.MEDIA_URL,
    )
DEFAULT_SMALL_LOGO_4_PERSONGROUP = getattr(
    settings,
    "DEFAULT_SMALL_LOGO_4_PERSONGROUP",
    "%simg/website/placeholder/persongroup_s.png" % settings.MEDIA_URL,
    )

class GroupType(MPTTModel, SlugMixin()):
    sort_order = models.IntegerField(
        _("sort order"), 
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
       'self',
       #related_name="%(class)s_children",
       related_name="child_set",
       blank=True,
       null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)

    objects = TreeManager()

    class Meta:
        verbose_name = _("group type")
        verbose_name_plural = _("group types")
        ordering = ["tree_id", "lft"]
        
    class MPTTMeta:
        order_insertion_by = ['sort_order']
        
    def __unicode__(self):
        return self.title

    def get_title(self, prefix="", postfix=""):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            GroupType.objects.insert_node(self, self.parent)
        super(GroupType, self).save(*args, **kwargs)


class PersonGroupManager(models.Manager):
    
    def get_queryset(self):
        """
        we need an extended queryset for advanced order_by options
        """
        return ExtendedQuerySet(self.model)
    
    
    def _get_title_fields(self, prefix=''):
        language = get_current_language()
        return ["%stitle" % prefix]
        
    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                self._get_title_fields(),
                ),
            'creation_date_desc': (
                2,
                _('Creation date'),
                ['-creation_date'],
                ),   
            }        
        return sort_order_mapper
    def latest_published(self):
        return self.filter(
            status="published",
            ).order_by("-creation_date")

PersonGroupObjectRelation = ObjectRelationMixin(
    limit_content_type_choices_to = {
        "model__in": ("address", "institution")
        },
    )

class PersonGroupBase(CreationModificationDateMixin, PersonGroupObjectRelation, UrlMixin, SlugMixin(verbose_name=_("Slug for URIs"), max_length=255, unique=True, separator="-")):
    """
    Model for storing groups of people
    
    PersonGroup fields:
    - id
    - content_type_id
    - object_id
    - title
    - title2
    - slug
    - description_en
    - description_de
    - group_type_id
    - organizing_institution_id
    - access_type
    - is_by_invitation
    - is_by_confirmation
    - creation_date
    - modified_date
    - preferred_language_id
    - status
    
    PersonGroup ManyToMany fields:
    - context_categories
    
    """
    
    title = models.CharField(_("Title"), max_length=255)
    title2 = models.CharField(_("Title 2"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    group_type = TreeForeignKey(GroupType, verbose_name=_("Group Type"), related_name="type_groups")

    organizing_institution = models.ForeignKey("institutions.Institution", verbose_name=_("Organizing institution"), blank=True, null=True)

    access_type = models.CharField(_("Access Type"), max_length=10, choices=ACCESS_TYPE_CHOICES, default="secret")

    is_by_invitation = models.BooleanField(_("Membership by Invitation"), default=False) 
    is_by_confirmation = models.BooleanField(_("Membership by Confirmation"), default=False) 

    context_categories = TreeManyToManyField(ContextCategory, verbose_name=_("Context categories"), limit_choices_to={'is_applied4persongroup': True}, blank=True)

    preferred_language = models.ForeignKey(Language, verbose_name=_("Preferred Language"), limit_choices_to={'display': True}, null=True, blank=True)

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="draft")

    image = FileBrowseField(_('Image'),max_length=255, directory="/%s/" % URL_ID_PERSONGROUPS, extensions=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True)

    perobjectgroup_set = generic.GenericRelation(PerObjectGroup)
    
    row_level_permissions = True
    grant_change_row_level_perm=True
    grant_delete_row_level_perm=True

    objects = PersonGroupManager()

    class Meta:
        abstract = True
        verbose_name = _("Group of People")
        verbose_name_plural = _("Groups of People")
        permissions = PG_PERMISSIONS

    def __unicode__(self):
        return force_unicode(self.title)

    def get_title(self, language=None):
        return self.title
    
    def _title_getter(self):
        return self.title

    def _title_setter(self, val):
        pass

    title_en = property(_title_getter, _title_setter)
    title_de = property(_title_getter, _title_setter)
    
    def get_description(self, language=None):
        language = language or get_current_language()
        return mark_safe(getattr(self, "description_%s" % language, "") or self.description)
    
    def get_absolute_url(self):
        from django.conf import settings
        return "%s%s/%s/" % (get_website_url(), URL_ID_PERSONGROUP, self.slug)
        
    def get_url_path(self):
        from django.conf import settings
        return "/%s/%s/" % (URL_ID_PERSONGROUP, self.slug)
        
    def get_slug(self):
        return self.slug
        
    def save(self, *args, **kwargs):
        is_new = not self.id
        
        if self.access_type=="secret":
            if self.status == "published":
                self.status = "not_listed"
        else:
            self.status = "published"
        
        super(PersonGroupBase, self).save(*args, **kwargs)
        if is_new:
            self.create_permission_roles()
    save.alters_data = True
    
    def create_permission_roles(self):
        owners_role = None
        for role_name, permissions in PG_ROLE_PERMISSIONS.items():
            role = PerObjectGroup(
                sysname=role_name,
                )
            role.title_en=get_translation(role_name.title(), language="en")
            role.title_de=get_translation(role_name.title(), language="de")
            # TODO: don't limit translations just to en and de.
            # Iterate through settings.LANGUAGES
            role.content_object = self
            role.save()
            for perm_name in permissions:
                RowLevelPermission.objects.create_row_level_permission(
                    model_instance=self,
                    owner=role,
                    permission=perm_name,
                    )
            if "owners" == role_name:
                owners_role = role
        if self.content_object and owners_role:
            RowLevelPermission.objects.create_default_row_permissions(
                model_instance=self.content_object,
                owner=owners_role,
                )
    create_permission_roles.alters_data = True
        
    def delete(self, *args, **kwargs):
        PerObjectGroup.objects.filter(
            object_id = self.pk,
            content_type = ContentType.objects.get_for_model(self),
            ).delete()
        FileManager.delete_file(self.get_filebrowser_dir())
        super(PersonGroupBase, self).delete(*args, **kwargs)
    delete.alters_data = True
        
    def get_object_permission_roles(self):
        """
        Returns the default owners of this object for permission manipulation
        """
        allowed_groups = [self.perobjectgroup_set.get(sysname__startswith="owners"),
                          self.perobjectgroup_set.get(sysname__startswith="moderators")]
        return allowed_groups
        
    def get_context_categories(self):
        return self.context_categories.all()
        
    def get_object_types(self):
        return self.group_type and [self.group_type] or []
        
    def get_all(self):
        from django.apps import apps
        Person = apps.get_model("people", "Person")
        qs = Person.objects.filter(
            user__groupmembership__person_group=self
            ).extra(
                select={
                    'membership_id':
                        'groups_networks_groupmembership.id',
                    'membership_role':
                        'groups_networks_groupmembership.role',
                    'membership_title':
                        'groups_networks_groupmembership.title',
                    'membership_title_de':
                        'groups_networks_groupmembership.title_de',
                    'membership_inviter_id':
                        'groups_networks_groupmembership.inviter_id',
                    'membership_is_accepted':
                        'groups_networks_groupmembership.is_accepted',
                    'membership_is_blocked':
                        'groups_networks_groupmembership.is_blocked',
                    'membership_confirmer_id':
                        'groups_networks_groupmembership.confirmer_id',
                    'membership_timestamp':
                        'groups_networks_groupmembership.timestamp',
                    'membership_activation':
                        'groups_networks_groupmembership.activation',
                    },
                ).select_related()
        return qs
            
    def get_all_members(self):
        """ Get all activated members including admins and moderators """
        members = self.get_all().extra(
            where=(
                '(groups_networks_groupmembership.activation IS NOT NULL)',
                )
            )
        members.sort_order_map = None
        members.sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                ['auth_user.last_name'],
                ),
            'activation_desc': (
                6,
                _('Activation date'),
                ['-membership_activation'],
                ),
            }
        return members
        
    def get_owners(self):
        """ get all admins """
        members = self.get_all_members().extra(
            where=(
                "(groups_networks_groupmembership.role = 'owners')",
            )
        )
        members.sort_order_map = None
        members.sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                ['auth_user.last_name'],
                ),
            'activation_desc': (
                2,
                _('Activation date'),
                ['-membership_activation'],
                ),
            }
        return members
        
    def get_moderators(self):
        """ get all moderators """
        members = self.get_all_members().extra(
            where=(
                '(groups_networks_groupmembership.role = "moderators")',
                )
            )
        members.sort_order_map = None
        members.sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                ['auth_user.last_name'],
                ),
            'activation_desc': (
                2,
                _('Activation date'),
                ['-membership_activation'],
                ),
            }
        return members
        
    def get_members(self):
        """ get all members which are neither admins nor moderators """
        members = self.get_all_members().extra(
            where=(
                '(groups_networks_groupmembership.role = "members")',
                )
            )
        members.sort_order_map = None
        members.sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                ['auth_user.last_name'],
                ),
            'activation_desc': (
                2,
                _('Activation date'),
                ['-membership_activation'],
                ),
            }
        return members
        
    def get_invited(self):
        """ get candidates to members who haven't accepted their invitations """
        people = self.get_all().extra(
            where=(
                '(groups_networks_groupmembership.inviter_id IS NOT NULL)',
                '(groups_networks_groupmembership.is_accepted = 0)',
                '(groups_networks_groupmembership.activation IS NULL)',
                )
            )
        people.sort_order_map = None
        people.sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                ['auth_user.last_name'],
                ),
            'request_desc': (
                2,
                _('Request date'),
                ['-membership_timestamp'],
                ),
            }
        return people
        
    def get_unconfirmed(self):
        """ get candidates to members who haven't been confirmed by group owners"""
        people = self.get_all().extra(
            where=(
                '(groups_networks_groupmembership.is_accepted = 1)',
                '(groups_networks_groupmembership.confirmer_id IS NULL)',
                '(groups_networks_groupmembership.activation IS NULL)',
                )
            )
        people.sort_order_map = None
        people.sort_order_mapper = {
            'alphabetical_asc': (
                1,
                _('Alphabetical'),
                ['auth_user.last_name'],
                ),
            'request_desc': (
                2,
                _('Request date'),
                ['-membership_timestamp'],
                ),
            }
        return people
        
    def is_persongroup(self):
        return True
        
    def are_members_shown(self):
        from base_libs.middleware import get_current_user
        user = get_current_user()
        return bool(
            user.has_perm("groups_networks.change_persongroup", self)
            or self.get_all_members().filter(user=user)
            or self.access_type == "public"
            )

    def is_forum_shown(self):
        from base_libs.middleware import get_current_user
        user = get_current_user()
        return bool(
            user and (user.has_perm("groups_networks.change_persongroup", self)
            or self.get_all_members().filter(user=user))
            or self.access_type == "public"
            )

    def is_membership_requestable(self, user=None):
        user = get_current_user(user)
        return bool(
            (self.is_by_confirmation or not (
                self.is_by_invitation
                or self.is_by_confirmation
                ))
            and not self.get_all().filter(user=user)
            )

    def is_member_request_cancelable(self, user=None):
        user = get_current_user(user)
        return bool(
            self.get_unconfirmed().filter(user=user)
            )

    def is_member_request_acceptable(self, user=None):
        current_user = get_current_user()
        return bool(
            current_user != user
            and self.get_unconfirmed().filter(user=user)
            and self.get_owners().filter(user=current_user)
            )
        
    def is_member_request_denyable(self, user=None):
        current_user = get_current_user()
        return bool(
            current_user != user
            and self.get_unconfirmed().filter(user=user)
            and self.get_owners().filter(user=current_user)
            )

    def is_member_invitable(self, user=None):
        if not user:
            return False
        current_user = get_current_user()
        return bool(
            (self.is_by_invitation or not (
                self.is_by_invitation
                or self.is_by_confirmation
                ))
            and self.get_owners().filter(user=current_user)
            and not self.get_all().filter(user=user)
            )

    def are_members_invitable(self, user=None):
        user = get_current_user(user)
        return bool(
            (self.is_by_invitation or not (
                self.is_by_invitation
                or self.is_by_confirmation
                ))
            and self.get_owners().filter(user=user)
            )

    def is_member_invitation_cancelable(self, user=None):
        if not user:
            return False
        current_user = get_current_user()
        return bool(
            self.get_owners().filter(user=current_user)
            and self.get_invited().filter(user=user)
            )
        
    def is_member_invitation_acceptable(self, user=None):
        user = get_current_user(user)
        return bool(
            (self.is_by_invitation or not (
                self.is_by_invitation
                or self.is_by_confirmation
                ))
            and self.get_invited().filter(user=user)
            )

    def is_member_invitation_denyable(self, user=None):
        user = get_current_user(user)
        return bool(
            (self.is_by_invitation or not (
                self.is_by_invitation
                or self.is_by_confirmation
                ))
            and self.get_invited().filter(user=user)
            )

    def is_membership_editable(self, user=None):
        user = get_current_user(user)
        return bool(
            self.get_all_members().filter(user=user)
            and not self.get_owners().filter(user=user)
            )
        
    def is_membership_removable(self, user=None):
        user = get_current_user(user)
        return bool(
            self.get_all_members().filter(user=user)
            and not self.get_owners().filter(user=user)
            )

    def is_member_removable(self, user=None):
        if not user:
            return False
        current_user = get_current_user()
        return bool(
            user != current_user
            and self.get_owners().filter(user=current_user)
            and self.get_all_members().filter(user=user)
            )

    def is_addable_to_memos(self, user=None):
        user = get_current_user(user)
        return bool(
            user.has_perm("groups_networks.change_persongroup", self)
            or self.get_all_members().filter(user=user)
            or self.access_type in ("public", "private",)
            )

    def is_addable_to_favorites(self, user=None):
        user = get_current_user(user)
        return bool(
            user.has_perm("groups_networks.change_persongroup", self)
            or self.get_all_members().filter(user=user)
            or self.access_type in ("public", "private",)
            )

    def get_filebrowser_dir(self):
        return "%s/%s/" % (
            URL_ID_PERSONGROUPS,
            self.slug,
            )

class GroupMembershipBase(models.Model):
    """
    Model for defining the members of groups of people (:model:`groups_networks.PersonGroup`)
    
    GroupMembership fields:
    - id
    - user_id
    - person_group_id
    - role
    - title_en
    - title_de
    - inviter_id
    - is_accepted
    - is_blocked
    - is_contact_person
    - confirmer_id
    - timestamp
    - activation
    """
    
    # a foreign key to PersonGroup will be added when PersonGroup is created
    person_group = models.ForeignKey(
        "groups_networks.PersonGroup",
        verbose_name=_("Group of People"),
        )

    user = models.ForeignKey(User, verbose_name=_("User"))
    role = models.CharField(_("Role"), choices=PG_ROLE_CHOICES, max_length=30, default='members') 
    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    
    inviter = models.ForeignKey(User, related_name="group_inviter", verbose_name=_("Inviter"), null=True, blank=True)
    is_accepted = models.BooleanField(_("Accepted by user"), default=False)
    is_blocked  = models.BooleanField(_("Blocked"), default=False)
    is_contact_person  = models.BooleanField(_("Contact Person"), default=False)
    confirmer = models.ForeignKey(User, related_name="group_confirmer", verbose_name=_("Confirmer"), null=True, blank=True)

    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True, editable=False, null=True) 
    activation = models.DateTimeField(_("Activated"), editable=False, null=True) 

    class Meta:
        abstract = True
        verbose_name = _("Membership at a Group of People")
        verbose_name_plural = _("Memberships at Groups of People")

    def get_title(self, language=None):
        language = language or get_current_language()
        return force_unicode(getattr(self, "title_%s" % language, "") or self.title)
    get_title = lazy(get_title, unicode)
        
    def __unicode__(self):
        return force_unicode("%s @ %s" % (self.user, self.person_group))
        
    # overriding methods
    
    def save(self, *args, **kwargs):
        is_new = not self.id
        if not is_new:
            self._remove_existing_roles()
        self._set_activation()
        if not self.title_de and hasattr(self, "title_en"):
            self.title_de = self.title_en
        super(GroupMembershipBase, self).save(*args, **kwargs)
        if self.activation:
            self._add_proper_role()
    save.alters_data = True

    def delete(self, *args, **kwargs):
        self._remove_existing_roles()
        super(GroupMembershipBase, self).delete(*args, **kwargs)
    delete.alters_data = True

    # helper methods
    
    def _remove_existing_roles(self):
        for role in PerObjectGroup.objects.filter(
            object_id=self.person_group.id,
            content_type=ContentType.objects.get_for_model(self.person_group),
            ):
            self.user.perobjectgroup_set.remove(role)
    _remove_existing_roles.alters_data = True
            
    def _add_proper_role(self):
        role = PerObjectGroup.objects.get(
            sysname__startswith=self.role,
            object_id=self.person_group.id,
            content_type=ContentType.objects.get_for_model(self.person_group),
            )
        self.user.perobjectgroup_set.add(role)
    _add_proper_role.alters_data = True

    def _set_activation(self):
        is_active = self.is_accepted
        if self.person_group.is_by_invitation and self.person_group.is_by_confirmation:
            is_active = is_active and (self.inviter or self.confirmer)
        elif self.person_group.is_by_invitation:
            is_active = is_active and self.inviter
        elif self.person_group.is_by_confirmation:
            is_active = is_active and self.confirmer
        self.activation = is_active and (self.activation or tz_now()) or None
    _set_activation.alters_data = True
