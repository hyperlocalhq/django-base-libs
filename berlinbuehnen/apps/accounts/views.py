# -*- coding: UTF-8 -*-

from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site, RequestSite
from django.http import Http404, HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

from jetson.apps.mailing.recipient import Recipient
from jetson.apps.mailing.views import send_email_using_template

from .forms import EmailOrUsernameAuthentication
from .forms import RegistrationForm
from .app_settings import DASHBOARD_USER_GROUPS

from base_libs.utils.crypt import cryptString, decryptString

User = models.get_model("auth", "User")

@never_cache
def login(request, template_name='registration/login.html', redirect_field_name=getattr(settings, "REDIRECT_FIELD_NAME", REDIRECT_FIELD_NAME), redirect_to=""):
    """ Displays the login form and handles the login action. """
    redirect_to = request.REQUEST.get(redirect_field_name, '') or redirect_to
    if request.method == "POST":
        form = EmailOrUsernameAuthentication(request, data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            user = form.get_user()
            login_as = request.REQUEST.get("login_as", "")
            if user.is_superuser and login_as:
                if "@" in login_as:
                    login_as_user = get_object_or_404(User, email=login_as)
                else:
                    login_as_user = get_object_or_404(User, username=login_as)
                login_as_user.backend = user.backend
                user = login_as_user
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            auth_login(request, user)
            request.session.save()
            if request.is_ajax():
                return HttpResponse("redirect=%s" % redirect_to)
            if user.groups.filter(name__in=DASHBOARD_USER_GROUPS).count():
                return redirect("dashboard")
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
    }
    if request.is_ajax():
        context['base_template'] = "base_ajax.html"
    return render(
        request,
        template_name,
        context,
    )


@never_cache
def register(request):
    """ Displays the registration form and handles the registration action. """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            # get or create a user
            u = User()
            u.email = cleaned['email']
            u.username = cleaned['email'][:30]
            # u.first_name = cleaned['first_name']
            # u.last_name = cleaned['last_name']
            u.set_password(cleaned['password'])
            u.is_active = False
            u.save()

            current_site = Site.objects.get_current()
            encrypted_email = cryptString(u.email)

            sender_name, sender_email = settings.MANAGERS[0]
            send_email_using_template(
                [Recipient(user=u)],
                "account_verification",
                obj_placeholders={
                    'encrypted_email': encrypted_email,
                    'site_name': current_site.name,
                },
                delete_after_sending=False,
                sender_name=sender_name,
                sender_email=sender_email,
                send_immediately=True,
            )

            return redirect("signup_almost_done")
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, "accounts/register.html", context)


def confirm_registration(request, encrypted_email):
    """ Handles the registration confirmation action. """
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    try:
        email = decryptString(encrypted_email)
    except:
        raise Http404
    user = authenticate(email=email)
    if not user:
        return redirect("signup")
    user.is_active = True
    user.save()
    auth_login(request, user)

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
    return redirect("signup_welcome")

