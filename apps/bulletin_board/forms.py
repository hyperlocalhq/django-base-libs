# -*- coding: UTF-8 -*-
from datetime import datetime, time, date

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.dates import MONTHS
from django.shortcuts import redirect
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

# from base_libs.forms.fields import AutocompleteField
from base_libs.utils.misc import get_related_queryset
from base_libs.middleware.threadlocals import get_current_user

from mptt.forms import TreeNodeChoiceField

from jetson.apps.utils.forms import ModelMultipleChoiceTreeField
from jetson.apps.utils.forms import ModelChoiceTreeField

from .models import Bulletin
from .models import TYPE_CHOICES, STATUS_CHOICES

Institution = models.get_model("institutions", "Institution")

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2016, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]
HOURS_CHOICES = [("", _("HH"))] + [(i, u"%02d" % i) for i in range(0, 24)]
MINUTES_CHOICES = [("", _("MM"))] + [(i, u"%02d" % i) for i in range(0, 60, 5)]

LOGO_SIZE = (850, 480)
STR_LOGO_SIZE = "%sx%s" % (850, 480)

# translatable strings to collect
_("Please enable JavaScript to use file uploader.")
_(u"Available formats are JPG, GIF, and PNG. Minimal size is 290 × 290 px.")


class BulletinForm(forms.ModelForm):
    # image_path = forms.CharField(
    #    max_length=255,
    #    widget=forms.HiddenInput(),
    #    required=False,
    # )

    # image_path = ImageField(
    #    label=' ',
    #    help_text=_(
    #        "You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_LOGO_SIZE,
    #    required=False,
    #    min_dimensions=LOGO_SIZE,
    # )

    end_yyyy = forms.ChoiceField(
        required=False,
        choices=YEARS_CHOICES,
        label=_("Start Year"),
    )

    end_mm = forms.ChoiceField(
        required=False,
        choices=MONTHS_CHOICES,
        label=_("Start Month"),
    )

    end_dd = forms.ChoiceField(
        required=False,
        choices=DAYS_CHOICES,
        label=_("Start Day"),
    )

    end_hh = forms.ChoiceField(
        required=False,
        choices=HOURS_CHOICES,
        label=_("Start Hours"),
    )

    end_ii = forms.ChoiceField(
        required=False,
        choices=MINUTES_CHOICES,
        label=_("Start Minutes"),
    )

    # published_till_date = forms.DateField(
    #    label=_("Published till date"),
    #    required=False,
    #    input_formats=('%Y-%m-%d',),
    #    widget=forms.DateInput(format='%Y-%m-%d')
    # )
    # published_till_time = forms.TimeField(
    #    label=_("Published till time"),
    #    required=False,
    #    input_formats=('%H:%M',),
    #    widget=forms.TimeInput(format='%H:%M')
    # )
    """
    institution = AutocompleteModelChoiceField(
    #institution = AutocompleteField(
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
    """
    institution = forms.CharField(
        required=False,
        label=_("Institution"),
        help_text=_("Please enter a letter to display a list of available institutions"),
        widget=forms.Select(choices=[]),
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
        queryset=get_related_queryset(Bulletin, "categories").filter(level=0),
    )

    class Meta:
        model = Bulletin
        fields = [
            'bulletin_type', 'bulletin_category', 'categories', 'title', 'description', 'locality_type',
            # 'institution',
            'institution_title', 'institution_url',
            'contact_person', 'phone', 'email',
            # 'image_description',
            'external_url',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        super(BulletinForm, self).__init__(*args, **kwargs)

        # add option of already choosen selections on multistep forms for autoload fields
        initial = kwargs.get("initial", None)
        if initial:
            if initial.get('institution', None):
                institution = Institution.objects.get(pk=initial.get('institution', None))
                self.fields['institution'].widget.choices = [(institution.id, institution.title)]

        # add option of choosen selections for autoload fields on error reload of page
        if self.data.get('institution', None):
            institution = Institution.objects.get(pk=self.data.get('institution', None))
            self.fields['institution'].widget.choices = [(institution.id, institution.title)]

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
                # published_till = timezone.localtime(self.instance.published_till)
                published_till = self.instance.published_till
                self.fields['end_dd'].initial = published_till.date().day
                self.fields['end_mm'].initial = published_till.date().month
                self.fields['end_yyyy'].initial = published_till.date().year
                self.fields['end_hh'].initial = published_till.time().hour
                self.fields['end_ii'].initial = published_till.time().minute

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Title"),
                layout.Field("title"),
                layout.Field("description"),
                layout.Field("bulletin_type"),
                layout.Field("external_url"),
            ),
            layout.Fieldset(
                _("Categories"),
                layout.Field("bulletin_category"),
                layout.HTML(string_concat('<dt>', _("Categories"), '</dt>')),
                layout.Field("categories", template="ccb_form/custom_widgets/checkboxselectmultipletree.html"),
                layout.Field("locality_type"),
            ),
            # layout.Fieldset(
            #    _("Image"),
            #    layout.HTML("""{% load image_modifications %}
            #        {% if form_step_data.bulletin_data.image_path %}
            #            <dt>"""+(_("Image")+"")+"""</dt><dd><img class="avatar" src="/helper/tmpimage/{{ form_step_data.bulletin_data.image_path.tmp_filename }}/{{ LOGO_PREVIEW_SIZE }}/" alt="{{ object.get_title|escape }}"/></dd>
            #        {% else %}
            #            <dt>"""+(_("Image")+"")+"""</dt><dd><img src="{{ STATIC_URL }}site/img/placeholder/image.png" alt="{{ object.get_title|escape }}"/></dd>
            #        {% endif %}
            #    """),
            #    "image_path",
            #    "image_description",

            # layout.HTML(u"""{% load i18n image_modifications %}
            #    <div id="image_preview">
            #        {% if object.image %}
            #            <img src="{{ UPLOADS_URL }}{{ object.image|modified_path:"ad" }}?now={% now "YmdHis" %}" alt="" />
            #        {% else %}
            #            {% if object.image_path %}
            #                <img src="{{ UPLOADS_URL }}{{ object.image_path|modified_path:"ad" }}?now={% now "YmdHis" %}" alt="" />
            #            {% endif %}
            #        {% endif %}
            #    </div>
            #    <div id="image_uploader">
            #        <noscript>
            #            <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
            #        </noscript>
            #    </div>
            #    <p id="image_help_text" class="help-block">{% trans "Available formats are JPG, GIF, and PNG." %}</p>
            #    <div class="control-group error"><div class="messages help-block"></div></div>
            # """),
            # layout.Field("image_description"),
            # layout.Field("image_path"),
            # css_id="profile_image_upload",
            # ),
            layout.Fieldset(
                _("Contact"),

                layout.Field(
                    "institution",
                    data_load_url="/helper/autocomplete/institutions/get_published_institutions/title/get_address_string/",
                    data_load_start="1",
                    data_load_max="20",
                    wrapper_class="institution-select",
                    css_class="autoload"
                ),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-select"> </dt><dd class="institution-select"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-input" data-toggle-hide=".institution-select">{% trans "Not listed? Enter manually" %}</a></dd>
                <dd class="clearfix"></dd>
                """),

                layout.Field("institution_title", wrapper_class="institution-input hidden", css_class="toggle-check"),
                layout.Field("institution_url", wrapper_class="institution-input hidden"),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-input hidden"> </dt><dd class="institution-input hidden"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-select" data-toggle-hide=".institution-input">{% trans "Back to selection" %}</a></dd>
                <dd class="clearfix"></dd>
                """),

                layout.Field("contact_person"),
                layout.Field("phone"),
                layout.Field("email"),
            ),

            layout.Fieldset(
                _("Publish until date and time"),
                layout.MultiField(
                    _("Date"),
                    layout.Field(
                        "end_dd",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html",
                        placeholder=_('Day')
                    ),
                    layout.Field(
                        "end_mm",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html",
                        placeholder=_('Month')
                    ),
                    layout.Field(
                        "end_yyyy",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html",
                        placeholder=_('Year')
                    ),
                ),
                layout.MultiField(
                    "Time",
                    layout.Field(
                        "end_hh",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html",
                        placeholder=_('Hour')
                    ),
                    layout.Field(
                        "end_ii",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html",
                        placeholder=_("Minute")
                    ),
                ),
                # layout.MultiField(
                #    layout.Div(
                #        layout.Field("published_till_date", autocomplete="off"),
                #        css_class="col-md-6",
                #    ),
                #    layout.Div(
                #        layout.Field("published_till_time", autocomplete="off"),
                #        css_class="col-md-6",
                #    ),
                #    css_class="row",
                # ),
            ),
            layout.Field("status"),
            layout.Field("reload_page"),

            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
        )

    def clean(self):
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')

        if not (email or phone):
            msg = _("Please enter either email or phone.")
            self._errors["email"] = self.error_class([msg])
            self._errors["phone"] = self.error_class([msg])

        if self.cleaned_data.get('institution_title', None):
            del self._errors['institution']
        else:
            if self.cleaned_data.get('institution', None):
                for field_name in [
                    'institution_title',
                    'institution_url',
                ]:
                    if self._errors.get(field_name, False):
                        del self._errors[field_name]


        # end date must be valid!
        published_till_date = None
        end_yyyy = self.cleaned_data.get('end_yyyy', None)
        end_mm = self.cleaned_data.get('end_mm', None)
        end_dd = self.cleaned_data.get('end_dd', None)

        # any error handling is overwritten!
        if self._errors.get('end_yyyy', False):
            del self._errors['end_yyyy']
        if self._errors.get('end_mm', False):
            del self._errors['end_mm']
        if self._errors.get('end_dd', False):
            del self._errors['end_dd']

        try:
            if end_yyyy or end_mm or end_dd:
                published_till_date = date(int(end_yyyy), int(end_mm), int(end_dd))
        except Exception:
            self._errors['end_dd'] = [_("Please enter a valid date.")]
            self._errors['end_mm'] = [_(" ")]
            self._errors['end_yyyy'] = [_(" ")]

        published_till_time = None
        end_hh = self.cleaned_data.get('end_hh', None)
        end_ii = self.cleaned_data.get('end_ii', None)

        if 'end_hh' in self._errors or 'end_ii' in self._errors:
            self._errors['end_dd'] = [_("Please enter a valid time using format 'HH:MM'")]

        # if end time is specified, day, month and year must be specified
        if end_hh:
            if not (end_yyyy and end_mm and end_dd):
                self._errors['end_hh'] = [_("If you choose a time, please enter a valid day, month and year.")]

        try:
            if end_hh or end_ii:
                published_till_time = time(int(end_hh), int(end_ii or 0))
        except Exception:
            self._errors['end_hh'] = [_("Please enter a valid time.")]
            self._errors['end_ii'] = [_(" ")]

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
            'institution',
            'institution_title', 'institution_url',
            'contact_person', 'phone', 'email',
            # 'image_description',
            'external_url',
            'status',
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
                                                       '+{phone_country} {phone_area} {phone_number}'.format(
                                                           **primary_contact)
                                                       if primary_contact.get('phone_number', None) else ''
                                                   ) or (
                                                       '+{phone_country} {phone_area} {phone_number}'.format(
                                                           **personal_primary_contact)
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


    # institution data
    institution = None
    institution_title = ''
    institution_url = ''
    if form_step_data['bulletin_data'].get('institution', None):
        institution = Institution.objects.get(pk=form_step_data['bulletin_data']['institution'])
        # institution = form_step_data['bulletin_data']['institution']
        # institution_title = institution.get_title()
        # institution_url = institution.get_url_path()
    else:
        institution_title = form_step_data['bulletin_data'].get('institution_title', None)
        institution_url = form_step_data['bulletin_data'].get('institution_title', None)

    instance.institution = institution
    instance.institution_title = institution_title
    instance.institution_url = institution_url

    fields = [
        'bulletin_type', 'bulletin_category', 'title', 'description', 'locality_type',
        'contact_person', 'phone', 'email',
        'external_url',
        # 'image_description',
        'status',
    ]
    for fname in fields:
        setattr(instance, fname, form_step_data['bulletin_data'][fname])

    instance.published_till = None
    if form_step_data['bulletin_data'].get('end_yyyy', None):
        published_till_date = date(int(form_step_data['bulletin_data']['end_yyyy']),
                                   int(form_step_data['bulletin_data']['end_mm']),
                                   int(form_step_data['bulletin_data']['end_dd']))

        if form_step_data['bulletin_data']['end_hh']:
            published_till_time = time(int(form_step_data['bulletin_data']['end_hh']),
                                       int(form_step_data['bulletin_data']['end_ii']))

            instance.published_till = datetime.combine(
                published_till_date,
                published_till_time,
            )
        else:
            instance.published_till = datetime.combine(
                published_till_date,
                time(0, 0),
            )

    instance.save()

    instance.categories.clear()
    for cat in form_step_data['bulletin_data']['categories']:
        instance.categories.add(cat)

    # rel_dir = "bulletin_board/"
    # if form_step_data['bulletin_data']['image_path']:
    #    tmp_path = form_step_data['bulletin_data']['image_path']
    #    abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)

    #    fname, fext = os.path.splitext(tmp_path)
    #    filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
    #    dest_path = "".join((rel_dir, filename))
    #    FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
    #    abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)

    #    shutil.copy2(abs_tmp_path, abs_dest_path)

    #    os.remove(abs_tmp_path)
    #    instance.image = dest_path
    #    instance.save()



    # media_file = form_step_data['bulletin_data'].get('image_path', '')
    # if media_file:
    #    tmp_path = os.path.join(settings.PATH_TMP, media_file['tmp_filename'])
    #    f = open(tmp_path, 'r')
    #    filename = tmp_path.rsplit("/", 1)[1]
    #    image_mods.FileManager.save_file_for_object(
    #        instance,
    #        filename,
    #        f.read(),
    #        subpath="bulletin_board/"
    #    )
    #    f.close()

    #    instance.save()


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
    category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(Bulletin, "categories").filter(level=0),
    )

    locality_type = ModelChoiceTreeField(
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

    bulletin_category = ModelChoiceTreeField(
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
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("bulletin_type", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("bulletin_category", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("category", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("locality_type", template="ccb_form/custom_widgets/locality_type_filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )
