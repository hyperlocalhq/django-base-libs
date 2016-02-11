# -*- coding: UTF-8 -*-
import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template import loader
from django.utils.dates import MONTHS
from django.utils.translation import string_concat
from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404

from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED
from base_libs.forms import dynamicforms
from base_libs.forms.fields import AutocompleteField
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_related_queryset

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType, EmailType, URLType
from jetson.apps.mailing.views import Recipient, send_email_using_template
from jetson.apps.utils.forms import ModelChoiceTreeField
from jetson.apps.utils.forms import ModelMultipleChoiceTreeField

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from ccb.apps.site_specific.models import ContextItem

app = models.get_app("marketplace")
JobOffer, JobSector, JobType = app.JobOffer, app.JobSector, app.JobType
URL_ID_JOB_OFFER = app.URL_ID_JOB_OFFER
URL_ID_JOB_OFFERS = app.URL_ID_JOB_OFFERS

Institution = models.get_model("institutions", "Institution")

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2008, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]

CONTACT_PERSON_CHOICES = [
    (0, _("I am the contact person")),
    (1, _("I am not the contact person")),
]

# prexixes of fields to guarantee uniqueness
PREFIX_JS = 'JS_'  # Job Sector

# Collect translatable strings
_("Not listed? Enter manually")
_("Back to selection")
_('Is some category missing? You can <a href="/ticket/new-category/">suggest it here</a>.')
_("Please activate the checkboxes if you want to send your jobposting to one of our partners.")


class MainDataForm(dynamicforms.Form):
    """
    Form for main data
    """
    position = forms.CharField(
        label=_("Position"),
        required=True,
    )

    job_type = forms.ModelChoiceField(
        label=_("Job Type"),
        required=True,
        queryset=get_related_queryset(JobOffer, "job_type"),
    )

    qualifications = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=get_related_queryset(JobOffer, "qualifications"),
        label=_("Qualification"),
    )

    description = forms.CharField(
        label=_("Description"),
        required=True,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )

    """
    offering_institution = AutocompleteField(
        required=False,
        label=_("Offering institution"),
        help_text=_("Please enter a letter to display a list of available institutions"),
        app="marketplace",
        qs_function="get_institutions",
        display_attr="title",
        add_display_attr="get_address_string",
        options={
            "minChars": 1,
            "max": 20,
            "mustMatch": 1,
            "highlight": False,
        },
    )
    """
    offering_institution = forms.CharField(
        required=False,
        label=_("Offering institution"),
        help_text=_("Please enter a letter to display a list of available institutions"),
        widget=forms.Select(choices=[]),
    )

    offering_institution_title = forms.CharField(
        required=False,
        label=_("Institution/Company Title"),
    )

    contact_person_ind = forms.ChoiceField(
        initial=0,
        choices=CONTACT_PERSON_CHOICES,
        widget=forms.RadioSelect()
    )

    contact_person_name = forms.CharField(
        required=False,
        label=_("Contact Person Name"),
    )

    street_address = forms.CharField(
        required=True,
        label=_("Street Address"),
    )
    street_address2 = forms.CharField(
        required=False,
        label=_("Street Address (2nd line)"),
    )
    city = forms.CharField(
        required=True,
        label=_("City"),
    )
    postal_code = forms.CharField(
        required=True,
        label=_("Postal Code"),
    )
    country = forms.ChoiceField(
        required=True,
        choices=Address._meta.get_field("country").get_choices(),
        label=_("Country"),
    )

    phone_country = forms.CharField(
        required=False,
        max_length=4,
        initial="49",
    )
    phone_area = forms.CharField(
        required=False,
        max_length=5,
    )
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        label=_("Phone"),
    )
    fax_country = forms.CharField(
        required=False,
        max_length=4,
        initial="49",
    )
    fax_area = forms.CharField(
        required=False,
        max_length=5,
    )
    fax_number = forms.CharField(
        required=False,
        max_length=15,
        label=_("Fax"),
    )

    email0_address = forms.EmailField(
        required=False,
        label=_("E-mail"),
    )

    url0_link = forms.URLField(
        required=False,
        label=_("Website"),
    )

    publish_emails = forms.BooleanField(
        label=_("Publish email to unregistered visitors"),
        initial=True,
        required=False,
    )

    end_yyyy = forms.ChoiceField(
        required=True,
        choices=YEARS_CHOICES,
        label=_("End Year"),
    )

    end_mm = forms.ChoiceField(
        required=True,
        choices=MONTHS_CHOICES,
        label=_("End Month"),
    )

    end_dd = forms.ChoiceField(
        required=True,
        choices=DAYS_CHOICES,
        label=_("End Day"),
    )

    def __init__(self, *args, **kwargs):
        super(MainDataForm, self).__init__(*args, **kwargs)
        six_weeks_from_now = datetime.datetime.now() + datetime.timedelta(days=7 * 6)
        self.fields['end_yyyy'].initial = six_weeks_from_now.year
        self.fields['end_mm'].initial = six_weeks_from_now.month
        self.fields['end_dd'].initial = six_weeks_from_now.day
                
        # add option of already choosen selections on multistep forms for autoload fields
        initial = kwargs.get("initial", None)
        if initial:
            if initial.get('offering_institution', None):
                institution = Institution.objects.get(pk=initial.get('offering_institution', None))
                self.fields['offering_institution'].widget.choices=[(institution.id, institution.title)]
        
        # add option of choosen selections for autoload fields on error reload of page
        if self.data.get('offering_institution', None):
            institution = Institution.objects.get(pk=self.data.get('offering_institution', None))
            self.fields['offering_institution'].widget.choices=[(institution.id, institution.title)]
        

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Job"),
                "position",
                "job_type",
                "qualifications",
                "description",
            ),
            layout.Fieldset(
                _("Institution"),
                layout.Field(
                    "offering_institution", 
                    data_load_url="/helper/autocomplete/marketplace/get_institutions/title/get_address_string/",
                    data_load_start="1",
                    data_load_max="20",
                    wrapper_class="institution-select",
                    css_class="autoload"
                ),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-select"> </dt><dd class="institution-select"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-input" data-toggle-hide=".institution-select">{% trans "Not listed? Enter manually" %}</a></dd>
                """),

                layout.Field("offering_institution_title", wrapper_class="institution-input hidden",
                             css_class="toggle-check"),
                layout.HTML("""{% load i18n %}
                    <dt class="institution-input hidden"> </dt><dd class="institution-input hidden"><a href="javascript:void(0);" class="toggle-visibility" data-toggle-show=".institution-select" data-toggle-hide=".institution-input">{% trans "Back to selection" %}</a></dd>
                """),
            ),
            layout.Fieldset(
                _("Address"),
                "street_address",
                "street_address2",
                layout.MultiField(
                    string_concat(_('ZIP'), "*, ", _('City'), "*"),
                    layout.Field(
                        "postal_code",
                        wrapper_class="col-xs-4 col-sm-5 col-md-3 col-lg-3",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "city",
                        wrapper_class="col-xs-8 col-sm-7 col-md-9 col-lg-9",
                        template="ccb_form/multifield.html"
                    )
                ),
                "country",
            ),
            layout.Fieldset(
                _("Contact person"),
                "contact_person_ind",
                "contact_person_name",
            ),
            layout.Fieldset(
                _("Contact info"),
                layout.MultiField(
                    _("Phone"),
                    layout.Field(
                        "phone_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    css_class="show-labels"
                ),
                layout.MultiField(
                    _("Fax"),
                    layout.Field(
                        "fax_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "fax_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    css_class="show-labels"
                ),
                "email0_address",
                "publish_emails",
                "url0_link",
            ),
            layout.Fieldset(
                _("Publishing"),
                layout.MultiField(
                    _("Publish until"),
                    layout.Field(
                        "end_dd",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "end_mm",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    layout.Field(
                        "end_yyyy",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="ccb_form/multifield.html"
                    ),
                    css_class="show-labels"
                ),
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
        )

    def clean(self):
        # if end date is specified, all fields must be specified!
        end_yyyy = self.cleaned_data.get('end_yyyy', None)
        end_mm = self.cleaned_data.get('end_mm', None)
        end_dd = self.cleaned_data.get('end_dd', None)

        if end_yyyy or end_mm or end_dd:
            if end_dd:
                if not end_mm:
                    self._errors['end_dd'] = [_("Please enter a valid month.")]
            try:
                end_date = datetime.date(int(end_yyyy), int(end_mm or 1), int(end_dd or 1))
            except Exception:
                self._errors['end_dd'] = [_("If you want to specify an end date, please enter a valid one.")]

        return self.cleaned_data

    def is_valid(self):
        is_valid = super(MainDataForm, self).is_valid()
        errors = self._errors
        return is_valid


class CategoriesForm(dynamicforms.Form):
    job_sectors = forms.ModelMultipleChoiceField(
        queryset=get_related_queryset(JobOffer, "job_sectors"),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        help_text="",
        label="",
    )

    tags = TagField(
        label=_("Tags"),
        help_text=_("Separate tags with commas"),
        max_length=200,
        required=False,
        widget=TagAutocomplete,
    )

    categories = ModelMultipleChoiceTreeField(
        label=_("Categories"),
        required=False,
        queryset=get_related_queryset(JobOffer, "categories").filter(level=0),
    )

    def __init__(self, *args, **kwargs):
        super(CategoriesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Categories"),
                layout.HTML(string_concat('<dt>', _("Job Sectors"), '</dt>')),
                "job_sectors",
                layout.HTML("""{% load i18n %}
                    <p class="disclaimer">{% blocktrans %}Is some category missing? You can <a href="/ticket/new-category/" target="_blank">suggest it here</a>.{% endblocktrans %}</p>
                """),
                "tags",
                layout.HTML(string_concat('<dt>', _("Categories"), '</dt>')),
                layout.Field(
                    "categories",
                    template="ccb_form/custom_widgets/checkboxselectmultipletree.html",
                ),
            ),
            bootstrap.FormActions(
                layout.HTML("""{% include "utils/step_buttons_reg.html" %}"""),
            )
        )


class ReportForm(dynamicforms.Form):
    report_kulturmanagement = forms.BooleanField(
        label=_('Report to <a href="http://kulturmanagement.net" target="_blank">Kulturmanagement.net</a>'),
        initial=False,
        required=False,
    )
    # report_creativeset = forms.BooleanField(
    #     label=_("Report to Creativeset.net"),
    #     initial=False,
    #     required=False,
    #     )
    report_talent_in_berlin = forms.BooleanField(
        label=_('Report to <a href="http://www.talent-in-berlin.de" target="_blank">talent-in-berlin.de</a>'),
        initial=False,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Report job offer"),
                layout.HTML("""{% load i18n %}
                    <p>{% trans "Please activate the checkboxes if you want to send your jobposting to one of our partners." %}</p>
                """),
                "report_kulturmanagement",
                "report_talent_in_berlin",
            ),
        )


def step_main_data_initial_data(request, **kwargs):
    institution_slug = request.GET.get('institution', None)
    initial_data = {}
    if institution_slug:
        institution = get_object_or_404(Institution, slug=institution_slug)
        initial_data['offering_institution'] = institution.pk
        contact_dict = institution.get_primary_contact()
        if contact_dict:
            initial_data['street_address'] = contact_dict['street_address']
            initial_data['street_address2'] = contact_dict['street_address2']
            initial_data['city'] = contact_dict['city']
            initial_data['postal_code'] = contact_dict['postal_code']
            initial_data['country'] = contact_dict['country']
            initial_data['phone_country'] = contact_dict.get('phone_country', '')
            initial_data['phone_area'] = contact_dict.get('phone_area', '')
            initial_data['phone_number'] = contact_dict.get('phone_number', '')
            initial_data['fax_country'] = contact_dict.get('fax_country', '')
            initial_data['fax_area'] = contact_dict.get('fax_area', '')
            initial_data['fax_number'] = contact_dict.get('fax_number', '')
            initial_data['email0_address'] = contact_dict['email0_address']
            initial_data['url0_link'] = contact_dict['url0_link']

    return initial_data


def submit_step(current_step, form_steps, form_step_data):
    if current_step == "step_main_data":
        step_main_data = form_step_data['step_main_data']
        end_yyyy = step_main_data.get('end_yyyy', None)
        end_mm = step_main_data.get('end_mm', None)
        end_dd = step_main_data.get('end_dd', None)

        if end_yyyy or end_mm or end_dd:
            try:
                step_main_data['end_date'] = datetime.date(int(end_yyyy), int(end_mm or 1), int(end_dd or 1))
            except Exception:
                pass
    return form_step_data


def save_data(form_steps, form_step_data):
    step_main_data = form_step_data['step_main_data']
    step_categories = form_step_data['step_categories']
    step_confirm_data = form_step_data['step_confirm_data']

    # institution
    offering_institution = None
    if step_main_data.get('offering_institution', None):
        offering_institution = Institution.objects.get(pk=step_main_data['offering_institution'])
    offering_institution_title = step_main_data.get('offering_institution_title', None)

    contact_person_ind = int(step_main_data.get("contact_person_ind", 0))
    # the creator is contact person
    contact_person = None
    if contact_person_ind == 0:
        contact_person = get_current_user().profile

    job_offer = JobOffer()

    job_offer.position = step_main_data.get('position', None)
    job_offer.job_type = step_main_data.get('job_type', None)
    job_offer.description = step_main_data.get('description', None)

    job_offer.offering_institution = offering_institution
    job_offer.contact_person = contact_person
    job_offer.offering_institution_title = step_main_data.get('offering_institution_title', None)
    job_offer.contact_person_name = step_main_data.get('contact_person_name', "")

    job_offer.phone0_type = PhoneType.objects.get(slug='phone')
    job_offer.phone0_country = step_main_data.get('phone_country', '')
    job_offer.phone0_area = step_main_data.get('phone_area', '')
    job_offer.phone0_number = step_main_data.get('phone_number', '')

    job_offer.phone1_type = PhoneType.objects.get(slug='fax')
    job_offer.phone1_country = step_main_data.get('fax_country', '')
    job_offer.phone1_area = step_main_data.get('fax_area', '')
    job_offer.phone1_number = step_main_data.get('fax_number', '')

    job_offer.email0_type = EmailType.objects.get(slug='email')
    job_offer.email0_address = step_main_data.get('email0_address', '')

    job_offer.url0_type = URLType.objects.get(slug='web')
    job_offer.url0_link = step_main_data.get('url0_link', '')
    job_offer.publish_emails = step_main_data.get('publish_emails', '')

    job_offer.tags = step_categories.get('tags', '')

    job_offer.status = STATUS_CODE_PUBLISHED

    end_date = step_main_data.get('end_date', None)
    if end_date:
        job_offer.published_till = end_date

    if step_confirm_data.get('report_talent_in_berlin', False):
        job_offer.talent_in_berlin = True

    job_offer.save()

    Address.objects.set_for(
        job_offer,
        "postal_address",
        country=step_main_data.get('country', None),
        city=step_main_data.get('city', None),
        street_address=step_main_data.get('street_address', None),
        street_address2=step_main_data.get('street_address2', None),
        postal_code=step_main_data.get('postal_code', None),
    )

    # job qualifications
    job_offer.qualifications.clear()
    for q in step_main_data.get('qualifications', None):
        job_offer.qualifications.add(q)

    # job sectors
    job_offer.job_sectors.clear()
    job_offer.job_sectors.add(*step_categories['job_sectors'])

    # categories
    job_offer.categories.clear()
    job_offer.categories.add(*step_categories['categories'])

    # save again without triggering any signals
    job_offer.save_base(raw=True)

    # report to third parties
    description = loader.render_to_string(
        "marketplace/emails/new_job_offer.html",
        {'object': job_offer},
    )
    recipients = []
    if step_confirm_data.get('report_kulturmanagement', False):
        recipients.append(Recipient(
            name="Kulturmanagement.net",
            email=settings.THIRD_PARTY_EMAILS['kulturmanagement.net'],
        ))
    if recipients:
        sender_name = ''
        sender_email = settings.DEFAULT_FROM_EMAIL
        send_email_using_template(
            recipients,
            "new_job_offer",
            obj_placeholders={
                'object_title': job_offer.position,
                'object_description': description,
                'object_url': job_offer.get_url(),
                'object_creator_url': job_offer.creator.profile.get_url(),
                'object_creator_title': job_offer.creator.profile.get_title(),
            },
            delete_after_sending=False,
            sender_name=sender_name,
            sender_email=sender_email,
            send_immediately=False,
        )
    # if step_confirm_data.get('report_creativeset', False):
    #     from ccb.apps.external_services.export_to_creativeset import export_job_offer_to_creativeset
    #     export_job_offer_to_creativeset(job_offer)


    form_steps['success_url'] = job_offer.get_url_path()

    return form_step_data


ADD_JOB_OFFER_FORM_STEPS = {
    'step_main_data': {
        'title': _("main data"),
        'template': "marketplace/add_job_offer_main_data.html",
        'form': MainDataForm,
        'initial_data': step_main_data_initial_data,
    },
    'step_categories': {
        'title': _("categories"),
        'template': "marketplace/add_job_offer_categories.html",
        'form': CategoriesForm,
    },
    'step_confirm_data': {
        'title': _("confirm data"),
        'template': "marketplace/add_job_offer_confirm.html",
        'form': ReportForm,
    },
    'onsubmit': submit_step,
    'onsave': save_data,
    'name': 'add_job_offer',
    'success_url': "/%s/" % URL_ID_JOB_OFFERS,
    'default_path': [
        'step_main_data',
        'step_categories',
        'step_confirm_data',
    ],
}


class JobOfferSearchForm(dynamicforms.Form):
    job_sector = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Job Sector"),
        required=False,
        queryset=get_related_queryset(JobOffer, "job_sectors"),
    )
    category = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Category"),
        required=False,
        queryset=get_related_queryset(ContextItem, "categories").filter(level=0),
    )
    job_type = ModelChoiceTreeField(
        empty_label=_("All"),
        label=_("Job Type"),
        required=False,
        queryset=get_related_queryset(JobOffer, "job_type"),
    )
    qualification = forms.ModelChoiceField(
        empty_label=_("All"),
        label=_("Qualification"),
        required=False,
        queryset=get_related_queryset(JobOffer, "qualifications"),
    )

    def __init__(self, *args, **kwargs):
        super(JobOfferSearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("job_sector", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("category", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("job_type", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("qualification", template="ccb_form/custom_widgets/filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            ),
        )
