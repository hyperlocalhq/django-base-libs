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

from jetson.apps.utils.decorators import login_required
from jetson.apps.mailing.recipient import Recipient
from jetson.apps.mailing.views import send_email_using_template

from forms import EmailOrUsernameAuthentication
from forms import ClaimingInvitationForm
from forms import ClaimingConfirmationForm

from base_libs.utils.misc import get_website_url
from base_libs.utils.crypt import cryptString, decryptString

ContentType = models.get_model("contenttypes", "ContentType")
User = models.get_model("auth", "User")
Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")

@never_cache
def login(request, template_name='registration/login.html', redirect_field_name=getattr(settings, "REDIRECT_FIELD_NAME", REDIRECT_FIELD_NAME), redirect_to=""):
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
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                if not redirect_to.startswith("http"):
                    redirect_to = smart_str(get_website_url(redirect_to))
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
        }
    if request.is_ajax():
        context['base_template'] = "base_ajax.html"
    return render(
        request,
        template_name,
        context,
        )

@never_cache
@login_required
def dashboard(request):
    owned_museums = Museum.objects.owned_by(request.user)
    owned_exhibitions = Exhibition.objects.owned_by(request.user)
    context = {
        'owned_museums': owned_museums,
        'owned_exhibitions': owned_exhibitions,
        }
    return render(request, "accounts/dashboard.html", context)

@never_cache
@staff_member_required
def invite_to_claim_museum(request):
    if request.method == "POST":
        form = ClaimingInvitationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            print cleaned
            invitation_code = cryptString(cleaned['email'] + "|" + str(cleaned['museum'].pk))
            # setting default values
            sender_name = settings.ADMINS[0][0]
            sender_email = settings.ADMINS[0][1]
            send_email_using_template(
                recipients_list=[Recipient(email=cleaned['email'])],
                email_template_slug="claiming_invitation",
                obj_placeholders={
                    'invitation_code': invitation_code,
                    'object_link': cleaned['museum'].get_url(),
                    'object_title': cleaned['museum'].title,
                },
                sender_name = sender_name,
                sender_email = sender_email,
                delete_after_sending = False,
                )
            
            return redirect("invite_to_claim_museum_done")
    else:
        museum_id = request.REQUEST.get("museum_id", None)
        try:
            museum = Museum.objects.get(pk=museum_id)
        except:
            museum = None
        form = ClaimingInvitationForm(initial={'museum': museum})
    context = {
        'form': form,
        }
    return render(request, "site_specific/claiming_invitation.html", context)
    
@never_cache
def register_and_claim_museum(request, invitation_code):
    try:
        email, museum_id = decryptString(invitation_code).split("|")
    except:
        raise Http404, _("Wrong invitation code.")
    try:
        museum = Museum.objects.get(pk=museum_id)
    except:
        raise Http404, _("Museum doesn't exist.")
    
    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        u = None
    
    if request.method == "POST":
        form = ClaimingConfirmationForm(u, request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            
            # get or create a user
            if not u:
                u = User(email=email)
            u.username = cleaned['username']
            u.first_name = cleaned['first_name']
            u.last_name = cleaned['last_name']
            u.is_active = True
            u.set_password(cleaned['password'])
            u.save()
            
            # set museum's and its exhibitions' owner
            museum.set_owner(u)
            for e in museum.exhibition_set.all():
                e.set_owner(u)
            for e in museum.organized_exhibitions.all():
                e.set_owner(u)
                
            # login the current user
            user = authenticate(username=cleaned['username'], password=cleaned['password'])
            auth_login(request, user)
            return redirect("museum_detail", slug=museum.slug)
    else:
        initial = None
        if u:
            initial = {
                'username': u.username,
                'first_name': u.first_name,
                'last_name': u.last_name,
                }
        form = ClaimingConfirmationForm(u, initial=initial)
    context = {
        'form': form,
        'museum': museum,
        }
    return render(request, "site_specific/claiming_confirmation.html", context)
    

