# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.utils.functional import lazy
from django.conf import settings
from django.utils.timezone import now as tz_now

from base_libs.models import HierarchyMixin
from base_libs.models import SlugMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.middleware import get_current_language, get_current_user
from base_libs.utils.misc import get_related_queryset
from base_libs.utils.misc import get_website_url

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

Person = models.get_model("people", "Person")

verbose_name = _("Individual Relations")

INDIVIDUAL_RELATION_STATUSES = (
    ('inviting',    _("Inviting")),
    ('invited',     _("Invited")),
    ('denying',     _("Denying")),
    ('denied',      _("Denied")),
    ('blocking',    _("Blocking")),
    ('blocked',     _("Blocked")),
    ('confirmed',   _("Confirmed")),
    )

BACKWARD_INDIVIDUAL_RELATION_STATUSES = {
    'inviting':     'invited',
    'invited':      'inviting',
    'denying':      'denied',
    'denied':       'denying',
    'blocking':     'blocked',
    'blocked':      'blocking',
    'confirmed':    'confirmed',
    }

PERSON2PERSON_PERMISSION_MAP = {
    'display_birthday':     'can_see_birthday',
    'display_address':      'can_see_addresses',
    'display_phone':        'can_see_phones',
    'display_fax':          'can_see_faxes',
    'display_mobile':       'can_see_mobiles',
    'display_im':           'can_see_ims',
    }

# validators
def isValidToUser(field_data, all_data):
    from django.core.exceptions import ValidationError
    IndividualRelation.objects.all()
    if field_data == all_data['user']:
        raise ValidationError(_("You cannot set relationship with the same user."))
        
def isItUniqueTogether(field_data, all_data):
    from django.core.exceptions import ValidationError
    rel = None
    try:
        rel = IndividualRelation.objects.get(user=int(all_data.get("user")), to_user=int(all_data.get("to_user")))
    except:
        pass
    if rel:
        raise ValidationError(_("%(user)s has been already related to %(to_user)s.") % {'user': rel.user, 'to_user': rel.to_user})

class IndividualRelationType(MPTTModel, SlugMixin()):
    """
    Model for storing individual relation types

    The backwards relation type should point to an oposite relation type (might also point to itself), like:
     - "student" for "teacher/coach"
     - "teacher/coach" for "student"
     - "employer" for "employee"
     - "employee" for "employer"
     - "friend" for "friend"
    """
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
    backwards = TreeForeignKey("self", verbose_name=_("Backwards relationship"), blank=True, null=True, related_name="backwards_relation_set")

    objects = TreeManager()

    class Meta(HierarchyMixin.Meta):
        verbose_name = _("individual relation type")
        verbose_name_plural = _("individual relation types")
        ordering = ["tree_id", "lft"]
        
    class MPTTMeta:
        order_insertion_by = ['sort_order']
        
    def __unicode__(self):
        return self.title
    __unicode__.admin_order_field = 'path'
        
    def get_title(self, prefix="", postfix=""):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            IndividualRelationType.objects.insert_node(self, self.parent)
        super(IndividualRelationType, self).save(*args, **kwargs)


class IndividualRelationManager(models.Manager):
    
    def get_status(self, user_1, user_2):
        status = "none"
        if user_1 == user_2:
            status = "self"
        else:
            rels = self.filter(user=user_1, to_user=user_2)
            if rels:
                status = rels[0].status
        return status
        
    def invite(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            relation_types = []
            if "relation_types" in kwargs:
                relation_types = get_related_queryset(
                    self.model,
                    "relation_types",
                    ).filter(
                        id__in=kwargs.pop("relation_types")
                        )
            try:
                rel = self.get(user=user_1, to_user=user_2)
                rel.__dict__.update(kwargs)
            except self.model.DoesNotExist:
                rel = self.model(user=user_1, to_user=user_2, **kwargs)
            rel.status = "inviting"
            rel.save()
            if relation_types:
                rel.relation_types.clear()
                rel.relation_types.add(*relation_types)
                try:
                    backwards = self.get(user=user_2, to_user=user_1)
                except:
                    pass
                else:
                    backwards_relations = [
                        el.backwards
                        for el in relation_types
                        if el.backwards
                        ]
                    backwards.relation_types.add(*backwards_relations)
            individual_relation_requested(self.model, rel)
        
    def accept(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            relation_types = []
            if "relation_types" in kwargs:
                relation_types = get_related_queryset(
                    self.model,
                    "relation_types",
                    ).filter(
                        id__in=kwargs.pop("relation_types")
                        )
            try:
                rel = self.get(user=user_1, to_user=user_2)
                rel.__dict__.update(kwargs)
            except self.model.DoesNotExist:
                rel = self.model(user=user_1, to_user=user_2, **kwargs)
            rel.status = "confirmed"
            rel.save()
            if relation_types:
                rel.relation_types.clear()
                rel.relation_types.add(*relation_types)
            individual_relation_confirmed(self.model, rel)
        
    def edit(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            relation_types = []
            if "relation_types" in kwargs:
                relation_types = get_related_queryset(
                    self.model,
                    "relation_types",
                    ).filter(
                        id__in=kwargs.pop("relation_types")
                        )
            try:
                rel = self.get(user=user_1, to_user=user_2)
                rel.__dict__.update(kwargs)
            except self.model.DoesNotExist:
                rel = self.model(user=user_1, to_user=user_2, **kwargs)
            rel.status = "confirmed"
            rel.save()
            if relation_types:
                rel.relation_types.clear()
                rel.relation_types.add(*relation_types)
        
    def cancel_invitation(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            self.filter(user=user_1, to_user=user_2).delete()
            self.filter(user=user_2, to_user=user_1).delete()
        
    def deny(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            if "relation_types" in kwargs:
                del kwargs["relation_types"]
            try:
                rel = self.get(user=user_1, to_user=user_2)
                rel.__dict__.update(kwargs)
            except self.model.DoesNotExist:
                rel = self.model(user=user_1, to_user=user_2, **kwargs)
            rel.status = "denying"
            rel.save()
        
    def block(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            if "relation_types" in kwargs:
                del kwargs["relation_types"]
            try:
                rel = self.get(user=user_1, to_user=user_2)
                rel.__dict__.update(kwargs)
            except self.model.DoesNotExist:
                rel = self.model(user=user_1, to_user=user_2, **kwargs)
            rel.status = "blocking"
            rel.save()
        
    def unblock(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            self.filter(user=user_2, to_user=user_1).delete()
            self.filter(user=user_1, to_user=user_2).delete()
        
    def remove_relation(self, user_1, user_2, **kwargs):
        if user_1 != user_2:
            self.filter(user=user_1, to_user=user_2).delete()
            self.filter(user=user_2, to_user=user_1).delete()
        
class IndividualRelation(models.Model):
    """
    Model for storing user-to-user relations and setting user-to-user permissions.

    IndividualRelation fields:
    - id
    - user_id
    - to_user_id
    - timestamp
    - activation
    - status
    - display_birthday
    - display_address
    - display_phone
    - display_fax
    - display_mobile
    - display_im
    - message
    IndividualRelation ManyToMany relations:
    - relation_types
    
    Each individual relation has its **backwards** relation, for example,
    - "A is an employee of B and inviting to join the relation", then
    - "B tends to be an employer of A and is invited to join".
    A user cannot be related to himself. A user cannot be related to the same user from the same direction more than once.

    The multiple types of relation (relation_types) are defined as instances of the :model:`individual_relations.IndividualRelationType`.
    
    The statuses of relation are from the following list: 
    - inviting
    - invited
    - denying
    - denied
    - blocking
    - blocked
    - confirmed
    """
    user = models.ForeignKey(User, verbose_name=_("User #1"))
    to_user = models.ForeignKey(User, related_name="to_user", verbose_name=_("to user #2"))
    relation_types = TreeManyToManyField(IndividualRelationType, verbose_name=_("is"), blank=True)
    timestamp = models.DateTimeField(_("Created"), auto_now_add=True, editable=False, null=True) 
    activation = models.DateTimeField(_("Activated"), editable=False, null=True)
    status = models.CharField(_("Status of the user #1"), choices=INDIVIDUAL_RELATION_STATUSES, max_length=10)

    display_birthday = models.BooleanField(_("Display birthday to user #2"), default=True)
    display_address = models.BooleanField(_("Display address data to user #2"), default=True)
    display_phone = models.BooleanField(_("Display phone numbers to user #2"), default=True)
    display_fax = models.BooleanField(_("Display fax numbers to user #2"), default=True)
    display_mobile = models.BooleanField(_("Display mobile phones to user #2"), default=True)
    display_im = models.BooleanField(_("Display instant messengers to user #2"), default=True)

    message = models.TextField(_("Message from user #1 to user #2"), blank=True)
    
    objects = IndividualRelationManager()
    
    class Meta:
        unique_together = (("user", "to_user"),)
        verbose_name = _("individual relation")
        verbose_name_plural = _("individual relations")

    def __unicode__(self):
        return force_unicode(_("%(user1)s to %(user2)s") % {
            'user1': self.user.username,
            'user2': self.to_user.username,
            })

    # overriding methods
    def save(self, *args, **kwargs):
        is_new = not self.id
        if is_new:
            self._check_if_unique_together()
        self._set_activation()
        super(IndividualRelation, self).save()
        # managing backward relation
        try:
            backward = IndividualRelation.objects.get(
                user=self.to_user,
                to_user=self.user,
                )
        except IndividualRelation.DoesNotExist:
            backward = IndividualRelation(
                user=self.to_user,
                to_user=self.user,
                )
        backward.status = BACKWARD_INDIVIDUAL_RELATION_STATUSES[self.status]
        backward.activation = self.activation
        super(IndividualRelation, backward).save(*args, **kwargs)
        # managing permissions
        if not is_new:
            self._remove_existing_permissions()
            backward._remove_existing_permissions()
        if self.activation:
            self._add_proper_permissions()
        if backward.activation:
            backward._add_proper_permissions()
    save.alters_data = True

    def _post_save(self):
        backward = IndividualRelation.objects.filter(user=self.to_user, to_user=self.user)
        if backward:
            backward = backward[0]
            backward.relation_types.clear()
            for relation_type in self.relation_types.all():
                if relation_type.backwards:
                    backward.relation_types.add(relation_type.backwards)
    _post_save.alters_data = True
        
    def delete(self):
        super(IndividualRelation, self).delete()
        try:
            backward = IndividualRelation.objects.get(user=self.to_user, to_user=self.user)
            super(IndividualRelation, backward).delete()
        except:
            pass
    delete.alters_data = True

    # methods for list display
    def is_activated(self):
        return self.activation and _("Yes") or _("No")
    is_activated.short_description = _("Activated")

    # helper methods
    def _set_activation(self):
        is_active = (self.status == "confirmed")
        self.activation = is_active and (self.activation or tz_now()) or None

    def _check_if_unique_together(self):
        try:
            existing = IndividualRelation.objects.get(user=self.user, to_user=self.to_user)
        except:
            existing = None
        if existing:
            from django.core.exceptions import ValidationError
            raise ValidationError(_("%(user)s has been already related to %(to_user)s.") % {'user': existing.user, 'to_user': existing.to_user})

    def _remove_existing_permissions(self):
        from django.contrib.contenttypes.models import ContentType
        from jetson.apps.permissions.models import RowLevelPermission
        person = Person.objects.get(user=self.user)
        content_type = ContentType.objects.get_for_model(person)
        owner_content_type = ContentType.objects.get_for_model(self.to_user)
        for f_name, perm_codename in PERSON2PERSON_PERMISSION_MAP.items():
            try:
                permission = RowLevelPermission.objects.get(
                    content_type=content_type,
                    object_id=person.id,
                    owner_content_type=owner_content_type,
                    owner_object_id=self.to_user.id,
                    permission__codename=perm_codename,
                    )
            except:
                continue
            else:
                permission.delete()
    _remove_existing_permissions.alters_data = True
            
    def _add_proper_permissions(self):
        from jetson.apps.permissions.models import RowLevelPermission
        person = Person.objects.get(user=self.user)
        for f_name, perm_codename in PERSON2PERSON_PERMISSION_MAP.items():
            if getattr(self, f_name):
                RowLevelPermission.objects.create_row_level_permission(
                    model_instance=person,
                    owner=self.to_user,
                    permission=perm_codename,
                    )
    _add_proper_permissions.alters_data = True

### Additional methods to Person model
def add_methods_to_person():
    def _get_individual_relation_status(self, user=None):
        if not hasattr(self, "_get_individual_relation_status_cache"):
            user = get_current_user(user)
            status = IndividualRelation.objects.get_status(user, self.user)
            self._get_individual_relation_status_cache = status
        return self._get_individual_relation_status_cache
    def is_contact_addable(self, user=None):
        if not hasattr(self, "_is_contact_addable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_addable_cache = status in ("none", "denied", "denying")
        return self._is_contact_addable_cache

    def is_contact_editable(self, user=None):
        if not hasattr(self, "_is_contact_editable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_editable_cache = status == "confirmed"
        return self._is_contact_editable_cache

    def is_contact_removable(self, user=None):
        if not hasattr(self, "_is_contact_removable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_removable_cache = status == "confirmed"
        return self._is_contact_removable_cache
        
    def is_contact_blockable(self, user=None):
        if not hasattr(self, "_is_contact_blockable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_blockable_cache = status in ("invited", "none", "denied", "denying")
        return self._is_contact_blockable_cache
        
    def is_contact_unblockable(self, user=None):
        if not hasattr(self, "_is_contact_unblockable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_unblockable_cache = status == "blocking"
        return self._is_contact_unblockable_cache

    def is_contact_acceptable(self, user=None):
        if not hasattr(self, "_is_contact_acceptable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_acceptable_cache = status == "invited"
        return self._is_contact_acceptable_cache

    def is_contact_denyable(self, user=None):
        if not hasattr(self, "_is_contact_denyable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_denyable_cache = status == "invited"
        return self._is_contact_denyable_cache
        
    def is_contact_cancelable(self, user=None):
        if not hasattr(self, "_is_contact_cancelable_cache"):
            status = self._get_individual_relation_status(user)
            self._is_contact_cancelable_cache = status == "inviting"
        return self._is_contact_cancelable_cache
        
    def is_contactable(self, user=None):
        if not hasattr(self, "_is_contactable_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._is_contactable_cache = bool(
                user
                and user != self.user
                and status != "blocked"
                and user.email
                )
        return self._is_contactable_cache
        
    def is_addable_to_memos(self, user=None):
        if not hasattr(self, "_is_addable_to_memos_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._is_addable_to_memos_cache = user != self.user and status != "blocked"
        return self._is_addable_to_memos_cache

    def is_addable_to_favorites(self, user=None):
        if not hasattr(self, "_is_addable_to_favorites_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._is_addable_to_favorites_cache = user.is_authenticated() and user != self.user and status != "blocked"
        return self._is_addable_to_favorites_cache
    def are_contacts_displayed(self, user=None):
        # TODO: eliminate ambiguousness of the name "contact"
        if not hasattr(self, "_are_contacts_displayed_cache"):
            user = get_current_user(user)
            status = self._get_individual_relation_status(user)
            self._are_contacts_displayed_cache = bool(
                status != "blocked"
                and self.get_contacts()
                and (
                    self.is_address_displayed(user)
                    or self.is_phone_displayed(user)
                    or self.is_fax_displayed(user)
                    or self.is_mobile_displayed(user)
                    or self.is_email_displayed(user)
                    or self.is_im_displayed(user)
                    )
                ) or bool(
                    user
                    and user.has_perm("people.change_person", self)
                    )
        return self._are_contacts_displayed_cache
    def get_individual_relations(self):
        if not hasattr(self, "_individual_relations_cache"):
            self._individual_relations_cache = self.user.individualrelation_set.all()
        return self._individual_relations_cache

    def get_all_person_invitations(self):
        ir_db_table = IndividualRelation._meta.db_table
        qs = Person.objects.filter(
               user__individualrelation__to_user=self.user
             ).extra(
                 select={
                     'individualrelation_id': 
                         '%s.id' % ir_db_table,
                     'individualrelation_timestamp': 
                         '%s.timestamp' % ir_db_table,
                     'individualrelation_message': 
                         '%s.message' % ir_db_table,
                     'individualrelation_status': 
                         '%s.status' % ir_db_table,
                 },
             ).select_related().distinct().order_by('-individualrelation_timestamp')
        return qs
        
    def get_person_invitation_requests(self, status_filter=None):
        """
        invititaions to an indvivdual relationship you sent
        """
        if not status_filter:
            status_filter = ["invited", "denying"]
        
        qs = self.get_all_person_invitations()
        qs = qs.filter(
            user__individualrelation__status__in=status_filter,
            # for any reason, it does not work loke this. But WHY??
            #user__to_user__status__in=status_filter,
            )
        
        return qs

    def get_person_invitation_requested(self, status_filter=None):
        """
        invititaions to an indvivdual relationship which has to be confirmed
        """
        
        if not status_filter:
            status_filter = ["inviting", "denied"]
        
        qs = self.get_all_person_invitations()
        qs = qs.filter(
            user__individualrelation__status__in=status_filter,
            # for any reason, it does not work loke this. But WHY??
            #user__to_user__status__in=status_filter,
            )
        return qs
    Person._get_individual_relation_status = _get_individual_relation_status
    Person.is_contact_addable = is_contact_addable
    Person.is_contact_editable = is_contact_editable
    Person.is_contact_removable = is_contact_removable
    Person.is_contact_blockable = is_contact_blockable
    Person.is_contact_unblockable = is_contact_unblockable
    Person.is_contact_acceptable = is_contact_acceptable
    Person.is_contact_denyable = is_contact_denyable
    Person.is_contact_cancelable = is_contact_cancelable
    Person.is_contactable = is_contactable
    Person.is_addable_to_memos = is_addable_to_memos
    Person.is_addable_to_favorites = is_addable_to_favorites
    Person.are_contacts_displayed = are_contacts_displayed
    Person.get_individual_relations = get_individual_relations
    Person.get_all_person_invitations = get_all_person_invitations
    Person.get_person_invitation_requests = get_person_invitation_requests
    Person.get_person_invitation_requested = get_person_invitation_requested
    
add_methods_to_person()

# Notify appropriate users about relation requests
def individual_relation_requested(sender, instance, **kwargs):
    from jetson.apps.notification import models as notification
    
    notification.send(
        instance.to_user,
        "individual_relation_requested",
        {
            "object_creator_url": instance.user.profile.get_absolute_url(),
            "object_creator_title": instance.user.profile.get_title(),
            "object_description": instance.message,
            "object_url": "%speople/requested/?by-status=pending" % get_website_url()
            },
        )

# Notify appropriate users about relation confirmations
def individual_relation_confirmed(sender, instance, **kwargs):
    from jetson.apps.notification import models as notification
    
    notification.send(
        instance.to_user,
        "individual_relation_confirmed",
        {
            "object_creator_url": instance.user.profile.get_absolute_url(),
            "object_creator_title": instance.user.profile.get_title(),
            "object_description": instance.message,
            },
        )

