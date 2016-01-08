# -*- coding: UTF-8 -*-
import os
import shutil
from datetime import datetime, time

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.shortcuts import redirect
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms.fields import AutocompleteModelChoiceField
from base_libs.utils.misc import get_related_queryset
from base_libs.middleware.threadlocals import get_current_user

from mptt.forms import TreeNodeChoiceField

from jetson.apps.image_mods.models import FileManager
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField

from .models import Bulletin, BulletinCategory
from .models import TYPE_CHOICES, STATUS_CHOICES

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

# translatable strings to collect
_("Please enable JavaScript to use file uploader.")
_(u"Available formats are JPG, GIF, and PNG. Minimal size is 290 × 290 px.")
        
        
class BulletinForm(forms.ModelForm):
    image_path = forms.CharField(
        max_length=255,
        widget=forms.HiddenInput(),
        required=False,
    )
    published_till_date = forms.DateField(
        label=_("Published till date"),
        required=False,
        input_formats=('%Y-%m-%d',),
        widget=forms.DateInput(format='%Y-%m-%d')
    )
    published_till_time = forms.TimeField(
        label=_("Published till time"),
        required=False,
        input_formats=('%H:%M',),
        widget=forms.TimeInput(format='%H:%M')
    )
    institution = AutocompleteModelChoiceField(
        required=False,
        label=_("Institution"),
        app="institutions",
        qs_function="get_published_institutions",
        display_attr="title",
        add_display_attr="get_address_string",
        help_text=u'Bitte geben Sie einen Anfangsbuchstaben ein, um eine entsprechende Auswahl der verfügbaren Institutionen angezeigt zu bekommen.',
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight": False,
            "multipleSeparator": ",,, ",
            "extraParams": {'noescape':'1',},
        },
    )
    locality_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=get_related_queryset(Bulletin, "locality_type"),
    )
    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=get_related_queryset(Bulletin, "categories"),
    )

    class Meta:
        model = Bulletin
        fields = [
            'bulletin_type', 'bulletin_category', 'categories', 'title', 'description', 'locality_type',
            'institution', 'institution_title', 'institution_url',
            'contact_person', 'phone', 'email',
            'image_description', 'status',
        ]

    def __init__(self, *args, **kwargs):
        super(BulletinForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.fields['bulletin_type'].widget = forms.RadioSelect()
        if len(self.fields['bulletin_type'].choices) > 2:
            del self.fields['bulletin_type'].choices[0]

        self.fields['bulletin_category'].widget = forms.RadioSelect()
        self.fields['bulletin_category'].empty_label = None

        # self.fields['categories'].widget = forms.CheckboxSelectMultiple()
        # self.fields['categories'].empty_label = None

        self.fields['status'].widget = forms.HiddenInput()

        if self.instance:
            if self.instance.published_till:
                #published_till = timezone.localtime(self.instance.published_till)
                published_till = self.instance.published_till
                self.fields['published_till_date'].initial = published_till.date()
                self.fields['published_till_time'].initial = published_till.time()

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Title"),
                layout.Field("title"),
                layout.Field("description"),
                layout.Field("bulletin_type"),
            ),
            layout.Fieldset(
                _("Categories"),
                layout.Field("bulletin_category"),
                layout.Div(layout.Field("categories", template="ccb_form/custom_widgets/checkboxselectmultipletree.html")),
                layout.Field("locality_type"),
            ),
            layout.Fieldset(
                _("Image"),
                layout.HTML(u"""{% load i18n image_modifications %}
                    <div id="image_preview">
                        {% if object.image %}
                            <img src="{{ UPLOADS_URL }}{{ object.image|modified_path:"ad" }}?now={% now "YmdHis" %}" alt="" />
                        {% else %}
                            {% if object.image_path %}
                                <img src="{{ UPLOADS_URL }}{{ object.image_path|modified_path:"ad" }}?now={% now "YmdHis" %}" alt="" />
                            {% endif %}
                        {% endif %}
                    </div>
                    <div id="image_uploader">
                        <noscript>
                            <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                        </noscript>
                    </div>
                    <p id="image_help_text" class="help-block">{% trans "Available formats are JPG, GIF, and PNG." %}</p>
                    <div class="control-group error"><div class="messages help-block"></div></div>
                """),
                layout.Field("image_description"),
                layout.Field("image_path"),
                css_id="profile_image_upload",
            ),
            layout.Fieldset(
                _("Contact"),
                layout.Div(
                    layout.Field("institution"),
                    css_id="block_institution_selection",
                ),
                layout.Div(
                    layout.Field("institution_title"),
                    layout.Field("institution_url"),
                    css_id="block_institution_title",
                ),
                layout.Field("contact_person"),
                layout.Field("phone"),
                layout.Field("email"),
            ),
            layout.Fieldset(
                _("Publishing date and time"),
                layout.Div(
                    layout.Div(
                        layout.Field("published_till_date", autocomplete="off"),
                        css_class="col-md-6",
                    ),
                    layout.Div(
                        layout.Field("published_till_time", autocomplete="off"),
                        css_class="col-md-6",
                    ),
                    css_class="row",
                ),
            ),
            layout.Field("status"),
            layout.Field("reload_page"),

            bootstrap.FormActions(
                layout.Submit('reset', _('Reset')),
                layout.Submit('submit', _('Next')),
            )
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')

        if not (email or phone):
            msg = _("Please enter a either email or phone.")
            self._errors["email"] = self.error_class([msg])
            self._errors["phone"] = self.error_class([msg])

        return self.cleaned_data


def load_data(instance=None):
    form_step_data = {}
    if instance:
        form_step_data = {
            'bulletin_data': {'_filled': True, 'sets': {}},
            '_pk': instance.pk,
        }

        ### The "bulletin_data" step ###

        fields = [
            'bulletin_type', 'bulletin_category', 'title', 'description', 'locality_type',
            'institution', 'institution_title', 'institution_url',
            'contact_person', 'phone', 'email',
            'image_description', 'status',
        ]
        for fname in fields:
            form_step_data['bulletin_data'][fname] = getattr(instance, fname)

        form_step_data['bulletin_data']['categories'] = instance.categories.all()

    else:
        form_step_data = {
            'bulletin_data': {'_filled': False, 'sets': {}},
        }
        person = get_current_user().profile
        own_institutions = person.get_institutions()
        form_step_data['bulletin_data']['contact_person'] = person.get_title()
        personal_primary_contact = person.get_primary_contact()
        primary_contact = {}
        if own_institutions:
            institution = own_institutions[0]
            form_step_data['bulletin_data']['institution'] = institution
            primary_contact = institution.get_primary_contact()  # institutional contact data is more preferable than personal

        form_step_data['bulletin_data']['email'] = primary_contact.get('email0_address', '') or person.user.email
        form_step_data['bulletin_data']['phone'] = (
            '+{phone_country} {phone_area} {phone_number}'.format(**primary_contact)
            if primary_contact.get('phone_number', None) else ''
        ) or (
            '+{phone_country} {phone_area} {phone_number}'.format(**personal_primary_contact)
            if personal_primary_contact.get('phone_number', None) else ''
        )


    return form_step_data


def submit_step(current_step, form_steps, form_step_data, instance=None):
    # this function actually is not necessary, but is here as boilerplate/stub
    if current_step == "bulletin_data":
        pass
    return form_step_data


def set_extra_context(current_step, form_steps, form_step_data, instance=None):
    if "_pk" in form_step_data:
        return {'bulletin': Bulletin.objects.get(pk=form_step_data['_pk'])}
    return {}


def save_data(form_steps, form_step_data, instance=None):
    # probably a dummy callback, because the data is already saved after each step
    is_new = not instance
    if not instance:
        if '_pk' in form_step_data:
            instance = Bulletin.objects.get(pk=form_step_data['_pk'])
        else:
            instance = Bulletin()

    fields = [
        'bulletin_type', 'bulletin_category', 'title', 'description', 'locality_type',
        'institution', 'institution_title', 'institution_url',
        'contact_person', 'phone', 'email',
        'image_description', 'status',
    ]
    for fname in fields:
        setattr(instance, fname, form_step_data['bulletin_data'][fname])

    if form_step_data['bulletin_data']['published_till_date']:
        if form_step_data['bulletin_data']['published_till_time']:
            instance.published_till = datetime.combine(
                form_step_data['bulletin_data']['published_till_date'],
                form_step_data['bulletin_data']['published_till_time'],
            )
        else:
            instance.published_till = datetime.combine(
                form_step_data['bulletin_data']['published_till_date'],
                time(0,0),
            )

    instance.save()

    instance.categories.clear()
    for cat in form_step_data['bulletin_data']['categories']:
        instance.categories.add(cat)

    rel_dir = "bulletin_board/"
    if form_step_data['bulletin_data']['image_path']:
        tmp_path = form_step_data['bulletin_data']['image_path']
        abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

        fname, fext = os.path.splitext(tmp_path)
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
        dest_path = "".join((rel_dir, filename))
        FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
        abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)

        shutil.copy2(abs_tmp_path, abs_dest_path)

        os.remove(abs_tmp_path)
        instance.image = dest_path
        instance.save()

    return form_step_data


def cancel_editing(request, instance=None):
    if instance:
        return redirect(instance)
    return redirect("bulletin_list")


def redirect_to_bulletin(request, instance=None):
    if instance:
        return redirect(instance)
    return redirect("bulletin_list")


BULLETIN_FORM_STEPS = {
    'bulletin_data': {
        'title': _("bulletin data"),
        'template': "bulletin_board/change_bulletin.html",
        'form': BulletinForm,
    },
    'confirm_data': {
        'title': _("confirm data"),
        'template': "bulletin_board/change_bulletin_confirm.html",
    },
    'oninit': load_data,
    'on_set_extra_context': set_extra_context,
    'onsubmit': submit_step,
    'onsave': save_data,
    'onreset': cancel_editing,
    'onsuccess': redirect_to_bulletin,
    'name': 'bulletin_form',
    'default_path': ['bulletin_data', 'confirm_data'],
}


class BulletinSearchForm(forms.Form):
    category = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(Bulletin, "categories"),
    )
        
    locality_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Locality Type"),
        required=False,
        queryset=get_related_queryset(Bulletin, "locality_type"),
    )

    bulletin_type = forms.ChoiceField(
        label=_("Bulletin Type"),
        required=False,
        choices=(("", _("All")),) + TYPE_CHOICES,
    )
    
    bulletin_category = forms.ModelChoiceField(
        empty_label=_("All"),
        label=_("Bulletin Category"),
        required=False,
        queryset=get_related_queryset(Bulletin, "bulletin_category"),
    )
        
    status = forms.ChoiceField(
        label=_("Status"),
        required=False,
        choices=(("", _("All")),) + STATUS_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        super(BulletinSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "."
        self.helper.form_method = "GET"
        self.helper.form_id = ""
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                "category",
                "locality_type",
                "bulletin_type",
                "bulletin_category",
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Filter')),
            )
        )

    def get_query(self):
        from django.template.defaultfilters import urlencode
        if self.is_valid():
            cleaned = self.cleaned_data
            return "&".join([
                ("%s=%s" % (k, urlencode(isinstance(v, models.Model) and v.pk or v)))
                for (k, v) in cleaned.items()
                if v
                ])
        return ""

