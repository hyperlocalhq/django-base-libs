# -*- coding: UTF-8 -*-
import requests

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.translation import string_concat

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from base_libs.forms import dynamicforms
from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import SingleEmailTextField
from kb.apps.tracker.models import Ticket

NULL_CONCERN_TYPES = XChoiceList(get_related_queryset(Ticket, "concern"))


RECAPTCHA_ERROR_CODES = {
    "missing-input-secret": _("The secret parameter is missing."),
    "invalid-input-secret": _("The secret parameter is invalid or malformed."),
    "missing-input-response": _("The response parameter is missing."),
    "invalid-input-response": _("The response parameter is invalid or malformed."),
}


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class TicketForm(dynamicforms.Form):
    content_type_id = None
    object_id = None
    url = None

    submitter_name = forms.CharField(
        label=_("Name"),
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={'class': 'vTextField'}),
    )

    submitter_email = SingleEmailTextField(
        label=_("Email"),
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={'class': 'vTextField'}),
    )

    concern = forms.ChoiceField(
        label=_("Concerns"),
        required=True,
        choices=NULL_CONCERN_TYPES,
    )

    description = forms.CharField(
        label=_("Description"),
        required=False,
        widget=forms.Textarea(attrs={'class': 'vSystemTextField'}),
    )
    client_info = forms.CharField(
        label=_("Client Info"),
        required=False,
        widget=forms.HiddenInput(),
    )

    def __init__(self, request, concern, content_type_id, object_id, url, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.request = request
        self.content_type_id = content_type_id
        self.object_id = object_id
        self.url = url
        meta = Ticket._meta
        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper_form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Write Feedback"),
                'concern',
                'submitter_name',
                'submitter_email',
                'description',
                layout.HTML("""
                <dt></dt>
                <dd>
                    <div class="input-field">
                        <div class="g-recaptcha" data-sitekey="{}"></div>
                    </div>
                </dd>
                """.format(settings.RECAPTCHA_SITE_KEY)),
                'client_info',
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Submit').upper())
            )
        )

        if concern:
            try:
                term = get_related_queryset(Ticket, "concern").get(
                    slug=concern,
                )
                self.fields["concern"].initial = term.id
            except Exception:
                pass

        self.fields["description"].required = not meta.get_field("description").blank

        user = get_current_user()
        if user is None or not user.is_authenticated():
            self.fields["submitter_name"].required = not meta.get_field("submitter_name").blank
            self.fields["submitter_email"].required = not meta.get_field("submitter_email").blank

    def clean(self):
        cleaned = self.cleaned_data
        if "g-recaptcha-response" not in self.request.POST:
            raise forms.ValidationError(_("reCAPTCHA Error."))
        result = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            {
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": self.request.POST["g-recaptcha-response"],
                "remoteip": get_client_ip(self.request),
            },
        ).json()
        if not result["success"]:
            raise forms.ValidationError(_("reCAPTCHA Error."))
        return cleaned

    def save(self):
        # do character encoding
        cleaned = self.cleaned_data
        # for key, value in cleaned.items():
        #    if type(value).__name__ == "unicode":
        #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)

        user = get_current_user()
        if user is None or not user.is_authenticated():
            submitter_name = cleaned['submitter_name']
            submitter_email = cleaned['submitter_email']
        else:
            submitter_name = None
            submitter_email = None

        try:
            content_type = ContentType.objects.get(id=self.content_type_id)
        except Exception:
            content_type = None

        concern = get_related_queryset(Ticket, "concern").get(
            pk=cleaned['concern'],
        )

        (ticket, created) = Ticket.objects.get_or_create(
            concern=concern,
            submitter_name=submitter_name,
            submitter_email=submitter_email,
            description=cleaned['description'],
            client_info=cleaned['client_info'],
            content_type=content_type,
            object_id=self.object_id or "",
            url=self.url
        )
        #ticket.save()
