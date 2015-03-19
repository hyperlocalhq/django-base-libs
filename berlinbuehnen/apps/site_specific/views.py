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
from jetson.apps.favorites.models import Favorite

from jetson.apps.mailing.recipient import Recipient
from jetson.apps.mailing.views import send_email_using_template

from forms import EmailOrUsernameAuthentication
from forms import ClaimingInvitationForm
from forms import ClaimingRegisterForm
from forms import ClaimingLoginForm
from forms import ClaimingConfirmForm
from forms import RegistrationForm

from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.default_storage import DefaultStorageUploadBackend

from base_libs.utils.crypt import cryptString, decryptString

ContentType = models.get_model("contenttypes", "ContentType")
User = models.get_model("auth", "User")
Location = models.get_model("locations", "Location")
Production = models.get_model("productions", "Production")
Parent = models.get_model("multiparts", "Parent")

# from forms import ExhibitionFilterForm, EventFilterForm, WorkshopFilterForm, ShopFilterForm


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
            if user.groups.filter(name="Location Owners").count():
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
    owned_locations = Location.objects.accessible_to(request.user).order_by("-modified_date", "-creation_date")[:3]
    owned_productions = Production.objects.accessible_to(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")[:3]
    owned_multiparts = Parent.objects.accessible_to(request.user).order_by("-modified_date", "-creation_date")[:3]
    context = {
        'owned_locations': owned_locations,
        'owned_productions': owned_productions,
        'owned_multiparts': owned_multiparts,
    }
    return render(request, "accounts/dashboard.html", context)

@never_cache
@login_required
def dashboard_locations(request):
    owned_location_qs = Location.objects.accessible_to(request.user).order_by("-modified_date", "-creation_date")
    paginator = Paginator(owned_location_qs, 50)
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
    return render(request, "accounts/dashboard_locations.html", context)


@never_cache
@login_required
def dashboard_productions(request):
    owned_production_qs = Production.objects.accessible_to(request.user).order_by("-modified_date", "-creation_date")
    paginator = Paginator(owned_production_qs, 50)
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
    return render(request, "accounts/dashboard_productions.html", context)


@never_cache
@login_required
def dashboard_multiparts(request):
    owned_multipart_qs = Parent.objects.accessible_to(request.user).order_by("-modified_date", "-creation_date")
    paginator = Paginator(owned_multipart_qs, 50)
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
    return render(request, "accounts/dashboard_multiparts.html", context)


@never_cache
@staff_member_required
def invite_to_claim_location(request):
    if request.method == "POST":
        form = ClaimingInvitationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            invitation_code = cryptString(cleaned['email'] + "|" + str(cleaned['location'].pk))
            # setting default values
            sender_name, sender_email = settings.MANAGERS[0]
            send_email_using_template(
                recipients_list=[Recipient(email=cleaned['email'])],
                email_template_slug="claiming_invitation",
                obj_placeholders={
                    'invitation_code': invitation_code,
                    'object_link': cleaned['location'].get_url(),
                    'object_title': cleaned['location'].title,
                },
                sender_name=sender_name,
                sender_email=sender_email,
                delete_after_sending=False,
            )

            return redirect("invite_to_claim_location_done")
    else:
        location_id = request.REQUEST.get("location_id", None)
        try:
            location = Location.objects.get(pk=location_id)
        except:
            location = None
        form = ClaimingInvitationForm(initial={'location': location})
    context = {
        'form': form,
    }
    return render(request, "site_specific/claiming_invitation.html", context)


@never_cache
def register_and_claim_location(request, invitation_code):
    try:
        email, location_id = decryptString(invitation_code).split("|")
    except:
        raise Http404, _("Wrong invitation code.")
    try:
        location = Location.objects.get(pk=location_id)
    except:
        raise Http404, _("Location doesn't exist.")

    try:
        u = User.objects.get(email=email)
    except User.DoesNotExist:
        u = None

    register_form = ClaimingRegisterForm(u, initial={'email': email}, prefix="register")
    login_form = ClaimingLoginForm(u, initial={'email_or_username': email}, prefix="login")

    if request.method == "POST":
        from django.contrib.auth.models import Group
        group, _created = Group.objects.get_or_create(name=u"Location Owners")

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
                # set location's and its exhibitions' owner
                location.set_owner(u)
                for p in location.program_productions.all():
                    p.set_owner(u)
                    try:
                        p.multipart.set_owner(u)
                    except models.ObjectDoesNotExist:
                        pass

                # login the current user
                user = authenticate(email=cleaned['email'], password=cleaned['password'])
                auth_login(request, user)
                return redirect("dashboard")
        if "login" in request.POST:
            login_form = ClaimingLoginForm(u, request.POST, prefix="login")
            if login_form.is_valid():
                u = login_form.get_user()
                u.groups.add(group)
                # set location's and its exhibitions' owner
                location.set_owner(u)
                for p in location.program_productions.all():
                    p.set_owner(u)
                    try:
                        p.multipart.set_owner(u)
                    except models.ObjectDoesNotExist:
                        pass
                auth_login(request, u)
                return redirect("dashboard")
        if "confirm" in request.POST:
            u = authenticate(email=email)
            u.groups.add(group)
            # set location's and its exhibitions' owner
            location.set_owner(u)
            for p in location.program_productions.all():
                p.set_owner(u)
                try:
                    p.multipart.set_owner(u)
                except models.ObjectDoesNotExist:
                    pass
            auth_login(request, u)
            return redirect("dashboard")

    context = {
        'register_form': register_form,
        'login_form': login_form,
        'location': location,
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


class ASCIIFileSystemStorageBackend(DefaultStorageUploadBackend):
    def update_filename(self, request, filename, *args, **kwargs):
        from django.core.files.storage import default_storage
        return default_storage.get_valid_name(filename)


uploader = AjaxFileUploader(backend=ASCIIFileSystemStorageBackend)

#
# @login_required
# def favorites(request, **kwargs):
#     """
#     Displays the list of favorite objects
#     """
#     location_ids = list(Favorite.objects.filter(
#         content_type__app_label="locations",
#         content_type__model="location",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     exhibition_ids = list(Favorite.objects.filter(
#         content_type__app_label="exhibitions",
#         content_type__model="exhibition",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     event_ids = list(Favorite.objects.filter(
#         content_type__app_label="events",
#         content_type__model="event",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     workshop_ids = list(Favorite.objects.filter(
#         content_type__app_label="workshops",
#         content_type__model="workshop",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     favorites = (
#         ('locations', Location.objects.filter(id__in=location_ids, status="published")),
#         ('exhibitions', Exhibition.objects.filter(id__in=exhibition_ids, status="published")),
#         ('events', Event.objects.filter(id__in=event_ids, status="published")),
#         ('workshops', Workshop.objects.filter(id__in=workshop_ids, status="published")),
#     )
#     return render(request, "favorites/favorites.html", {
#         'favorites': favorites,
#     })
#
#
# @login_required
# def favorite_locations(request, **kwargs):
#     """
#     Displays the list of favorite objects
#     """
#     location_ids = list(Favorite.objects.filter(
#         content_type__app_label="locations",
#         content_type__model="location",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     favorites = (
#         ('locations', Location.objects.filter(id__in=location_ids, status="published")),
#     )
#     return render(request, "favorites/favorite_locations.html", {
#         'favorites': favorites,
#     })
#
#
# @login_required
# def favorite_exhibitions(request, **kwargs):
#     """
#     Displays the list of favorite objects
#     """
#     exhibition_ids = list(Favorite.objects.filter(
#         content_type__app_label="exhibitions",
#         content_type__model="exhibition",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     favorites = (
#         ('exhibitions', Exhibition.objects.filter(id__in=exhibition_ids, status="published")),
#     )
#     return render(request, "favorites/favorite_exhibitions.html", {
#         'favorites': favorites,
#     })
#
#
# @login_required
# def favorite_events(request, **kwargs):
#     """
#     Displays the list of favorite objects
#     """
#     event_ids = list(Favorite.objects.filter(
#         content_type__app_label="events",
#         content_type__model="event",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     favorites = (
#         ('events', Event.objects.filter(id__in=event_ids, status="published")),
#     )
#     return render(request, "favorites/favorite_events.html", {
#         'favorites': favorites,
#     })
#
#
# @login_required
# def favorite_workshops(request, **kwargs):
#     """
#     Displays the list of favorite objects
#     """
#     workshop_ids = list(Favorite.objects.filter(
#         content_type__app_label="workshops",
#         content_type__model="workshop",
#         user=request.user,
#     ).values_list("object_id", flat=True))
#
#     favorites = (
#         ('workshops', Workshop.objects.filter(id__in=workshop_ids, status="published")),
#     )
#     return render(request, "favorites/favorite_workshops.html", {
#         'favorites': favorites,
#     })
