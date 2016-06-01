# -*- coding: UTF-8 -*-

from django.db import models
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site, RequestSite
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.encoding import smart_str
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from museumsportal.apps.mailing.recipient import Recipient
from museumsportal.apps.mailing.views import send_email_using_template

from .models import PrivacySettings
from .forms import EmailOrUsernameAuthentication
from .forms import RegistrationForm
from .forms import PrivacySettingsForm
from .forms import ProfileForm

from base_libs.utils.misc import get_website_url
from base_libs.middleware.threadlocals import get_current_language
from base_libs.utils.crypt import cryptString, decryptString

from jetson.apps.utils.decorators import login_required

User = models.get_model("auth", "User")

@never_cache
def login(request, template_name='registration/login.html', redirect_field_name=getattr(settings, "REDIRECT_FIELD_NAME", REDIRECT_FIELD_NAME), redirect_to="dashboard"):
    "Displays the login form and handles the login action."
    redirect_to = request.REQUEST.get(redirect_field_name, '') or redirect_to
    if request.method == "POST":
        form = EmailOrUsernameAuthentication(request, data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
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
            #if not redirect_to.startswith("http"):
            #    redirect_to = smart_str(get_website_url(redirect_to))
            if request.is_ajax():
                return HttpResponse("redirect=%s" % redirect_to)
            if redirect_to:
                return redirect(redirect_to)
            return redirect('/{}/dashboard/'.format(get_current_language()))
    else:
        data = {
            'email_or_username': request.GET.get('login_as', ''),
            'login_as': request.GET.get('login_as', ''),
        }
        form = EmailOrUsernameAuthentication(request, initial=data)
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
    from mailsnake import MailSnake, EmailAlreadySubscribedException
    from jetson.apps.mailchimp.models import MList
    from jetson.apps.mailchimp.models import Subscription
    from jetson.apps.mailchimp.models import Settings

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            # get or create a user
            u = User()
            u.email = cleaned['email']
            u.username = cleaned['username']
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

            try:
                s = Settings.objects.get()
            except Exception:
                pass
            else:
                ms = MailSnake(s.api_key)
                for ml in MList.site_objects.filter(is_public=True):
                    if cleaned['newsletter_%s' % ml.pk]:
                        if s.double_optin:
                            status = "pending"
                        else:
                            status = "subscribed"
                        try:
                            sub = Subscription.objects.create(
                                subscriber=u,
                                ip=request.META['REMOTE_ADDR'],
                                mailinglist=ml,
                                status=status,
                            )
                        except:
                            pass
                        else:
                            if ml.mailchimp_id:
                                try:
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
                                except EmailAlreadySubscribedException:
                                    pass

            return redirect('/{}/signup/almost-done/'.format(get_current_language()))
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, "accounts/register.html", context)


def confirm_registration(request, encrypted_email):
    "Displays the registration form and handles the registration action"
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    try:
        email = decryptString(encrypted_email)
    except:
        raise Http404
    user = authenticate(email=email)
    if not user:
        return redirect('/{}/signup/'.format(get_current_language()))
    user.is_active = True
    user.save()
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
    return redirect('/{}/signup/welcome/'.format(get_current_language()))


@never_cache
@login_required
def change_privacy_settings(request):
    try:
        privacy_settings = request.user.privacysettings
    except:
        privacy_settings = PrivacySettings(user=request.user)
    if request.method == "POST":
        form = PrivacySettingsForm(data=request.POST, instance=privacy_settings)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your privacy settings have been successfully saved.'))
            return redirect(request.path)
    else:
        form = PrivacySettingsForm(instance=privacy_settings)
    return render(request, "accounts/privacy_settings.html", {'form': form})


@never_cache
@login_required
def change_profile(request):
    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile has been successfully saved.'))
            return redirect(request.path)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {'form': form})
