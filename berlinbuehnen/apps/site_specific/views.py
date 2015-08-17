# -*- coding: UTF-8 -*-

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
Parent = models.get_model("multiparts", "Parent")

# from forms import ExhibitionFilterForm, EventFilterForm, WorkshopFilterForm, ShopFilterForm

@never_cache
@login_required
def dashboard(request):
    owned_locations = Location.objects.accessible_to(request.user).order_by("-modified_date", "-creation_date")[:3]
    owned_productions = Production.objects.accessible_to(request.user).filter(status__in=('published', 'draft', 'expired', 'not_listed', 'import')).order_by("-modified_date", "-creation_date")[:3]
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
    owned_location_qs = Location.objects.accessible_to(request.user)

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
        owned_location_qs = owned_location_qs.order_by("modified_date", "creation_date")
    else:
        owned_location_qs = owned_location_qs.order_by("-modified_date", "-creation_date")

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
    return render(request, "accounts/dashboard_locations.html", context)


@never_cache
@login_required
def dashboard_productions(request):
    owned_production_qs = Production.objects.accessible_to(request.user)

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
        owned_production_qs = owned_production_qs.order_by("modified_date", "creation_date")
    else:
        owned_production_qs = owned_production_qs.order_by("-modified_date", "-creation_date")

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
    return render(request, "accounts/dashboard_productions.html", context)


@never_cache
@login_required
def dashboard_multiparts(request):
    owned_multipart_qs = Parent.objects.accessible_to(request.user)

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
        owned_multipart_qs = owned_multipart_qs.order_by("modified_date", "creation_date")
    else:
        owned_multipart_qs = owned_multipart_qs.order_by("-modified_date", "-creation_date")

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
        models.Q(play_locations=location)
    ).distinct():

        prod_image_nodes = []
        for image in prod.productionimage_set.all():
            try:
                file_description = FileDescription.objects.filter(
                    file_path=mf.path,
                ).order_by("pk")[0]
            except:
                 author = ""
                 image_title = ""
                 copyright = ""
            else:
                 author = file_description.author
                 image_title = file_description.title
                 copyright = file_description.copyright_limitations

            prod_image_nodes.append(
                E.erBild(
                    E.bildUrl(get_website_url()[:-1] + settings.MEDIA_URL + FileManager.modified_path(image.path.path, "list_image_url")),
                    E.bildUrheber(CDATA(author)),
                    E.bildCopyright(CDATA(copyright)),
                    E.bildUntertitel(CDATA(image_title)),
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
                E.erWerbezeile(CDATA(event.get_rendered_teaser())),
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
            ))

        first_date = prod.event_set.order_by("start_date")[0].start_date.strftime('%Y-%m-%d')
        last_date = prod.event_set.order_by("-start_date")[0].start_date.strftime('%Y-%m-%d')
        persons = '\n'.join([
            u'%s - %s' % (involvement.person, involvement.get_function()) for involvement in prod.productioninvolvement_set.all()
        ])
        categories = ','.join([
            str(REVERSE_CATEGORY_MAPPER[cat.pk]) for cat in prod.categories.all() if REVERSE_CATEGORY_MAPPER.get(cat.pk, False)
        ])
        production_nodes.append(E.eventReihe(
            E.erId(str(prod.pk)),
            E.erName(CDATA(prod.title)),
            E.erLink(CDATA(prod.get_url())),
            E.erBeschreibung(CDATA(prod.get_rendered_description())),
            E.erInhalt(CDATA(prod.get_rendered_contents())),
            E.erWerbezeile(CDATA(prod.get_rendered_teaser())),
            E.erPersons(CDATA(persons)),
            E.erKoproduktion(CDATA(""), alwaysEmpty="1"),
            E.erKritik(CDATA(""), alwaysEmpty="1"),
            E.erSondermerkmal(CDATA(prod.get_rendered_remarks())),
            E.erWerkinfo(CDATA(prod.get_rendered_work_info())),
            E.erAltersangabe(CDATA(prod.age_text)),
            E.erLocation(CDATA(location.title)),
            E.erStrasse(CDATA(location.street_address)),
            E.erPlz(CDATA(location.postal_code)),
            E.erStadt(CDATA(location.city)),
            E.erBegin(first_date),
            E.erEnde(last_date),
            E.erSpieldauer(CDATA(prod.duration_text)),
            E.erSchlagworte(CDATA(""), alwaysEmpty="1"),
            E.erKategorie(CDATA(categories)),
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