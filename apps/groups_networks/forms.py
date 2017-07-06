# -*- coding: UTF-8 -*-
import re

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode, smart_str
from django.http import Http404
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.apps import apps

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField

image_mods = models.get_app("image_mods")

from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_related_queryset,get_unique_value, XChoiceList
from base_libs.utils.crypt import cryptString
from base_libs.utils.betterslugify import better_slugify
from jetson.apps.mailing.views import Recipient, send_email_using_template
from jetson.apps.location.models import Address
from jetson.apps.optionset.models import IndividualLocationType, InstitutionalLocationType, PhoneType

groups_networks_models = apps.get_app("groups_networks")
PersonGroup = groups_networks_models.PersonGroup
GroupMembership = groups_networks_models.GroupMembership
URL_ID_PERSONGROUP = groups_networks_models.URL_ID_PERSONGROUP
URL_ID_PERSONGROUPS = groups_networks_models.URL_ID_PERSONGROUPS

Person = models.get_model("people", "Person")
Institution = models.get_model("institutions", "Institution")

NULL_PREFIX_CHOICES = XChoiceList(get_related_queryset(Person, 'prefix'))

PG_ROLE_CHOICES = GroupMembership._meta.get_field('role').get_choices()
PG_ROLE_CHOICES[0] = ('', _("- Please select -"))

ACCESS_TYPE_CHOICES = (
    ("", _("- Please select -")),
    ("public", _("Public")),
    ("private", _("Private")),
    ("secret", _("Secret")),
    )

GROUP_TYPE_CHOICES = XChoiceList(
    get_related_queryset(PersonGroup, 'group_type').exclude(slug="institutional"),
    null_choice_text=_("- Please select -"),
    )

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

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_' # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_' # Context Category aka Business Category
PREFIX_OT = 'OT_' # Object Type
PREFIX_LT = 'LT_' # Location Type

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100,100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE

class GroupMembershipForm(dynamicforms.Form):
    title_en = forms.CharField(
        required=False,
        label=_("Title (English)"),
        )
    title_de = forms.CharField(
        label=_("Title (German)"),
        required=False,
        )    
    def __init__(self, relation_action, user, group, **kwargs):
        super(GroupMembershipForm, self).__init__(**kwargs)
        fields = self.fields
        self.relation_action = relation_action
        self.user = user
        self.group = group
        try:
            person = group.get_all().get(
                user=user
                )
        except:
            pass
        else:
            self.fields['title_en'].initial = person.membership_title_en
            self.fields['title_de'].initial = person.membership_title_de
    
    def save(self):
        cleaned = self.cleaned_data
        action = self.relation_action
        current_user = get_current_user()
        user = self.user
        group = self.group
        
        try:
            membership = group.groupmembership_set.get(user=user)
        except:
            membership = group.groupmembership_set.create(
                user=user,
                is_accepted=True
                )
        
        if action=="edit":
            membership.title_en = cleaned.get("title_en", "")
            membership.title_de = cleaned.get("title_de", "")
            membership.save()
        elif action=="request":
            membership.save()
        elif action=="accept-%s" % URL_ID_PERSONGROUP:
            membership.is_accepted = True
            membership.save()
        elif action=="deny-%s" % URL_ID_PERSONGROUP:
            membership.delete()
        elif action=="accept-user":
            membership.confirmer = current_user
            membership.save()
        elif action=="deny-user":
            membership.delete()
        elif action=="cancel":
            membership.delete()
        elif action=="cancel-user":
            membership.delete()
        elif action=="remove":
            membership.delete()
        elif action=="remove-user":
            membership.delete()
     

class EditMemberForm(dynamicforms.Form):
    role = forms.ChoiceField(
        label=_("Role"),
        required=True,
        choices=PG_ROLE_CHOICES,
        )    

### ADD INSTITUTION ###

class GroupAddingForm: # Namespace

    class MainDataForm(dynamicforms.Form):
        title = forms.CharField(
            required=True,
            label=_("Group Title"),
            )
        
        title2 = forms.CharField(
            required=False,
            label=_("Subtitle"),
            )

        group_type = forms.ChoiceField(
            required=True,
            choices=GROUP_TYPE_CHOICES,
            label=_("Group type"),
            )
        
        access_type = forms.ChoiceField(
            required=True,
            choices=ACCESS_TYPE_CHOICES,
            label=_("Visibility"),
            )
        
        institution = forms.ModelChoiceField(
            required=False,
            queryset=Institution.objects.all().only("id", "title", "title2"),
            label=_("Organizing institution"),
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
        
        def __init__(self, *args, **kwargs):
            super(GroupAddingForm.MainDataForm, self).__init__(*args, **kwargs)
            self.fields['institution'].queryset = get_current_user().profile.get_institutions()

    class ProfileForm(dynamicforms.Form):
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
        avatar = ImageField(
            label= _("Profile photo"),
            help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_LOGO_SIZE,
            required=False,
            min_dimensions=LOGO_SIZE,
            )
        
    class CategoriesForm(dynamicforms.Form):
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
            
        def __init__(self, *args, **kwargs):
            super(GroupAddingForm.CategoriesForm, self).__init__(*args, **kwargs)
            
            self.context_categories = {}
            for item in get_related_queryset(PersonGroup, "context_categories"):
                self.context_categories[item.sysname] = {
                    'id' : item.id,
                    'field_name' : PREFIX_BC + str(item.id),
                    }
            
            for c in self.context_categories.values():
                self.fields[c['field_name']] = forms.BooleanField(
                    required=False
                    )
    
    @staticmethod
    def submit_step(current_step, form_steps, form_step_data):
        return form_step_data

    @staticmethod
    def save_data(form_steps, form_step_data):
        user = get_current_user()
        group = PersonGroup(
            title = form_step_data[0].get('title', ''),
            title2 = form_step_data[0].get('title2', ''),
            slug = get_unique_value(
                PersonGroup,
                better_slugify(
                    form_step_data[0].get('title', '')
                    ).replace("-","_"),
                separator="_"
                ),
            group_type = get_related_queryset(
                PersonGroup,
                "group_type"
                ).get(
                    pk=form_step_data[0].get('group_type', ''),
                    ),
            access_type = form_step_data[0].get('access_type', 'secret'),
            preferred_language = get_related_queryset(
                PersonGroup,
                "preferred_language"
                ).get(
                    pk=form_step_data[0].get('main_language', ''),
                    ),
            description_en=form_step_data[2].get('description_en', ""),
            description_de=form_step_data[2].get('description_de', ""),
            )
        group.organizing_institution = form_step_data[0].get('institution', None)
            
        membership_options = form_step_data[0].get(
            'membership_options',
            'anyone',
            )
        group.is_by_invitation = membership_options in ("invite", "invite_or_confirm")
        group.is_by_confirmation = membership_options == "invite_or_confirm"
        group.save()
        
        membership = GroupMembership.objects.create(
            user = user,
            person_group = group,
            role = "owners",
            inviter = user,
            confirmer = user,
            is_accepted = True,
        )
        
        cleaned = form_step_data[1]
        
        selected_cc = {}
        for item in get_related_queryset(PersonGroup, "context_categories"):
            if cleaned.get(PREFIX_BC + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cc:
                        del(selected_cc[ancestor.id])
                # add current
                selected_cc[item.id] = item
        group.context_categories.add(*selected_cc.values())
        
        media_file_path = form_step_data[2].get('avatar', '')
        if media_file_path:
            f = open(media_file_path, 'r')
            filename = media_file_path.rsplit("/", 1)[1]
            image_mods.FileManager.save_file_for_object(
                group,
                filename,
                f.read(),
                subpath = "avatar/"
                )
            f.close()
        
        # this is used for redirection to the events details page
        form_steps['success_url'] = '%s/%s/' % (URL_ID_PERSONGROUP, group.slug)
        return form_step_data

ADD_GROUP_FORM_STEPS = {
    0: {
        'title': _("main data"),
        'template': "groups_networks/persongroups/add_group_main_data.html",
        'form': GroupAddingForm.MainDataForm,
    },
    1: {
        'title': _("categories"),
        'template': "groups_networks/persongroups/add_group_categories.html",
        'form': GroupAddingForm.CategoriesForm,
    },
    2: {
        'title': _("profile data"),
        'template': "groups_networks/persongroups/add_group_profile.html",
        'form': GroupAddingForm.ProfileForm,
    },
    3: {
        'title': _("confirm data"),
        'template': "groups_networks/persongroups/add_group_confirm.html",
        'form': forms.Form, # dummy form
    },

    'onsubmit': GroupAddingForm.submit_step,
    'onsave': GroupAddingForm.save_data,
    'name': 'add_group',
    'success_url': "%s/" % URL_ID_PERSONGROUPS,
    'default_path': [0, 1, 2, 3],
}

### INVITATION ###

class Invitation: # Namespace
    class InstitutionInvitedPeople(dynamicforms.Form):
        # the 1st person
        p1_prefix = forms.ChoiceField(
            required=False,
            choices=NULL_PREFIX_CHOICES,
            label=_("Prefix"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        p1_first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            )
        p1_last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            )
        p1_position = forms.CharField(
            required=True,
            label=_("Position"),
            )
        p1_phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p1_phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p1_phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        p1_fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p1_fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p1_fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        p1_mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p1_mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p1_mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        p1_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            )
        p1_is_contact_person = forms.BooleanField(
            required=False,
            label=_("Contact person"),
            initial=True,
            )
        # the 2nd person
        p2_prefix = forms.ChoiceField(
            required=False,
            choices=NULL_PREFIX_CHOICES,
            label=_("Prefix"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        p2_first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            )
        p2_last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            )
        p2_position = forms.CharField(
            required=True,
            label=_("Position"),
            )
        p2_phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p2_phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p2_phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        p2_fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p2_fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p2_fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        p2_mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p2_mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p2_mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        p2_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            )
        p2_is_contact_person = forms.BooleanField(
            required=False,
            label=_("Contact person"),
            initial=True,
            )
        # the 3rd person
        p3_prefix = forms.ChoiceField(
            required=False,
            choices=NULL_PREFIX_CHOICES,
            label=_("Prefix"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        p3_first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            )
        p3_last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            )
        p3_position = forms.CharField(
            required=True,
            label=_("Position"),
            )
        p3_phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p3_phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p3_phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        p3_fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p3_fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p3_fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        p3_mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p3_mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p3_mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        p3_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            )
        p3_is_contact_person = forms.BooleanField(
            required=False,
            label=_("Contact person"),
            initial=True,
            )
        # the 4th person
        p4_prefix = forms.ChoiceField(
            required=False,
            choices=NULL_PREFIX_CHOICES,
            label=_("Prefix"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        p4_first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            )
        p4_last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            )
        p4_position = forms.CharField(
            required=True,
            label=_("Position"),
            )
        p4_phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p4_phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p4_phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        p4_fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p4_fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p4_fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        p4_mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p4_mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p4_mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        p4_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            )
        p4_is_contact_person = forms.BooleanField(
            required=False,
            label=_("Contact person"),
            initial=True,
            )
        # the 5th person
        p5_prefix = forms.ChoiceField(
            required=False,
            choices=NULL_PREFIX_CHOICES,
            label=_("Prefix"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        p5_first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            error_messages={
                'required': _("First name is required"),
                },
            )
        p5_last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        p5_position = forms.CharField(
            required=True,
            label=_("Position"),
            )
        p5_phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p5_phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p5_phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        p5_fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p5_fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p5_fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        p5_mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p5_mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p5_mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        p5_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            )
        p5_is_contact_person = forms.BooleanField(
            required=False,
            label=_("Contact person"),
            initial=True,
            )
            
        def __init__(self, *args, **kwargs):
            super(Invitation.InstitutionInvitedPeople, self).__init__(*args, **kwargs)
            for index in range(1,6):
                if self.data and not self.data['p%d_first_name' % index]:
                    self.fields['p%d_prefix' % index].required = False
                    self.fields['p%d_first_name' % index].required = False
                    self.fields['p%d_last_name' % index].required = False
                    self.fields['p%d_position' % index].required = False
                    self.fields['p%d_email' % index].required = False
            
    @staticmethod
    def submit_step(current_step, form_steps, form_step_data):
        if current_step == 0:
            for i in range(1,6):
                email = form_step_data[current_step].get('p%d_email' % i, "")
                if email:
                    try:
                        p = form_step_data[current_step]["p%d" % i] = Person.objects.get(
                            user__email=email,
                            )
                    except:
                        pass
                    else:
                        if p.prefix_id:
                            form_step_data[current_step]["p%d_prefix" % i] = p.prefix_id
                            form_step_data[current_step]["get_p%d_prefix_display" % i] = force_unicode(p.prefix.get_title())
                        form_step_data[current_step]["p%d_first_name" % i] = p.user.first_name
                        form_step_data[current_step]["p%d_last_name" % i] = p.user.last_name
        return form_step_data

    @staticmethod
    def save_data(form_steps, form_step_data):
        existing_additional_contacts = []
        new_additional_contacts = []
        institution = form_steps.get('institution', None)
        user = form_steps.get('user', None)
        if not institution or not user:
            raise Http404()
        group = institution._get_related_group()
        contact = institution.get_primary_contact()
        for i in range(1, 6):
            p = form_step_data[0].get('p%d' % i, None)
            if not (p and group.get_all_members().filter(user=p.user)):
                if p:
                    existing_additional_contacts.append(p)
                elif (
                    form_step_data[0].get('p%d_first_name' % i, False)
                    and form_step_data[0].get('p%d_last_name' % i, False)
                    and form_step_data[0].get('p%d_email' % i, False)
                    ):
                    # create user
                    username = get_unique_value(
                        User,
                        better_slugify("_".join((
                            form_step_data[0]['p%d_first_name' % i],
                            form_step_data[0]['p%d_last_name' % i]
                            ))).replace("-", "_"),
                        field_name="username",
                        separator="_",
                        )
                    u = User(
                        first_name = form_step_data[0]['p%d_first_name' % i],
                        last_name = form_step_data[0]['p%d_last_name' % i],
                        email = form_step_data[0]['p%d_email' % i],
                        username = username,
                        is_active = False,
                        )
                    u.save()
                    p = Person(
                        user=u,
                        prefix_id=form_step_data[0].get('p%d_prefix' % i, None),
                        )
                    try:
                        prefix = Prefix.objects.get(
                            pk=int(form_step_data[0].get('p%d_prefix' % i, 0))
                            )
                    except:
                        prefix = None
                    if prefix:
                        p.gender=p.prefix.gender
                    p.save()
                    new_additional_contacts.append(p)
                if p:
                    individual_contact = p.individualcontact_set.create(
                        location_type=IndividualLocationType.objects.all()[0],
                        is_primary=True,
                        institution=institution,
                        phone0_type=PhoneType.objects.get(slug='phone'),
                        phone0_country=form_step_data[0].get('p%d_phone_country' % i, ""),
                        phone0_area=form_step_data[0].get('p%d_phone_area' % i, ""),
                        phone0_number=form_step_data[0].get('p%d_phone_number' % i, ""),
                        phone1_type=PhoneType.objects.get(slug='fax'),
                        phone1_country=form_step_data[0].get('p%d_fax_country' % i, ""),
                        phone1_area=form_step_data[0].get('p%d_fax_area' % i, ""),
                        phone1_number=form_step_data[0].get('p%d_phone_number' % i, ""),
                        phone2_type=PhoneType.objects.get(slug='mobile'),
                        phone2_country=form_step_data[0].get('p%d_mobile_country' % i, ""),
                        phone2_area=form_step_data[0].get('p%d_mobile_area' % i, ""),
                        phone2_number=form_step_data[0].get('p%d_mobile_number' % i, ""),
                        url0_type_id=contact.get("url0_type_id",None),
                        url1_type_id=contact.get('url1_type_id', None),
                        url2_type_id=contact.get('url2_type_id', None),
                        url0_link=contact.get('url0_link', ''),
                        url1_link=contact.get('url1_link', ''),
                        url2_link=contact.get('url2_link', ''),
                        email0_address=contact.get('email0_address', ''),
                        )
                    Address.objects.set_for(
                        individual_contact,
                        "postal_address",
                        country=contact.get('country', ''),
                        district=contact.get('district', ''),
                        city=contact.get('city', ''),
                        street_address=contact.get('street_address', ''),
                        street_address2=contact.get('street_address2', ''),
                        postal_code=contact.get('postal_code', ''),
                        latitude=contact.get('latitude', ''),
                        longitude=contact.get('longitude', ''),
                        )
                    p._is_contact_person = form_step_data[0].get(
                        'p%d_is_contact_person' % i,
                        False,
                        )
        raise Warning
        for p in existing_additional_contacts + new_additional_contacts:
            membership, created = GroupMembership.objects.get_or_create(
                user = p.user,
                person_group = group,
                defaults = {
                    'role':  "members",
                    'inviter': user,
                    'is_accepted': False,
                    },
                )
            if created or p._is_contact_person:
                membership.is_contact_person = p._is_contact_person
                membership.save()
            
        current_site = Site.objects.get_current()
        encrypted_email = cryptString(user.email)
        
        for p in new_additional_contacts:
            encrypted_email = cryptString(p.user.email)
            sender_name = ''
            sender_email = settings.DEFAULT_FROM_EMAIL
            send_email_using_template(
                [Recipient(user=p.user)],
                "invite_external_people_to_group",
                obj=institution,
                obj_placeholders={
                    'site_name': current_site.name,
                    'encrypted_email': encrypted_email,
                    },
                delete_after_sending=True,
                sender_name=sender_name,
                sender_email=sender_email,
                send_immediately=True,
                )
        recipients = [
            Recipient(user=p.user)
            for p in existing_additional_contacts
            ]
        if recipients:
            sender_name = ''
            sender_email = settings.DEFAULT_FROM_EMAIL
            send_email_using_template(
                recipients,
                "invite_internal_people_to_group",
                obj=group,
                obj_placeholders={
                    'site_name': current_site.name,
                    },
                delete_after_sending=True,
                sender_name=sender_name,
                sender_email=sender_email,
                send_immediately=True,
                )
        
        return form_step_data

INVITATION_FORM_STEPS = {
    0: {
        'title': _("People to Invite"),
        'template': "groups_networks/institution_invitation.html",
        'form': Invitation.InstitutionInvitedPeople,
    },
    1: {
        'title': _("Confirm Data"),
        'template': "groups_networks/institution_invitation_confirmation.html",
        'form': forms.Form, # dummy form
    },

    'onsubmit': Invitation.submit_step,
    'onsave': Invitation.save_data,
    'name': 'institution_invitations',
    'success_template': "groups_networks/institution_invitation_done.html",
    'default_path': [0,1],
}


