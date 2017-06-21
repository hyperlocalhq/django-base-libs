# -*- coding: UTF-8 -*-
import datetime
from itertools import chain

from django.db import models
from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.dates import MONTHS
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import string_concat

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.forms.fields import ImageField
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import AutocompleteField
from base_libs.middleware import get_current_user
from base_libs.forms.fields import SecurityField, SingleEmailTextField

image_mods = models.get_app("image_mods")

from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from jetson.apps.location.models import Address
from jetson.apps.optionset.models import PhoneType
from jetson.apps.mailing.models import EmailMessage

from kb.apps.people.models import Person, IndividualContact
from kb.apps.institutions.models import Institution, InstitutionalContact
from kb.apps.events.models import Event, EventTime
from kb.apps.resources.models import Document
from kb.apps.marketplace.models import JobOffer
from kb.apps.groups_networks.models import PersonGroup
from kb.apps.site_specific.models import ContextItem, ClaimRequest

from .fields import CCBCheckboxSelectMultiple

NULL_PREFIX_CHOICES = XChoiceList(get_related_queryset(Person, 'prefix'))

LEGAL_FORM_CHOICES = XChoiceList(get_related_queryset(Institution, 'legal_form'))

WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

YEARS_CHOICES = [("", _("Year"))] + [(i, i) for i in range(2008, 2040)]
MONTHS_CHOICES = [("", _("Month"))] + MONTHS.items()
DAYS_CHOICES = [("", _("Day"))] + [(i, i) for i in range(1, 32)]
HOURS_CHOICES = [("", _("HH"))] + [(i, u"%02d" % i) for i in range(0, 24)]
MINUTES_CHOICES = [("", _("MM"))] + [(i, u"%02d" % i) for i in range(0, 60, 5)]

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type
PREFIX_JS = 'JS_'  # Job Sector

BIRTHDAY_DD_CHOICES = Person._meta.get_field('birthday_dd').get_choices()
BIRTHDAY_DD_CHOICES[0] = ("", "----")
BIRTHDAY_MM_CHOICES = Person._meta.get_field('birthday_mm').get_choices()
BIRTHDAY_MM_CHOICES[0] = ("", "----")
BIRTHDAY_YYYY_CHOICES = Person._meta.get_field('birthday_yyyy').get_choices()
BIRTHDAY_YYYY_CHOICES[0] = ("", "----")

NATIONALITY_CHOICES = XChoiceList(get_related_queryset(Person, 'nationality'))
SALUTATION_CHOICES = XChoiceList(get_related_queryset(Person, 'salutation'))

contact_meta = IndividualContact._meta
URL_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'url0_type'))
IM_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'im0_type'))

ORGANIZER_CHOICES = [
    (0, _("selected venue is organizer")),
    (1, _("organized by other institution")),
    (2, _("organized by myself")),
]

CONTACT_PERSON_CHOICES = [
    (0, _("I am the contact person")),
    (1, _("I am not the contact person")),
]

LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, "location_type"))
INSTITUTION_LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(InstitutionalContact, "location_type"))
INDIVIDUAL_TYPE_CHOICES = XChoiceList(get_related_queryset(Person, "individual_type"))
EVENT_TYPE_CHOICES = XChoiceList(get_related_queryset(Event, "event_type"))
ORGANIZING_INSTITUTION_CHOICES = XChoiceList(get_related_queryset(Event, "organizing_institution"))

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

ESTABLISHMENT_YYYY_CHOICES = Institution._meta.get_field('establishment_yyyy').get_choices()
ESTABLISHMENT_YYYY_CHOICES[0] = ("", _("Year"))
ESTABLISHMENT_MM_CHOICES = Institution._meta.get_field('establishment_mm').get_choices()
ESTABLISHMENT_MM_CHOICES[0] = ("", _("Month"))

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
MIN_LOGO_SIZE = getattr(settings, "MIN_LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE


class ClaimForm(dynamicforms.Form):
    """
    Form for claiming institutions, events, documents
    """

    name = forms.CharField(
        label=_("Name"),
        required=True,
        max_length=80,
    )

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        max_length=80,
    )

    best_time_to_call = forms.ChoiceField(
        required=False,
        choices=ClaimRequest._meta.get_field("best_time_to_call").get_choices(),
        label=_("Best Time to Call"),
    )

    phone_country = forms.CharField(
        required=False,
        max_length=4,
        label=string_concat(
            _('Country Code'),
            '<br>',
            _('without'),
            ' "00"',
        )
    )

    phone_area = forms.CharField(
        required=False,
        max_length=5,
        label=string_concat(
            _('Area Code'),
            '<br>',
            _('without'),
            ' "0"',
        )
    )

    phone_number = forms.CharField(
        required=False,
        max_length=15,
        label=string_concat(
            _('Number'),
            '<br>',
            _('with direct dial'),
        )
    )

    role = forms.CharField(
        label=_("Role"),
        required=False,
        max_length=80,
    )

    comments = forms.CharField(
        label=_("Comments"),
        required=False,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )

    def __init__(self, content_type, object_id, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)

        self.content_type = content_type
        self.object_id = object_id
        self.user = get_current_user()
        self.fields["name"].initial = "%s %s" % (self.user.first_name, self.user.last_name)
        self.fields["email"].initial = self.user.email

        person = self.user.profile
        contacts = person.get_contacts()
        if contacts:
            for phone in contacts[0].get_phones():
                if phone["type"] == get_related_queryset(type(contacts[0]), "phone0_type").get(slug="phone"):
                    self.fields["phone_country"].initial = phone["country"]
                    self.fields["phone_area"].initial = phone["area"]
                    self.fields["phone_number"].initial = phone["number"]
                    break

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _('Claim'),
                'name',
                'email',
                layout.MultiField(
                    _("Phone"),
                    layout.Field(
                        "phone_country",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_area",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    layout.Field(
                        "phone_number",
                        wrapper_class="col-xs-4 col-sm-4 col-md-4 col-lg-4",
                        template="kb_form/multifield.html"
                    ),
                    css_class="show-labels"
                ),
                'best_time_to_call',
                'role',
            ),
            layout.Fieldset(
                _('comment'),
                'comments',
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Send'))
            )
        )

    def save(self):
        # do character encoding
        cleaned = self.cleaned_data
        # for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)

        claim_request, created = ClaimRequest.objects.get_or_create(
            user=self.user,
            name=cleaned.get('name', None),
            email=cleaned.get('email', None),
            best_time_to_call=cleaned.get('best_time_to_call', None),
            phone_country=cleaned.get('phone_country', None),
            phone_area=cleaned.get('phone_area', None),
            phone_number=cleaned.get('phone_number', None),
            role=cleaned.get('role', None),
            comments=cleaned.get('comments', None),
            content_type=self.content_type,
            object_id=self.object_id,
            status=0,
        )


class InvitationForm(dynamicforms.Form):
    body = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )

    recipient_email = forms.EmailField(
        label=_("Recipient email"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'vTextField'}),
        help_text=_("Enter an email of a person you want to invite to this website."),
    )

    # prevent spam
    prevent_spam = SecurityField()

    def __init__(self, sender, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.sender = sender

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _('Invitation'),
                'recipient_email',
                'body',
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Send'))
            )
        )

    def send(self):
        from jetson.apps.mailing.views import send_email_using_template
        from jetson.apps.mailing.recipient import Recipient

        sender = self.sender
        cleaned = self.cleaned_data

        body = cleaned["body"]
        recipient_email = cleaned["recipient_email"]

        send_email_using_template(
            recipients_list=[Recipient(
                email=recipient_email,
            )],
            email_template_slug="invitation",
            obj_placeholders={
                'object_creator_title': self.sender.profile.get_title(),
                'object_creator_url': self.sender.profile.get_url(),
                'object_description': body,
            },
            sender_name='',
            sender_email=settings.DEFAULT_FROM_EMAIL,
            send_immediately=True,
        )


class ProfileDeletionForm(dynamicforms.Form):
    delete_events = forms.BooleanField(
        required=False,
        label=_("Delete related events")
    )
    delete_job_offers = forms.BooleanField(
        required=False,
        label=_("Delete related job offers")
    )

    user_deleted = False
    deleted_institutions = []

    def __init__(self, user, *args, **kwargs):
        self.user_deleted = False
        self.deleted_institutions = []

        super(ProfileDeletionForm, self).__init__(*args, **kwargs)
        self.user = user
        profile_choices = [
            ('auth.user', user.profile.get_title()),
        ]
        for inst in user.profile.get_institutions(clear_cache=True):
            profile_choices.append((inst.slug, inst.get_title()))

        self.fields['profiles'] = forms.MultipleChoiceField(
            required=False,
            label=_("Profiles to delete"),
            choices=profile_choices,
            widget=CCBCheckboxSelectMultiple,
        )

        self.helper = FormHelper()
        self.helper.form_action = "."
        self.helper.form_method = "POST"
        self.helper.form_id = "delete_profile_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Profiles to delete"),
                'profiles',
            ),
            layout.Fieldset(
                _("Additional Options"),
                'delete_events',
                'delete_job_offers',
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Delete'))
            )
        )

    def clean_profiles(self):
        value = self.cleaned_data.get('profiles', [])
        if not value:
            raise forms.ValidationError(_("You haven't selected anything to delete."))
        if 'auth.user' in value and self.user.is_superuser:
            raise forms.ValidationError(_("Superuser's profile cannot be deleted."))
        return value

    def delete(self):
        for p in self.cleaned_data['profiles']:
            if p == "auth.user":
                self.user_deleted = True
            else:
                self.deleted_institutions.append(
                    Institution.objects.get(slug=p)
                )

        User = models.get_model("auth", "User")
        Blog = models.get_model("blog", "Blog")
        MediaGallery = models.get_model("media_gallery", "MediaGallery")
        Bookmark = models.get_model("bookmarks", "Bookmark")
        Memo = models.get_model("memos", "Memo")
        Favorite = models.get_model("favorites", "Favorite")
        Comment = models.get_model("comments", "Comment")
        Ticket = models.get_model("tracker", "Ticket")
        ContentType = models.get_model("contenttypes", "ContentType")

        delete_events = self.cleaned_data['delete_events']
        delete_job_offers = self.cleaned_data['delete_job_offers']

        inst_content_type = ContentType.objects.get_for_model(Institution)
        event_content_type = ContentType.objects.get_for_model(Event)
        job_offer_content_type = ContentType.objects.get_for_model(JobOffer)
        # DELETE INSTITUTIONS
        for inst in self.deleted_institutions:
            # delete person group
            PersonGroup.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
            ).delete()
            # delete blog
            Blog.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
            ).delete()
            # delete media gallery
            MediaGallery.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
            ).delete()
            # delete bookmarks
            Bookmark.objects.filter(
                url_path=inst.get_url_path(),
            ).delete()
            # delete memos
            Memo.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
            ).delete()
            # delete favorites
            Favorite.objects.filter(
                content_type=inst_content_type,
                object_id=inst.pk,
            ).delete()
            # optionally keep events
            if not delete_events:
                for ev in Event.objects.filter(
                        models.Q(organizing_institution=inst) |
                        models.Q(venue=inst)
                ):
                    if ev.organizing_institution == inst:
                        if not ev.organizer_title:
                            ev.organizer_title = ev.organizing_institution.get_title()
                        ev.organizing_institution = None
                    if ev.venue == inst:
                        if not ev.venue_title:
                            ev.venue_title = ev.venue.get_title()
                        ev.venue = None
                    ev.save()
            else:
                for ev in Event.objects.filter(
                        models.Q(organizing_institution=inst) |
                        models.Q(venue=inst)
                ):
                    # delete media galleries
                    MediaGallery.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                    ).delete()
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=ev.get_url_path(),
                    ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                    ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                    ).delete()
                    # delete event
                    ev.delete()
            # optionally keep job offers
            if not delete_job_offers:
                for job in JobOffer.objects.filter(
                    offering_institution=inst,
                ):
                    if not job.offering_institution_title:
                        job.offering_institution_title = job.offering_institution.get_title()
                    job.offering_institution = None
                    job.save()
            else:
                for job in JobOffer.objects.filter(
                    offering_institution=inst,
                ):
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=job.get_url_path(),
                    ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                    ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                    ).delete()
                    # delete job offer
                    job.delete()
            # delete institution
            inst.delete()
        # DELETE USER
        person = self.user.profile
        person_content_type = ContentType.objects.get_for_model(person)
        superuser = User.objects.filter(is_superuser=True)[0]
        if self.user_deleted:
            # delete blog
            Blog.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
            ).delete()
            # delete media gallery
            MediaGallery.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
            ).delete()
            # keep comments
            for comment in Comment.objects.filter(
                user=self.user,
            ):
                comment.name = person.get_title()
                comment.email = self.user.email
                comment.user = None
                comment.save()
            # keep tickets
            Ticket.objects.filter(
                submitter=self.user
            ).update(
                submitter_name=person.get_title(),
                submitter_email=self.user.email,
                submitter=None,
            )
            Ticket.objects.filter(
                modifier=self.user,
            ).update(
                modifier=None
            )
            # delete bookmarks
            Bookmark.objects.filter(
                url_path=person.get_url_path(),
            ).delete()
            # delete memos
            Memo.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
            ).delete()
            # delete favorites
            Favorite.objects.filter(
                content_type=person_content_type,
                object_id=person.pk,
            ).delete()
            # optionally keep events
            if not delete_events:
                for ev in Event.objects.filter(
                            models.Q(organizing_person=person) |
                            models.Q(creator=self.user) |
                        models.Q(modifier=self.user)
                ):
                    if ev.organizing_person == person:
                        ev.organizing_person = None
                    if ev.creator == self.user:
                        ev.creator = superuser
                    if ev.modifier == self.user:
                        ev.modifier = None
                    ev.save_base()
            else:
                for ev in Event.objects.filter(
                            models.Q(organizing_person=person) |
                            models.Q(creator=self.user) |
                        models.Q(modifier=self.user)
                ):
                    # delete media galleries
                    MediaGallery.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                    ).delete()
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=ev.get_url_path(),
                    ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                    ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=event_content_type,
                        object_id=ev.pk,
                    ).delete()
                    # delete event
                    ev.delete()
            # optionally keep job offers
            if not delete_job_offers:
                JobOffer.objects.filter(
                    contact_person=person,
                ).update(
                    contact_person_name=person.get_title(),
                    contact_person=None,
                )
                JobOffer.objects.filter(
                    creator=self.user
                ).update(
                    creator=superuser,
                )
                JobOffer.objects.filter(
                    author=self.user
                ).update(
                    author=superuser,
                )
                JobOffer.objects.filter(
                    modifier=self.user
                ).update(
                    modifier=None,
                )
            else:
                for job in JobOffer.objects.filter(
                            models.Q(contact_person=person) |
                            models.Q(creator=self.user) |
                        models.Q(modifier=self.user)
                ):
                    # delete bookmarks
                    Bookmark.objects.filter(
                        url_path=job.get_url_path(),
                    ).delete()
                    # delete memos
                    Memo.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                    ).delete()
                    # delete favorites
                    Favorite.objects.filter(
                        content_type=job_offer_content_type,
                        object_id=job.pk,
                    ).delete()
                    # delete job offer
                    job.delete()
            # delete user
            self.user.delete()


class ObjectDeletionForm(dynamicforms.Form):
    def __init__(self, obj, *args, **kwargs):
        super(ObjectDeletionForm, self).__init__(*args, **kwargs)
        self.obj = obj

    def delete(self):
        self.obj.delete()


class KreativArbeitenContactForm(dynamicforms.Form):
    subject = forms.CharField(
        label=_("Subject"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'vTextField'}),
    )

    body = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )

    sender_name = forms.CharField(
        label=_("Your name"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'vTextField'}),
    )
    sender_email = SingleEmailTextField(
        label=_("Your e-mail address"),
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'vTextField'}),
    )

    # prevent spam
    prevent_spam = SecurityField()

    def __init__(self, *args, **kwargs):
        super(KreativArbeitenContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = ''
        self.helper.form_method = 'POST'
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _('Contact us'),
                'sender_name',
                'sender_email',
                'subject',
                'body',
                'prevent_spam',
            ),
            bootstrap.FormActions(
                layout.Submit(
                    'submit',
                    _('Submit'),
                ),
            ),
        )

    def save(self, sender=None):
        # do character encoding
        cleaned = self.cleaned_data
        # for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)

        if not sender.is_authenticated():
            sender = None

        subject = cleaned["subject"]
        body = cleaned["body"]
        sender_name = cleaned["sender_name"]
        sender_email = cleaned["sender_email"]

        recipient_emails = ["%s <%s>" % (
            "Dirk Kiefer",
            "kiefer@rkw.de",
        )]
        message = EmailMessage.objects.create(
            sender=sender,
            sender_name=sender_name,
            sender_email=sender_email,
            recipient_emails=",".join(recipient_emails),
            subject=subject,
            body_html=body,
        )
        message.send()
