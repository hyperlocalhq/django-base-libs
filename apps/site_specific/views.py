# -*- coding: UTF-8 -*-

from django.db import models
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import Http404
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout

from jetson.apps.utils.decorators import login_required
from jetson.apps.favorites.models import Favorite

from museumsportal.apps.mailing.recipient import Recipient
from museumsportal.apps.mailing.views import send_email_using_template

from .forms import ClaimingInvitationForm
from .forms import ClaimingRegisterForm
from .forms import ClaimingLoginForm
from .forms import ClaimingConfirmForm
from .forms import ProfileDeletionForm

from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.default_storage import DefaultStorageUploadBackend

from base_libs.utils.misc import get_website_url
from base_libs.utils.crypt import cryptString, decryptString

ContentType = models.get_model("contenttypes", "ContentType")
User = models.get_model("auth", "User")
Museum = models.get_model("museums", "Museum")
Exhibition = models.get_model("exhibitions", "Exhibition")
Event = models.get_model("events", "Event")
Workshop = models.get_model("workshops", "Workshop")
ShopProduct = models.get_model("shop", "ShopProduct")

from .forms import ExhibitionFilterForm, EventFilterForm, WorkshopFilterForm, ShopFilterForm


@never_cache
@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.groups.filter(name__in=("Museum Owners", "Shop Admins")):
        owned_museums = Museum.objects.owned_by(request.user).order_by("-modified_date", "-creation_date")[:3]
        owned_exhibitions = Exhibition.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")[:3]
        owned_events = Event.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")[:3]
        owned_workshops = Workshop.objects.owned_by(request.user).filter(status__in=("published", "draft", "expired")).order_by("-modified_date", "-creation_date")[:3]
        owned_products = ShopProduct.objects.owned_by(request.user).filter(status__in=("published", "draft")).order_by("-modified_date", "-creation_date")[:3]
        context = {
            'owned_museums': owned_museums,
            'owned_exhibitions': owned_exhibitions,
            'owned_events': owned_events,
            'owned_workshops': owned_workshops,
            'owned_products': owned_products,
        }
        return render(request, "accounts/dashboard_admin.html", context)
    else:
        return render(request, "accounts/dashboard.html")

    
@never_cache
@login_required
def dashboard_shopproducts(request):
    owned_shop_qs = ShopProduct.objects.owned_by(request.user).filter(status__in=("published", "draft")).order_by("-modified_date", "-creation_date")

    status = None
    form = ShopFilterForm(request.REQUEST)
    if form.is_valid():
        status = form.cleaned_data['status'] or "published"
        owned_shop_qs = owned_shop_qs.filter(status=status)
        
    paginator = Paginator(owned_shop_qs, 50)
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
    return render(request, "accounts/dashboard_shopproducts.html", context)
    

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


class ASCIIFileSystemStorageBackend(DefaultStorageUploadBackend):
    def update_filename(self, request, filename, *args, **kwargs):
        from django.core.files.storage import default_storage
        return default_storage.get_valid_name(filename)


uploader = AjaxFileUploader(backend=ASCIIFileSystemStorageBackend)

USER_TOKEN_SUMMAND = 564654


@login_required
def redirect_to_user_favorites(request):
    user = request.user
    user_token = user.pk + USER_TOKEN_SUMMAND
    return redirect('user_favorites', user_token=user_token)


def user_favorites(request, user_token, **kwargs):
    """
    Displays the list of favorite objects
    """
    user_id = int(user_token) - USER_TOKEN_SUMMAND

    favorites = Favorite.objects.filter(
        user__pk=user_id,
    )
    return render(request, kwargs["template_name"], {
        'object_list': favorites,
    })


@login_required
def favorites(request, **kwargs):
    """
    Displays the list of favorite objects
    """
    museum_ids = list(Favorite.objects.filter(
        content_type__app_label="museums",
        content_type__model="museum",
        user=request.user,
    ).values_list("object_id", flat=True))

    exhibition_ids = list(Favorite.objects.filter(
        content_type__app_label="exhibitions",
        content_type__model="exhibition",
        user=request.user,
    ).values_list("object_id", flat=True))

    event_ids = list(Favorite.objects.filter(
        content_type__app_label="events",
        content_type__model="event",
        user=request.user,
    ).values_list("object_id", flat=True))

    workshop_ids = list(Favorite.objects.filter(
        content_type__app_label="workshops",
        content_type__model="workshop",
        user=request.user,
    ).values_list("object_id", flat=True))

    favorites = (
        ('museums', Museum.objects.filter(id__in=museum_ids, status="published")),
        ('exhibitions', Exhibition.objects.filter(id__in=exhibition_ids, status="published")),
        ('events', Event.objects.filter(id__in=event_ids, status="published")),
        ('workshops', Workshop.objects.filter(id__in=workshop_ids, status="published")),
    )
    return render(request, "favorites/favorites.html", {
        'favorites': favorites,
    })


@login_required
def favorite_museums(request, **kwargs):
    """
    Displays the list of favorite objects
    """
    museum_ids = list(Favorite.objects.filter(
        content_type__app_label="museums",
        content_type__model="museum",
        user=request.user,
    ).values_list("object_id", flat=True))

    favorites = (
        ('museums', Museum.objects.filter(id__in=museum_ids, status="published")),
    )
    return render(request, "favorites/favorite_museums.html", {
        'favorites': favorites,
    })


@login_required
def favorite_exhibitions(request, **kwargs):
    """
    Displays the list of favorite objects
    """
    exhibition_ids = list(Favorite.objects.filter(
        content_type__app_label="exhibitions",
        content_type__model="exhibition",
        user=request.user,
    ).values_list("object_id", flat=True))

    favorites = (
        ('exhibitions', Exhibition.objects.filter(id__in=exhibition_ids, status="published")),
    )
    return render(request, "favorites/favorite_exhibitions.html", {
        'favorites': favorites,
    })


@login_required
def favorite_events(request, **kwargs):
    """
    Displays the list of favorite objects
    """
    event_ids = list(Favorite.objects.filter(
        content_type__app_label="events",
        content_type__model="event",
        user=request.user,
    ).values_list("object_id", flat=True))

    favorites = (
        ('events', Event.objects.filter(id__in=event_ids, status="published")),
    )
    return render(request, "favorites/favorite_events.html", {
        'favorites': favorites,
    })


@login_required
def favorite_workshops(request, **kwargs):
    """
    Displays the list of favorite objects
    """
    workshop_ids = list(Favorite.objects.filter(
        content_type__app_label="workshops",
        content_type__model="workshop",
        user=request.user,
    ).values_list("object_id", flat=True))

    favorites = (
        ('workshops', Workshop.objects.filter(id__in=workshop_ids, status="published")),
    )
    return render(request, "favorites/favorite_workshops.html", {
        'favorites': favorites,
    })


@never_cache
@login_required
def delete_profile(request):
    context = {}
    if request.method == "POST":
        form = ProfileDeletionForm(request.user, request.POST)
        if form.is_valid():
            # delete chosen profiles
            form.delete()
            # if user deleted, logout
            logout(request)
            return redirect("delete_profile_done")
    else:
        form = ProfileDeletionForm(request.user)

    context['form'] = form

    return render(request, 'accounts/delete_profile.html', context)
