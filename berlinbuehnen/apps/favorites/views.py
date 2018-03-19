# -*- coding: UTF-8 -*-
import json
import random

from django.contrib.contenttypes.models import ContentType
from datetime import datetime, date, time

from django.db import models
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _, ugettext
from django import forms
from django.core.urlresolvers import reverse

from jetson.apps.utils.decorators import login_required
from jetson.apps.favorites.models import Favorite

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from berlinbuehnen.utils.forms import PrimarySubmit
from jetson.apps.mailing.recipient import Recipient
from jetson.apps.mailing.views import send_email_using_template

from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_website_url
from base_libs.forms import dynamicforms
from base_libs.views.views import access_denied

Favorite = models.get_model("favorites", "Favorite")
FavoriteListOptions = models.get_model("favorites", "FavoriteListOptions")

Location = models.get_model("locations", "Location")
Event = models.get_model("productions", "Event")
Festival = models.get_model("festivals", "Festival")
Department = models.get_model("education", "Department")
Project = models.get_model("education", "Project")

from .templatetags.favorites_tags import get_favorites_count


def json_set_favorite(request, content_type_id, object_id):
    "Sets the object as a favorite for the current user"
    json_str = "false"
    if request.user.is_authenticated():
        content_type = ContentType.objects.get(id=content_type_id)
        instance = content_type.get_object_for_this_type(pk=object_id)
        favorite, is_created = Favorite.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            user=request.user,
        )
        if not is_created:
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


USER_TOKEN_SUMMAND = 564654


@login_required
def redirect_to_user_favorites(request):
    user = request.user
    user_token = user.pk + USER_TOKEN_SUMMAND
    return redirect('user_favorites', user_token=user_token)


class FavoritesFilterForm(dynamicforms.Form):
    latitude = forms.FloatField(
        required=False,
    )
    longitude = forms.FloatField(
        required=False,
    )


def user_favorites(request, user_token, **kwargs):
    """
    Displays the list of favorite objects
    """
    user_id = int(user_token) - USER_TOKEN_SUMMAND

    try:
        opts = FavoriteListOptions.objects.get(user__pk=user_id)
    except FavoriteListOptions.DoesNotExist:
        opts = FavoriteListOptions()

    location_ids = list(Favorite.objects.filter(
        content_type__app_label="locations",
        content_type__model="location",
        user__pk=user_id,
    ).values_list("object_id", flat=True))

    event_ids = list(Favorite.objects.filter(
        content_type__app_label="productions",
        content_type__model="event",
        user__pk=user_id,
    ).values_list("object_id", flat=True))

    festival_ids = list(Favorite.objects.filter(
        content_type__app_label="festivals",
        content_type__model="festival",
        user__pk=user_id,
    ).values_list("object_id", flat=True))

    department_ids = list(Favorite.objects.filter(
        content_type__app_label="education",
        content_type__model="department",
        user__pk=user_id,
    ).values_list("object_id", flat=True))

    project_ids = list(Favorite.objects.filter(
        content_type__app_label="education",
        content_type__model="project",
        user__pk=user_id,
    ).values_list("object_id", flat=True))

    favorites = dict((
        ('locations', Location.objects.filter(id__in=location_ids, status="published")),
        ('events', Event.objects.filter(id__in=event_ids, production__status="published")),
        ('festivals', Festival.objects.filter(id__in=festival_ids, status="published")),
        ('departments', Department.objects.filter(id__in=department_ids, status="published")),
        ('projects', Project.objects.filter(id__in=project_ids, status="published")),
    ))

    facets = {
        'selected': {},
        'categories': {
        },
    }

    form = FavoritesFilterForm(data=request.REQUEST)

    latitude = longitude = None
    if form.is_valid():
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        if latitude and longitude:
            facets['selected']['latitude'] = latitude
            facets['selected']['longitude'] = longitude
            # favorites['events'] = favorites['events'].extra(
            #     select={'distance': 'ST_Distance(POINT(events_event.latitude, events_event.longitude), POINT(%f, %f))' % (latitude, longitude)}
            # )
            # favorites['museums'] = favorites['museums'].extra(
            #     select={'distance': 'ST_Distance(POINT(museums_museum.latitude, museums_museum.longitude), POINT(%f, %f))' % (latitude, longitude)}
            # )

    favorites['locations'] = favorites['locations'].distinct()
    favorites['events'] = favorites['events'].distinct()
    favorites['festivals'] = favorites['festivals'].distinct()
    favorites['departments'] = favorites['departments'].distinct()
    favorites['projects'] = favorites['projects'].distinct()

    if latitude and longitude:
        favorites['events'] = favorites['events'].order_by('distance')

    if latitude and longitude:
        favorites['locations'] = favorites['locations'].order_by('distance')
    else:
        favorites['locations'] = favorites['locations'].extra(select={
            'title_uni': "IF (locations_location.title_%(lang_code)s = '', locations_location.title_de, locations_location.title_%(lang_code)s)" % {
                'lang_code': request.LANGUAGE_CODE,
            }
        }).order_by("title_uni")

    if opts.description:
        opts.description_striped = opts.description.replace("\r\n"," ")
        opts.description_striped = opts.description_striped.replace("\n"," ")

    return render(request, kwargs["template_name"], {
        'facets': facets,
        'form': form,
        'favorites': favorites,
        'list_options': opts,
        'random': random.randint(-99999999, 99999999),
        'user_id': user_id,
    })


class FavoritesByEmailForm(forms.Form):
    sender_name = forms.CharField(
        label=_("Your name")
    )
    sender_email = forms.EmailField(
        label=_("Your email")
    )
    recipient_name = forms.CharField(
        label=_("Your friend's name")
    )
    recipient_email = forms.EmailField(
        label=_("Your friend's email")
    )
    message = forms.CharField(
        label=_("Message"),
        required=False,
        widget=forms.Textarea(),
    )

    def __init__(self, *args, **kwargs):
        super(FavoritesByEmailForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Send your favorites to a friend"),
                "sender_name",
                "sender_email",
                "recipient_name",
                "recipient_email",
                "message",
            ),
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Send')),
            )
        )

@login_required
def send_user_favorites_by_email(request, user_token, **kwargs):
    if request.method == "POST":
        form = FavoritesByEmailForm(data=request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            sender_name, sender_email = cleaned['sender_name'], cleaned['sender_email']  # settings.MANAGERS[0]
            user_favorites_view = get_website_url(reverse('user_favorites', kwargs={'user_token': user_token}))
            send_email_using_template(
                recipients_list=[Recipient(name=cleaned['recipient_name'], email=cleaned['recipient_email'])],
                email_template_slug="favorites_shared",
                obj_placeholders={
                    'object_url': user_favorites_view,
                    'object_title': ugettext("Favorites"),
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


class FavoriteListOptionsForm(forms.ModelForm):
    class Meta:
        model = FavoriteListOptions
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super(FavoriteListOptionsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Edit My Favorites description"),
                "title",
                layout.Field("description", rows=5),
            ),
            bootstrap.FormActions(
                PrimarySubmit('submit', _('Save')),
            )
        )

@login_required
def change_favorite_list(request, user_token, **kwargs):
    """
    Displays the list of favorite objects
    """
    user_id = int(user_token) - USER_TOKEN_SUMMAND

    if request.user.pk != user_id and not request.user.is_staff:
        return access_denied(request)

    try:
        opts = FavoriteListOptions.objects.get(user__pk=user_id)
    except FavoriteListOptions.DoesNotExist:
        opts = FavoriteListOptions()
        opts.title = ugettext("Favorites")

    if request.method == "POST":
        form = FavoriteListOptionsForm(data=request.POST, instance=opts)
        if form.is_valid():
            opts = form.save(commit=False)
            opts.user_id = user_id
            opts.save()
            return render(request, "favorites/change_favorite_list_done.html", {})

    else:
        form = FavoriteListOptionsForm(instance=opts)

    return render(request, "favorites/change_favorite_list.html", {
        'form': form,
    })
