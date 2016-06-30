# -*- coding: UTF-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from datetime import datetime, date, time

from django.db import models
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse

from jetson.apps.utils.decorators import login_required
from jetson.apps.favorites.models import Favorite

from langenacht.apps.mailing.recipient import Recipient
from langenacht.apps.mailing.views import send_email_using_template

from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_website_url
from base_libs.views.views import access_denied

Favorite = models.get_model("favorites", "Favorite")
FavoriteList = models.get_model("favorites", "FavoriteList")
Museum = models.get_model("museums", "Museum")
MuseumRoute = models.get_model("museums", "MuseumRoute")
Exhibition = models.get_model("exhibitions", "Exhibition")
Event = models.get_model("events", "Event")
Workshop = models.get_model("workshops", "Workshop")

from .models import TOKEN_SUMMAND
from .templatetags.favorites_tags import get_favorites_count
from .forms import FavoritesFilterForm, FavoriteListForm, FavoritesByEmailForm, EVENT_TIME_CHOICES


def json_set_favorite(request, content_type_id, object_id):
    "Sets the object as a favorite for the current user"
    json_str = "false"
    if request.user.is_authenticated():
        content_type = ContentType.objects.get(id=content_type_id)
        instance = content_type.get_object_for_this_type(pk=object_id)

        is_created = False
        try:
            # get favorite
            favorite = Favorite.objects.filter(
                favorite_list__user=request.user,
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.pk,
            )[0]
        except IndexError:
            # set favorite
            try:
                favorite_list = FavoriteList.objects.filter(user=request.user)[0]
            except IndexError:
                favorite_list = FavoriteList()
                favorite_list.user = request.user
                favorite_list.title_en = u"A Tour of {}".format(request.user.username)
                favorite_list.title_de = u"Eine Tour von {}".format(request.user.username)
                favorite_list.save()
            favorite = Favorite(favorite_list=favorite_list)
            favorite.content_object = instance
            favorite.save()
            is_created = True
        else:
            favorite.delete()

        result = favorite.__dict__
        result = dict([
            (item[0], item[1])
            for item in result.items()
            if not item[0].startswith("_")
        ])
        result['action'] = is_created and "added" or "removed"
        result['count'] = get_favorites_count(instance)
        # update favorites_count field if it exists in the model
        if hasattr(instance, "favorites_count"):
            type(instance).objects.filter(pk=instance.pk).update(favorites_count=result['count'])
        json_str = json.dumps(
            result,
            ensure_ascii=False,
            cls=ExtendedJSONEncoder,
        )
    return HttpResponse(json_str, mimetype='text/javascript; charset=utf-8')
json_set_favorite = never_cache(json_set_favorite)


@login_required
def redirect_to_user_favorites(request):
    try:
        favorite_list = FavoriteList.objects.filter(user=request.user)[0]
    except IndexError:
        favorite_list = FavoriteList()
        favorite_list.user = request.user
        favorite_list.title_en = u"A Tour of {}".format(request.user.username)
        favorite_list.title_de = u"Eine Tour von {}".format(request.user.username)
        favorite_list.save()
    favorite_list_token = favorite_list.pk + TOKEN_SUMMAND
    return redirect('user_favorites', favorite_list_token=favorite_list_token)


def user_favorites(request, favorite_list_token, **kwargs):
    """
    Displays the list of favorite objects
    """
    favorite_list_id = int(favorite_list_token) - TOKEN_SUMMAND

    try:
        favorite_list = FavoriteList.objects.filter(pk=favorite_list_id)[0]
    except IndexError:
        favorite_list = FavoriteList()

    museum_ids = list(Favorite.objects.filter(
        content_type__app_label="museums",
        content_type__model="museum",
        favorite_list=favorite_list,
    ).values_list("object_id", flat=True))

    exhibition_ids = list(Favorite.objects.filter(
        content_type__app_label="exhibitions",
        content_type__model="exhibition",
        favorite_list=favorite_list,
    ).values_list("object_id", flat=True))

    event_ids = list(Favorite.objects.filter(
        content_type__app_label="events",
        content_type__model="event",
        favorite_list=favorite_list,
    ).values_list("object_id", flat=True))

    workshop_ids = list(Favorite.objects.filter(
        content_type__app_label="workshops",
        content_type__model="workshop",
        favorite_list=favorite_list,
    ).values_list("object_id", flat=True))

    favorites = dict((
        ('museums', Museum.objects.filter(id__in=museum_ids, status="published")),
        ('exhibitions', Exhibition.objects.filter(id__in=exhibition_ids, status="published")),
        ('events', Event.objects.filter(id__in=event_ids, status="published")),
        ('workshops', Workshop.objects.filter(id__in=workshop_ids, status="published")),
    ))

    facets = {
        'selected': {},
        'categories': {
            'routes': MuseumRoute.objects.all(),
            'event_times': EVENT_TIME_CHOICES,
        },
    }

    form = FavoritesFilterForm(data=request.REQUEST)

    latitude = longitude = None
    event_time = None
    if form.is_valid():
        route = form.cleaned_data['route']
        if route:
            facets['selected']['route'] = route
            favorites['events'] = favorites['events'].filter(
                museum__stop__routestop__route=route,
            ).distinct()
            favorites['museums'] = favorites['museums'].filter(
                stop__routestop__route=route,
            ).distinct()
        event_time = form.cleaned_data['event_time']
        if event_time:
            facets['selected']['event_time'] = (event_time, dict(EVENT_TIME_CHOICES)[event_time])
            now = datetime.now()
            if event_time == "now":
                favorites['events'] = favorites['events'].filter(
                    models.Q(
                        eventtime__start__gte=now.time(),
                        eventtime__end__lte=now.time(),
                    ) | models.Q(
                        eventtime__start__gte=now.time(),
                        eventtime__end=None,
                    ),
                    eventtime__event_date=now.date(),
                ).distinct()
            else:
                start_hour, end_hour = event_time.split("-")
                start_time = time(int(start_hour), 0)
                if end_hour == "24":
                    end_time = time(23, 59)
                else:
                    end_time = time(int(end_hour), 0)
                event_date = date(2015, 8, 29)
                # if start_time.hour < 3:
                #     event_date = date(2015, 8, 30)

                if start_time.hour < 3:
                    favorites['events'] = favorites['events'].filter(
                        models.Q(
                            eventtime__start__lte=start_time,
                            eventtime__end__gt=start_time,
                            eventtime__start__lt=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__start__lt=end_time,
                            eventtime__end__gt=end_time,
                            eventtime__start__lte=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__start__gte=start_time,
                            eventtime__end__lt=end_time,
                            eventtime__start__lt=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__start__lte=start_time,
                            eventtime__end__gt=end_time,
                            eventtime__start__lt=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__end__gt=start_time,
                            eventtime__end__lte=end_time,
                            eventtime__start__gt=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__end__gte=end_time,
                            eventtime__start__gt=models.F('eventtime__end'),
                        ),
                    ).distinct()
                else:
                    favorites['events'] = favorites['events'].filter(
                        models.Q(
                            eventtime__start__lte=start_time,
                            eventtime__end__gt=start_time,
                            eventtime__start__lt=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__start__lt=end_time,
                            eventtime__end__gt=end_time,
                            eventtime__start__lte=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__start__gte=start_time,
                            eventtime__end__lt=end_time,
                            eventtime__start__lt=models.F('eventtime__end'),
                        ) | models.Q(
                            eventtime__start__lte=end_time,
                            eventtime__end__gte=end_time,
                            eventtime__end__lt=models.F('eventtime__start'),
                        ) | models.Q(
                            eventtime__start__lte=start_time,
                            eventtime__end__lte=end_time,
                            eventtime__end__lt=models.F('eventtime__start'),
                        ),
                        eventtime__event_date=event_date,
                    ).distinct()
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        if latitude and longitude:
            facets['selected']['latitude'] = latitude
            facets['selected']['longitude'] = longitude
            favorites['events'] = favorites['events'].extra(
                select={'distance': 'ST_Distance(POINT(events_event.latitude, events_event.longitude), POINT(%f, %f))' % (latitude, longitude)}
            )
            favorites['museums'] = favorites['museums'].extra(
                select={'distance': 'ST_Distance(POINT(museums_museum.latitude, museums_museum.longitude), POINT(%f, %f))' % (latitude, longitude)}
            )

    favorites['events'] = favorites['events'].distinct()
    favorites['museums'] = favorites['museums'].distinct()

    if latitude and longitude:
        favorites['events'] = favorites['events'].order_by('distance')
    elif event_time:
        favorites['events'] = favorites['events'].extra(
            select={
                'event_time_count': 'SELECT COUNT(*) FROM events_eventtime WHERE event_id=events_event.id'
            }
        ).order_by("event_time_count", "eventtime__event_date", "eventtime__start", "title_%s" % request.LANGUAGE_CODE)
    else:
        favorites['events'] = favorites['events'].annotate(
            null_date=models.Count("closest_event_date")
        ).order_by("-null_date", "closest_event_date", "closest_event_time", "title_%s" % request.LANGUAGE_CODE)

    if latitude and longitude:
        favorites['museums'] = favorites['museums'].order_by('distance')
    else:
        favorites['museums'] = favorites['museums'].extra(select={
            'title_uni': "IF (museums_museum.title_%(lang_code)s = '', museums_museum.title_de, museums_museum.title_%(lang_code)s)" % {
                'lang_code': request.LANGUAGE_CODE,
            }
        }).order_by("title_uni")

    other_favorite_lists = FavoriteList.objects.filter(is_featured=True).exclude(pk=favorite_list.pk).order_by("?")[:4]

    return render(request, kwargs["template_name"], {
        'facets': facets,
        'form': form,
        'favorites': favorites,
        'favorite_list': favorite_list,
        'other_favorite_lists': other_favorite_lists,
    })


@login_required
def send_user_favorites_by_email(request, favorite_list_token, **kwargs):
    if request.method == "POST":
        form = FavoritesByEmailForm(data=request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            sender_name, sender_email = settings.MANAGERS[0]
            user_favorites_view = get_website_url(reverse('user_favorites', kwargs={'favorite_list_token': favorite_list_token}))
            send_email_using_template(
                recipients_list=[Recipient(name=cleaned['recipient_name'], email=cleaned['recipient_email'])],
                email_template_slug="tour_shared",
                obj_placeholders={
                    'object_url': user_favorites_view,
                    'object_title': ugettext("My Tour"),
                    'object_creator_title': '%s (%s)' % (cleaned['sender_name'], cleaned['sender_email']),
                    'object_description': cleaned['message'],
                },
                sender_name=sender_name,
                sender_email=sender_email,
                delete_after_sending=False,
            )
            return render(request, 'favorites/send_user_favorites_by_email_done.html')
    else:
        form = FavoritesByEmailForm(initial={'sender_email': request.user.email})

    return render(request, kwargs["template_name"], {
        'form': form,
    })


@login_required
def favorite_museums(request, **kwargs):
    """
    Displays the list of favorite objects
    """
    museum_ids = list(Favorite.objects.filter(
        content_type__app_label="museums",
        content_type__model="museum",
        favorite_list__user=request.user,
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
        favorite_list__user=request.user,
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
        favorite_list__user=request.user,
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
        favorite_list__user=request.user,
    ).values_list("object_id", flat=True))

    favorites = (
        ('workshops', Workshop.objects.filter(id__in=workshop_ids, status="published")),
    )
    return render(request, "favorites/favorite_workshops.html", {
        'favorites': favorites,
    })


@login_required
def change_favorite_list(request, favorite_list_token, **kwargs):
    """
    Displays the list of favorite objects
    """
    favorite_list_id = int(favorite_list_token) - TOKEN_SUMMAND
    try:
        favorite_list = FavoriteList.objects.filter(pk=favorite_list_id)[0]
    except IndexError:
        raise Http404

    if request.user != favorite_list.user and not request.user.is_staff:
        return access_denied(request)

    if request.method == "POST":
        form = FavoriteListForm(data=request.POST, instance=favorite_list)
        if form.is_valid():
            opts = form.save(commit=False)
            opts.save()
            return render(request, "favorites/change_favorite_list_done.html", {})

    else:
        form = FavoriteListForm(instance=favorite_list)

    return render(request, "favorites/change_favorite_list.html", {
        'form': form,
    })


def featured_curated_lists(request):
    qs = FavoriteList.objects.filter(is_featured=True)
    return render(request, "curated_lists/featured_curated_lists.html", {'object_list': qs})