# -*- coding: UTF-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.formsets import BaseFormSet

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ObjectChoiceField

from museumsportal.apps.permissions.models import RowLevelPermission, PerObjectGroup

def get_owners(obj_instance=None, obj_ct=None):
    perm_owners = []
    qs = User.objects.order_by("username")
    if qs:
        perm_owners.append(qs)
    qs = Group.objects.order_by("name")
    if qs:
        perm_owners.append(qs)
    if obj_instance:
        if not obj_ct:
            obj_ct = ContentType.objects.get_for_model(obj_instance)
        # add per object groups which are already selected
        pks = list(RowLevelPermission.objects.filter(
            owner_content_type__app_label="permissions",
            owner_content_type__model="perobjectgroup",
            content_type=obj_ct,
            object_id=obj_instance.pk,
            ).values_list("owner_object_id", flat=True))
        qs = PerObjectGroup.objects.filter(
            pk__in=pks,
            ).order_by("title")
        if qs:
            perm_owners.append(qs)
    return perm_owners


PERMISSION_STATUS_CHOICES = (
    ('inherited', _("Inherited")),
    ('allowed', _("Allowed")),
    ('disallowed', _("Disallowed")),
    )

def _get_permission_codename(action, opts):
    return u'%s_%s' % (action, opts.object_name.lower())

def _get_all_permissions(opts):
    "Returns (codename, name) for all permissions in the given opts."
    perms = []
    for action in ('change', 'delete'):
        perms.append((_get_permission_codename(action, opts), u'Can %s %s' % (action, opts.verbose_name_raw)))
    return perms + list(opts.permissions)

class RLPForm(dynamicforms.Form):
    owner = ObjectChoiceField(
        label=_("Owner"),
        required=True,
        default_text=_("Select an option"),
        )
    def __init__(self, obj_instance, *args, **kwargs):
        super(RLPForm, self).__init__(*args, **kwargs)
        self.obj_instance = obj_instance
        self.ct = ContentType.objects.get_for_model(obj_instance)
        self.fields['owner'].obj_list = get_owners(obj_instance, self.ct)
        self.original = self.initial.get("owner", None)
        for perm in _get_all_permissions(obj_instance._meta):
            initial="inherited"
            if 'owner' in self.initial:
                try:
                    rlp = RowLevelPermission.objects.get(
                        permission__codename=perm[0],
                        owner_content_type=ContentType.objects.get_for_model(self.initial['owner']),
                        owner_object_id=self.initial['owner'].pk,
                        content_type=self.ct,
                        object_id=obj_instance.pk,
                        )
                except RowLevelPermission.DoesNotExist:
                    pass
                else:
                    initial=["allowed", "disallowed"][rlp.negative]
            self.fields[perm[0]] = forms.ChoiceField(
                label=_(perm[1]),
                required=False,
                choices=PERMISSION_STATUS_CHOICES,
                initial=initial,
                )

class BaseRLPFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = []
            for rlp_owner in RowLevelPermission.objects.filter(
                content_type=ContentType.objects.get_for_model(self.obj_instance),
                object_id=self.obj_instance.pk,
                ).values_list("owner_content_type", "owner_object_id").distinct():
                owner = ContentType.objects.get(
                    pk=rlp_owner[0],
                    ).get_object_for_this_type(pk=rlp_owner[1])
                kwargs['initial'].append({
                    'owner': owner
                    })
        super(BaseRLPFormSet, self).__init__(*args, **kwargs)
    
    def _construct_forms(self):
        # instantiate all the forms and put them in self.forms
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(i, obj_instance=self.obj_instance))

    def _get_empty_form(self, **kwargs):
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix('__prefix__'),
            'empty_permitted': True,
            'obj_instance': self.obj_instance,
        }
        if self.data or self.files:
            defaults['data'] = self.data
            defaults['files'] = self.files
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, None)
        return form
    empty_form = property(_get_empty_form)

    def clean(self):
        """Checks that no two articles have the same title."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        owners = []
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            owner = form.cleaned_data.get('owner', None)
            if owner:
                if owner in owners:
                    raise forms.ValidationError, _("Each permission owner should be selected just once.")
                owners.append(owner)

    def save(self):
        obj_instance = self.obj_instance
        ct = ContentType.objects.get_for_model(obj_instance)
        for form in self.forms:
            cleaned = form.cleaned_data
            owner = cleaned.get('owner', None)
            if owner:
                owner_ct = ContentType.objects.get_for_model(owner)
                delete = self.can_delete and cleaned.get('DELETE', False)
                if delete:
                    RowLevelPermission.objects.filter(
                        owner_content_type=owner_ct,
                        owner_object_id=owner.pk,
                        content_type=ct,
                        object_id=obj_instance.pk,
                        ).delete()
                else:
                    for perm in _get_all_permissions(self.obj_instance._meta):
                        perm_name = perm[0]
                        if cleaned[perm_name] == "inherited":
                            RowLevelPermission.objects.filter(
                                permission__codename=perm_name,
                                owner_content_type=owner_ct,
                                owner_object_id=owner.pk,
                                content_type=ct,
                                object_id=obj_instance.pk,
                                ).delete()
                        else:
                            p = Permission.objects.get(codename=perm_name) 
                            rlp, created = RowLevelPermission.objects.get_or_create(
                                permission=p,
                                owner_content_type=owner_ct,
                                owner_object_id=owner.pk,
                                content_type=ct,
                                object_id=obj_instance.pk
                                )
                            rlp.negative = (cleaned[perm_name] == "disallowed")
                            rlp.save()

