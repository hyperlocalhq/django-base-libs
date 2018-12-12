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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from jetson.apps.utils.decorators import login_required
from jetson.apps.mailing.recipient import Recipient
from jetson.apps.mailing.views import send_email_using_template

from forms import EmailOrUsernameAuthentication
from forms import ClaimingInvitationForm
from forms import ClaimingRegisterForm
from forms import ClaimingLoginForm
from forms import ClaimingConfirmForm
from forms import RegistrationForm

from ajaxuploader.views import AjaxFileUploader

from base_libs.utils.misc import get_website_url
from base_libs.utils.crypt import cryptString, decryptString

ContentType = models.get_model("contenttypes", "ContentType")
User = models.get_model("auth", "User")
Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")
Event = models.get_model("events", "Event")
Workshop = models.get_model("workshops", "Workshop")

from forms import ExhibitionFilterForm, EventFilterForm, WorkshopFilterForm


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
            #if not redirect_to.startswith("http"):
            #    redirect_to = smart_str(get_website_url(redirect_to))
            if request.is_ajax():
                return HttpResponse("redirect=%s" % redirect_to)
            if user.groups.filter(name="Museum Owners").count():
                return redirect("dashboard")
            return redirect(redirect_to)
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
@login_required
def dashboard(request):
    owned_museums = Museum.objects.owned_by(request.user).order_by("-modified_date", "-creation_date")[:3]
    owned_exhibitions = Exhibition.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")[:3]
    owned_events = Event.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")[:3]
    owned_workshops = Workshop.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")[:3]
    context = {
        'owned_museums': owned_museums,
        'owned_exhibitions': owned_exhibitions,
        'owned_events': owned_events,
        'owned_workshops': owned_workshops,
    }
    return render(request, "accounts/dashboard.html", context)


@never_cache
@login_required
def dashboard_museums(request):
    owned_museum_qs = Museum.objects.owned_by(request.user).order_by("-modified_date", "-creation_date")
    paginator = Paginator(owned_museum_qs, 50)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)
    context = {
        'page': page,
    }
    return render(request, "accounts/dashboard_museums.html", context)


@never_cache
@login_required
def dashboard_exhibitions(request):
    owned_exhibition_qs = Exhibition.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")

    status = None
    form = ExhibitionFilterForm(request.REQUEST)
    if form.is_valid():
        status = form.cleaned_data['status'] or "published"
        owned_exhibition_qs = owned_exhibition_qs.filter(status=status)

    paginator = Paginator(owned_exhibition_qs, 50)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'status': status,
        'page': page,
        }
    return render(request, "accounts/dashboard_exhibitions.html", context)


@never_cache
@login_required
def dashboard_events(request):
    owned_event_qs = Event.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")

    status = None
    form = EventFilterForm(request.REQUEST)
    if form.is_valid():
        status = form.cleaned_data['status'] or "published"
        owned_event_qs = owned_event_qs.filter(status=status)

    paginator = Paginator(owned_event_qs, 50)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'status': status,
        'page': page,
    }
    return render(request, "accounts/dashboard_events.html", context)


@never_cache
@login_required
def dashboard_workshops(request):
    owned_workshop_qs = Workshop.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")

    status = None
    form = WorkshopFilterForm(request.REQUEST)
    if form.is_valid():
        status = form.cleaned_data['status'] or "published"
        owned_workshop_qs = owned_workshop_qs.filter(status=status)

    paginator = Paginator(owned_workshop_qs, 50)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'status': status,
        'page': page,
    }
    return render(request, "accounts/dashboard_workshops.html", context)
    

@never_cache
@staff_member_required
def invite_to_claim_museum(request):
    if request.method == "POST":
        form = ClaimingInvitationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            invitation_code = cryptString(cleaned['email'] + "|" + str(cleaned['museum'].pk))
            # setting default values
            sender_name, sender_email = settings.MANAGERS[0]
            send_email_using_template(
                recipients_list=[Recipient(email=cleaned['email'])],
                email_template_slug="claiming_invitation",
                obj_placeholders={
                    'invitation_code': invitation_code,
                    'object_link': cleaned['museum'].get_url(),
                    'object_title': cleaned['museum'].title,
                },
                sender_name=sender_name,
                sender_email=sender_email,
                delete_after_sending=False,
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
    
    register_form = ClaimingRegisterForm(u, initial={'email': email}, prefix="register")
    login_form = ClaimingLoginForm(u, initial={'email_or_username': email}, prefix="login")
    
    if request.method == "POST":
        from django.contrib.auth.models import Group
        group, _created = Group.objects.get_or_create(name=u"Museum Owners")
        
        if "register" in request.POST:
            register_form = ClaimingRegisterForm(u, request.POST, prefix="register")
            if register_form.is_valid():
                cleaned = register_form.cleaned_data
                
                # get or create a user
                if not u:
                    u = User(email=email)
                u.email = cleaned['email']
                u.username = cleaned['email'][:30]
                u.is_active = True
                u.set_password(cleaned['password'])
                u.save()
                u.groups.add(group)
                # set museum's and its exhibitions' owner
                museum.set_owner(u)
                for e in museum.get_exhibitions():
                    e.set_owner(u)
                for e in museum.get_events():
                    e.set_owner(u)
                for w in museum.get_workshops():
                    w.set_owner(u)
                    
                # login the current user
                user = authenticate(email=cleaned['email'], password=cleaned['password'])
                auth_login(request, user)
                return redirect("dashboard")
        if "login" in request.POST:
            login_form = ClaimingLoginForm(u, request.POST, prefix="login")
            if login_form.is_valid():
                u = login_form.get_user()
                u.groups.add(group)
                # set museum's and its exhibitions' owner
                museum.set_owner(u)
                for e in museum.get_exhibitions():
                    e.set_owner(u)
                for e in museum.get_events():
                    e.set_owner(u)
                for w in museum.get_workshops():
                    w.set_owner(u)
                auth_login(request, u)
                return redirect("dashboard")
        if "confirm" in request.POST:
            u = authenticate(email=email)
            u.groups.add(group)
            # set museum's and its exhibitions' owner
            museum.set_owner(u)
            for e in museum.get_exhibitions():
                e.set_owner(u)
            for e in museum.get_events():
                e.set_owner(u)
            for w in museum.get_workshops():
                w.set_owner(u)
            auth_login(request, u)
            return redirect("dashboard")
            
    context = {
        'register_form': register_form,
        'login_form': login_form,
        'museum': museum,
        'user': u,
    }
    if u:
        confirm_form = ClaimingConfirmForm(u, prefix="confirm")
        context['confirm_form'] = confirm_form
    return render(request, "site_specific/claiming_confirmation.html", context)


@never_cache
def register(request):
    
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
            
            return redirect('/signup/almost-done/')
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
        return redirect('/signup/')
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
    return redirect('/signup/welcome/')

uploader = AjaxFileUploader()
