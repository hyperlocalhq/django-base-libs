# -*- coding: UTF-8 -*-

from django.db import models
from jetson.apps.people.forms import *
from django.utils.translation import ugettext_lazy as _
from jetson.apps.people.forms import SimpleRegistrationForm as SimpleRegistrationFormBase
from jetson.apps.mailchimp.models import MList
from jetson.apps.mailchimp.models import Subscription
from jetson.apps.mailchimp.models import Settings

from base_libs.forms import dynamicforms

from mptt.forms import TreeNodeChoiceField

from mailsnake import MailSnake

class SimpleRegistrationForm(SimpleRegistrationFormBase):
    
    choose_creative_sectors = forms.BooleanField(
        initial=True,
        widget=forms.HiddenInput(
            attrs={
                "class": "form_hidden",
                }
            ),
        required=False,
        )
    
    def __init__(self, *args, **kwargs):
        super(SimpleRegistrationForm, self).__init__(*args, **kwargs)
        
        self.creative_sectors = {}
        for item in get_related_queryset(Person, "creative_sectors"):
            self.creative_sectors[item.sysname] = {
                'id' : item.id,
                'field_name' : PREFIX_CI + str(item.id),
                }
                
        for s in self.creative_sectors.values():
            self.fields[s['field_name']] =  forms.BooleanField(
                required=False
                )
        
        self.newsletter_fields = []
        for ml in MList.site_objects.filter(is_public=True):
            f = self.fields['newsletter_%s' % ml.pk] = forms.BooleanField(
                label=_("I want to subscribe to %s.") % ml.title,
                initial=True,
                required=False,
                )
            self.newsletter_fields.append(("newsletter_%s" % ml.pk, f))
        
    def clean(self):
        super(SimpleRegistrationForm, self).clean()
        cleaned = self.cleaned_data
        non_field_errors = []
        errors = False
        
        # check if at least one creative sector is chosen
        el_count = 0
        for el in self.creative_sectors.values():
            if cleaned.get(el['field_name'], False):
                el_count += 1
        if not el_count:
            non_field_errors.append(_("Please choose at least one creative sector."))
            errors = True
        
        if errors:
            # raise an error so that the form doesn't validate
            raise forms.ValidationError(non_field_errors)
            
        return cleaned


    def save(self, activate_immediately=False):
        user = super(SimpleRegistrationForm, self).save(activate_immediately=activate_immediately)
        cleaned = self.cleaned_data
        
        person = user.get_profile()
        
        selected_cs = {}
        for item in get_related_queryset(Person, "creative_sectors"):
            if cleaned.get(PREFIX_CI + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cs:
                        del(selected_cs[ancestor.id])
                # add current
                selected_cs[item.id] = item
        person.creative_sectors.clear()
        person.creative_sectors.add(*selected_cs.values())
        
        try:
            s = Settings.objects.get()
        except:
            pass
        else:
            ms = MailSnake(s.api_key)
            for ml in MList.site_objects.filter(is_public=True):
                if cleaned['newsletter_%s' % ml.pk]:
                    if s.double_optin:
                        status = "pending"
                    else:
                        status = "subscribed"
                    sub = Subscription.objects.create(
                        subscriber=user,
                        ip=self.request.META['REMOTE_ADDR'],
                        mailinglist=ml,
                        status=status,
                        )
                    if ml.mailchimp_id:
                        ms.listSubscribe(
                            id=ml.mailchimp_id,
                            email_address=sub.email,
                            merge_vars={
                                'FNAME': sub.first_name,
                                'LNAME': sub.last_name,
                                },
                            double_optin=s.double_optin,
                            update_existing=s.update_existing,
                            send_welcome=s.send_welcome,
                            )
        return user
        
        
### REGISTRATION ###

class Registration: # Namespace

    class AccountType(dynamicforms.Form):
        account_type = forms.ChoiceField(
            required=True,
            choices=((0, 'Individual'), (1, 'Institutional')),
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        is_hidden = forms.BooleanField(
            required=False,
            label=_("Do not publish the profile."),
            )
    
    class MainPersonData(dynamicforms.Form):
        prefix = forms.ChoiceField(
            required=False,
            choices=NULL_PREFIX_CHOICES,
            label=_("Prefix"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            error_messages={
                'required': _("First name is required"),
                },
            )
        last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            )
        salutation = forms.ChoiceField(
            required=False,
            choices=SALUTATION_CHOICES,
            label=_("Salutation"),
            )
        login_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            )
        login_email_confirm = forms.EmailField(
            required=True,
            label=_("Confirm E-mail"),
            help_text=_("IMPORTANT: The provided email address must be valid! You will receive your account data via this address.")
            )
        username = forms.RegexField(
            required=True,
            regex=username_re,
            label=_("Username"),
            error_messages = {
                'invalid': _("Username can only consist of letters, digits, dashes, and underscores. It should start with a letter and be not shorter than 3 symbols."),
                },
            )
        password = forms.CharField(
            widget=forms.PasswordInput,
            required=True,
            label=_("Password"),
            )
        password_confirm = forms.CharField(
            widget=forms.PasswordInput,
            required=True,
            label=_("Confirm Password"),
            )
        birthday_dd = forms.ChoiceField(
            required=True,
            choices=BIRTHDAY_DD_CHOICES,
            label=_("Birthday"),
            error_messages={
                'required': _("Day of birth is required"),
                },
            )
        birthday_mm = forms.ChoiceField(
            required=True,
            choices=BIRTHDAY_MM_CHOICES,
            label=_("Birthday"),
            error_messages={
                'required': _("Month of birth is required"),
                },
            )
        birthday_yyyy = forms.ChoiceField(
            required=True,
            choices=BIRTHDAY_YYYY_CHOICES,
            label=_("Birthday"),
            error_messages={
                'required': _("Year of birth is required"),
                },
            )
        privacy_policy = forms.BooleanField(
            required=True,
            label=_("I accept the privacy policy."),
            )
        terms_of_use = forms.BooleanField(
            required=True,
            label=_("I accept the terms of use."),
            )
        nationality = forms.ChoiceField(
            required=False,
            label=_("Nationality"),
            choices=NATIONALITY_CHOICES,
            )
        
        display_profile = forms.BooleanField(
             required=False,
             label=_("Display profile to public"),
             initial=True,
             )    
        display_username = forms.BooleanField(
            required=False,
            label=_("Display user name instead of full name"),
            initial=False,
            )
        allow_search_engine_indexing = forms.BooleanField(
            required=False,
            label=_("Allow indexing by search engines"),
            initial=True,
            )
        
        display_birthday = forms.BooleanField(
            required=False,
            label=_("Display birthday to public"),
            initial=False,
            )
        display_address = forms.BooleanField(
            required=False,
            label=_("Display address data to public"),
            initial=True,
            )
        display_phone = forms.BooleanField(
            required=False,
            label=_("Display phone numbers to public"),
            initial=True,
            )
        display_fax = forms.BooleanField(
            required=False,
            label=_("Display fax numbers to public"),
            initial=True,
            )
        display_mobile = forms.BooleanField(
            required=False,
            label=_("Display mobile phones to public"),
            initial=True,
            )
        display_im = forms.BooleanField(
            required=False,
            label=_("Display instant messangers to public"),
            initial=True,
            )
        def clean_username(self):
            username = self.cleaned_data['username']
            suggested = get_unique_value(
                User,
                username or slugify("_".join((
                    cleaned_data['first_name'],
                    cleaned_data['last_name'],
                    ))).replace("-", "_"),
                field_name="username",
                separator="_",
                )
            if username.lower() != suggested.lower():
                raise forms.ValidationError(_("This username is already used for another account. But you can use \"%s\" as your username.") % suggested)
            return username
        def clean_login_email(self):
            login_email = self.cleaned_data['login_email']
            if User.objects.filter(email=login_email).count():
                raise forms.ValidationError(_("This email address is already used for another account."))
            return login_email
        def clean_login_email_confirm(self):
            if not 'login_email' in self.cleaned_data:
                raise forms.ValidationError(_("Please, correct the error for the login email at first."))
            login_email = self.cleaned_data['login_email']
            login_email_confirm = self.cleaned_data['login_email_confirm']
            if login_email != login_email_confirm:
                raise forms.ValidationError(_("The confirmed e-mail doesn't match the e-mail."))
            return login_email
        def clean_password(self):
            password = self.cleaned_data['password']
            if len(password) <3 :
                raise forms.ValidationError(_("Passwords must be at least 3 characters long"))
            return password
        def clean_password_confirm(self):
            if not 'password' in self.cleaned_data:
                raise forms.ValidationError(_("Please, correct the error for the password at first."))
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']
            if password != password_confirm:
                raise forms.ValidationError(_("The confirmed password doesn't match the password."))
            return password
        def clean_privacy_policy(self):
            privacy_policy = self.cleaned_data['privacy_policy']
            if not privacy_policy:
                raise forms.ValidationError(_("You must accept the privacy policy to register."))
            return privacy_policy
        def clean_terms_of_use(self):
            terms_of_use = self.cleaned_data['terms_of_use']
            if not terms_of_use:
                raise forms.ValidationError(_("You must accept the terms of use to register."))
            return terms_of_use
    
    class PersonContactData(dynamicforms.Form):
        individual_type = TreeNodeChoiceField(
            required=True,
            queryset=get_related_queryset(Person, "individual_type"),
            label=_("Individual type"),
            )
        occupation = forms.CharField(
            required=False,
            label=_("Position in the company"),
            )
        institution = AutocompleteField(
            required=False,
            label=_("Company/Institution"),
            help_text=_("Please enter a letter to display a list of available institutions"),
            app="institutions", 
            qs_function="get_published_institutions",
            display_attr="title", 
            add_display_attr="get_address_string",
            options={
                "minChars": 1,
                "max": 20,
                "mustMatch": 1,
                "highlight" : False,
            }
        )
        location_type = forms.ChoiceField(
            required=True,
            label=_("Location type"),
            choices=LOCATION_TYPE_CHOICES,
            )
        location_title = forms.CharField(
            required=False,
            label=_("Location title"),
            max_length=255,
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
            error_messages={
                'required': _("City is required"),
                },
            )
        postal_code = forms.CharField(
            required=True,
            label=_("Postal Code"),
            error_messages={
                'required': _("Postal code is required"),
                },
            )
        district = forms.CharField(
            required=False,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        country = forms.ChoiceField(
            required=True,
            choices=Address._meta.get_field("country").get_choices(),
            label=_("Country"),
            )
        longitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        latitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
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
        mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        email0 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email1 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email2 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        url0_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url0_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url1_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url1_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url2_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url2_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        im0_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im0_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im1_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im1_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im2_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im2_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        
    class PersonProfile(dynamicforms.Form):
        description_en = forms.CharField(
            required=False,
            label=_("Description (English)"),
            widget=forms.Textarea,
            )
        description_de = forms.CharField(
            required=False,
            label=_("Description (German)"),
            widget=forms.Textarea,
            )
        avatar = ImageField(
            label= _("Profile photo"),
            help_text= _("You can upload GIF, JPG, PNG, TIFF, and BMP images. The minimal dimensions are %s px.") % STR_LOGO_SIZE,
            required=False,
            min_dimensions=LOGO_SIZE,
            )
    
    class PersonCategories(dynamicforms.Form):
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
            
        def __init__(self, *args, **kwargs):
            super(Registration.PersonCategories, self).__init__(*args, **kwargs)
            
            self.creative_sectors = {}
            for item in get_related_queryset(Person, "creative_sectors"):
                self.creative_sectors[item.sysname] = {
                    'id' : item.id,
                    'field_name' : PREFIX_CI + str(item.id),
                    }
            
            self.context_categories = {}
            for item in get_related_queryset(Person, "context_categories"):
                self.context_categories[item.sysname] = {
                    'id' : item.id,
                    'field_name' : PREFIX_BC + str(item.id),
                    }
            
            for s in self.creative_sectors.values():
                self.fields[s['field_name']] =  forms.BooleanField(
                    required=False
                    )
            
            for c in self.context_categories.values():
                self.fields[c['field_name']] =  forms.BooleanField(
                    required=False
                    )
    
    class InstitutionCategories(dynamicforms.Form):
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
            
        def __init__(self, *args, **kwargs):
            super(Registration.InstitutionCategories, self).__init__(*args, **kwargs)
            
            self.creative_sectors = {}
            for item in get_related_queryset(Institution, "creative_sectors"):
                self.creative_sectors[item.sysname] = {
                    'id' : item.id,
                    'field_name' : PREFIX_CI + str(item.id),
                    }
            
            self.context_categories = {}
            for item in get_related_queryset(Institution, "context_categories"):
                self.context_categories[item.sysname] = {
                    'id' : item.id,
                    'field_name' : PREFIX_BC + str(item.id),
                    }
            
            self.object_types = {}
            for item in get_related_queryset(Institution, "institution_types"):
                self.object_types[item.sysname] = {
                    'id' : item.id,
                    'field_name' : PREFIX_OT + str(item.id),
                    }
            
            for s in self.creative_sectors.values():
                self.fields[s['field_name']] =  forms.BooleanField(
                    required=False
                    )
            
            for c in self.context_categories.values():
                self.fields[c['field_name']] =  forms.BooleanField(
                    required=False
                    )
            
            for t in self.object_types.values():
                self.fields[t['field_name']] =  forms.BooleanField(
                    required=False
                    )
                
    class InstitutionOpeningHoursPayment(dynamicforms.Form):
        """
        Form for opening ours and payment data
        """

        show_breaks = forms.BooleanField(
            required=False,                                 
            label=_("Morning/Afternoon"),
            initial=False,
        )
        
        is_appointment_based = forms.BooleanField(
            label=_("Visiting by Appointment"),
            required=False,
            initial=False,
        )
        
        mon_open0 = forms.TimeField(required=False)
        mon_close0 = forms.TimeField(required=False)
        mon_open1 = forms.TimeField(required=False)
        mon_close1 = forms.TimeField(required=False)
        mon_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        tue_open0 = forms.TimeField(required=False)
        tue_close0 = forms.TimeField(required=False)
        tue_open1 = forms.TimeField(required=False)
        tue_close1 = forms.TimeField(required=False)
        tue_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
    
        wed_open0 = forms.TimeField(required=False)
        wed_close0 = forms.TimeField(required=False)
        wed_open1 = forms.TimeField(required=False)
        wed_close1 = forms.TimeField(required=False)
        wed_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        thu_open0 = forms.TimeField(required=False)
        thu_close0 = forms.TimeField(required=False)
        thu_open1 = forms.TimeField(required=False)
        thu_close1 = forms.TimeField(required=False)
        thu_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        fri_open0 = forms.TimeField(required=False)
        fri_close0 = forms.TimeField(required=False)
        fri_open1 = forms.TimeField(required=False)
        fri_close1 = forms.TimeField(required=False)
        fri_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sat_open0 = forms.TimeField(required=False)
        sat_close0 = forms.TimeField(required=False)
        sat_open1 = forms.TimeField(required=False)
        sat_close1 = forms.TimeField(required=False)
        sat_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        sun_open0 = forms.TimeField(required=False)
        sun_close0 = forms.TimeField(required=False)
        sun_open1 = forms.TimeField(required=False)
        sun_close1 = forms.TimeField(required=False)
        sun_is_closed = forms.BooleanField(
            label=_("Closed"),
            required=False,
            initial=False,
            )
        
        exceptions_en = forms.CharField(
            label=_('Exceptions for working hours (English)'),
            required=False,
            widget=forms.Textarea,
            )
        exceptions_de = forms.CharField(
            label=_('Exceptions for working hours (German)'),
            required=False,
            widget=forms.Textarea,
            )
        
        # Payment
        is_card_visa_ok = forms.BooleanField(
            label=_("Visa"),
            required=False,
            initial=False,
        )
        
        is_card_mastercard_ok = forms.BooleanField(
            label=_("MasterCard"),
            required=False,
            initial=False,
        )

        is_card_americanexpress_ok = forms.BooleanField(
            label=_("American Express"),
            required=False,
            initial=False,
        )        

        is_paypal_ok = forms.BooleanField(
            label=_("PayPal"),
            required=False,
            initial=False,
        )  
        
        is_cash_ok = forms.BooleanField(
            label=_("Cash"),
            required=False,
            initial=False,
        )  

        is_transaction_ok = forms.BooleanField(
            label=_("Bank transfer"),
            required=False,
            initial=False,
        )
        
        is_prepayment_ok = forms.BooleanField(
            label=_("Prepayment"),
            required=False,
            initial=False,
        )
        
        is_on_delivery_ok = forms.BooleanField(
            label=_("Payment on delivery"),
            required=False,
            initial=False,
        )  

        is_invoice_ok = forms.BooleanField(
            label=_("Invoice"),
            required=False,
            initial=False,
        )  

        is_ec_maestro_ok = forms.BooleanField(
            label=_("EC Maestro"),
            required=False,
            initial=False,
        )  
        
        is_giropay_ok = forms.BooleanField(
            label=_("Giropay"),
            required=False,
            initial=False,
        )  
        
        def clean(self):
            
            show_breaks = self.cleaned_data.get('show_breaks', False)
            for week_day in WEEK_DAYS:

                is_closed = self.cleaned_data.get(week_day + '_is_closed', False)
                open0 = self.cleaned_data.get(week_day + '_open0', None)
                close0 = self.cleaned_data.get(week_day + '_close0', None)
                open1 = self.cleaned_data.get(week_day + '_open1', None)
                close1 = self.cleaned_data.get(week_day + '_close1', None)
                    
                # here, we apply opening hours and do some checks
                if not is_closed:
                    if open0:
                        if not close0:
                            self._errors[week_day + '_open0'] = [_("Please enter a closing time.")]
                        elif close0 < open0:
                            self._errors[week_day + '_open0'] = [_("A closing time must not be before an opening time.")]
                    if close0:
                        if not open0:
                            self._errors[week_day + '_open0'] = [_("Please enter an opening time.")]
                    
                    if show_breaks:
                        if open1:
                            if not close1:
                                self._errors[week_day + '_open1'] = [_("Please enter a closing time.")]
                            elif close1 < open1:
                                self._errors[week_day + '_open1'] = [_("A closing time must not be before an opening time.")]
                        if close1:
                            if not open1:
                                self._errors[week_day + '_open1'] = [_("Please enter an opening time.")]
                        
                        if open1 or close1:
                            if not open0 or not close0:
                                self._errors[week_day + '_open1']  = [_("When specifying breaks, you must enter all data.")]
                            else:
                                if open1 < close0:
                                    self._errors[week_day + '_open1']  = [_("An opening time after break must not be before the closing time to break.")]
                        
                        if open0 and open1 and close0 and close1:
                           self.cleaned_data[week_day + '_open'] = open0
                           self.cleaned_data[week_day + '_break_close'] = close0
                           self.cleaned_data[week_day + '_break_open'] = open1
                           self.cleaned_data[week_day + '_close'] = close1
                        elif open0 and close0:
                           self.cleaned_data[week_day + '_open'] = open0
                           self.cleaned_data[week_day + '_close'] = close0
                    else:
                        if open0 and close0:
                           self.cleaned_data[week_day + '_open'] = open0
                           self.cleaned_data[week_day + '_close'] = close0
                        
            return self.cleaned_data                
    
    class MainInstitutionData(dynamicforms.Form):
        institution_name = forms.CharField(
            required=True,
            label=_("Institution Name"),
            )
        
        institution_name2 = forms.CharField(
            required=False,
            label=_("Institution Name 2nd line"),
            )

        legal_form = forms.ChoiceField(
            required=True,
            choices=LEGAL_FORM_CHOICES,
            label=_("Legal Form"),
            )
    
        prefix = forms.ChoiceField(
            required=True,
            choices=NULL_PREFIX_CHOICES,
            label=_("Prefix"),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            error_messages={
                'required': _("First name is required"),
                },
            )
        last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            )
        salutation = forms.ChoiceField(
            required=False,
            choices=SALUTATION_CHOICES,
            label=_("Salutation"),
            )
        individual_type = TreeNodeChoiceField(
            required=True,
            queryset=get_related_queryset(Person, "individual_type"),
            label=_("Status"),
            )
        
        login_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            )
        login_email_confirm = forms.EmailField(
            required=True,
            label=_("Confirm E-mail"),
            help_text=_("IMPORTANT: The provided email address must be valid! You will receive your account data via this address.")
            #help_text=_("WICHTIG: Diese angegebene Email-Adresse muss gültig sein, damit wir Ihnen die Zugangsdaten zu Ihrem Profil zusenden können.")
            )
        username = forms.RegexField(
            required=True,
            regex=username_re,
            error_messages = {
                'invalid': _("Username can only consist of letters, digits, dashes, and underscores. It should start with a letter and be not shorter than 3 symbols."),
                },
            label=_("Username"),
            )
        password = forms.CharField(
            widget=forms.PasswordInput,
            required=True,
            label=_("Password"),
            )
        password_confirm = forms.CharField(
            widget=forms.PasswordInput,
            required=True,
            label=_("Confirm Password"),
            )
        birthday_dd = forms.ChoiceField(
            required=True,
            choices=BIRTHDAY_DD_CHOICES,
            label=_("Birthday"),
            error_messages={
                'required': _("Day of birth is required"),
                },
            )
        birthday_mm = forms.ChoiceField(
            required=True,
            choices=BIRTHDAY_MM_CHOICES,
            label=_("Birthday"),
            error_messages={
                'required': _("Month of birth is required"),
                },
            )
        birthday_yyyy = forms.ChoiceField(
            required=True,
            choices=BIRTHDAY_YYYY_CHOICES,
            label=_("Birthday"),
            error_messages={
                'required': _("Year of birth is required"),
                },
            )
        privacy_policy = forms.BooleanField(
            required=True,
            label=_("I accept the privacy policy."),
            )
        terms_of_use = forms.BooleanField(
            required=True,
            label=_("I accept the terms of use."),
            )
        occupation = forms.CharField(
            required=True,
            label=_("Position in the company"),
            )
        nationality = forms.ChoiceField(
            required=False,
            label=_("Nationality"),
            choices=NATIONALITY_CHOICES,
            )
        
        def clean_username(self):
            username = self.cleaned_data['username']
            suggested = get_unique_value(
                User,
                username or slugify("_".join((
                    cleaned_data['first_name'],
                    cleaned_data['last_name'],
                    ))).replace("-", "_"),
                field_name="username",
                separator="_",
                )
            if username.lower() != suggested.lower():
                raise forms.ValidationError(_("This username is already used for another account. But you can use \"%s\" as your username.") % suggested)
            return username
        def clean_login_email(self):
            login_email = self.cleaned_data['login_email']
            if User.objects.filter(email=login_email).count():
                raise forms.ValidationError(_("This email address is already used for another account."))
            return login_email
        def clean_login_email_confirm(self):
            if not 'login_email' in self.cleaned_data:
                raise forms.ValidationError(_("Please, correct the error for the login email at first."))
            login_email = self.cleaned_data['login_email']
            login_email_confirm = self.cleaned_data['login_email_confirm']
            if login_email != login_email_confirm:
                raise forms.ValidationError(_("The confirmed e-mail doesn't match the e-mail."))
            return login_email
        def clean_password(self):
            password = self.cleaned_data['password']
            if len(password) <3 :
                raise forms.ValidationError(_("Passwords must be at least 3 characters long"))
            return password
        def clean_password_confirm(self):
            if not 'password' in self.cleaned_data:
                raise forms.ValidationError(_("Please, correct the error for the password at first."))
            password = self.cleaned_data['password']
            password_confirm = self.cleaned_data['password_confirm']
            if password != password_confirm:
                raise forms.ValidationError(_("The confirmed password doesn't match the password."))
            return password
        def clean_privacy_policy(self):
            privacy_policy = self.cleaned_data['privacy_policy']
            if not privacy_policy:
                raise forms.ValidationError(_("You must accept the privacy policy to register."))
            return privacy_policy
        def clean_terms_of_use(self):
            terms_of_use = self.cleaned_data['terms_of_use']
            if not terms_of_use:
                raise forms.ValidationError(_("You must accept the terms of use to register."))
            return terms_of_use
    
    class InstitutionContactData(dynamicforms.Form):
        
        establishment_yyyy = forms.ChoiceField(
            required=False, #should be required=True ???
            choices=ESTABLISHMENT_YYYY_CHOICES,
            label=_("Establishment"),
            error_messages={
                'required': _("Year of establishment is required"),
                },
            )
        
        establishment_mm = forms.ChoiceField(
            required=False, #should be required=True ???
            choices=ESTABLISHMENT_MM_CHOICES,
            label=_("Establishment"),
            error_messages={
                'required': _("Month of establishment is required"),
                },
            )
        
        nof_employees = forms.IntegerField(
            required=False,
            label=_("Number of Employees")
            )
        
        location_type = forms.ChoiceField(
            required=True,
            label=_("Location type"),
            choices=INSTITUTION_LOCATION_TYPE_CHOICES,
            )
        location_title = forms.CharField(
            required=False,
            label=_("Location title"),
            max_length=255,
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
            error_messages={
                'required': _("City is required"),
                },
            )
        postal_code = forms.CharField(
            required=True,
            label=_("Postal Code"),
            error_messages={
                'required': _("Postal code is required"),
                },
            )
        district = forms.CharField(
            required=False,
            widget=forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        country = forms.ChoiceField(
            required=True,
            choices=Address._meta.get_field("country").get_choices(),
            label=_("Country"),
            )
        longitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
            )
        latitude = forms.CharField(
            required=False,
            widget = forms.HiddenInput(
                attrs={
                    "class": "form_hidden",
                    }
                ),
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
        mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        email0 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email1 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        email2 = forms.EmailField(
            required=False,
            label=_("E-mail"),
            )
        url0_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url0_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url1_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url1_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        url2_type = forms.ChoiceField(
            required=False,
            choices=URL_TYPE_CHOICES,
            label=_("Type"),
            )
        url2_link = forms.URLField(
            required=False,
            label=_("URL"),
            )
        im0_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im0_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im1_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im1_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        im2_type = forms.ChoiceField(
            required=False,
            choices=IM_TYPE_CHOICES,
            label=_("Type"),
            )
        im2_address = forms.CharField(
            required=False,
            max_length=255,
            label=_("Address"),
            )
        
        def clean_nof_employees(self):
            nof_employees = self.cleaned_data['nof_employees']
            if nof_employees and nof_employees < 0:
                raise forms.ValidationError(_("Please enter a positive integer value"))
            return nof_employees
        
        def clean_establishment_mm(self):
            establishment_yyyy = self.cleaned_data.get('establishment_yyyy', None)
            establishment_mm = self.cleaned_data.get('establishment_mm', None)
            if establishment_mm and not establishment_yyyy:
                raise forms.ValidationError(_("Please enter a valid year"))
            return establishment_mm
        
    class InstitutionContactPersons(dynamicforms.Form):
        # main administrator
        p0_prefix = forms.CharField(
            required=True,
            label=_("Prefix"),
            widget=forms.TextInput(
                attrs={'readonly': 'readonly'}
                ),
            error_messages={
                'required': _("Prefix is required"),
                },
            )
        p0_first_name = forms.CharField(
            required=True,
            label=_("First Name"),
            widget=forms.TextInput(
                attrs={'readonly': 'readonly'}
                ),
            )
        p0_last_name = forms.CharField(
            required=True,
            label=_("Last Name"),
            widget=forms.TextInput(
                attrs={'readonly': 'readonly'}
                ),
            )
        p0_position = forms.CharField(
            required=True,
            label=_("Position/Occupation"),
            widget=forms.TextInput(
                attrs={'readonly': 'readonly'}
                ),
            )
        p0_email = forms.EmailField(
            required=True,
            label=_("E-mail"),
            widget=forms.TextInput(
                attrs={'readonly': 'readonly'}
                ),
            )
        p0_phone_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p0_phone_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p0_phone_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Phone"),
            )
        p0_fax_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p0_fax_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p0_fax_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Fax"),
            )
        p0_mobile_country = forms.CharField(
            required=False,
            max_length=4,
            initial="49",
            )
        p0_mobile_area = forms.CharField(
            required=False,
            max_length=5,
            )
        p0_mobile_number = forms.CharField(
            required=False,
            max_length=15,
            label=_("Mobile"),
            )
        p0_display_birthday = forms.BooleanField(
            required=False,
            label=_("Display birthday to public"),
            initial=False,
            )
        p0_display_address = forms.BooleanField(
            required=False,
            label=_("Display address data to public"),
            initial=True,
            )
        p0_display_phone = forms.BooleanField(
            required=False,
            label=_("Display phone numbers to public"),
            initial=True,
            )
        p0_display_fax = forms.BooleanField(
            required=False,
            label=_("Display fax numbers to public"),
            initial=True,
            )
        p0_display_mobile = forms.BooleanField(
            required=False,
            label=_("Display mobile phones to public"),
            initial=True,
            )
        p0_display_im = forms.BooleanField(
            required=False,
            label=_("Display instant messangers to public"),
            initial=True,
            )
            
    def submit_step(current_step, form_steps, form_step_data):
        if current_step == 0:
            if form_step_data[current_step]['account_type'] == '0':
                form_step_data['path'] = [0,101,102,104,303,305,]
            else:
                form_step_data['path'] = [0,201,202,205,204,303,203,305,]
        elif current_step == 101:
            if 102 not in form_step_data:
                form_step_data[102] = {}
            if "email0" not in form_step_data[102] or not form_step_data[102]:
                form_step_data[102]['email0'] = form_step_data[101]['login_email']
        elif current_step == 201:
            if 205 not in form_step_data:
                form_step_data[205] ={}
            form_step_data[205]['p0_prefix'] = form_step_data[current_step]['get_prefix_display']
            form_step_data[205]['p0_first_name'] = form_step_data[current_step]['first_name']
            form_step_data[205]['p0_last_name'] = form_step_data[current_step]['last_name']
            form_step_data[205]['p0_position'] = form_step_data[current_step]['occupation']
            form_step_data[205]['p0_email'] = form_step_data[current_step]['login_email']
        elif current_step == 202:    
            if 205 not in form_step_data:
                form_step_data[205] ={}
            if not form_step_data[205].get('p0_phone_number', False):
                form_step_data[205]['p0_phone_country'] = form_step_data[current_step]['phone_country']
                form_step_data[205]['p0_phone_area'] = form_step_data[current_step]['phone_area']
                form_step_data[205]['p0_phone_number'] = form_step_data[current_step]['phone_number']
            if not form_step_data[205].get('p0_fax_number', False):
                form_step_data[205]['p0_fax_country'] = form_step_data[current_step]['fax_country']
                form_step_data[205]['p0_fax_area'] = form_step_data[current_step]['fax_area']
                form_step_data[205]['p0_fax_number'] = form_step_data[current_step]['fax_number']
            if not form_step_data[205].get('p0_mobile_number', False):
                form_step_data[205]['p0_mobile_country'] = form_step_data[current_step]['mobile_country']
                form_step_data[205]['p0_mobile_area'] = form_step_data[current_step]['mobile_area']
                form_step_data[205]['p0_mobile_number'] = form_step_data[current_step]['mobile_number']
        elif current_step == 205:
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
                        form_step_data[current_step]["p%d_prefix" % i] = p.prefix_id
                        form_step_data[current_step]["get_p%d_prefix_display" % i] = force_unicode(p.prefix.get_title())
                        form_step_data[current_step]["p%d_first_name" % i] = p.user.first_name
                        form_step_data[current_step]["p%d_last_name" % i] = p.user.last_name
                        
        return form_step_data
    submit_step = staticmethod(submit_step)
    
    def save_data(form_steps, form_step_data):
        existing_additional_contacts = []
        new_additional_contacts = []
        institution = None
        if form_step_data[0]['account_type'] == '0':
            username = get_unique_value(
                User,
                slugify(form_step_data[101].get(
                    'username',
                    "_".join((
                        form_step_data[101]['first_name'],
                        form_step_data[101]['last_name'],
                        )),
                    )).replace("-", "_"),
                field_name="username",
                separator="_",
                )
            password = form_step_data[101]['password']
            user = User.objects.create_user(
                username,
                form_step_data[101]['login_email'],
                password,
                )
            user.first_name = form_step_data[101].get('first_name', '')
            user.last_name = form_step_data[101].get('last_name', '')
            user.is_active = False
            user.save()
            try:
                prefix = Prefix.objects.get(pk=int(form_step_data[101].get('prefix', 0)))
            except:
                prefix = None
            
            #init the status from display_profile checkbox    
            display_profile=form_step_data[101].get('display_profile', True)
            if display_profile:
                status = "published"
            else:
                status = "not_listed"
                            
            person, created = Person.objects.get_or_create(user=user)
            person.prefix_id=form_step_data[101].get('prefix', None)
            person.salutation_id=form_step_data[101].get('salutation', None)
            person.birthday_dd=form_step_data[101].get('birthday_dd', None)
            person.birthday_mm=form_step_data[101].get('birthday_mm', None)
            person.birthday_yyyy=form_step_data[101].get('birthday_yyyy', None)
            person.individual_type=form_step_data[102].get('individual_type', None)
            person.occupation=form_step_data[102].get('occupation', "")
            person.nationality_id=form_step_data[101].get('nationality', None)
            person.description_en=form_step_data[303].get('description_en', None)
            person.description_de=form_step_data[303].get('description_de', None)
            person.display_username=form_step_data[101].get('display_username', False)
            person.allow_search_engine_indexing=form_step_data[101].get('allow_search_engine_indexing', True)
            person.display_birthday=form_step_data[101].get('display_birthday', True)
            person.display_address=form_step_data[101].get('display_address', True)
            person.display_phone=form_step_data[101].get('display_phone', True)
            person.display_fax=form_step_data[101].get('display_fax', True)
            person.display_mobile=form_step_data[101].get('display_mobile', True)
            person.display_im=form_step_data[101].get('display_im', True)
            person.status=status
            if prefix:
                person.gender=person.prefix.gender
            if form_step_data[0].get('is_hidden', False):
                person.status = "not_listed"
            person.save()
            
            individual_contact = person.individualcontact_set.create(
                location_type_id=form_step_data[102].get('location_type', None),
                institution_id=form_step_data[102].get('institution', None),
                is_primary=True,
                phone0_type=PhoneType.objects.get(slug='phone'),
                phone0_country=form_step_data[102].get('phone_country', ''),
                phone0_area=form_step_data[102].get('phone_area', ''),
                phone0_number=form_step_data[102].get('phone_number', ''),
                phone1_type=PhoneType.objects.get(slug='fax'),
                phone1_country=form_step_data[102].get('fax_country', ''),
                phone1_area=form_step_data[102].get('fax_area', ''),
                phone1_number=form_step_data[102].get('fax_number', ''),
                phone2_type=PhoneType.objects.get(slug='mobile'),
                phone2_country=form_step_data[102].get('mobile_country', ''),
                phone2_area=form_step_data[102].get('mobile_area', ''),
                phone2_number=form_step_data[102].get('mobile_number', ''),
                url0_type_id=form_step_data[102].get('url0_type', None),
                url1_type_id=form_step_data[102].get('url1_type', None),
                url2_type_id=form_step_data[102].get('url2_type', None),
                url0_link=form_step_data[102].get('url0_link', ''),
                url1_link=form_step_data[102].get('url1_link', ''),
                url2_link=form_step_data[102].get('url2_link', ''),
                im0_type_id=form_step_data[102].get('im0_type', None),
                im1_type_id=form_step_data[102].get('im1_type', None),
                im2_type_id=form_step_data[102].get('im2_type', None),
                im0_address=form_step_data[102].get('im0_address', ''),
                im1_address=form_step_data[102].get('im1_address', ''),
                im2_address=form_step_data[102].get('im2_address', ''),
                email0_address=form_step_data[102].get('email0_address', user.email),
                email1_address=form_step_data[102].get('email1_address', ''),
                email2_address=form_step_data[102].get('email2_address', ''),
                )
            Address.objects.set_for(
                individual_contact,
                "postal_address",
                country=form_step_data[102].get('country', ''),
                city=form_step_data[102].get('city', ''),
                district=form_step_data[102].get('district', ''),
                street_address=form_step_data[102].get('street_address', ''),
                street_address2=form_step_data[102].get('street_address2', ''),
                postal_code=form_step_data[102].get('postal_code', ''),
                latitude=form_step_data[102].get('latitude', ''),
                longitude=form_step_data[102].get('longitude', ''),
                )
            
            
            cleaned = form_step_data[104]
            selected_cs = {}
            for item in Term.objects.filter(
                vocabulary__sysname='categories_creativesectors',
                ):
                if cleaned.get(PREFIX_CI + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cs:
                            del(selected_cs[ancestor.id])
                    # add current
                    selected_cs[item.id] = item
            person.creative_sectors.add(*selected_cs.values())
            
            selected_cc = {}
            for item in ContextCategory.objects.filter(is_applied4person=True):
                if cleaned.get(PREFIX_BC + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cc:
                            del(selected_cc[ancestor.id])
                    # add current
                    selected_cc[item.id] = item
            person.context_categories.add(*selected_cc.values())
        else:
            username = get_unique_value(
                User,
                slugify(form_step_data[201].get(
                    'username',
                    "_".join((
                        form_step_data[201]['first_name'],
                        form_step_data[201]['last_name'],
                        )),
                    )).replace("-", "_"),
                field_name="username",
                separator="_",
                )
            password = form_step_data[201]['password']
            user = User.objects.create_user(
                username,
                form_step_data[201]['login_email'],
                password,
                )
            user.first_name = form_step_data[201].get('first_name', '')
            user.last_name = form_step_data[201].get('last_name', '')
            user.is_active = False
            user.save()
            try:
                prefix = Prefix.objects.get(pk=int(form_step_data[201].get('prefix', 0)))
            except:
                prefix = None
                
            #init the status from display_profile checkbox    
            display_profile=form_step_data[101].get('display_profile', True)
            if display_profile:
                status = "published"
            else:
                status = "not_listed"
                                
            person, created = Person.objects.get_or_create(user=user)
            person.prefix_id=form_step_data[201].get('prefix', None)
            person.salutation_id=form_step_data[201].get('salutation', None)
            person.birthday_dd=form_step_data[201].get('birthday_dd', None)
            person.birthday_mm=form_step_data[201].get('birthday_mm', None)
            person.birthday_yyyy=form_step_data[201].get('birthday_yyyy', None)
            person.individual_type=form_step_data[201].get('individual_type', None)
            person.occupation=form_step_data[201].get('occupation', "")
            person.nationality_id=form_step_data[201].get('nationality', None)
            person.description_en=form_step_data[303].get('description_en', None)
            person.description_de=form_step_data[303].get('description_de', None)
            person.display_username=form_step_data[205].get('display_username', False)
            person.allow_search_engine_indexing=form_step_data[205].get('allow_search_engine_indexing', True)
            person.display_birthday=form_step_data[205].get('display_birthday', True)
            person.display_address=form_step_data[205].get('display_address', True)
            person.display_phone=form_step_data[205].get('display_phone', True)
            person.display_fax=form_step_data[205].get('display_fax', True)
            person.display_mobile=form_step_data[205].get('display_mobile', True)
            person.display_im=form_step_data[205].get('display_im', True)
            person.status=status
            if prefix:
                person.gender=person.prefix.gender
            person.save()
    
            institution = Institution(
                title=form_step_data[201].get('institution_name', ''),
                title2=form_step_data[201].get('institution_name2', ''),
                slug=get_unique_value(Institution, slugify(form_step_data[201].get('institution_name', '')).replace("-","_"), separator="_"),
                )
            LegalForm = models.get_model("institutions", "LegalForm")
            institution.legal_form = LegalForm.objects.get(
                id=form_step_data[201]['legal_form'],
                )
            
            # opening hours
            for f in ("open", "break_close", "break_open", "close"):
                for d in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
                    setattr(
                        institution,
                        "%s_%s" % (d, f),
                        form_step_data[203].get('%s_%s' % (d, f), None)
                        )
                    
            institution.exceptions_en = form_step_data[203].get('exceptions_en', '')
            institution.exceptions_de = form_step_data[203].get('exceptions_de', '')
            institution.is_appointment_based = form_step_data[203].get('is_appointment_based', False)

            # payment
            institution.is_card_visa_ok = form_step_data[203].get('is_card_visa_ok', None) 
            institution.is_card_mastercard_ok = form_step_data[203].get('is_card_mastercard_ok', None) 
            institution.is_card_americanexpress_ok = form_step_data[203].get('is_card_americanexpress_ok', None)
            institution.is_paypal_ok = form_step_data[203].get('is_paypal_ok', None)
            institution.is_cash_ok = form_step_data[203].get('is_cash_ok', None)
            institution.is_transaction_ok = form_step_data[203].get('is_transaction_ok', None)
            institution.is_prepayment_ok = form_step_data[203].get('is_prepayment_ok', None)
            institution.is_on_delivery_ok = form_step_data[203].get('is_on_delivery_ok', None)
            institution.is_invoice_ok = form_step_data[203].get('is_invoice_ok', None)
            institution.is_ec_maestro_ok = form_step_data[203].get('is_ec_maestro_ok', None)
            institution.is_giropay_ok = form_step_data[203].get('is_giropay_ok', None)

            institution.establishment_yyyy = form_step_data[202].get('establishment_yyyy', None)
            institution.establishment_mm = form_step_data[202].get('establishment_mm', None)
            institution.nof_employees = form_step_data[202].get('nof_employees', None)
            
            institution.save()
            
            institutional_contact = institution.institutionalcontact_set.create(
                location_type_id=form_step_data[202].get('location_type', ''),
                location_title=form_step_data[201].get('institution_name', ''),
                is_primary=True,
                is_temporary=False,
                phone0_type=PhoneType.objects.get(slug='phone'),
                phone0_country=form_step_data[202].get('phone_country', ''),
                phone0_area=form_step_data[202].get('phone_area', ''),
                phone0_number=form_step_data[202].get('phone_number', ''),
                phone1_type=PhoneType.objects.get(slug='fax'),
                phone1_country=form_step_data[202].get('fax_country', ''),
                phone1_area=form_step_data[202].get('fax_area', ''),
                phone1_number=form_step_data[202].get('fax_number', ''),
                url0_type_id=form_step_data[202].get('url0_type', None),
                url1_type_id=form_step_data[202].get('url1_type', None),
                url2_type_id=form_step_data[202].get('url2_type', None),
                url0_link=form_step_data[202].get('url0_link', ''),
                url1_link=form_step_data[202].get('url1_link', ''),
                url2_link=form_step_data[202].get('url2_link', ''),
                im0_type_id=form_step_data[202].get('im0_type', None),
                im1_type_id=form_step_data[202].get('im1_type', None),
                im2_type_id=form_step_data[202].get('im2_type', None),
                im0_address=form_step_data[202].get('im0_address', ''),
                im1_address=form_step_data[202].get('im1_address', ''),
                im2_address=form_step_data[202].get('im2_address', ''),
                email0_address=form_step_data[202].get('email0_address', ''),
                email1_address=form_step_data[202].get('email1_address', ''),
                email2_address=form_step_data[202].get('email2_address', ''),
                )
            Address.objects.set_for(
                institutional_contact,
                "postal_address",
                country=form_step_data[202].get('country', ''),
                district=form_step_data[202].get('district', ''),
                city=form_step_data[202].get('city', ''),
                street_address=form_step_data[202].get('street_address', ''),
                street_address2=form_step_data[202].get('street_address2', ''),
                postal_code=form_step_data[202].get('postal_code', ''),
                latitude=form_step_data[202].get('latitude', ''),
                longitude=form_step_data[202].get('longitude', ''),
                )
            individual_contact = person.individualcontact_set.create(
                location_type=IndividualLocationType.objects.all()[0],
                is_primary=True,
                institution=institution,
                phone0_type=PhoneType.objects.get(slug='phone'),
                phone0_country=form_step_data[205].get('p0_phone_country', ''),
                phone0_area=form_step_data[205].get('p0_phone_area', ''),
                phone0_number=form_step_data[205].get('p0_phone_number', ''),
                phone1_type=PhoneType.objects.get(slug='fax'),
                phone1_country=form_step_data[205].get('p0_fax_country', ''),
                phone1_area=form_step_data[205].get('p0_fax_area', ''),
                phone1_number=form_step_data[205].get('p0_fax_number', ''),
                phone2_type=PhoneType.objects.get(slug='mobile'),
                phone2_country=form_step_data[205].get('p0_mobile_country', ''),
                phone2_area=form_step_data[205].get('p0_mobile_area', ''),
                phone2_number=form_step_data[205].get('p0_mobile_number', ''),
                url0_type_id=form_step_data[202].get('url0_type', None),
                url1_type_id=form_step_data[202].get('url1_type', None),
                url2_type_id=form_step_data[202].get('url2_type', None),
                url0_link=form_step_data[202].get('url0_link', ''),
                url1_link=form_step_data[202].get('url1_link', ''),
                url2_link=form_step_data[202].get('url2_link', ''),
                im0_type_id=form_step_data[202].get('im0_type', None),
                im1_type_id=form_step_data[202].get('im1_type', None),
                im2_type_id=form_step_data[202].get('im2_type', None),
                im0_address=form_step_data[202].get('im0_address', ''),
                im1_address=form_step_data[202].get('im1_address', ''),
                im2_address=form_step_data[202].get('im2_address', ''),
                email0_address=form_step_data[202].get('email0_address', user.email),
                email1_address=form_step_data[202].get('email1_address', ''),
                email2_address=form_step_data[202].get('email2_address', ''),
                )
            Address.objects.set_for(
                individual_contact,
                "postal_address",
                country=form_step_data[202].get('country', ''),
                district=form_step_data[202].get('district', ''),
                city=form_step_data[202].get('city', ''),
                street_address=form_step_data[202].get('street_address', ''),
                street_address2=form_step_data[202].get('street_address2', ''),
                postal_code=form_step_data[202].get('postal_code', ''),
                latitude=form_step_data[202].get('latitude', ''),
                longitude=form_step_data[202].get('longitude', ''),
                )
            
            if "jetson.apps.groups_networks" in settings.INSTALLED_APPS:
                from jetson.apps.groups_networks.models import PersonGroup, GroupMembership
                group = PersonGroup(
                    title = institution.title,
                    slug = institution.slug,
                    is_by_invitation = True,
                    group_type = get_related_queryset(
                        PersonGroup,
                        "group_type"
                        ).get(
                            sysname="institutional",
                            ),
                    access_type = get_related_queryset(
                        PersonGroup,
                        "access_type"
                        ).get(
                            sysname="secret_access",
                            ),
                    )
                group.content_object = institution
                group.save()
                membership = GroupMembership.objects.create(
                    user = person.user,
                    person_group = group,
                    role = "owners",
                    inviter = user,
                    confirmer = user,
                    is_accepted = True,
                    )
            
            cleaned = form_step_data[204]
            selected_cs = {}
            for item in Term.objects.filter(
                vocabulary__sysname='categories_creativesectors',
                ):
                if cleaned.get(PREFIX_CI + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cs:
                            del(selected_cs[ancestor.id])
                    # add current
                    selected_cs[item.id] = item
            person.creative_sectors.add(*selected_cs.values())
            institution.creative_sectors.add(*selected_cs.values())
            
            selected_cc = {}
            for item in ContextCategory.objects.filter(is_applied4person=True):
                if cleaned.get(PREFIX_BC + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_cc:
                            del(selected_cc[ancestor.id])
                    # add current
                    selected_cc[item.id] = item
            person.context_categories.add(*selected_cc.values())
            institution.context_categories.add(*selected_cc.values())
            
            selected_ot = {}
            InstitutionType = models.get_model("institutions", "InstitutionType")
            for item in InstitutionType.objects.all():
                if cleaned.get(PREFIX_OT + str(item.id), False):
                    # remove all the parents
                    for ancestor in item.get_ancestors():
                        if ancestor.id in selected_ot:
                            del(selected_ot[ancestor.id])
                    # add current
                    selected_ot[item.id] = item
            institution.institution_types.add(*selected_ot.values())
            
        media_file = form_step_data[303].get('avatar', '')
        if media_file:
            tmp_path = os.path.join(settings.PATH_TMP, media_file['tmp_filename'])
            filename = tmp_path.rsplit("/", 1)[1]
            f = open(tmp_path, 'r')
            image_mods.FileManager.save_file_for_object(
                person,
                filename,
                f.read(),
                subpath = "avatar/"
                )
            f.close()
            if institution:
                f = open(tmp_path, 'r')
                image_mods.FileManager.save_file_for_object(
                    institution,
                    filename,
                    f.read(),
                    subpath = "avatar/"
                    )
                f.close()
                
        current_site = Site.objects.get_current()
        encrypted_email = cryptString(user.email)
        
        sender_name, sender_email = settings.MANAGERS[0]
        send_email_using_template(
            [Recipient(user=user)],
            "account_verification",
            obj=institution,
            obj_placeholders={
                'encrypted_email': encrypted_email,
                'site_name': current_site.name,
                },
            delete_after_sending=True,
            sender_name=sender_name,
            sender_email=sender_email,
            send_immediately=True,
            )
        return form_step_data
    save_data = staticmethod(save_data)

REGISTRATION_FORM_STEPS = {
    0: {
        'title': _("account type"),
        'template': "accounts/reg_choose_type.html",
        'form': Registration.AccountType,
    },
    101: {
        'title': _("name and login"),
        'template': "accounts/reg_person.html",
        'form': Registration.MainPersonData,
    },
    102: {
        'title': _("contact data"),
        'template': "accounts/reg_person_contacts.html",
        'form': Registration.PersonContactData,
        'initial_data': {
            'url0_link': 'http://',
            'url1_link': 'http://',
            'url2_link': 'http://',
        },
    },
    104: {
        'title': _("categories"),
        'template': "accounts/reg_categories.html",
        'form': Registration.PersonCategories,
    },
    
    201: {
        'title': _("name and login"),
        'template': "accounts/reg_institution.html",
        'form': Registration.MainInstitutionData,
    },
    202: {
        'title': _("main data"),
        'template': "accounts/reg_institution_contacts.html",
        'form': Registration.InstitutionContactData,
        'initial_data': {
            'url0_link': 'http://',
            'url1_link': 'http://',
            'url2_link': 'http://',
        },
    },
    203: {
        'title': _("opening hours and payment"),
        'template': "accounts/reg_institution_opening_hours.html",
        'form': Registration.InstitutionOpeningHoursPayment,
    },
    204: {
        'title': _("categories"),
        'template': "accounts/reg_categories.html",
        'form': Registration.InstitutionCategories,
    },
    205: {
        'title': _("contact person"),
        'template': "accounts/reg_institution_contact_persons.html",
        'form': Registration.InstitutionContactPersons,
    },
    
    303: {
        'title': _("profile data"),
        'template': "accounts/reg_person_profile.html",
        'form': Registration.PersonProfile,
    },
    305: {
        'title': _("confirm data"),
        'template': "accounts/reg_confirm.html",
        'form': forms.Form, # dummy form
    },

    'onsubmit': Registration.submit_step,
    'onsave': Registration.save_data,
    'name': 'account_registration',
    'success_template': "accounts/reg_approve.html",
    'default_path': [0],
}

class PersonSearchForm(dynamicforms.Form):
    creative_sector = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Creative Sector"),
        required=False,
        queryset=get_related_queryset(Person, "creative_sectors"),
        )
    context_category = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Business Category"),
        required=False,
        queryset=get_related_queryset(Person, "context_categories"),
        )
    individual_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Type"),
        required=False,
        queryset=get_related_queryset(Person, "individual_type"),
        )
    location_type = TreeNodeChoiceField(
        empty_label=_("All"),
        label=_("Location Type"),
        required=False,
        queryset=Term.objects.filter(
            vocabulary__sysname='basics_locality',
            ).order_by("tree_id", "lft"),
        )
    
    def get_query(self):
        from django.template.defaultfilters import urlencode
        cleaned = self.cleaned_data
        return "&".join([
            ("%s=%s" % (k, urlencode(isinstance(v, models.Model) and v.pk or v)))
            for (k, v) in cleaned.items()
            if v
            ])
        

