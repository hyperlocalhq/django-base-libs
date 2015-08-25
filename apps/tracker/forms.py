# -*- coding: UTF-8 -*-
from django.db.models.loading import load_app
from django import forms
from django.conf import settings
from django.template import RequestContext, loader, Context
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from base_libs.forms import dynamicforms

from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_related_queryset, XChoiceList
from base_libs.forms.fields import SingleEmailTextField
from base_libs.forms.fields import SecurityField

from ccb.apps.tracker.models import Ticket
from ccb.apps.configuration.models import SiteSettings

NULL_CONCERN_TYPES = XChoiceList(get_related_queryset(Ticket, "concern"))

from captcha.fields import ReCaptchaField

class TicketForm(dynamicforms.Form):
    
    content_type_id = None
    object_id = None
    url = None
    
    submitter_name = forms.CharField(
        label=_("Name"),
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    
    submitter_email = SingleEmailTextField(
        label=_("Email"),
        required=False,
        max_length=80,
        widget=forms.TextInput(attrs={'class':'vTextField'}),
        )
    
    concern = forms.ChoiceField(
        label=_("Concerns"),
        required=True,
        choices=NULL_CONCERN_TYPES,
        )
    
    description = forms.CharField(
        label= _("Description"),
        required=False,
        widget=forms.Textarea(attrs={'class':'vSystemTextField'}),
        )
    client_info = forms.CharField(
        label= _("Client Info"),
        required=False,
        widget=forms.HiddenInput(),
        )
    
    captcha = ReCaptchaField(attrs={'theme' : 'white'})    
    #prevent_spam = SecurityField()
    
    def __init__(self, concern, content_type_id, object_id, url, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        
        self.content_type_id = content_type_id
        self.object_id = object_id
        self.url = url
        meta = Ticket._meta
        
        if concern:
            try:
                term = get_related_queryset(Ticket, "concern").get(
                    slug=concern,
                    )
                self.fields["concern"].initial = term.id
            except:
                pass 
        
        self.fields["description"].required = not meta.get_field("description").blank
        
        user = get_current_user()
        if user is None or not user.is_authenticated():
            self.fields["submitter_name"].required = not meta.get_field("submitter_name").blank
            self.fields["submitter_email"].required = not meta.get_field("submitter_email").blank

    def save(self):
        # do character encoding
        cleaned = self.cleaned_data
        #for key, value in cleaned.items():
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
        except:
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
        ticket.save()    



