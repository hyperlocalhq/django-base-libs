# -*- coding: UTF-8 -*-
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_unicode

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.middleware import get_current_user

image_mods = models.get_app("image_mods")

from kb.apps.groups_networks.models import PersonGroup
from kb.apps.site_specific.models import ContextItem

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type
PREFIX_JS = 'JS_'  # Job Sector

ACCESS_TYPE_CHOICES = (
    ("", _("- Please select -")),
    ("public", _("Public")),
    ("private", _("Private")),
    ("secret", _("Secret")),
)

GROUP_TYPE_CHOICES = [
    ('', _("- Please select -"))
] + [
    (str(el.id), el.get_title())
    for el in get_related_queryset(PersonGroup, 'group_type')
]

MEMBERSHIP_OPTION_CHOICES = (
    ('', _("- Please select -")),
    ("invite", _("By invitation only")),
    ("invite_or_confirm", _("By approved request or by invitation")),
    ("anyone", _("Anyone can join")),
)
PREFERRED_LANGUAGE_CHOICES = XChoiceList(
    get_related_queryset(PersonGroup, 'preferred_language'),
    null_choice_text=_("- Please select -"),
)

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE


# TODO: each form could be ModelForm. Each formset could be ModelFormSet.
# noinspection PyClassHasNoInit
class DescriptionForm(dynamicforms.Form):
    description_en = forms.CharField(
        label=_("Description (English)"),
        required=False,
        widget=forms.Textarea(),
    )
    description_de = forms.CharField(
        label=_("Description (German)"),
        required=False,
        widget=forms.Textarea(),
    )

    def __init__(self, group, index, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.group = group
        self.index = index
        if not args and not kwargs:  # if nothing is posted
            self.fields['description_en'].initial = group.description_en
            self.fields['description_de'].initial = group.description_de

    def save(self):
        group = self.group
        group.description_en = self.cleaned_data['description_en']
        group.description_de = self.cleaned_data['description_de']
        group.save()
        return group

    def get_extra_context(self):
        return {}

class AvatarForm(dynamicforms.Form):
    media_file = ImageField(
        label=_("Photo"),
        help_text=_(
            "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
        required=False,
        min_dimensions=MIN_LOGO_SIZE,
    )

    def __init__(self, group, index, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.group = group
        self.index = index

    def save(self):
        group = self.group
        if "media_file" in self.files:
            media_file = self.files['media_file']
            image_mods.FileManager.save_file_for_object(
                group,
                media_file.name,
                media_file,
                subpath="avatar/"
            )
        return group

    def get_extra_context(self):
        return {}

class DetailsForm(dynamicforms.Form):
    group_type = forms.ChoiceField(
        required=True,
        choices=GROUP_TYPE_CHOICES,
        label=_("Group type"),
    )

    access_type = forms.ChoiceField(
        required=True,
        choices=ACCESS_TYPE_CHOICES,
        label=_("Security"),
    )

    institution = forms.ChoiceField(
        required=False,
        choices=[],
        label=_("Attach to profile"),
    )

    membership_options = forms.ChoiceField(
        required=True,
        choices=MEMBERSHIP_OPTION_CHOICES,
        label=_("Membership"),
    )

    main_language = forms.ChoiceField(
        required=True,
        choices=PREFERRED_LANGUAGE_CHOICES,
        label=_("Main language"),
    )

    def __init__(self, group, index, *args, **kwargs):
        super(DetailsForm, self).__init__(*args, **kwargs)
        self.group = group
        self.index = index
        user = get_current_user()
        person = user.profile
        INSTITUTION_CHOICES = [("", "---------")]
        INSTITUTION_CHOICES.extend([(str(el.id), force_unicode(el))
                                    for el in person.get_institutions()
                                    ])
        self.fields['institution'].choices = self.fields['institution'].widget.choices = INSTITUTION_CHOICES
        if not args and not kwargs:  # if nothing is posted
            self.fields['group_type'].initial = group.group_type_id
            self.fields['access_type'].initial = group.access_type_id
            self.fields['institution'].initial = group.organizing_institution_id
            self.fields['main_language'].initial = group.preferred_language_id
            if group.is_by_invitation and group.is_by_confirmation:
                self.fields['membership_options'].initial = "invite_or_confirm"
            elif group.is_by_invitation:
                self.fields['membership_options'].initial = "invite"
            else:
                self.fields['membership_options'].initial = "anyone"

    def save(self):
        group = self.group
        cleaned = self.cleaned_data
        group.group_type_id = cleaned['group_type']
        group.access_type_id = cleaned['access_type']
        group.organizing_institution_id = cleaned.get('institution', None)
        group.preferred_language = get_related_queryset(
            PersonGroup,
            "preferred_language"
        ).get(
            pk=cleaned.get('main_language', ""),
        )
        membership_options = cleaned.get('membership_options', 'anyone')
        group.is_by_invitation = membership_options in ("invite", "invite_or_confirm")
        group.is_by_confirmation = membership_options == "invite_or_confirm"
        group.save()
        return group

    def get_extra_context(self):
        return {}

class CategoriesForm(dynamicforms.Form):
    choose_creative_sectors = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
        required=False,
    )

    def clean_choose_creative_sectors(self):
        data = self.data
        el_count = 0
        for el in self.creative_sectors.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(_("Please choose at least one creative sector."))
        return True

    choose_context_categories = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
        required=False,
    )

    def clean_choose_context_categories(self):
        data = self.data
        el_count = 0
        for el in self.context_categories.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(_("Please choose at least one context category."))
        return True

    choose_object_types = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
            }
        ),
        required=False,
    )

    def clean_choose_object_types(self):
        data = self.data
        el_count = 0
        for el in self.object_types.values():
            if el['field_name'] in data:
                el_count += 1
        if not el_count:
            raise forms.ValidationError(_("Please choose at least one object type."))
        return True

    def __init__(self, group, index, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)
        self.group = group
        self.creative_sectors = {}
        for item in get_related_queryset(PersonGroup, "creative_sectors"):
            self.creative_sectors[item.sysname] = {
                'id': item.id,
                'field_name': PREFIX_CI + str(item.id),
            }
        self.context_categories = {}
        for item in get_related_queryset(PersonGroup, "context_categories"):
            self.context_categories[item.sysname] = {
                'id': item.id,
                'field_name': PREFIX_BC + str(item.id),
            }
        for s in self.creative_sectors.values():
            self.fields[s['field_name']] = forms.BooleanField(
                required=False
            )
        for el in group.get_creative_sectors():
            for ancestor in el.get_ancestors(include_self=True):
                self.fields[PREFIX_CI + str(ancestor.id)].initial = True
        for c in self.context_categories.values():
            self.fields[c['field_name']] = forms.BooleanField(
                required=False
            )
        for el in group.get_context_categories():
            for ancestor in el.get_ancestors(include_self=True):
                self.fields[PREFIX_BC + str(ancestor.id)].initial = True

    def save(self, *args, **kwargs):
        group = self.group
        cleaned = self.cleaned_data
        selected_cs = {}
        for item in get_related_queryset(PersonGroup, "creative_sectors"):
            if cleaned.get(PREFIX_CI + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cs:
                        del (selected_cs[ancestor.id])
                # add current
                selected_cs[item.id] = item
        group.creative_sectors.clear()
        group.creative_sectors.add(*selected_cs.values())

        selected_cc = {}
        for item in get_related_queryset(PersonGroup, "context_categories"):
            if cleaned.get(PREFIX_BC + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cc:
                        del (selected_cc[ancestor.id])
                # add current
                selected_cc[item.id] = item
        group.context_categories.clear()
        group.context_categories.add(*selected_cc.values())
        ContextItem.objects.update_for(group)
        return group

    def get_extra_context(self):
        return {}

profile_forms = {
    'description': DescriptionForm,
    'avatar': AvatarForm,
    'details': DetailsForm,
    'categories': CategoriesForm,
}
