# -*- coding: UTF-8 -*-
import hashlib
import json

from django.db import models
from django.db import transaction
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.shortcuts import render
from base_libs.utils.crypt import decryptString
from base_libs.utils.misc import get_installed
from jetson.apps.utils.decorators import login_required
from jetson.apps.configuration.models import SiteSettings
from jetson.apps.mailing.views import send_email_using_template, Recipient

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa

from ccb.apps.accounts.forms import EmailOrUsernameAuthentication
from ccb.apps.accounts.forms import SimpleRegistrationForm
from ccb.apps.accounts.forms import PrivacySettingsForm

URL_ID_PERSON = get_installed("people.models.URL_ID_PERSON")
URL_ID_PEOPLE = get_installed("people.models.URL_ID_PEOPLE")
Person = models.get_model("people", "Person")


def social_auth_context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)


@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=getattr(settings, "REDIRECT_FIELD_NAME", REDIRECT_FIELD_NAME)):
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
            auth_login(request, user)
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

def social_login(request):
    return render(request, "accounts/social_login.html", social_auth_context())

@transaction.atomic
@never_cache
def register(request, *arguments, **keywords):
    """Displays the registration form and handles the registration action"""
    m = hashlib.md5()
    m.update(request.META['REMOTE_ADDR'])
    request.session.session_id = m.hexdigest()[:20]
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    site_settings = SiteSettings.objects.get_current()
    if request.method == "POST":
        form = SimpleRegistrationForm(request, request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('register_done')
    else:
        form = SimpleRegistrationForm(request)
    request.session.set_test_cookie()
    return render_to_response('accounts/register.html', {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'site_name': Site.objects.get_current().name,
        'login_by_email': site_settings.login_by_email,
    }, context_instance=RequestContext(request))


@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')


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
        return redirect('register')
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
    return redirect('register_all_done')


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
