# -*- coding: UTF-8 -*-
import operator
import json

from django.utils.translation import ugettext_lazy as _

from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import template

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

from django.http import Http404

from django.conf import settings
from django.utils.encoding import force_unicode, smart_str

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.admin.views.main import PAGE_VAR, ALL_VAR, IS_POPUP_VAR, SEARCH_VAR, ORDER_VAR, ORDER_TYPE_VAR

from django.contrib import messages

from jetson.apps.location.models import Address
from jetson.apps.mailing.recipient import Recipient
from jetson.apps.mailing.views import do_generic_mail

from base_libs.utils.misc import get_installed
from base_libs.utils.misc import ExtendedJSONEncoder

def person_add(request):
    return person_change(request, object_id=None)

def person_change(request, object_id=None):
    """Displays the person add/change form and handles person saving."""
    from jetson.apps.extendedadmin.forms import PersonForm
    from jetson.apps.extendedadmin.forms import IndividualContactFormSet
    Person = get_installed("people.models.Person")
    person = None
    if object_id:
        person = get_object_or_404(Person, id=object_id)
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        form = PersonForm(
            data=request.POST,
            files=request.FILES,
            instance=person,
            )
        contact_formset = IndividualContactFormSet(
            data=request.POST,
            files=request.FILES,
            instance=person,
            )
        if form.is_valid() and contact_formset.is_valid():
            person = form.save(commit=False)
            person.save()
            form.save_m2m()
            
            contact_formset.instance = person
            contacts = contact_formset.save()
            for contact, contact_form in zip(contacts, contact_formset.forms):
                Address.objects.set_for(
                    contact,
                    "postal_address",
                    country=contact_form.cleaned_data["country"],
                    state=contact_form.cleaned_data["state"],
                    city=contact_form.cleaned_data["city"],
                    street_address=contact_form.cleaned_data["street_address"],
                    street_address2=contact_form.cleaned_data["street_address2"],
                    street_address3=contact_form.cleaned_data["street_address3"],
                    postal_code=contact_form.cleaned_data["postal_code"],
                    district=contact_form.cleaned_data["district"],
                    neighborhood=contact_form.cleaned_data["neighborhood"],
                    latitude=contact_form.cleaned_data["latitude"],
                    longitude=contact_form.cleaned_data["longitude"],
                    altitude=contact_form.cleaned_data["altitude"],
                    )
            
            if not redirect_to or '://' in redirect_to or ' ' in redirect_to:
                redirect_to = '/admin/people/person/'
            
            messages.success(request, _('%s was successfully saved.') % unicode(person))
            if request.POST.has_key("_addanother"):
                return HttpResponseRedirect("/admin/people/person/add/")
            elif request.POST.has_key("_continue"):
                return HttpResponseRedirect("/admin/people/person/%d/" % person.id)
            else:
                return HttpResponseRedirect(redirect_to)
    else:
        form = PersonForm(
            instance=person,
            )
        contact_formset = IndividualContactFormSet(
            instance=person,
            )
    return render_to_response("extendedadmin/person_change.html", {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'contact_formset': contact_formset,
        'title': _("Change Person"),
        'change': True,
        'object': person,
        'original': person,
    }, context_instance=RequestContext(request))
person_change = staff_member_required(never_cache(person_change))

def institution_add(request):
    return institution_change(request, object_id=None)

def institution_change(request, object_id=None):
    """Displays the institution add/change form and handles institution saving."""
    from jetson.apps.extendedadmin.forms import InstitutionForm
    from jetson.apps.extendedadmin.forms import InstitutionalContactFormSet
    Institution = get_installed("institutions.models.Institution")
    institution = None
    if object_id:
        institution = get_object_or_404(Institution, id=object_id)
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        form = InstitutionForm(
            data=request.POST,
            files=request.FILES,
            instance=institution,
            )
        contact_formset = InstitutionalContactFormSet(
            data=request.POST,
            files=request.FILES,
            instance=institution,
            )
        if form.is_valid() and contact_formset.is_valid():
            institution = form.save(commit=False)
            institution.save()
            form.save_m2m()
            
            contact_formset.instance = institution
            contacts = contact_formset.save()
            for contact, contact_form in zip(contacts, contact_formset.forms):
                Address.objects.set_for(
                    contact,
                    "postal_address",
                    country=contact_form.cleaned_data["country"],
                    state=contact_form.cleaned_data["state"],
                    city=contact_form.cleaned_data["city"],
                    street_address=contact_form.cleaned_data["street_address"],
                    street_address2=contact_form.cleaned_data["street_address2"],
                    street_address3=contact_form.cleaned_data["street_address3"],
                    postal_code=contact_form.cleaned_data["postal_code"],
                    district=contact_form.cleaned_data["district"],
                    neighborhood=contact_form.cleaned_data["neighborhood"],
                    latitude=contact_form.cleaned_data["latitude"],
                    longitude=contact_form.cleaned_data["longitude"],
                    altitude=contact_form.cleaned_data["altitude"],
                    )
            
            if not redirect_to or '://' in redirect_to or ' ' in redirect_to:
                redirect_to = '/admin/institutions/institution/'
            
            messages.success(request, _('%s was successfully saved.') % unicode(institution))
            if request.POST.has_key("_addanother"):
                return HttpResponseRedirect("/admin/institutions/institution/add/")
            elif request.POST.has_key("_continue"):
                return HttpResponseRedirect("/admin/institutions/institution/%d/" % institution.id)
            else:
                return HttpResponseRedirect(redirect_to)
    else:
        form = InstitutionForm(
            instance=institution,
            )
        contact_formset = InstitutionalContactFormSet(
            instance=institution,
            )
    return render_to_response("extendedadmin/institution_change.html", {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'contact_formset': contact_formset,
        'title': _("Change Institution"),
        'change': True,
        'object': institution,
        'original': institution,
    }, context_instance=RequestContext(request))
institution_change = staff_member_required(never_cache(institution_change))

def document_add(request):
    return document_change(request, object_id=None)

def document_change(request, object_id=None):
    """Displays the document add/change form and handles document saving."""
    from jetson.apps.extendedadmin.forms import DocumentForm
    Document = get_installed("resources.models.Document")
    document = None
    if object_id:
        document = get_object_or_404(Document, id=object_id)
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        form = DocumentForm(
            data=request.POST,
            files=request.FILES,
            instance=document,
            )
        if form.is_valid():
            document = form.save(commit=False)
            document.save()
            form.save_m2m()
            
            if not redirect_to or '://' in redirect_to or ' ' in redirect_to:
                redirect_to = '/admin/resources/document/'
            
            messages.success(request, _('%s was successfully saved.') % unicode(document))
            if request.POST.has_key("_addanother"):
                return HttpResponseRedirect("/admin/resources/document/add/")
            elif request.POST.has_key("_continue"):
                return HttpResponseRedirect("/admin/resources/document/%d/" % document.id)
            else:
                return HttpResponseRedirect(redirect_to)
    else:
        form = DocumentForm(
            instance=document,
            )
    return render_to_response("extendedadmin/document_change.html", {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'title': _("Change Document"),
        'change': True,
        'object': document,
        'original': document,
    }, context_instance=RequestContext(request))
document_change = staff_member_required(never_cache(document_change))

def event_add(request):
    return event_change(request, object_id=None)

def event_change(request, object_id=None):
    """Displays the event add/change form and handles event saving."""
    from jetson.apps.extendedadmin.forms import EventForm
    Event = get_installed("events.models.Event")
    event = None
    if object_id:
        event = get_object_or_404(Event, id=object_id)
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        form = EventForm(
            data=request.POST,
            files=request.FILES,
            instance=event,
            )
        if form.is_valid():
            event = form.save(commit=False)
            Address.objects.set_for(
                event,
                "postal_address",
                country=form.cleaned_data["country"],
                state=form.cleaned_data["state"],
                city=form.cleaned_data["city"],
                street_address=form.cleaned_data["street_address"],
                street_address2=form.cleaned_data["street_address2"],
                street_address3=form.cleaned_data["street_address3"],
                postal_code=form.cleaned_data["postal_code"],
                district=form.cleaned_data["district"],
                neighborhood=form.cleaned_data["neighborhood"],
                latitude=form.cleaned_data["latitude"],
                longitude=form.cleaned_data["longitude"],
                altitude=form.cleaned_data["altitude"],
                )
            form.save_m2m()
            
            if not redirect_to or '://' in redirect_to or ' ' in redirect_to:
                redirect_to = '/admin/events/event/'
            
            messages.success(request, _('%s was successfully saved.') % unicode(event))
            if request.POST.has_key("_addanother"):
                return HttpResponseRedirect("/admin/events/event/add/")
            elif request.POST.has_key("_continue"):
                return HttpResponseRedirect("/admin/events/event/%d/" % event.id)
            else:
                return HttpResponseRedirect(redirect_to)
    else:
        form = EventForm(
            instance=event,
            )
    return render_to_response("extendedadmin/event_change.html", {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'title': _("Change Event"),
        'change': True,
        'object': event,
        'original': event,
    }, context_instance=RequestContext(request))
event_change = staff_member_required(never_cache(event_change))


def json_institutional_contacts(request, object_id):
    Institution = get_installed("institutions.models.Institution")
    institution = Institution.objects.get(id=object_id)
    if request.user.has_perm("institutions.change_institution", institution) or  (
        request.user.is_authenticated() and
        request.user.profile.get_institutions().filter(pk=institution.id)
        ):
        contacts = institution.get_primary_contact()
        for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
            for field in ("open", "break_close", "break_open", "close"):
                if getattr(institution, "%s_%s" % (day, field)):
                    contacts["%s_%s" % (day, field)] = getattr(institution, "%s_%s" % (day, field)).strftime("%H:%M")
        json_str = json.dumps(contacts, ensure_ascii=False, cls=ExtendedJSONEncoder)
        return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')
    else:
        return HttpResponse('false', content_type='text/javascript; charset=utf-8')
#json_institutional_contacts = staff_member_required(never_cache(json_institutional_contacts))

def user_send_mail(request, email_template_slug=None):
    """
    opens the generic mail form to send a template based email to selected recipients
    
    email_template_id:    The id of the email template to use...
    """
    User = get_installed("auth.models.User")
    UserAdmin = get_installed("auth.admin.UserAdmin")

    # filtering by the filters set
    search_filter = dict([
        (str(k), v)
        for k, v in request.GET.items()
        if k not in (ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR, IS_POPUP_VAR)
        ])
    qs = User.objects.filter(**search_filter)
    # filtering by search query
    
    # Apply keyword searches.
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    query = request.GET.get(SEARCH_VAR, "")
    search_fields = UserAdmin.search_fields
    if search_fields and query:
        for bit in query.split():
            or_queries = [models.Q(**{construct_search(field_name): bit}) for field_name in search_fields]
            other_qs = QuerySet(User)
            if getattr(qs, "_select_related", False):
                other_qs = other_qs.select_related()
            other_qs = other_qs.filter(reduce(operator.or_, or_queries))
            qs = qs & other_qs    
    # recipient_list contains instances of class Recipient
    recipients_list = []
    for item in qs:
        try:
            name = item.profile.get_title()
            email = item.email
            url = item.profile.get_absolute_url()
        except:
            name = (u"%s %s" % (item.first_name, item.last_name)).strip() or item.username
            email = item.email
            url = ""
        recipients_list.append(
            Recipient(
                user=item,
                name=name,
                email=email,
                display_name="%s (%s)" % (name, email),
                id=item.id,
                slug=item.username,
                url=url,
                )
            )
            
    return do_generic_mail(
        request,
        template_name = 'extendedadmin/person_mail.html', 
        redirect_to= '/admin/auth/user/',
        recipients_list=recipients_list,
        display_recipients_list=True,
        display_recipients_input=True,
        display_en = True,
        display_de = True,
        email_template_slug=email_template_slug,
        )
user_send_mail = staff_member_required(never_cache(user_send_mail))

def person_send_mail(request, email_template_slug=None):
    """
    opens the generic mail form to send a template based email to selected recipients
    
    email_template_id:    The id of the email template to use...
    """
    Person = get_installed("people.models.Person")
    PersonOptions = get_installed("people.admin.PersonOptions")

    # filtering by the filters set
    search_filter = dict([
        (str(k), v)
        for k, v in request.GET.items()
        if k not in (ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR, IS_POPUP_VAR)
        ])
    qs = Person.objects.filter(**search_filter)
    # filtering by search query
    
    # Apply keyword searches.
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    query = request.GET.get(SEARCH_VAR, "")
    search_fields = PersonOptions.search_fields
    if search_fields and query:
        for bit in query.split():
            or_queries = [models.Q(**{construct_search(field_name): bit}) for field_name in search_fields]
            other_qs = QuerySet(Person)
            if getattr(qs, "_select_related", False):
                other_qs = other_qs.select_related()
            other_qs = other_qs.filter(reduce(operator.or_, or_queries))
            qs = qs & other_qs    
    # recipient_list contains instances of class Recipient
    recipients_list = []
    for item in qs:
        try:
            name = item.get_title()
            email = item.user.email
        except:
            pass
        else:
            recipients_list.append(
                Recipient(
                    user=item.user,
                    name=name,
                    email=email,
                    display_name="%s (%s)" % (name, email),
                    id=item.id,
                    slug=item.slug,
                    url=item.get_absolute_url(),
                    )
                )
            
    return do_generic_mail(
        request,
        template_name = 'extendedadmin/person_mail.html', 
        redirect_to= '/admin/people/person/',
        recipients_list=recipients_list,
        display_recipients_list=True,
        display_recipients_input=True,
        display_en = True,
        display_de = True,
        email_template_slug=email_template_slug,
        )
person_send_mail = staff_member_required(never_cache(person_send_mail))

def institution_send_mail(request, email_template_slug=None):
    """
    opens the generic mail form to send a template based email to selected recipients
    
    email_template_id:    The id of the email template to use...
    """
    Institution = get_installed("institutions.models.Institution")
    InstitutionOptions = get_installed("institutions.admin.InstitutionOptions")
    # filtering by the filters set
    search_filter = dict([
        (str(k), v)
        for k, v in request.GET.items()
        if k not in (ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR, IS_POPUP_VAR)
        ])
    qs = Institution.objects.filter(**search_filter)
    # filtering by search query
    
    # Apply keyword searches.
    def construct_search(field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    query = request.GET.get(SEARCH_VAR, "")
    search_fields = InstitutionOptions.search_fields
    if search_fields and query:
        for bit in query.split():
            or_queries = [models.Q(**{construct_search(field_name): bit}) for field_name in search_fields]
            other_qs = QuerySet(Institution)
            if getattr(qs, "_select_related", False):
                other_qs = other_qs.select_related()
            other_qs = other_qs.filter(reduce(operator.or_, or_queries))
            qs = qs & other_qs
    # recipient_list contains instances of class Recipient
    recipients_list = []
    for item in qs:
        try:
            name = item.get_title()
            email = item.get_contacts()[0].get_emails()[0]["address"]
        except:
            pass
        else:
            recipients_list.append(
                Recipient(
                    name=name,
                    email=email,
                    display_name="%s (%s)" % (name, email),
                    id=item.id,
                    slug=item.slug,
                    url=item.get_absolute_url(),
                    )
                )
            
    return do_generic_mail(
        request,
        template_name = 'extendedadmin/institution_mail.html', 
        redirect_to= '/admin/institutions/institution/',
        recipients_list=recipients_list,
        display_recipients_list=True,
        display_recipients_input=True,
        display_en = True,
        display_de = True,
        email_template_slug=email_template_slug,
        )
institution_send_mail = staff_member_required(never_cache(institution_send_mail))
