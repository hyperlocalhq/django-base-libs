# -*- coding: UTF-8 -*-
import hashlib
import json

from django.apps import apps
from django.core.urlresolvers import reverse
from django.db import models
from django.db import transaction
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.shortcuts import render
import actstream.models
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify
from base_libs.utils.crypt import decryptString
from base_libs.utils.misc import get_installed
from jetson.apps.utils.decorators import login_required
from jetson.apps.configuration.models import SiteSettings
from jetson.apps.mailing.views import send_email_using_template, Recipient
from jetson.apps.utils.views import object_list
from jetson.apps.utils.context_processors import prev_next_processor
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social_django.utils import psa

from ccb.apps.curated_lists.models import ListOwner
from ccb.apps.accounts.forms import EmailOrUsernameAuthentication, SimpleRegistrationForm
from ccb.apps.accounts.forms import SimpleRegistrationForm
from ccb.apps.accounts.forms import PrivacySettingsForm

Site = apps.get_model("sites", "Site")
SiteSettings = apps.get_model("configuration", "SiteSettings")
User = apps.get_model("auth", "User")
image_mods = models.get_app("image_mods")
Institution = models.get_model("institutions", "Institution")

URL_ID_PERSON = get_installed("people.models.URL_ID_PERSON")
URL_ID_PEOPLE = get_installed("people.models.URL_ID_PEOPLE")
Person = apps.get_model("people", "Person")


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
    redirect_to = request.REQUEST.get(redirect_field_name, 'dashboard')
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
                    login_as_user = get_object_or_404(User, email__iexact=login_as)
                else:
                    login_as_user = get_object_or_404(User, username__iexact=login_as)
                login_as_user.backend = user.backend
                user = login_as_user
            auth_login(request, user)

            from ccb.apps.logins.models import LoginAction
            LoginAction.objects.create(user=user, user_agent=request.META.get('HTTP_USER_AGENT', ""))

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                # if not redirect_to.startswith("http"):
                #     redirect_to = smart_str(get_website_url(redirect_to))
                if request.is_ajax():
                    return HttpResponse("redirect=%s" % redirect_to)
                return redirect(redirect_to)
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


@never_cache
def social_connection_link(request):
    """
    logs in existing account by facebook account or gives a choice to
    * login and link to an existing account
    * register and link to the new account
    """
    backend = request.session.get('partial_pipeline', {}).get('backend', None)
    if not backend:
        return redirect("social_login")
    """
    request.session['partial_pipeline'] == {
        u'args': [],
        u'backend': u'yahoo',
        u'kwargs': {
            u'details': {
                u'email': u'aidasbend@yahoo.com',
                u'first_name': u'Aidas',
                u'fullname': u'Aidas Bendoraitis',
                u'last_name': u'Bendoraitis',
                u'nickname': u'archatas',
                u'username': u'AidasBendoraitis'
            },
            u'is_new': True,
            u'new_association': False,
            u'social': None,
            u'uid': u'https://me.yahoo.com/aaiddennium#6a55e',
            u'user': None,
            u'username': u'AidasBendoraitis'
        },
        u'next': 5
    }
    """
    return render(request, "accounts/unlinked_user.html")


@never_cache
def social_connection_login(request):
    """
    logs the user in and links him with facebook account
    """
    backend = request.session.get('partial_pipeline', {}).get('backend', None)
    if not backend:
        return redirect("social_login")
    """
    request.session['partial_pipeline'] == {
        u'args': [],
        u'backend': u'yahoo',
        u'kwargs': {
            u'details': {
                u'email': u'aidasbend@yahoo.com',
                u'first_name': u'Aidas',
                u'fullname': u'Aidas Bendoraitis',
                u'last_name': u'Bendoraitis',
                u'nickname': u'archatas',
                u'username': u'AidasBendoraitis'
            },
            u'is_new': True,
            u'new_association': False,
            u'social': None,
            u'uid': u'https://me.yahoo.com/aaiddennium#6a55e',
            u'user': None,
            u'username': u'AidasBendoraitis'
        },
        u'next': 5
    }
    """

    template_name = "accounts/login_and_link.html"

    response = login(request, template_name=template_name)

    # if there are any validation errors, return the form
    if response.status_code != 302:
        return response

    return redirect("social:complete", backend=backend)


@never_cache
def social_connection_register(request):
    """
    registers the new user in and links him with facebook account
    """
    backend = request.session.get('partial_pipeline', {}).get('backend', None)
    if not backend:
        return redirect("social_login")
    details = request.session['partial_pipeline']['kwargs']['details']
    """
    request.session['partial_pipeline'] == {
        u'args': [],
        u'backend': u'yahoo',
        u'kwargs': {
            u'details': {
                u'email': u'aidasbend@yahoo.com',
                u'first_name': u'Aidas',
                u'fullname': u'Aidas Bendoraitis',
                u'last_name': u'Bendoraitis',
                u'nickname': u'archatas',
                u'username': u'AidasBendoraitis'
            },
            u'is_new': True,
            u'new_association': False,
            u'social': None,
            u'uid': u'https://me.yahoo.com/aaiddennium#6a55e',
            u'user': None,
            u'username': u'AidasBendoraitis'
        },
        u'next': 5
    }
    """
    site_settings = SiteSettings.objects.get_current()

    if request.method == "POST":
        form = SimpleRegistrationForm(request, request.POST, request.FILES)
        if form.is_valid():
            # create User and Person instances
            user = form.save(activate_immediately=True)
            # login the user
            user.backend = "django.contrib.auth.backends.ModelBackend"
            auth_login(request, user)

            # change the next page from whatever it was to "registration complete"
            request.session['next'] = reverse('register_all_done')
            return redirect("social:complete", backend=backend)
    else:
        initial = {
            'email': details['email'],
            'username': get_unique_value(
                User,
                better_slugify(request.session['partial_pipeline']['kwargs']['username']).replace("-", "_"),
                field_name="username",
                separator="_",
            ),
            'first_name': details['first_name'],
            'last_name': details['last_name'],
        }

        form = SimpleRegistrationForm(request, initial=initial)

    return render(request, "accounts/register_and_link.html", {
        'form': form,
        'site_name': Site.objects.get_current().name,
        'login_by_email': site_settings.login_by_email,
    })


@login_required
@never_cache
def social_connections(request):
    return render(request, "accounts/social_connections.html", social_auth_context())


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
    try:
        user = User.objects.get(email=email)
    except:
        return redirect('register')
    user.backend = "django.contrib.auth.backends.ModelBackend"
    user.is_active = True
    user.save()
    person = user.profile
    person.status = "published"
    person.calculate_completeness()
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


@never_cache
def register_curator(request, encrypted_email, *arguments, **keywords):
    """The custom registration form should add create the user from with the default first_name, last_name, email values, and add them to the Curators group, and assign the user.profile to this owner.owner_content_object.
"""
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    try:
        email = decryptString(encrypted_email)
    except Exception as e:
        raise Http404
    try:
        owner = ListOwner.objects.get(email=email)
    except Exception as e:
        return redirect('register')
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
        form = SimpleRegistrationForm(request, initial=dict(first_name=owner.first_name, last_name=owner.last_name,
                                                            email=owner.email))
    request.session.set_test_cookie()
    return render_to_response('accounts/register.html', {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'site_name': Site.objects.get_current().name,
        'login_by_email': site_settings.login_by_email,
    }, context_instance=RequestContext(request))


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


@login_required
@never_cache
def dashboard(request, **kwargs):
    kwargs.setdefault('paginate_by', 24)
    kwargs.setdefault('allow_empty', True)
    kwargs.setdefault('context_processors', (prev_next_processor,))
    kwargs.setdefault('template_name', 'accounts/my_profile/dashboard.html')
    kwargs.setdefault('queryset', actstream.models.user_stream(request.user, with_user_activity=True))
    kwargs['extra_context'] = {
        'object': request.user.profile,
    }
    return object_list(request, **kwargs)


@login_required
@never_cache
def user_stream(request):
    """
    Render the template showing recent activitiy of the user, using actstream
    user_stream
    """
    # retrieve the stream from an user
    stream = actstream.models.user_stream(request.user, with_user_activity=True)
    template = "ccb/accounts/activities/user_stream.html"
    context = {
        # show the latest 20 activities
        "stream": stream[:20]
    }
    return render(request, template, context)


@login_required
@never_cache
def actor_stream(request):
    """
    Render the template showing recent activitiy of the user, using actstream
    user_stream
    """
    # retrieve the stream from an user
    stream = actstream.models.actor_stream(request.user)
    template = "ccb/accounts/activities/actor_stream.html"
    context = {
        # show the latest 20 activities
        "stream": stream[:20]
    }
    return render(request, template, context)


@login_required
@never_cache
def action_object_stream(request):
    """
    Render the template showing recent activitiy of the user, using actstream
    user_stream
    """
    # retrieve the stream from an user
    stream = actstream.models.action_object_stream(request.user)
    template = "ccb/accounts/activities/action_object_stream.html"
    context = {
        # show the latest 20 activities
        "stream": stream[:20]
    }
    return render(request, template, context)


@login_required
@never_cache
def target_stream(request):
    """
    Render the template showing recent activitiy of the user, using actstream
    user_stream
    """
    # retrieve the stream from an user
    stream = actstream.models.target_stream(request.user)
    template = "ccb/accounts/activities/target_stream.html"
    context = {
        # show the latest 20 activities
        "stream": stream[:20]
    }
    return render(request, template, context)


@login_required
@never_cache
def model_stream(request):
    """
    Render the template showing recent activitiy of the user, using actstream
    user_stream
    """
    # retrieve the stream from an user
    stream = actstream.models.model_stream(request.user)
    template = "ccb/accounts/activities/model_stream.html"
    context = {
        # show the latest 20 activities
        "stream": stream[:20]
    }
    return render(request, template, context)


@login_required
@never_cache
def any_stream(request):
    """
    Render the template showing recent activitiy of the user, using actstream
    user_stream
    """
    # retrieve the stream from an user
    stream = actstream.models.any_stream(request.user)
    template = "ccb/accounts/activities/any_stream.html"
    context = {
        # show the latest 20 activities
        "stream": stream[:20]
    }
    return render(request, template, context)
