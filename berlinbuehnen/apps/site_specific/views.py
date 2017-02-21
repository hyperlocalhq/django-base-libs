# -*- coding: UTF-8 -*-
from datetime import datetime
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from jetson.apps.utils.decorators import login_required
from jetson.apps.favorites.models import Favorite

from jetson.apps.mailing.recipient import Recipient
from jetson.apps.mailing.views import send_email_using_template

from .forms import ClaimingInvitationForm
from .forms import ClaimingRegisterForm
from .forms import ClaimingLoginForm
from .forms import ClaimingConfirmForm

from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.default_storage import DefaultStorageUploadBackend

from base_libs.utils.crypt import cryptString, decryptString

ContentType = models.get_model("contenttypes", "ContentType")
User = models.get_model("auth", "User")
Location = models.get_model("locations", "Location")
Production = models.get_model("productions", "Production")
Festival = models.get_model("festivals", "Festival")
Parent = models.get_model("multiparts", "Parent")
JobOffer = models.get_model("marketplace", "JobOffer")
EducationalDepartment = models.get_model("education", "Department")
EducationalProjects = models.get_model("education", "Project")

# from forms import ExhibitionFilterForm, EventFilterForm, WorkshopFilterForm, ShopFilterForm

@never_cache
@login_required
def dashboard(request):
    owned_locations = Location.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(locations_location.modified_date, locations_location.creation_date)'
    }).order_by("-modified_or_creation_date")[:3]
    owned_productions = Production.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(productions_production.modified_date, productions_production.creation_date)'
    }).filter(status__in=('published', 'draft', 'expired', 'not_listed', 'import')).order_by("-modified_or_creation_date")[:3]
    owned_multiparts = Parent.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(multiparts_parent.modified_date, multiparts_parent.creation_date)'
    }).order_by("-modified_or_creation_date")[:3]
    owned_festivals = Festival.objects.accessible_to(request.user).filter(status__in=('published', 'draft', 'expired', 'not_listed', 'import')).extra(select={
        'modified_or_creation_date': 'IFNULL(festivals_festival.modified_date, festivals_festival.creation_date)'
    }).order_by("-modified_or_creation_date")[:3]
    owned_job_offers = JobOffer.objects.accessible_to(request.user).filter(status__in=('published', 'draft', 'expired', 'not_listed', 'import')).extra(select={
        'modified_or_creation_date': 'IFNULL(marketplace_joboffer.modified_date, marketplace_joboffer.creation_date)'
    }).order_by("-modified_or_creation_date")[:3]
    owned_educational_departments = EducationalDepartment.objects.accessible_to(request.user).filter(status__in=('published', 'draft', 'expired', 'not_listed', 'import')).extra(select={
        'modified_or_creation_date': 'IFNULL(education_department.modified_date, education_department.creation_date)'
    }).order_by("-modified_or_creation_date")[:3]
    owned_educational_projects = EducationalProjects.objects.accessible_to(request.user).filter(status__in=('published', 'draft', 'expired', 'not_listed', 'import')).extra(select={
        'modified_or_creation_date': 'IFNULL(education_project.modified_date, education_project.creation_date)'
    }).order_by("-modified_or_creation_date")[:3]
    context = {
        'owned_locations': owned_locations,
        'owned_productions': owned_productions,
        'owned_multiparts': owned_multiparts,
        'owned_festivals': owned_festivals,
        'owned_job_offers': owned_job_offers,
        'owned_educational_departments': owned_educational_departments,
        'owned_educational_projects': owned_educational_projects,
    }
    return render(request, "site_specific/dashboard.html", context)

@never_cache
@login_required
def dashboard_locations(request):
    owned_location_qs = Location.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(locations_location.modified_date, locations_location.creation_date)'
    })

    status = request.REQUEST.get('status', 'published')
    if status in ('published', 'draft', 'not_listed'):
        owned_location_qs = owned_location_qs.filter(status=status)

    q = request.REQUEST.get('q', '')
    if q:
        owned_location_qs = owned_location_qs.filter(
            models.Q(title_de__icontains=q) | models.Q(title_en__icontains=q) |
            models.Q(subtitle_de__icontains=q) | models.Q(subtitle_en__icontains=q)
        )

    sort_by = request.REQUEST.get('sort_by', 'date')
    if sort_by == 'title':
        owned_location_qs = owned_location_qs.order_by("title_de")
    elif sort_by == '-title':
        owned_location_qs = owned_location_qs.order_by("-title_de")
    elif sort_by == '-date':
        owned_location_qs = owned_location_qs.order_by("modified_or_creation_date")
    else:
        owned_location_qs = owned_location_qs.order_by("-modified_or_creation_date")

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
        'q': q,
        'status': status,
        'sort_by': sort_by,
    }
    return render(request, "site_specific/dashboard_locations.html", context)


@never_cache
@login_required
def dashboard_productions(request):
    owned_production_qs = Production.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(productions_production.modified_date, productions_production.creation_date)'
    })

    status = request.REQUEST.get('status', 'published')
    if status in ('published', 'draft', 'expired', 'not_listed', 'import'):
        owned_production_qs = owned_production_qs.filter(status=status)

    q = request.REQUEST.get('q', '')
    if q:
        owned_production_qs = owned_production_qs.filter(
            models.Q(title_de__icontains=q) | models.Q(title_en__icontains=q) |
            models.Q(prefix_de__icontains=q) | models.Q(prefix_en__icontains=q) |
            models.Q(subtitle_de__icontains=q) | models.Q(subtitle_en__icontains=q) |
            models.Q(original_de__icontains=q) | models.Q(original_en__icontains=q)
        )

    sort_by = request.REQUEST.get('sort_by', 'date')
    if sort_by == 'title':
        owned_production_qs = owned_production_qs.order_by("title_de")
    elif sort_by == '-title':
        owned_production_qs = owned_production_qs.order_by("-title_de")
    elif sort_by == '-date':
        owned_production_qs = owned_production_qs.order_by("modified_or_creation_date")
    else:
        owned_production_qs = owned_production_qs.order_by("-modified_or_creation_date")

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
        'q': q,
        'status': status,
        'sort_by': sort_by,
    }
    return render(request, "site_specific/dashboard_productions.html", context)


@never_cache
@login_required
def dashboard_festivals(request):
    owned_festival_qs = Festival.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(festivals_festival.modified_date, festivals_festival.creation_date)'
    })

    status = request.REQUEST.get('status', 'published')
    if status in ('published', 'draft', 'expired', 'not_listed', 'import'):
        owned_festival_qs = owned_festival_qs.filter(status=status)

    q = request.REQUEST.get('q', '')
    if q:
        owned_festival_qs = owned_festival_qs.filter(
            models.Q(title_de__icontains=q) | models.Q(title_en__icontains=q) |
            models.Q(subtitle_de__icontains=q) | models.Q(subtitle_en__icontains=q)
        )

    sort_by = request.REQUEST.get('sort_by', 'date')
    if sort_by == 'title':
        owned_festival_qs = owned_festival_qs.order_by("title_de")
    elif sort_by == '-title':
        owned_festival_qs = owned_festival_qs.order_by("-title_de")
    elif sort_by == '-date':
        owned_festival_qs = owned_festival_qs.order_by("modified_or_creation_date")
    else:
        owned_festival_qs = owned_festival_qs.order_by("-modified_or_creation_date")

    paginator = Paginator(owned_festival_qs, 50)
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
        'q': q,
        'status': status,
        'sort_by': sort_by,
    }
    return render(request, "site_specific/dashboard_festivals.html", context)


@never_cache
@login_required
def dashboard_multiparts(request):
    owned_multipart_qs = Parent.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(multiparts_parent.modified_date, multiparts_parent.creation_date)'
    })

    status = request.REQUEST.get('status', 'published')
    if status in ('published', 'draft', 'expired', 'not_listed'):
        owned_multipart_qs = owned_multipart_qs.filter(production__status=status)

    q = request.REQUEST.get('q', '')
    if q:
        owned_multipart_qs = owned_multipart_qs.filter(
            models.Q(production__title_de__icontains=q) | models.Q(production__title_en__icontains=q) |
            models.Q(production__prefix_de__icontains=q) | models.Q(production__prefix_en__icontains=q) |
            models.Q(production__subtitle_de__icontains=q) | models.Q(production__subtitle_en__icontains=q) |
            models.Q(production__original_de__icontains=q) | models.Q(production__original_en__icontains=q)
        )

    sort_by = request.REQUEST.get('sort_by', 'date')
    if sort_by == 'title':
        owned_multipart_qs = owned_multipart_qs.order_by("production__title_de")
    elif sort_by == '-title':
        owned_multipart_qs = owned_multipart_qs.order_by("-production__title_de")
    elif sort_by == '-date':
        owned_multipart_qs = owned_multipart_qs.order_by("modified_or_creation_date")
    else:
        owned_multipart_qs = owned_multipart_qs.order_by("-modified_or_creation_date")

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
        'q': q,
        'status': status,
        'sort_by': sort_by,
    }
    return render(request, "site_specific/dashboard_multiparts.html", context)


@never_cache
@login_required
def dashboard_job_offers(request):
    owned_job_offer_qs = JobOffer.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(marketplace_joboffer.modified_date, marketplace_joboffer.creation_date)'
    })

    status = request.REQUEST.get('status', 'published')
    if status in ('published', 'draft', 'not_listed'):
        owned_job_offer_qs = owned_job_offer_qs.filter(status=status)

    q = request.REQUEST.get('q', '')
    if q:
        owned_job_offer_qs = owned_job_offer_qs.filter(
            models.Q(title_de__icontains=q) | models.Q(title_en__icontains=q) |
            models.Q(subtitle_de__icontains=q) | models.Q(subtitle_en__icontains=q)
        )

    sort_by = request.REQUEST.get('sort_by', 'date')
    if sort_by == 'title':
        owned_job_offer_qs = owned_job_offer_qs.order_by("title_de")
    elif sort_by == '-title':
        owned_job_offer_qs = owned_job_offer_qs.order_by("-title_de")
    elif sort_by == '-date':
        owned_job_offer_qs = owned_job_offer_qs.order_by("modified_or_creation_date")
    else:
        owned_job_offer_qs = owned_job_offer_qs.order_by("-modified_or_creation_date")

    paginator = Paginator(owned_job_offer_qs, 50)
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
        'q': q,
        'status': status,
        'sort_by': sort_by,
    }
    return render(request, "site_specific/dashboard_job_offers.html", context)


@never_cache
@login_required
def dashboard_educational_department(request):
    owned_department_qs = EducationalDepartment.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(education_department.modified_date, education_department.creation_date)'
    })

    status = request.REQUEST.get('status', 'published')
    if status in ('published', 'draft', 'not_listed'):
        owned_department_qs = owned_department_qs.filter(status=status)

    q = request.REQUEST.get('q', '')
    if q:
        owned_department_qs = owned_department_qs.filter(
            models.Q(title_de__icontains=q) | models.Q(title_en__icontains=q) |
            models.Q(subtitle_de__icontains=q) | models.Q(subtitle_en__icontains=q)
        )

    sort_by = request.REQUEST.get('sort_by', 'date')
    if sort_by == 'title':
        owned_department_qs = owned_department_qs.order_by("title_de")
    elif sort_by == '-title':
        owned_department_qs = owned_department_qs.order_by("-title_de")
    elif sort_by == '-date':
        owned_department_qs = owned_department_qs.order_by("modified_or_creation_date")
    else:
        owned_department_qs = owned_department_qs.order_by("-modified_or_creation_date")

    paginator = Paginator(owned_department_qs, 50)
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
        'q': q,
        'status': status,
        'sort_by': sort_by,
    }
    return render(request, "site_specific/dashboard_educational_department.html", context)


@never_cache
@login_required
def dashboard_educational_project(request):
    owned_project_qs = EducationalProjects.objects.accessible_to(request.user).extra(select={
        'modified_or_creation_date': 'IFNULL(education_project.modified_date, education_project.creation_date)'
    })

    status = request.REQUEST.get('status', 'published')
    if status in ('published', 'draft', 'not_listed'):
        owned_project_qs = owned_project_qs.filter(status=status)

    q = request.REQUEST.get('q', '')
    if q:
        owned_project_qs = owned_project_qs.filter(
            models.Q(title_de__icontains=q) | models.Q(title_en__icontains=q) |
            models.Q(subtitle_de__icontains=q) | models.Q(subtitle_en__icontains=q)
        )

    sort_by = request.REQUEST.get('sort_by', 'date')
    if sort_by == 'title':
        owned_project_qs = owned_project_qs.order_by("title_de")
    elif sort_by == '-title':
        owned_project_qs = owned_project_qs.order_by("-title_de")
    elif sort_by == '-date':
        owned_project_qs = owned_project_qs.order_by("modified_or_creation_date")
    else:
        owned_project_qs = owned_project_qs.order_by("-modified_or_creation_date")

    paginator = Paginator(owned_project_qs, 50)
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
        'q': q,
        'status': status,
        'sort_by': sort_by,
    }
    return render(request, "site_specific/dashboard_educational_project.html", context)


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
                for p in location.located_productions.all():
                    p.set_owner(u)
                for event in location.event_set.all():
                    event.production.set_owner(u)

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
                for p in location.located_productions.all():
                    p.set_owner(u)
                for event in location.event_set.all():
                    event.production.set_owner(u)
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
                for p in location.located_productions.all():
                    p.set_owner(u)
                for event in location.event_set.all():
                    event.production.set_owner(u)
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


class ASCIIFileSystemStorageBackend(DefaultStorageUploadBackend):
    def update_filename(self, request, filename, *args, **kwargs):
        from django.core.files.storage import default_storage
        return default_storage.get_valid_name(filename)


uploader = AjaxFileUploader(backend=ASCIIFileSystemStorageBackend)


def culturebase_export_productions(request, location_slug):
    from lxml.etree import tostring
    from lxml.builder import E
    from lxml.etree import CDATA
    from base_libs.utils.misc import get_website_url
    from jetson.apps.image_mods.models import FileManager
    from filebrowser.models import FileDescription
    location = get_object_or_404(Location, slug=location_slug)

    CATEGORY_MAPPER = {
        7002: 74,  # Ausstellung
        6999: 25,  # Ballett
        6995: 35,  # Blues
        6988: 36,  # Chanson
        7009: 56,  # Comedy
        6994: 37,  # Country
        7003: 68,  # Diskussion
        7001: 38,  # Elektro
        7010: 76,  # Film
        6993: 39,  # Folk
        6986: 77,  # Fotografie
        6992: 40,  # Funk
        6987: 78,  # Fuhrung
        6991: 41,  # HipHop
        6990: 42,  # Jazz
        7008: 57,  # Kabarett
        7022: 8,  # Kinder/Jugend
        7013: 43,  # Klassik
        #7017: 14,  # Komödie
        7019: 69,  # Konferenz
        6998: 17,  # Konzertante Vorstellung
        7020: 15,  # Lesung
        7000: 14,  # Liederabend
        7014: 18,  # Musical
        7018: 79,  # Neue Medien
        6996: 45,  # Neue Musik
        7024: 20,  # Oper
        7015: 22,  # Operette
        7012: 80,  # Party
        7016: 32,  # Performance
        7006: 46,  # Pop
        7007: 66,  # Puppentheater
        7026: 52,  # Revue
        7005: 47,  # Rock
        7028: 16,  # Schauspiel
        7025: 53,  # Show
        7023: 5,  # Sonstige Musik
        6989: 48,  # Soul
        7011: 49,  # Special
        6997: 27,  # Tanztheater
        7027: 54,  # Variete
        7021: 70,  # Vortrag
        7004: 82,  # Workshop
    }
    REVERSE_CATEGORY_MAPPER = dict(zip(CATEGORY_MAPPER.values(), CATEGORY_MAPPER.keys()))

    production_nodes = []
    for prod in Production.objects.filter(
        models.Q(in_program_of=location) |
        models.Q(play_locations=location),
        status="published",
    ).distinct():

        prod_image_nodes = []
        for image in prod.productionimage_set.all():
            try:
                file_description = FileDescription.objects.filter(
                    file_path=image.path.path,
                ).order_by("pk")[0]
            except:
                 author = ""
                 image_title_de = ""
                 image_title_en = ""
                 copyright = ""
            else:
                 author = file_description.author
                 image_title_de = file_description.title_de
                 image_title_en = file_description.title_en
                 copyright = file_description.copyright_limitations

            list_image_url = ""
            list_image_path = FileManager.modified_path(image.path.path, "list_image")
            if list_image_path:
                list_image_url = "".join((
                    get_website_url(),
                    settings.MEDIA_URL[1:],
                    list_image_path,
                ))

                prod_image_nodes.append(
                    E.erBild(
                        E.bildUrl(list_image_url),
                        E.bildUrheber(CDATA(author)),
                        E.bildCopyright(CDATA(copyright)),
                        E.bildUntertitel(CDATA(image_title_de)),
                        E.bildUntertitelEn(CDATA(image_title_en)),
                    )
                )

        event_nodes = []
        for event in prod.event_set.all():
            persons = '\n'.join([
                u'%s - %s' % (involvement.person, involvement.get_function()) for involvement in event.eventinvolvement_set.all()
            ])
            if event.price_from:
                price_range = "%s - %s" % (event.price_from, event.price_till)
            else:
                price_range = ""
            event_nodes.append(E.event(
                E.eventId(str(event.pk)),
                E.eventBezeichnung(CDATA(""), alwaysEmpty="1"),
                E.erWerbezeile(CDATA(event.get_rendered_teaser_de())),
                E.erWerbezeileEn(CDATA(event.get_rendered_teaser_en())),
                E.eventPersonen(CDATA(persons)),
                E.eventOrtId("", alwaysEmpty="1"),
                E.eventOrt(CDATA(event.city)),
                E.eventDatum(event.start_date.strftime('%d.%m.%Y')),
                E.eventZeit(event.start_time.strftime('%H:%M')),
                E.eventLink(CDATA(event.get_url())),
                E.eventStrasse(CDATA(event.street_address)),
                E.eventPlz(str(event.postal_code)),
                E.eventVenue(CDATA(event.location_title)),
                E.platzkategorie(
                    E.vkpreis(price_range)
                ),
                E.eventMerkmal(CDATA(', '.join(event.characteristics.values_list("title_de", flat=True)))),
                E.eventMerkmalEn(CDATA(', '.join(event.characteristics.values_list("title_en", flat=True)))),
                E.eventTicketsWebseite(CDATA(event.tickets_website)),
                E.erUntertitel(CDATA(event.subtitles_text_de)),
                E.erUntertitelEn(CDATA(event.subtitles_text_en)),
            ))
        try:
            first_date = prod.event_set.order_by("start_date")[0].start_date.strftime('%Y-%m-%d')
        except:
            first_date = ""
        try:
            last_date = prod.event_set.order_by("-start_date")[0].start_date.strftime('%Y-%m-%d')
        except:
            last_date = ""
        persons = '\n'.join([
            u'%s - %s' % (involvement.person, involvement.get_function()) for involvement in prod.productioninvolvement_set.all()
        ])
        categories = ','.join([
            str(REVERSE_CATEGORY_MAPPER[cat.pk]) for cat in prod.categories.all() if REVERSE_CATEGORY_MAPPER.get(cat.pk, False)
        ])
        language_and_subtitles_de = u""
        language_and_subtitles_en = u""
        if prod.language_and_subtitles:
            language_and_subtitles_de = prod.language_and_subtitles.title_de
            language_and_subtitles_en = prod.language_and_subtitles.title_en

        production_nodes.append(E.eventReihe(
            E.erId(str(prod.pk)),
            E.erName(CDATA(prod.title_de)),
            E.erNameEn(CDATA(prod.title_en)),
            E.erLink(CDATA(prod.get_url())),
            E.erBeschreibung(CDATA(prod.get_rendered_description_de())),
            E.erBeschreibungEn(CDATA(prod.get_rendered_description_en())),
            E.erInhalt(CDATA(prod.get_rendered_contents_de())),
            E.erInhaltEn(CDATA(prod.get_rendered_contents_en())),
            E.erWerbezeile(CDATA(prod.get_rendered_teaser_de())),
            E.erWerbezeileEn(CDATA(prod.get_rendered_teaser_en())),
            E.erPersons(CDATA(persons)),
            E.erKoproduktion(CDATA(""), alwaysEmpty="1"),
            E.erKritik(CDATA(""), alwaysEmpty="1"),
            E.erSondermerkmal(CDATA(prod.get_rendered_remarks_de())),
            E.erSondermerkmalEn(CDATA(prod.get_rendered_remarks_en())),
            E.erWerkinfo(CDATA(prod.get_rendered_work_info_de())),
            E.erWerkinfoEn(CDATA(prod.get_rendered_work_info_en())),
            E.erAltersangabe(CDATA(prod.age_text)),
            E.erLocation(CDATA(location.title)),
            E.erStrasse(CDATA(location.street_address)),
            E.erPlz(CDATA(location.postal_code)),
            E.erStadt(CDATA(location.city)),
            E.erBegin(first_date),
            E.erEnde(last_date),
            E.erSpieldauer(CDATA(prod.duration_text_de)),
            E.erSpieldauerEn(CDATA(prod.duration_text_en)),
            E.erSchlagworte(CDATA(""), alwaysEmpty="1"),
            E.erKategorie(CDATA(categories)),
            E.erTicketsWebseite(CDATA(prod.tickets_website)),
            E.erMerkmal(CDATA(', '.join(prod.characteristics.values_list("title_de", flat=True)))),
            E.erMerkmalEn(CDATA(', '.join(prod.characteristics.values_list("title_en", flat=True)))),
            E.erUntertitel(CDATA(prod.subtitles_text_de)),
            E.erUntertitelEn(CDATA(prod.subtitles_text_en)),
            E.erSpracheUndUntertitel(CDATA(language_and_subtitles_de)),
            E.erSpracheUndUntertitelEn(CDATA(language_and_subtitles_en)),
            *prod_image_nodes + event_nodes
        ))

    return HttpResponse(
        tostring(
            E.detaildEventList(
                xmlns="",
                *production_nodes
            ),
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        ).replace(  # a hack to add the namespace attributes without modifying the tags of the XML
            'xmlns=""',
            'xmlns="http://export.culturebase.org/schema/event/standardExport" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="http://export.culturebase.org/schema/event/standardExport http://export.culturebase.org/schema/event/standardExport.xsd"'
        ),
        content_type="text/xml"
    )

API_CHANGELOG = [
    {
        'date': datetime(2017, 2, 21, 12, 0),
        'changes': [
            u"The website now uses HTTPS protocol.",
        ],
    },
    {
        'date': datetime(2016, 12, 20, 12, 0),
        'changes': [
            u"The <strong>classiccard</strong> fields added to productions and events.",
        ],
    },
    {
        'date': datetime(2016, 12, 13, 12, 0),
        'changes': [
            u"The <strong>author</strong>, <strong>photographer</strong>, and <strong>copyright</strong> fields return the author/copyright text. If the value is empty, \"Promo\" is set at the <strong>copyright</strong> field.",
        ],
    },
    {
        'date': datetime(2016, 11, 29, 12, 0),
        'changes': [
            u"For unpublished productions only ID, status, and creation and modification dates are shown.",
        ],
    },
    {
        'date': datetime(2016, 8, 1, 12, 0),
        'changes': [
            u"Documentation introduction added.",
            u"Documentation updated regarding determining play location(s) of an event.",
        ],
    },
    {
        'date': datetime(2016, 1, 20, 12, 0),
        'changes': [
            u"Field <strong>language_and_subtitles</strong> added to events.",
        ],
    },
    {
        'date': datetime(2015, 11, 4, 12, 0),
        'changes': [
            u"The <strong>copyright</strong> field contains \"Promo\" if an image or PDF document has no copyright information.",
        ],
    },
    {
        'date': datetime(2015, 11, 3, 12, 0),
        'changes': [
            u"Festival export",
        ],
    },
    {
        'date': datetime(2015, 10, 12, 12, 0),
        'changes': [
            u"Field <strong>copyright</strong> added to production and event images.",
            u"Field <strong>photographer</strong> added to production and event images.",
            u"Field <strong>copyright</strong> added to production and event pdfs.",
        ],
    },
    {
        'date': datetime(2015, 8, 11, 12, 0),
        'changes': [
            u"Custom location added to production with fields: <strong>location_title</strong>, <strong>street_address</strong>, <strong>street_address2</strong>, <strong>postal_code</strong>, <strong>city</strong>, <strong>country</strong>, <strong>latitude</strong>, <strong>longitude</strong>.",
        ],
    },
    {
        'date': datetime(2015, 7, 9, 12, 0),
        'changes': [
            u"Field <strong>event_status</strong> added to events.",
            u"Field <strong>ticket_status</strong> added to events.",
            u"Field <strong>list_image_url</strong> added to production and event images.",
        ],
    },
    {
        'date': datetime(2015, 6, 16, 12, 0),
        'changes': [
            u"Filtering productions by <strong>in_program_of</strong>.",
            u"Filtering productions by <strong>play_locations</strong>.",
            u"Filtering productions by <strong>status</strong>.",
            u"Filtering productions by <strong>categories</strong>.",
            u"Filtering productions by <strong>creation_date</strong>.",
            u"Filtering productions by <strong>modified_date</strong>.",
        ],
    },
    {
        'date': datetime(2015, 4, 2, 12, 0),
        'changes': [
            u"Field <strong>concert_programm_de</strong> changed to <strong>concert_program_de</strong>.",
            u"Field <strong>concert_programm_en</strong> changed to <strong>concert_program_en</strong>.",
            u"Field <strong>supporting_programm_de</strong> changed to <strong>supporting_program_de</strong>.",
            u"Field <strong>supporting_programm_en</strong> changed to <strong>supporting_program_en</strong>.",
        ],
    },
    {
        'date': datetime(2015, 4, 2, 12, 0),
        'changes': [u"Field <strong>sort_order</strong> added to media files."],
    },
    {
        'date': datetime(2015, 3, 23, 12, 0),
        'changes': [u"Field <strong>organizer_title</strong> changed to <strong>organizers</strong> at events."],
    },
    {
        'date': datetime(2015, 3, 12, 12, 0),
        'changes': [u"Location, production, and event export."],
    },
]

def api_changelog(request):
    return render(request, "site_specific/api_changelog.html", {'api_changelog': API_CHANGELOG})

class APIChangeLogFeed(Feed):
    title = "Export API Change Log"

    def link(self):
        return reverse("api_changelog")

    def items(self):
        return API_CHANGELOG

    def item_title(self, item):
        return u"API Changes on %s" % item['date'].strftime('%Y-%m-%d')

    def item_description(self, item):
        return '<ul><li>%s</li></ul>' % '</li><li>'.join(item['changes'])

    def item_pubdate(self, item):
        return item['date']

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse("api_changelog") + '#d' + item['date'].strftime('%Y-%m-%d')
