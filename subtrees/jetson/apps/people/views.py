# -*- coding: UTF-8 -*-
import hashlib
import urllib

from django.db import models
from django.db import transaction
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.mail import send_mail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site, RequestSite
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login
from django.utils.encoding import smart_str
from django.conf import settings

from base_libs.utils.misc import get_related_queryset
from base_libs.utils.crypt import decryptString
from base_libs.utils.misc import get_installed
from base_libs.utils.misc import get_website_url

from jetson.apps.utils.decorators import login_required
from jetson.apps.configuration.models import SiteSettings
from jetson.apps.mailing.views import send_email_using_template, Recipient
from jetson.apps.utils.views import object_list
from jetson.apps.utils.views import object_detail
from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.views import get_abc_list
from jetson.apps.utils.views import filter_abc

AuthenticationForm = get_installed("people.forms.AuthenticationForm")
EmailAuthentication = get_installed("people.forms.EmailAuthentication")
EmailOrUsernameAuthentication = get_installed("people.forms.EmailOrUsernameAuthentication")
SimpleRegistrationForm = get_installed("people.forms.SimpleRegistrationForm")
PrivacySettingsForm = get_installed("people.forms.PrivacySettingsForm")
REGISTRATION_FORM_STEPS = get_installed("people.forms.REGISTRATION_FORM_STEPS")
URL_ID_PERSON = get_installed("people.models.URL_ID_PERSON")
URL_ID_PEOPLE = get_installed("people.models.URL_ID_PEOPLE")
Person = models.get_model("people", "Person")

@never_cache
def login(request, template_name='registration/login.html', redirect_field_name=getattr(settings, "REDIRECT_FIELD_NAME", REDIRECT_FIELD_NAME)):
    """Displays the login form and handles the login action."""
    site_settings = SiteSettings.objects.get_current()
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = EmailOrUsernameAuthentication(request, data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                from django.conf import settings
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            user = form.get_user()
            login_as = request.REQUEST.get("login_as", "")
            if user.is_superuser and login_as:
                if "@" in login_as:
                    login_as_user = User.objects.get(
                        email=login_as,
                    )
                else:
                    login_as_user = User.objects.get(
                        username=login_as,
                    )
                login_as_user.backend = user.backend
                user = login_as_user
            login(request, user)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                # if not redirect_to.startswith("http"):
                #     redirect_to = smart_str(get_website_url(redirect_to))
                if request.is_ajax():
                    return HttpResponse("redirect=%s" % redirect_to)
                return HttpResponseRedirect(redirect_to)
    else:
        data = {
            'email_or_username': request.GET.get('login_as', ''),
            'login_as': request.GET.get('login_as', ''),
        }
        form = EmailOrUsernameAuthentication(request, initial=data)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
        'login_by_email': site_settings.login_by_email,
    }
    if request.is_ajax():
        context['base_template'] = "base_ajax.html"
    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request),
    )
    
NULL_PREFIX_CHOICES = Person._meta.get_field('prefix').get_choices()

@transaction.atomic
@never_cache
def register(request, *arguments, **keywords):
    """Displays the registration form and handles the registration action"""
    m = hashlib.md5()
    m.update(request.META['REMOTE_ADDR'])
    request.session.session_id = m.hexdigest()[:20]
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    site_settings = SiteSettings.objects.get_current()
    if site_settings.registration_type == "advanced":
        extra_context = {
            settings.REDIRECT_FIELD_NAME: redirect_to,
            'site_name': Site.objects.get_current().name,
            'login_by_email': site_settings.login_by_email,
        }
        return show_form_step(request, REGISTRATION_FORM_STEPS, extra_context)
    else:
        if request.method == "POST":
            form = SimpleRegistrationForm(request, request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                return HttpResponseRedirect('/register/done/')
        else:
            form = SimpleRegistrationForm(request)
        request.session.set_test_cookie()
        return render_to_response('accounts/register.html' ,{
            'form': form,
            settings.REDIRECT_FIELD_NAME: redirect_to,
            'site_name': Site.objects.get_current().name,
            'login_by_email': site_settings.login_by_email,
        }, context_instance=RequestContext(request))

@never_cache
def confirm_registration(request, encrypted_email):
    """Displays the registration form and handles the registration action"""
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    try:
        email = decryptString(encrypted_email)
    except:
        raise Http404
    user = authenticate(email=email)
    if not user:
        return HttpResponseRedirect('/register/')
    user.is_active = True
    user.save()
    person = user.profile
    person.status = "published"
    person.save()
    from django.contrib.auth import login
    login(request, user)

    current_site = Site.objects.get_current()

    sender_name, sender_email = settings.MANAGERS[0]
    send_email_using_template(
        [Recipient(user=user)],
        "account_created",
        obj_placeholders={
            'site_name': current_site.name,
            },
        delete_after_sending=True,
        sender_name=sender_name,
        sender_email=sender_email,
        send_immediately=True,
        )
    return HttpResponseRedirect('/register/alldone/')

@login_required
@never_cache
def change_privacy_settings(request):
    """Displays the form for personal privacy settings"""
    person = get_object_or_404(Person, user=request.user)
    if request.method == "POST":
        form = PrivacySettingsForm(request.POST)
        if form.is_valid():
            person.display_username = form.cleaned_data['display_username']
            person.allow_search_engine_indexing = form.cleaned_data['allow_search_engine_indexing']
            person.display_birthday = form.cleaned_data['display_birthday']
            person.display_address = form.cleaned_data['display_address']
            person.display_phone = form.cleaned_data['display_phone']
            person.display_fax = form.cleaned_data['display_fax']
            person.display_mobile = form.cleaned_data['display_mobile']
            person.display_im = form.cleaned_data['display_im']

            # update the status
            # TODO mapping the checkbox values to statuses
            display_profile = form.cleaned_data['display_profile']
            if display_profile:
                person.status = "published"
            else:
                person.status = "not_listed"
                
            
            person.save()
            return HttpResponseRedirect('/my-profile/')
    else:
        form = PrivacySettingsForm(initial=person.__dict__)
    return render_to_response('accounts/my_profile/privacy_settings.html', {
        'object': person,
        'form': form,
    }, context_instance=RequestContext(request))


def _person_list_filter(request, queryset, show):
    return queryset.filter(
        status="published",
        )

@never_cache
def person_list(
    request,
    criterion="",
    slug="",
    show="",
    list_filter=_person_list_filter,
    **kwargs
    ):
    """Displays the list of people"""
    
    abc_list = None
    abc_filter = request.GET.get('by-abc', None)
    
    kwargs['queryset'] = list_filter(request, kwargs['queryset'], show)

    person_filters = {}
    for var in ("type", "commerciality", "location-type", "actuality", "neighborhood"):
        if var in request.GET:
            person_filters[var] = request.GET[var]
    if not person_filters:
        person_filters = request.httpstate.get('person_filters', {})
        
    if slug=="all":
        try:
            del(person_filters[criterion])
        except:
            pass
    else:
        if person_filters.get('criterion', '') != slug:
            person_filters[criterion] = slug
    request.httpstate['person_filters'] = person_filters
    
    if len(person_filters) == 0 and criterion:
        return HttpResponseRedirect('/%s/' % URL_ID_PEOPLE)
    elif len(person_filters) == 1 and criterion != person_filters.keys()[0]:
        for k, v in person_filters.items():
            page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
            return HttpResponseRedirect('/%s/by-%s/%s/%s' % (URL_ID_PEOPLE, k, v, page))
    elif not len(request.GET) and len(person_filters) > 1:
        query_vars = "?" + "&".join(["%s=%s" % (k, v) for k, v in person_filters.items()])
        page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
        return HttpResponseRedirect('/%s/%s%s' % (URL_ID_PEOPLE, page, query_vars))
    else:
        queryset = kwargs['queryset']
        for k, v in person_filters.items():
            if k=="type":
                pass
            elif k=="commerciality":
                queryset = queryset.filter(is_non_profit = True)
            elif k=="location-type" and request.user.is_authenticated():
                q = None
                for n in request.user.get_person().get_neighborhoods():
                    if not q:
                        q = models.Q(neighborhoods__icontains=n)
                    else:
                        q |= models.Q(neighborhoods__icontains=n)
                if q:
                    queryset = queryset.filter(q)
            elif k=="actuality":
                if v=="activity":
                    queryset = queryset.order_by("-last_activity_timestamp")
                elif v=="rating":
                    queryset = queryset.order_by("rating")
                elif v=="new":
                    queryset = queryset.order_by("-creation_date")
                elif v=="my-contacts":
                    person_ids = [p.id for p in Person.objects.filter(user__to_user__user=request.user).distinct()]
                    person_ctype = ContentType.objects.get_for_model(Person)
                    institution_ids = [i.id for i in Institution.objects.filter(persongroup__groupmembership__user=request.user).distinct()]
                    institution_ctype = ContentType.objects.get_for_model(Institution)
                    queryset = queryset.filter(models.Q(object_id__in=person_ids) & models.Q(content_type=person_ctype) | models.Q(object_id__in=institution_ids) & models.Q(content_type=institution_ctype))
            
        abc_list = get_abc_list(queryset, "user__last_name", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "user__last_name", abc_filter)

        view_type = request.REQUEST.get('view_type', request.httpstate.get(
            "%s_view_type" % URL_ID_PEOPLE,
            "icons",
            ))
        if view_type == "map":
            queryset = queryset.filter(
                individualcontact__postal_address__geoposition__latitude__gte=-90,
                ).distinct()
        
        extra_context = {'abc_list': abc_list, 'show': ("", "/%s" % show)[bool(show)], 'source_list': URL_ID_PEOPLE}
        if request.is_ajax():
            extra_context['base_template'] = "base_ajax.html"

        kwargs['extra_context'] = extra_context  
        kwargs['httpstate_prefix'] = URL_ID_PEOPLE
        kwargs['queryset'] = queryset
              
        return object_list(request, **kwargs)
