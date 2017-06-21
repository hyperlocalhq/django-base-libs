# -*- coding: utf-8 -*-

import os
import urllib2
from datetime import datetime

import facebook
from dateutil.parser import parse as parse_datetime
from django.contrib.auth.views import logout as django_logout
from django.shortcuts import render_to_response
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import models
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from base_libs.utils.misc import get_installed
from base_libs.utils.misc import get_unique_value
from base_libs.utils.betterslugify import better_slugify
from base_libs.views import access_denied
from kb.apps.accounts.views import login as jetson_login

Site = models.get_model("sites", "Site")
SiteSettings = models.get_model("configuration", "SiteSettings")
User = models.get_model("auth", "User")
FacebookAppSettings = models.get_model("facebook_app", "FacebookAppSettings")
FacebookPage = models.get_model("facebook_app", "FacebookPage")
SimpleRegistrationForm = get_installed("people.forms.SimpleRegistrationForm")
image_mods = models.get_app("image_mods")
Institution = models.get_model("institutions", "Institution")

facebook_app_models = models.get_app("facebook_app")


def get_user_from_session(request):
    return request.session.get("facebook_user", {})


@never_cache
def logout(request, *args, **kwargs):
    """
    logs the current user out 
    """
    response = django_logout(request, *args, **kwargs)
    response.delete_cookie('fbs_%s' % settings.FACEBOOK_APP_ID)
    # TODO: does it make sense to do this ^?
    return response


@never_cache
def login_and_link(request):
    """
    logs in existing account by facebook account or gives a choice to
    * login and link to an existing account
    * register and link to the new account
    """
    redirect_to = request.REQUEST.get("goto_next", reverse("my_profile"))

    if request.POST:
        request.session['facebook_user'] = {
            'uid': request.POST['uid'],
            'access_token': request.POST['access_token'],
        }

    facebook_user = get_user_from_session(request)

    # if noone connected with facebook user 
    if not facebook_user:
        return HttpResponseRedirect(reverse("login"))

    # If the user already bounded, log him/her in
    try:
        fas = FacebookAppSettings.objects.get(fb_id=facebook_user['uid'])
    except FacebookAppSettings.DoesNotExist:
        pass
    else:
        # fas.user has no attribute "backend" required for login, so get it.
        user = fas.user
        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth_login(request, user)
        return HttpResponseRedirect(redirect_to)

    template_name = "facebook_app/new_facebook_user.html"
    return render_to_response(template_name, {
        'goto_next': redirect_to,
    }, context_instance=RequestContext(request))


@never_cache
def login(request):
    """
    logs the user in and links him with facebook account
    """
    redirect_to = request.REQUEST.get("goto_next", reverse("my_profile"))
    template_name = "facebook_app/login.html"

    facebook_user = get_user_from_session(request)

    # if noone connected with facebook user 
    if not facebook_user:
        return HttpResponseRedirect(reverse("login"))

    response = jetson_login(
        request,
        template_name=template_name,
    )

    # if there are any validation errors, return the form
    if response.status_code != 302:
        return response

    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))

    if facebook_user:
        graph = facebook.GraphAPI(facebook_user["access_token"])
        profile = graph.get_object("me")

        fas = FacebookAppSettings.objects.create(
            user=user,
            fb_id=facebook_user['uid'],
            name=profile['name'],
            profile_url=profile['link'],
            access_token=facebook_user["access_token"],
        )

    return HttpResponseRedirect(redirect_to)


@never_cache
def register(request):
    """
    registers the new user in and links him with facebook account
    """
    redirect_to = request.REQUEST.get("goto_next", "/register/alldone/")

    facebook_user = get_user_from_session(request)

    # if noone connected with facebook user 
    if not facebook_user:
        return HttpResponseRedirect(reverse("login"))

    site_settings = SiteSettings.objects.get_current()

    if request.method == "POST":
        form = SimpleRegistrationForm(request, request.POST, request.FILES)
        if form.is_valid():
            # create User and Person instances
            user = form.save(activate_immediately=True)

            graph = facebook.GraphAPI(facebook_user["access_token"])
            profile = graph.get_object("me")
            # create FacebookAppSettings
            fas = FacebookAppSettings.objects.create(
                user=user,
                fb_id=facebook_user['uid'],
                name=profile['name'],
                profile_url=profile['link'],
                access_token=facebook_user["access_token"],
            )
            # login the user
            user.backend = "django.contrib.auth.backends.ModelBackend"
            auth_login(request, user)

            return HttpResponseRedirect(redirect_to)
    else:
        # show registration form with credentials prefilled from facebook account
        graph = facebook.GraphAPI(facebook_user["access_token"])
        profile = graph.get_object("me")

        initial = {
            'email': profile['email'],
            'username': get_unique_value(
                User,
                better_slugify(profile['name']).replace("-", "_"),
                field_name="username",
                separator="_",
            ),
            'first_name': profile['first_name'],
            'last_name': profile['last_name'],
        }

        form = SimpleRegistrationForm(request, initial=initial)

    template_name = "facebook_app/register.html"

    return render_to_response(template_name, {
        'form': form,
        'site_name': Site.objects.get_current().name,
        'login_by_email': site_settings.login_by_email,
        'goto_next': redirect_to,
    }, context_instance=RequestContext(request))


@never_cache
@login_required
def manage_facebook_connections(request):
    """
    connects or disconnects facebook accounts to current user's account
    """
    if request.method == "POST":
        action = request.POST.get("a", "")
        if action == "connect":
            request.session['facebook_user'] = {
                'uid': request.POST['uid'],
                'access_token': request.POST['access_token'],
            }

            facebook_user = get_user_from_session(request)

            if facebook_user:
                graph = facebook.GraphAPI(facebook_user["access_token"])
                profile = graph.get_object("me")

                fas = FacebookAppSettings.objects.create(
                    user=request.user,
                    fb_id=facebook_user['uid'],
                    name=profile['name'],
                    profile_url=profile['link'],
                    access_token=facebook_user["access_token"],
                )
        if action == "disconnect":
            FacebookAppSettings.objects.filter(
                user=request.user,
                fb_id=request.POST.get("uid", None),
            ).delete()

    fass = FacebookAppSettings.objects.filter(user=request.user)

    template_name = "facebook_app/manage_connections.html"

    return render_to_response(template_name, {
        'fass': fass,
    }, context_instance=RequestContext(request))


@never_cache
@login_required
def manage_facebook_pages(request):
    """
    connects or disconnects facebook accounts to current user's account
    """
    fb_pages = []
    unlinked_pages = []
    unlinked_institutions = []

    linked_inst_pks = []
    linked_page_ids = []

    for fb_page in FacebookPage.objects.filter(owner_settings__user=request.user):
        fb_pages.append(fb_page)
        linked_inst_pks.append(fb_page.institution.pk)
        linked_page_ids.append(fb_page.fb_id)

    fass = FacebookAppSettings.objects.filter(user=request.user)
    if not fass:
        return HttpResponseRedirect("/facebook/manage/")

    facebook_user = get_user_from_session(request)
    if facebook_user:
        graph = facebook.GraphAPI(facebook_user["access_token"])
        pages = graph.get_connections("me", "accounts").get("data", [])
        for page in pages:
            if int(page['id']) not in linked_page_ids:
                page_details = graph.get_object(page['id'])
                page_details['access_token'] = page['access_token']
                unlinked_pages.append(page_details)

    unlinked_institutions = request.user.profile.get_institutions().exclude(
        pk__in=linked_inst_pks,
    )

    if request.is_ajax():
        if request.method == "POST":
            action = request.POST.get("a", "")
            institution = Institution.objects.get(
                pk=request.POST.get("institution", ""),
            )
            if action == "connect":
                fb_page_id = request.POST.get("page", "")

                facebook_user = get_user_from_session(request)

                for unlinked_page in unlinked_pages:
                    if unlinked_page['id'] == fb_page_id:
                        fb_page = FacebookPage.objects.create(
                            owner_settings=FacebookAppSettings.objects.filter(user=request.user)[0],
                            institution=institution,
                            fb_id=unlinked_page['id'],
                            name=unlinked_page['name'],
                            profile_url=unlinked_page['link'],
                            access_token=unlinked_page['access_token'],
                        )
                        break
            if action == "disconnect":
                FacebookPage.objects.filter(
                    institution=institution,
                ).delete()
            return HttpResponseRedirect(request.path)

    template_name = "facebook_app/manage_pages.html"

    base_template = "base.html"
    if request.is_ajax():
        base_template = "base_ajax.html"

    return render_to_response(template_name, {
        'fb_pages': fb_pages,
        'unlinked_pages': unlinked_pages,
        'unlinked_institutions': unlinked_institutions,
        'base_template': base_template,
    }, context_instance=RequestContext(request))


@never_cache
@login_required
def data_exchange(request):
    """
    gets data from facebook and sends data to facebook
    """
    import os

    facebook_user_datas = []

    facebook_user = get_user_from_session(request)
    if facebook_user:
        graph = facebook.GraphAPI(facebook_user["access_token"])
        profile = graph.get_object("me")
        profile['feed'] = graph.get_connections("me", "feed")
        profile['likes'] = graph.get_connections("me", "likes")
        profile['statuses'] = graph.get_connections("me", "statuses")
        profile['checkins'] = graph.get_connections("me", "checkins")
        profile['movies'] = graph.get_connections("me", "movies")
        profile['television'] = graph.get_connections("me", "television")
        profile['accounts'] = graph.get_connections("me", "accounts")

        fql_api = facebook.FQLAPI(facebook_user["access_token"])

        result = fql_api.query("SELECT user_photos FROM permissions WHERE uid = me()")
        facebook_user_datas.append(result)

        # result = fql_api.query("SELECT uid, name, pic_square FROM user WHERE uid = me() OR uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")
        # facebook_user_datas.append(result)

        result = fql_api.query("SELECT src_big FROM photo WHERE owner=me()")
        facebook_user_datas.append(result)

        if request.method == "POST":
            from datetime import datetime

            '''
            graph.put_object(
                "me",
                "feed",
                message="Today is %s. <b>What a wonderful day!</b>" % datetime.now()
                )
            '''

            '''
            graph.put_wall_post(
                "Wall post test",
                attachment= {
                    "name": "Google",
                    "link": "http://www.google.com/",
                    "caption": "{*actor*} posted a new review",
                    "description": "This is a longer description of the attachment",
                    "picture": "http://www.google.de/intl/en_com/images/srpr/logo1w.png",
                    },
                # profile_id="581252806", # to whom; if a friend
                )
            '''

            for account in profile['accounts']['data']:
                if account['id'] == "108037845932470":
                    graph = facebook.GraphAPI(account['access_token'])
                    break

            """ Create album and upload two big photos """
            # '''
            result = graph.put_object(
                "108037845932470",
                "albums",
                name="Creative-City-Berlin Portfolio 2 for a Page",
                description="I feel good!",
            )

            from poster.encode import multipart_encode
            from poster.streaminghttp import register_openers
            import urllib2

            register_openers()
            datagen, headers = multipart_encode({
                "access_token": facebook_user["access_token"],
                "message": "Be Berlin!",
                "source": open(os.path.join(settings.UPLOADS_ROOT, "beberlin.jpg")),
            })
            request = urllib2.Request(
                "https://graph.facebook.com/me/photos",
                datagen,
                headers,
            )
            response = urllib2.urlopen(request).read()
            '''
            file_data = ""
            f = open(os.path.join(settings.UPLOADS_ROOT, "beberlin.jpg"))
            try:
                file_data = f.read()
            finally:
                f.close()
            result = graph.multipart_request(
                #"/%s/photos" % result['id'],
                "/me/photos",
                post_args={
                    'message': "Be Berlin"
                    },
                files={
                    'source': file_data
                    })
            '''

            # '''

            '''
                       
            file_data = ""
            f = open(os.path.join(settings.UPLOADS_ROOT, "5000x3000.jpg"))
            try:
                file_data = f.read()
            finally:
                f.close()
            graph.multipart_request(
                "/%s/photos" % result['id'],
                post_args={
                    'message': "5000 x 3000"
                    },
                files={
                    'source': file_data
                    })
            file_data = ""
            f = open(os.path.join(settings.UPLOADS_ROOT, "3000x5000.jpg"))
            try:
                file_data = f.read()
            finally:
                f.close()
            graph.multipart_request(
                "/%s/photos" % result['id'],
                post_args={
                    'message': "3000 x 5000"
                    },
                files={
                    'source': file_data
                    })
            
            '''
            '''
            event_start = (datetime.now() + timedelta(hours=16)).strftime("%Y-%m-%dT%H:%M:%SZ")
            event_end = (datetime.now() + timedelta(hours=16, minutes=60)).strftime("%Y-%m-%dT%H:%M:%SZ")
            
            graph.put_event(
                name="The present of my existence",
                location="test",
                street="Rosenthaler Str 38",
                city="Berlin",
                zip="10178",
                country="Germany",
                latitude="52.524466",
                longitude="13.402065",
                start_time=event_start,
                end_time=event_end,
                picture="http://www.bestmarketingspain.com/picts/laser-event.jpg",
                privacy="OPEN",
                description="Hello World!",
                )
            '''

        facebook_user_datas.append(profile)

    template_name = "facebook_app/data_exchange.html"

    return render_to_response(template_name, {
        'facebook_user_datas': facebook_user_datas,
    }, context_instance=RequestContext(request))


def upload_image(access_token, fb_album_id, image_path, message):
    """
    Upload an image without loading it all to the memory
    """
    import json
    import urllib2
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers

    register_openers()
    datagen, headers = multipart_encode({
        "access_token": access_token,
        "message": message,
        "source": open(image_path),
    })
    request = urllib2.Request(
        "https://graph.facebook.com/%s/photos" % fb_album_id,
        datagen,
        headers,
    )
    response = urllib2.urlopen(request).read()
    return json.loads(response)


def sync_personal_portfolio(request, slug):
    """
    A view for listing albums and displaying what is synced with facebook and what is not
    """
    Person = models.get_model("people", "Person")
    MediaGallery = models.get_model("media_gallery", "MediaGallery")
    MediaFile = models.get_model("media_gallery", "MediaFile")
    URL_ID_PORTFOLIO = models.get_app("media_gallery").URL_ID_PORTFOLIO
    TOKENIZATION_SUMMAND = models.get_app("media_gallery").TOKENIZATION_SUMMAND
    ObjectMapper = models.get_model("external_services", "ObjectMapper")
    Service = models.get_model("external_services", "Service")

    facebook_user = get_user_from_session(request)
    if facebook_user:
        graph = facebook.GraphAPI(facebook_user["access_token"])
    else:
        return HttpResponseRedirect("/facebook/manage/")

    obj = Person.objects.get(user__username=slug)
    can_manage_portfolio = request.user.has_perm("people.change_person", obj) and facebook_user
    if not can_manage_portfolio:
        return access_denied(request)

    s, created = Service.objects.get_or_create(
        sysname="facebook",
        defaults={
            'url': "https://graph.facebook.com/",
            'title': "Facebook",
        },
    )

    if request.method == "POST" and request.is_ajax():
        action = request.POST.get("action", "")
        kb_gallery_token = request.POST.get("kb_gallery_token", "")
        fb_album_id = request.POST.get("fb_album_id", "")
        mapper = None
        gallery = None

        if action in ["kb-to-fb", "sync"]:
            gallery = MediaGallery.objects.get(
                pk=int(kb_gallery_token) - TOKENIZATION_SUMMAND,
            )
            try:
                mapper = s.objectmapper_set.get(
                    content_type__app_label="media_gallery",
                    content_type__model="mediagallery",
                    object_id=gallery.pk,
                )
            except Exception:
                mapper = None
            fb_album = None
            if mapper:
                fb_album = graph.get_object(mapper.external_id)
            if not fb_album:
                fb_album = graph.put_object(
                    "me",
                    "albums",
                    name=gallery.title,
                    description=gallery.description,
                )
                if mapper:
                    mapper.external_id = fb_album['id']
                else:
                    mapper = ObjectMapper(
                        service=s,
                        external_id="%s" % fb_album['id'],
                    )
                    mapper.content_object = gallery
                mapper.save()
                fb_album = graph.get_object(mapper.external_id)

            for media_file in gallery.mediafile_set.filter(
                file_type="i",
            ):
                if media_file.path:
                    try:
                        file_mapper = s.objectmapper_set.get(
                            content_type__app_label="media_gallery",
                            content_type__model="mediafile",
                            object_id=media_file.pk
                        )
                    except Exception:
                        file_mapper = None

                    fb_photo = None
                    if file_mapper:
                        fb_photo = graph.get_object(file_mapper.external_id)
                    if not file_mapper or not fb_photo:
                        fb_photo = upload_image(
                            facebook_user["access_token"],
                            fb_album['id'],
                            os.path.join(settings.UPLOADS_ROOT, media_file.path.path),
                            "%s. %s" % (media_file.title, media_file.description)
                        )
                        if file_mapper:
                            file_mapper.external_id = fb_photo['id']
                        else:
                            file_mapper = ObjectMapper(
                                service=s,
                                external_id="%s" % fb_photo['id'],
                            )
                            file_mapper.content_object = media_file
                        file_mapper.save()

        if action in ["fb-to-kb", "sync"]:
            fb_album = graph.get_object(fb_album_id)
            try:
                mapper = s.objectmapper_set.get(
                    content_type__app_label="media_gallery",
                    content_type__model="mediagallery",
                    external_id=fb_album_id
                )
            except Exception:
                mapper = None
            if mapper:
                gallery = mapper.content_object
            else:
                gallery = MediaGallery(
                    title_en=fb_album.get('name', ''),
                    title_de=fb_album.get('name', ''),
                    description_en=fb_album.get("description", ""),
                    description_de=fb_album.get("description", ""),
                )
                gallery.content_object = obj
                gallery.save()
                mapper = ObjectMapper(
                    service=s,
                    external_id="%s" % fb_album['id'],
                )
                mapper.content_object = gallery
                mapper.save()

            position = 0
            for fb_photo in graph.get_connections(fb_album_id, "photos")['data']:
                try:
                    file_mapper = s.objectmapper_set.get(
                        content_type__app_label="media_gallery",
                        content_type__model="mediafile",
                        external_id="%s" % fb_photo['id']
                    )
                except Exception:
                    file_mapper = None

                if file_mapper and file_mapper.content_object:
                    media_file = file_mapper.content_object
                    media_file.title_en = fb_photo.get('name', '')
                    media_file.title_de = fb_photo.get('name', '')
                    media_file.sort_order = position
                    media_file.save()
                else:
                    media_file = MediaFile(
                        gallery=gallery,
                        title_en=fb_photo.get('name', ''),
                        title_de=fb_photo.get('name', ''),
                        sort_order=position,
                    )
                    image_url = fb_photo['source']
                    rel_dir = getattr(obj, "get_filebrowser_dir", lambda: "")()
                    rel_dir += URL_ID_PORTFOLIO + "/"
                    fname, fext = os.path.splitext(image_url)
                    filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                    path = "".join((rel_dir, filename))
                    image_data = urllib2.urlopen(image_url)
                    image_mods.FileManager.save_file(
                        path=path,
                        content=image_data.read(),
                    )
                    media_file.path = path
                    media_file.save()
                    if not file_mapper:
                        file_mapper = ObjectMapper(
                            service=s,
                            external_id="%s" % fb_photo['id'],
                        )
                    file_mapper.content_object = media_file
                    file_mapper.save()
                position += 1
            gallery.save()  # updating modification date

        fb_album = graph.get_object(mapper.external_id)  # update file count
        if "created_time" in fb_album:
            fb_album['created_time'] = parse_datetime(fb_album['created_time'])
        if "updated_time" in fb_album:
            fb_album['updated_time'] = parse_datetime(fb_album['updated_time'])

        context_dict = {
            'object': obj,
            'can_manage_portfolio': can_manage_portfolio,
            'fb_access_token': facebook_user["access_token"],
            'gallery_opts': {
                'kb_gallery': gallery,
                'kb_gallery_count': gallery.mediafile_set.filter(file_type="i").count(),
                'fb_album': fb_album,
            },
        }
        return render_to_response(
            "facebook_app/gallery_linking.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    external_ids = []

    linked_galleries = []
    kb_only_galleries = []
    fb_only_galleries = []

    fb_albums = {}
    for fb_album in graph.get_connections("me", "albums")['data']:
        if fb_album['type'] == "normal":
            if "created_time" in fb_album:
                fb_album['created_time'] = parse_datetime(fb_album['created_time'])
            if "updated_time" in fb_album:
                fb_album['updated_time'] = parse_datetime(fb_album['updated_time'])
            fb_albums[fb_album['id']] = fb_album

    for gallery in MediaGallery.objects.filter(
        content_type__app_label="people",
        content_type__model="person",
        object_id=obj.pk,
    ).order_by("section__sort_order", "sort_order"):
        try:
            mapper = s.objectmapper_set.get(
                content_type__app_label="media_gallery",
                content_type__model="mediagallery",
                object_id=gallery.pk
            )
        except Exception:
            mapper = None

        if mapper and mapper.external_id in fb_albums:
            linked_galleries.append({
                'kb_gallery': gallery,
                'kb_gallery_count': gallery.mediafile_set.filter(file_type="i").count(),
                'fb_album': fb_albums[mapper.external_id],
            })
            external_ids.append(mapper.external_id)
        else:
            kb_only_galleries.append({
                'kb_gallery': gallery,
                'kb_gallery_count': gallery.mediafile_set.filter(file_type="i").count(),
            })

    for k, v in fb_albums.items():
        if k not in external_ids:
            fb_only_galleries.append({
                'fb_album': v,
            })

    published_gallery_list = MediaGallery.published_objects.filter(
        content_type=ContentType.objects.get_for_model(Person),
        object_id=obj.pk,
    ).order_by("section__sort_order", "sort_order")

    context_dict = {
        'object': obj,
        'can_manage_portfolio': can_manage_portfolio,
        'linked_galleries': linked_galleries,
        'kb_only_galleries': kb_only_galleries,
        'fb_only_galleries': fb_only_galleries,
        'fb_access_token': facebook_user["access_token"],
        'base_template': "people/details_base.html",
        'published_gallery_list': published_gallery_list
    }
    return render_to_response(
        "facebook_app/sync_portfolio.html",
        context_dict,
        context_instance=RequestContext(request),
    )


def sync_institutional_portfolio(request, slug):
    """
    A view for listing albums and displaying what is synced with facebook and what is not
    """
    Institution = models.get_model("institutions", "Institution")
    MediaGallery = models.get_model("media_gallery", "MediaGallery")
    MediaFile = models.get_model("media_gallery", "MediaFile")
    URL_ID_PORTFOLIO = models.get_app("media_gallery").URL_ID_PORTFOLIO
    TOKENIZATION_SUMMAND = models.get_app("media_gallery").TOKENIZATION_SUMMAND
    ObjectMapper = models.get_model("external_services", "ObjectMapper")
    Service = models.get_model("external_services", "Service")

    facebook_user = get_user_from_session(request)
    if facebook_user:
        graph = facebook.GraphAPI(facebook_user["access_token"])
    else:
        return HttpResponseRedirect("/facebook/manage/")
    obj = Institution.objects.get(slug=slug)
    try:
        fb_page = FacebookPage.objects.get(institution=obj)
    except Exception:
        return HttpResponseRedirect("/facebook/manage/")
    # get updated access_token of the page for the institution
    pages = graph.get_connections("me", "accounts").get("data", [])
    for page in pages:
        if int(page['id']) == fb_page.fb_id:
            fb_page.access_token = page['access_token']
            fb_page.save()
            graph = facebook.GraphAPI(fb_page.access_token)
            break

    can_manage_portfolio = request.user.has_perm("institutions.change_institution", obj) and fb_page
    if not can_manage_portfolio:
        return access_denied(request)

    s, created = Service.objects.get_or_create(
        sysname="facebook",
        defaults={
            'url': "https://graph.facebook.com/",
            'title': "Facebook",
        },
    )

    if request.method == "POST" and request.is_ajax():
        action = request.POST.get("action", "")
        kb_gallery_token = request.POST.get("kb_gallery_token", "")
        fb_album_id = request.POST.get("fb_album_id", "")

        if action in ["kb-to-fb", "sync"]:
            gallery = MediaGallery.objects.get(
                pk=int(kb_gallery_token) - TOKENIZATION_SUMMAND,
            )
            try:
                mapper = s.objectmapper_set.get(
                    content_type__app_label="media_gallery",
                    content_type__model="mediagallery",
                    object_id=gallery.pk,
                )
            except Exception:
                mapper = None
            fb_album = None
            if mapper:
                fb_album = graph.get_object(mapper.external_id)
            if not fb_album:
                fb_album = graph.put_object(
                    "me",
                    "albums",
                    name=gallery.title,
                    description=gallery.description,
                )
                if mapper:
                    mapper.external_id = fb_album['id']
                else:
                    mapper = ObjectMapper(
                        service=s,
                        external_id="%s" % fb_album['id'],
                    )
                    mapper.content_object = gallery
                mapper.save()
                fb_album = graph.get_object(mapper.external_id)

            for media_file in gallery.mediafile_set.filter(
                file_type="i",
            ):
                if media_file.path:
                    try:
                        file_mapper = s.objectmapper_set.get(
                            content_type__app_label="media_gallery",
                            content_type__model="mediafile",
                            object_id=media_file.pk
                        )
                    except Exception:
                        file_mapper = None

                    fb_photo = None
                    if file_mapper:
                        fb_photo = graph.get_object(file_mapper.external_id)
                    if not file_mapper or not fb_photo:
                        fb_photo = upload_image(
                            fb_page.access_token,
                            fb_album['id'],
                            os.path.join(settings.UPLOADS_ROOT, media_file.path.path),
                            "%s. %s" % (media_file.title, media_file.description)
                        )
                        if file_mapper:
                            file_mapper.external_id = fb_photo['id']
                        else:
                            file_mapper = ObjectMapper(
                                service=s,
                                external_id="%s" % fb_photo['id'],
                            )
                            file_mapper.content_object = media_file
                        file_mapper.save()

        mapper = None
        gallery = None
        if action in ["fb-to-kb", "sync"]:
            fb_album = graph.get_object(fb_album_id)
            try:
                mapper = s.objectmapper_set.get(
                    content_type__app_label="media_gallery",
                    content_type__model="mediagallery",
                    external_id=fb_album_id
                )
            except Exception:
                mapper = None
            if mapper:
                gallery = mapper.content_object
            else:
                gallery = MediaGallery(
                    title_en=fb_album.get('name', ''),
                    title_de=fb_album.get('name', ''),
                    description_en=fb_album.get("description", ""),
                    description_de=fb_album.get("description", ""),
                )
                gallery.content_object = obj
                gallery.save()
                mapper = ObjectMapper(
                    service=s,
                    external_id="%s" % fb_album['id'],
                )
                mapper.content_object = gallery
                mapper.save()

            for fb_photo in graph.get_connections(fb_album_id, "photos")['data']:
                try:
                    file_mapper = s.objectmapper_set.get(
                        content_type__app_label="media_gallery",
                        content_type__model="mediafile",
                        external_id="%s" % fb_photo['id']
                    )
                except Exception:
                    file_mapper = None

                if file_mapper and file_mapper.content_object:
                    media_file = file_mapper.content_object
                    media_file.title_en = fb_photo.get('name', '')
                    media_file.title_de = fb_photo.get('name', '')
                    media_file.sort_order = int(fb_photo['position']) - 1
                    media_file.save()
                else:
                    media_file = MediaFile(
                        gallery=gallery,
                        title_en=fb_photo.get('name', ''),
                        title_de=fb_photo.get('name', ''),
                        sort_order=int(fb_photo['position']) - 1,
                    )
                    image_url = fb_photo['source']
                    rel_dir = getattr(obj, "get_filebrowser_dir", lambda: "")()
                    rel_dir += URL_ID_PORTFOLIO + "/"
                    fname, fext = os.path.splitext(image_url)
                    filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                    path = "".join((rel_dir, filename))
                    image_data = urllib2.urlopen(image_url)
                    image_mods.FileManager.save_file(
                        path=path,
                        content=image_data.read(),
                    )
                    media_file.path = path
                    media_file.save()
                    if not file_mapper:
                        file_mapper = ObjectMapper(
                            service=s,
                            external_id="%s" % fb_photo['id'],
                        )
                    file_mapper.content_object = media_file
                    file_mapper.save()
            gallery.save()  # updating modification date

        fb_album = graph.get_object(mapper.external_id)  # update file count
        if "created_time" in fb_album:
            fb_album['created_time'] = parse_datetime(fb_album['created_time'])
        if "updated_time" in fb_album:
            fb_album['updated_time'] = parse_datetime(fb_album['updated_time'])

        published_gallery_list = MediaGallery.published_objects.filter(
            content_type=ContentType.objects.get_for_model(Institution),
            object_id=obj.pk,
        ).order_by("section__sort_order", "sort_order")

        context_dict = {
            'object': obj,
            'can_manage_portfolio': can_manage_portfolio,
            'fb_access_token': fb_page.access_token,
            'gallery_opts': {
                'kb_gallery': gallery,
                'kb_gallery_count': gallery.mediafile_set.filter(file_type="i").count(),
                'fb_album': fb_album,
            },
            'published_gallery_list': published_gallery_list
        }
        return render_to_response(
            "facebook_app/gallery_linking.html",
            context_dict,
            context_instance=RequestContext(request),
        )

    external_ids = []

    linked_galleries = []
    kb_only_galleries = []
    fb_only_galleries = []

    fb_albums = {}
    for fb_album in graph.get_connections("me", "albums")['data']:
        if fb_album['type'] == "normal":
            if "created_time" in fb_album:
                fb_album['created_time'] = parse_datetime(fb_album['created_time'])
            if "updated_time" in fb_album:
                fb_album['updated_time'] = parse_datetime(fb_album['updated_time'])
            fb_albums[fb_album['id']] = fb_album

    for gallery in MediaGallery.objects.filter(
        content_type__app_label="institutions",
        content_type__model="institution",
        object_id=obj.pk,
    ).order_by("section__sort_order", "sort_order"):
        try:
            mapper = s.objectmapper_set.get(
                content_type__app_label="media_gallery",
                content_type__model="mediagallery",
                object_id=gallery.pk
            )
        except Exception:
            mapper = None

        if mapper and mapper.external_id in fb_albums:
            linked_galleries.append({
                'kb_gallery': gallery,
                'kb_gallery_count': gallery.mediafile_set.filter(file_type="i").count(),
                'fb_album': fb_albums[mapper.external_id],
            })
            external_ids.append(mapper.external_id)
        else:
            kb_only_galleries.append({
                'kb_gallery': gallery,
                'kb_gallery_count': gallery.mediafile_set.filter(file_type="i").count(),
            })

    for k, v in fb_albums.items():
        if k not in external_ids:
            fb_only_galleries.append({
                'fb_album': v,
            })

    context_dict = {
        'object': obj,
        'can_manage_portfolio': can_manage_portfolio,
        'linked_galleries': linked_galleries,
        'kb_only_galleries': kb_only_galleries,
        'fb_only_galleries': fb_only_galleries,
        'fb_access_token': fb_page.access_token,
        'base_template': "institutions/details_base.html",
    }
    return render_to_response(
        "facebook_app/sync_portfolio.html",
        context_dict,
        context_instance=RequestContext(request),
    )
