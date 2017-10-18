# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, time

#from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django import forms

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from jetson.apps.image_mods.models import FileManager

from base_libs.views.views import access_denied
from base_libs.utils.misc import get_related_queryset

from jetson.apps.utils.views import show_form_step
from jetson.apps.utils.decorators import login_required
from jetson.apps.structure.models import Category

from .models import Bulletin, TYPE_CHOICES, STATUS_CHOICES
from .forms import BulletinForm, BULLETIN_FORM_STEPS, BulletinSearchForm

PersonGroup = models.get_model("groups_networks", "PersonGroup")

ContextItem = models.get_model("site_specific", "ContextItem")
TOKENIZATION_SUMMAND = models.get_app("bulletin_board").TOKENIZATION_SUMMAND


@never_cache
def bulletin_list(request, category_slug=None, template_name="bulletin_board/bulletin_list.html", show="", **kwargs):
    kwargs.setdefault('queryset', Bulletin.published_objects.order_by("-published_from"))

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        kwargs['queryset'] = kwargs['queryset'].filter(categories__tree_id=category.tree_id)

    form = BulletinSearchForm(data=request.REQUEST)
    
    if show == "favorites":
        queryset = kwargs['queryset']
        if not request.user.is_authenticated():
            return access_denied(request)
        tables = ["favorites_favorite"]
        condition = [
            "favorites_favorite.user_id = %d" % request.user.id,
            "favorites_favorite.object_id = bulletin_board_bulletin.id",
            "favorites_favorite.content_type_id = %d" % ContentType.objects.get_for_model(queryset.model).pk,
        ]
        queryset = queryset.extra(
            tables=tables,
            where=condition,
        ).distinct()
        kwargs['queryset'] = queryset

    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(Bulletin, "categories"),
            'locality_types': get_related_queryset(Bulletin, "locality_type"),
            'bulletin_types': TYPE_CHOICES,
            'bulletin_categories': get_related_queryset(Bulletin, "bulletin_category"),
            },
        }
        
    if form.is_valid():
    
        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            kwargs['queryset'] = kwargs['queryset'].filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()
                
        lt = form.cleaned_data['locality_type']
        if lt:
            facets['selected']['locality_type'] = lt
            kwargs['queryset'] = kwargs['queryset'].filter(
                locality_type__lft__gte=lt.lft,
                locality_type__rght__lte=lt.rght,
                locality_type__tree_id=lt.tree_id,
                ).distinct()
                
        bulletin_type = form.cleaned_data['bulletin_type']
        if bulletin_type:
            facets['selected']['bulletin_type'] = bulletin_type
            kwargs['queryset'] = kwargs['queryset'].filter(
                bulletin_type=bulletin_type,
            ).distinct()
            
        cat = form.cleaned_data['bulletin_category']
        if cat:
            facets['selected']['bulletin_category'] = cat
            kwargs['queryset'] = kwargs['queryset'].filter(
                bulletin_category=cat,
            ).distinct()

    extra_context = kwargs.setdefault("extra_context", {})
    extra_context['facets'] = facets
    extra_context['form'] = form
    extra_context['source_list'] = reverse("bulletin_list")
    extra_context['category'] = category

    #extra_context = {
    #    'form': form,
    #    'facets': facets,
    #    'source_list': reverse("bulletin_list"),
    #}

    return object_list(
        request,
        queryset=kwargs['queryset'],
        template_name=template_name,
        paginate_by=24,
        extra_context=extra_context,
        context_processors=(prev_next_processor,),
        httpstate_prefix="bulletin_list",
    )


def bulletin_detail(request, token):
    pk = int(token) - TOKENIZATION_SUMMAND
    if "preview" in request.REQUEST:
        qs = Bulletin.objects.all()
        obj = get_object_or_404(qs, pk=pk)
        if request.user != obj.creator and not request.user.has_perm("bulletin_board.change_bulletin", obj):
            return access_denied(request)
    else:
        qs = Bulletin.objects.filter(status="published")
        obj = get_object_or_404(qs, pk=pk)
    return render(
        request,
        "bulletin_board/bulletin_detail.html",
        {'object': obj},
    )


@never_cache
@login_required
def add_bulletin(request):
    return show_form_step(request, BULLETIN_FORM_STEPS, extra_context={});


@never_cache
@login_required
def change_bulletin(request, token):
    instance = get_object_or_404(Bulletin, pk=int(token) - TOKENIZATION_SUMMAND)
    if not request.user.has_perm("bulletin_board.change_production", instance) and instance.creator != request.user:
        return access_denied(request)
    return show_form_step(request, BULLETIN_FORM_STEPS, extra_context={'bulletin': instance}, instance=instance);


# @login_required
# def add_bulletin(request):
#     if request.method == "POST":
#         form = BulletinForm(request.POST, request.FILES)
#         if form.is_valid():
#
#             #direct to confirmation page
#             if form.cleaned_data['confirmed'] == "0":
#                 form = BulletinFormConfirm(request.POST, request.FILES)
#                 if form.is_valid():
#                     object = form.cleaned_data
#                     object["is_add"] = True
#                     return render(request, "bulletin_board/change_bulletin_confirm.html", {'form': form, 'object': object})
#
#             #comming back from confirmation page to keep editing
#             if form.cleaned_data['confirmed'] == "2":
#                 object = form.cleaned_data
#                 object["is_add"] = True
#                 return render(request, "bulletin_board/change_bulletin.html", {'form': form, 'object': object})
#
#             instance = form.save(commit=False)
#             #instance.status = "published"
#             if form.cleaned_data['published_till_date']:
#                 if form.cleaned_data['published_till_time']:
#                     instance.published_till = datetime.combine(
#                         form.cleaned_data['published_till_date'],
#                         form.cleaned_data['published_till_time'],
#                     )
#                 else:
#                     instance.published_till = datetime.combine(
#                         form.cleaned_data['published_till_date'],
#                         time(0,0),
#                     )
#                 #instance.published_till.replace(tzinfo=timezone.get_current_timezone())
#             instance.save()
#             form.save_m2m()
#
#             rel_dir = "bulletin_board/"
#             if form.cleaned_data.get("image_path", None):
#                 tmp_path = form.cleaned_data['image_path']
#                 abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
#
#                 fname, fext = os.path.splitext(tmp_path)
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
#                 dest_path = "".join((rel_dir, filename))
#                 FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
#                 abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
#
#                 shutil.copy2(abs_tmp_path, abs_dest_path)
#
#                 os.remove(abs_tmp_path)
#                 instance.image = dest_path
#                 instance.save()
#
#             if form.cleaned_data.get('reload_page', False):
#                 return redirect("change_bulletin", token=instance.get_token())
#
#             return redirect("my_bulletin_list")
#     else:
#         initial = {}
#         if request.user.is_authenticated():
#             if request.user.first_name and request.user.last_name:
#                 initial['contact_person'] = u"%s %s" % (request.user.first_name, request.user.last_name)
#             else:
#                 initial['contact_person'] = request.user.username
#             if request.user.profile.individualcontact_set.count():
#                 contact = request.user.profile.individualcontact_set.all()[:1].get()
#                 if contact.is_phone2_default:
#                     initial['phone'] = '+' + contact.phone2_country + contact.phone2_area + contact.phone2_number
#                 elif contact.is_phone1_default:
#                     initial['phone'] = '+' + contact.phone1_country + contact.phone1_area + contact.phone1_number
#                 else:
#                     initial['phone'] = '+' + contact.phone0_country + contact.phone0_area + contact.phone0_number
#             initial['email'] = request.user.email
#
#
#         form = BulletinForm(initial=initial)
#
#     return render(request, "bulletin_board/change_bulletin.html", {'form': form})
#
#
# @login_required
# def change_bulletin(request, token):
#     instance = get_object_or_404(Bulletin, pk=int(token) - TOKENIZATION_SUMMAND)
#     if request.user != instance.creator and not request.user.has_perm("bulletin_board.change_bulletin", instance):
#         return access_denied(request)
#
#     if request.method == "POST":
#         form = BulletinForm(request.POST, request.FILES, instance=instance)
#         if form.is_valid():
#
#             #direct to confirmation page
#             if form.cleaned_data['confirmed'] == "0":
#                 form = BulletinFormConfirm(request.POST, request.FILES, instance=instance)
#                 if form.is_valid():
#                     object = form.cleaned_data
#                     if not form.cleaned_data.get("image_path", None):
#                         object["image"] = instance.image
#                     return render(request, "bulletin_board/change_bulletin_confirm.html", {'form': form, 'object': object})
#
#             #comming back from confirmation page to keep editing
#             if form.cleaned_data['confirmed'] == "2":
#                 object = form.cleaned_data
#                 if not form.cleaned_data.get("image_path", None):
#                     object["image"] = instance.image
#                 return render(request, "bulletin_board/change_bulletin.html", {'form': form, 'object': object})
#
#
#             instance = form.save(commit=False)
#             if form.cleaned_data['published_till_date']:
#                 if form.cleaned_data['published_till_time']:
#                     instance.published_till = datetime.combine(
#                         form.cleaned_data['published_till_date'],
#                         form.cleaned_data['published_till_time'],
#                     )
#                 else:
#                     instance.published_till = datetime.combine(
#                         form.cleaned_data['published_till_date'],
#                         time(0,0),
#                     )
#                 #instance.published_till.replace(tzinfo=timezone.get_current_timezone())
#             instance.save()
#             form.save_m2m()
#
#             rel_dir = "bulletin_board/"
#             if form.cleaned_data.get("image_path", None):
#                 tmp_path = form.cleaned_data['image_path']
#                 abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
#
#                 fname, fext = os.path.splitext(tmp_path)
#                 #filename = timezone.now().strftime("%Y%m%d%H%M%S") + fext
#                 filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
#                 dest_path = "".join((rel_dir, filename))
#                 FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
#                 abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
#
#                 shutil.move(abs_tmp_path, abs_dest_path)
#
#                 instance.image = dest_path
#                 instance.save()
#             if form.cleaned_data.get('reload_page', False):
#                 return redirect("change_bulletin", token=instance.get_token())
#
#             return redirect("my_bulletin_list")
#     else:
#         form = BulletinForm(instance=instance)
#
#     return render(request, "bulletin_board/change_bulletin.html", {'form': form, 'object': instance})


@never_cache
@login_required
def delete_bulletin(request, token):
    instance = get_object_or_404(Bulletin, pk=int(token) - TOKENIZATION_SUMMAND)
    if request.user != instance.creator and not request.user.has_perm("bulletin_board.delete_bulletin", instance):
        return access_denied(request)

    context = {
        'object': instance,
    }
    if request.method == "POST":
        form = forms.Form(request.POST)  # dummy form. we just care about the csrf token
        if form.is_valid():
            instance.delete()
            return redirect("bulletin_deleted")
    else:
        form = forms.Form()  # dummy form. we just care about the csrf token

    context['form'] = form

    return render(request, 'bulletin_board/delete_bulletin.html', context)


@never_cache
@login_required
def change_bulletin_status(request, token):
    instance = get_object_or_404(Bulletin, pk=int(token) - TOKENIZATION_SUMMAND)
    if request.user != instance.creator and not request.user.has_perm("bulletin_board.change_bulletin", instance):
        return access_denied(request)
    if request.method == "POST" and request.is_ajax():
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    if instance.status == "published":
        return redirect(instance)
    else:
        return redirect("dashboard")


STATUS_CHOICES = (
    ('published', _("Published")),
    ('draft', _("Draft")),
    #('expired', _("Expired")),
)


class MyBulletinFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
    )


@login_required
@never_cache
def my_bulletin_list(request, **kwargs):
    owned_inst_ids = PersonGroup.objects.filter(
        groupmembership__user=request.user,
        content_type__model="institution",
    ).values_list("object_id", flat=True)

    qs = Bulletin.objects.filter(
        models.Q(creator=request.user)
        | models.Q(institution__pk__in=owned_inst_ids)
    )

    form = MyBulletinFilterForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories': {
            'statuses': STATUS_CHOICES,
        }
    }

    if form.is_valid():
        status = form.cleaned_data['status']
        if status:
            facets['selected']['status'] = status
            qs = qs.filter(status=status)

    extra_context = {
        'form': form,
        'source_list': 'my_bulletin_list',
        'facets': facets,
    }
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"

    kwargs['extra_context'] = extra_context
    kwargs['httpstate_prefix'] = 'my_bulletin_list'
    kwargs['queryset'] = qs
    kwargs['template_name'] = "bulletin_board/my_bulletin_list.html"

    return object_list(request, **kwargs)


