# -*- coding: UTF-8 -*-
import hashlib
import os

from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.core.urlresolvers import reverse
from django.db import models
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django import forms

from ccb.apps.accounts.forms import SimpleRegistrationForm
from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list

from base_libs.views.views import access_denied

from jetson.apps.mailing.views import send_email_using_template

from jetson.apps.mailing.recipient import Recipient

from django.contrib.sites.models import Site
from base_libs.utils.crypt import cryptString, decryptString

image_mods = apps.get_app("image_mods")
SiteSettings = apps.get_model("configuration", "SiteSettings")


from .forms import (
    CuratedListForm,
    CuratedListItemForm,
    CuratedListFilterForm,
    OwnerInvitationForm,
    PersonOrInstitutionInvitationForm,
    CuratedListDeletionForm,
    CuratedListItemRemovalForm,
    CuratedListOwnerRemovalForm,
    AddItemToNewCuratedListForm,
    ItemAtCuratedListForm,
    PersonAndInstitutionRegistrationForm,
)
from .models import CuratedList, ListOwner, ListItem


def get_unique_filename(filename):
    from django.utils.timezone import now as timezone_now
    filename_base, filename_ext = os.path.splitext(filename)
    now = timezone_now()
    filename = "".join((
        now.strftime("%Y%m%d%H%M%S"),
        ("000" + str(int(round(now.microsecond / 1000))))[-4:],
        filename_ext.lower(),
    ))
    return filename


def save_tmp_image(f):
    filename = get_unique_filename(f.name)
    with open(os.path.join(settings.PATH_TMP, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


def save_final_image(curated_list, tmp_image_filename):
    tmp_file_path = os.path.join(settings.PATH_TMP, tmp_image_filename)
    with open(tmp_file_path, 'r') as source:
        image_mods.FileManager.save_file_for_object(
            curated_list,
            tmp_image_filename,
            source.read(),
            subpath="curated-lists/{}/".format(curated_list.pk)
        )
    os.unlink(tmp_file_path)


def delete_blog_post_image(post):
    image_mods.FileManager.delete_file_for_object(post)


def curated_list_detail(request, token, **kwargs):
    """
    Displays the list of favorite objects
    """
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    other_curated_lists = []
    if curated_list.is_featured:
        other_curated_lists = CuratedList.objects.filter(is_featured=True).exclude(pk=curated_list.pk)

    editable = curated_list.is_editable(user=request.user)

    return render(request, "curated_lists/curated_list_detail.html", {
        'curated_list': curated_list,
        'other_curated_lists': other_curated_lists,
        'visible_list_items': curated_list.get_visible_list_items(user=request.user),
        'editable': editable,
    })


@login_required
def change_curated_list(request, token, **kwargs):
    """
    Displays the list of favorite objects
    """
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == "POST":
        data = request.POST.copy()
        if 'image' in request.FILES:
            # the image will be saved temporarily in case if there are any form validation errors,
            # so that it can be retrieved later
            data['tmp_image_filename'] = save_tmp_image(request.FILES['image'])
        form = CuratedListForm(request=request, curated_list=curated_list, data=data)
        if form.is_valid():
            curated_list = form.save(commit=False)
            curated_list.save()
            if form.cleaned_data['tmp_image_filename']:
                save_final_image(curated_list, form.cleaned_data['tmp_image_filename'])
            return redirect('curated_list_detail', token=token)

    else:
        form = CuratedListForm(request=request, curated_list=curated_list)

    return render(request, "curated_lists/change_curated_list.html", {
        'form': form,
        'curated_list': curated_list,
    })


def featured_curated_lists(request, **kwargs):
    qs = CuratedList.objects.filter(is_featured=True)
    form = CuratedListFilterForm(data=request.GET)

    facets = {
        'selected': {},
        'categories': {
            'owners': form.fields['owner'].queryset,
            'categories': form.fields['category'].queryset,
        },
    }

    if form.is_valid():
        owner = form.cleaned_data.get("owner")
        if owner:
            facets['selected']['owner'] = owner
            qs = qs.filter(
                listowner__owner_content_type=owner.content_type,
                listowner__owner_object_id=owner.object_id,
            )
        cat = form.cleaned_data.get("category")
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                categories__tree_id=cat.tree_id,
            )

    context = {
        'facets': facets,
        'object_list': qs,
        'form': form,
    }

    kwargs['template_name'] = "curated_lists/featured_curated_lists.html"
    kwargs['queryset'] = qs.distinct()

    extra_context = kwargs.setdefault("extra_context", {})
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(request, **kwargs)


### JSON views ###

@login_required
def user_curated_lists_json(request):
    """
    Returns a list of curated lists created by the currently logged in user or their institutions

    If content_type_id and object_id are passed as query parameters,
    also checks each list if an item with that content_type_id and object_id exists in that list.

    :param request:
    :return: Example: [
        {
            "owner": {"id": 123, "title": "Joe Smith", "type": "person"}
            "lists": [
                {"token": "sdfgbyx", "title": "Best Companies", "item_included": false}, 
                {"token": "nbyasf", "title": "Best Galleries", "item_included": true}]
        },
        {
            "owner": {"id": 124, "title": "Joe & Co", "type": "institution"}
            "lists": [
                {"token": "sdfbsdf", "title": "Geniuses", "item_included": false},
                {"token": "dfbddss", "title": "Best Galleries", "item_included": false}]
        },
        {
            "owner": {"id": 124, "title": "The Smiths", "type": "institution"}
            "lists": [
                {"token": "bjdfsms", "title": "Favorites", "item_included": false}
            ]
        },
    ]
    """
    item_content_type = item_object_id = None
    if request.GET:
        item_content_type = ContentType.objects.get(pk=request.GET.get('content_type_id'))
        item_object_id = request.GET.get('object_id')
    data = []
    data_item = {}
    person = request.user.profile
    data_item['owner'] = {
        'id': person.pk,
        'title': person.get_title(),
        'type': 'people.person',
    }
    curated_lists = CuratedList.objects.filter(
        listowner__owner_content_type=ContentType.objects.get_for_model(person),
        listowner__owner_object_id=person.pk,
    )

    if item_content_type and item_object_id:
        curated_lists = curated_lists.annotate(
            item_included=models.Sum(
                models.Case(
                    models.When(
                        listitem__content_type=item_content_type,
                        listitem__object_id=item_object_id,
                        then=1,
                    ),
                    default=0,
                    output_field=models.IntegerField()
                )
            )
        )
    data_item['lists'] = [{
        'token': curated_list.get_token(),
        'title': curated_list.title,
        'item_included': bool(getattr(curated_list, "item_included", False)),
    } for curated_list in curated_lists]
    data.append(data_item)

    for contact in person.individualcontact_set.exclude(institution=None).only("institution"):
        data_item = {}
        institution = contact.institution
        curated_lists = CuratedList.objects.filter(
            listowner__owner_content_type=ContentType.objects.get_for_model(institution),
            listowner__owner_object_id=institution.pk,
        )
        if item_content_type and item_object_id:
            curated_lists = curated_lists.annotate(
                item_included=models.Sum(
                    models.Case(
                        models.When(
                            listitem__content_type=item_content_type,
                            listitem__object_id=item_object_id,
                            then=1,
                        ),
                        default=0,
                        output_field=models.IntegerField()
                    )
                )
            )
        data_item['owner'] = {
            'id': institution.pk,
            'title': institution.get_title(),
            'type': 'institutions.institution',
        }
        data_item['lists'] = [{
            'token': curated_list.get_token(),
            'title': curated_list.title,
            'item_included': bool(getattr(curated_list, "item_included", False)),
        } for curated_list in curated_lists]
        data.append(data_item)

    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def add_item_to_new_curated_list_json(request):
    if not request.user.is_staff and not request.user.profile.is_curator():
        return access_denied(request)

    if request.method == "POST":
        form = AddItemToNewCuratedListForm(data=request.POST)
        if form.is_valid():
            curated_list = CuratedList()
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(curated_list, 'title_{}'.format(lang_code), form.cleaned_data['title'])
            curated_list.save()

            owner_model = apps.get_model(*form.cleaned_data['owner_app_model'].split('.'))
            try:
                owner_content_object = owner_model.objects.get(pk=form.cleaned_data['owner_pk'])
            except owner_model.DoesNotExist:
                raise Http404
            owner = ListOwner(curated_list=curated_list)
            owner.owner_content_object = owner_content_object
            owner.save()

            item_content_type = ContentType.objects.get(pk=form.cleaned_data['item_content_type_id'])
            item_content_object = item_content_type.get_object_for_this_type(pk=form.cleaned_data['item_object_id'])
            item = ListItem(curated_list=curated_list)
            item.content_object = item_content_object
            item.save()

            data = {
                'success': True,
                'redirect_url': curated_list.get_url_path(),
            }
            return JsonResponse(data)
        data = {
            'success': False,
            'errors': form.errors,
        }
        return JsonResponse(data)
    data = {}
    return JsonResponse(data)


@csrf_exempt
@login_required
def add_item_to_existing_curated_list_json(request):
    if not request.user.is_staff and not request.user.profile.is_curator():
        return access_denied(request)

    if request.method == "POST":
        form = ItemAtCuratedListForm(data=request.POST)
        if form.is_valid():
            curated_list = CuratedList.objects.get_by_token(form.cleaned_data['curated_list_token'])
            if not curated_list:
                raise Http404

            item_content_type = ContentType.objects.get(pk=form.cleaned_data['item_content_type_id'])
            item_content_object = item_content_type.get_object_for_this_type(pk=form.cleaned_data['item_object_id'])
            item = ListItem(curated_list=curated_list)
            item.content_object = item_content_object
            item.save()

            data = {
                'success': True,
                'redirect_url': curated_list.get_url_path(),
            }
            return JsonResponse(data)
        data = {
            'success': False,
            'errors': form.errors,
        }
        return JsonResponse(data)
    data = {}
    return JsonResponse(data)


@csrf_exempt
@login_required
def remove_item_from_curated_list_json(request):
    if not request.user.is_staff and not request.user.profile.is_curator():
        return access_denied(request)

    if request.method == "POST":
        form = ItemAtCuratedListForm(data=request.POST)
        if form.is_valid():
            curated_list = CuratedList.objects.get_by_token(form.cleaned_data['curated_list_token'])
            if not curated_list:
                raise Http404

            ListItem.objects.filter(
                curated_list=curated_list,
                content_type__pk=form.cleaned_data['item_content_type_id'],
                object_id=form.cleaned_data['item_object_id'],
            ).delete()

            data = {
                'success': True,
                'redirect_url': curated_list.get_url_path(),
            }
            return JsonResponse(data)
        data = {
            'success': False,
            'errors': form.errors,
        }
        return JsonResponse(data)
    data = {}
    return JsonResponse(data)


### Editing of curated lists, items, and owners ###

@login_required
def delete_curated_list(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == 'POST':
        form = CuratedListDeletionForm(curated_list=curated_list, data=request.POST)
        if form.is_valid():
            form.delete()
            return redirect('featured_curated_lists')
    else:
        form = CuratedListDeletionForm(curated_list=curated_list)

    return render(request, "curated_lists/delete_curated_list.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def change_curated_list_item(request, token, item_id):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    try:
        item = curated_list.listitem_set.filter(pk=item_id)[0]
    except IndexError:
        raise Http404

    if request.method == 'POST':
        form = CuratedListItemForm(curated_list=curated_list, item=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("curated_list_detail", token=token)
    else:
        form = CuratedListItemForm(curated_list=curated_list, item=item)

    return render(request, "curated_lists/change_curated_list_item.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def remove_curated_list_item(request, token, item_id):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    try:
        item = curated_list.listitem_set.filter(pk=item_id)[0]
    except IndexError:
        raise Http404

    if request.method == 'POST':
        form = CuratedListItemRemovalForm(curated_list=curated_list, item=item, data=request.POST)
        if form.is_valid():
            form.remove()
            return redirect('curated_list_detail', token=token)
    else:
        form = CuratedListItemRemovalForm(curated_list=curated_list, item=item)

    return render(request, "curated_lists/remove_curated_list_item.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def curated_list_owners(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    return render(request, "curated_lists/curated_list_owners.html", {
        'curated_list': curated_list,
    })


@login_required
def invite_curated_list_owner(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == 'POST':
        form = OwnerInvitationForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            try:
                user = User.objects.filter(email=email)[0]
            except IndexError:
                # It's a person who is not yet registered at CCB
                owner = ListOwner(curated_list=curated_list)
                owner.first_name = first_name
                owner.last_name = last_name
                owner.email = email
                owner.save()

                # Send an invitation email with a special link to create user's account.
                current_site = Site.objects.get_current()
                encrypted_email = cryptString(email)

                sender_name, sender_email = settings.MANAGERS[0]
                send_email_using_template(
                    [Recipient(email=email)],
                    "curation_invitation",
                    obj_placeholders={
                        'encrypted_email': encrypted_email,
                        'site_name': current_site.name,
                    },
                    delete_after_sending=False,
                    sender_name=sender_name,
                    sender_email=sender_email,
                    send_immediately=True,
                )
            else:
                # A user with this email exists. Add them to the owners and to the Curators group
                # (but skip the user if he already is the owner of this curated list)
                ct = ContentType.objects.get_for_model(user.profile)
                if not ListOwner.objects.filter(
                    curated_list=curated_list,
                    owner_content_type=ct,
                    object_id=user.profile.pk,
                ).exists():
                    owner = ListOwner(curated_list=curated_list)
                    owner.owner_content_object = user.profile
                    owner.save()
                    group = Group.objects.get(name="Curators")
                    user.groups.add(group)
            return redirect("curated_list_owners", token=token)
    else:
        form = OwnerInvitationForm()

    return render(request, "curated_lists/invite_curated_list_owner.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def invite_person_or_institution_to_curated_list(request, token):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    if request.method == 'POST':
        form = PersonOrInstitutionInvitationForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            institution_title = form.cleaned_data['institution_title']

            if not User.objects.filter(email=email).exists():
                # It's the person who is not yet registered at CCB
                item = ListItem(curated_list=curated_list)
                item.first_name = first_name
                item.last_name = last_name
                item.institution_title = institution_title
                item.email = email
                item.save()

                # Send an invitation email with a special link to create user's account.
                current_site = Site.objects.get_current()
                encrypted_email = cryptString(email)

                sender_name, sender_email = settings.MANAGERS[0]
                send_email_using_template(
                    [Recipient(email=email)],
                    "curated_list_invitation",
                    obj_placeholders={
                        'encrypted_email': encrypted_email,
                        'site_name': current_site.name,
                    },
                    delete_after_sending=False,
                    sender_name=sender_name,
                    sender_email=sender_email,
                    send_immediately=True,
                )
            return redirect("curated_list_detail", token=token)
    else:
        form = PersonOrInstitutionInvitationForm()

    return render(request, "curated_lists/invite_curated_list_owner.html", {
        'curated_list': curated_list,
        'form': form,
    })


@login_required
def remove_curated_list_owner(request, token, owner_id):
    curated_list = CuratedList.objects.get_by_token(token=token)
    if not curated_list:
        raise Http404

    if not curated_list.is_editable(user=request.user):
        return access_denied(request)

    try:
        owner = curated_list.listowner_set.filter(pk=owner_id)[0]
    except IndexError:
        raise Http404

    if request.method == 'POST':
        form = CuratedListOwnerRemovalForm(curated_list=curated_list, owner=owner, data=request.POST)
        if form.is_valid():
            form.remove()
            return redirect('curated_list_owners', token=token)
    else:
        form = CuratedListOwnerRemovalForm(curated_list=curated_list, owner=owner)

    return render(request, "curated_lists/remove_curated_list_owner.html", {
        'curated_list': curated_list,
        'form': form,
    })


@never_cache
def register_curator(request, encrypted_email, *arguments, **keywords):
    """
    The custom registration should do these things:
    - create the user form with the default first_name, last_name, email values,
    - create the user,
    - add the user to the "Curators" group,
    - and assign the user.profile to owner.owner_content_object.
    """
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    try:
        email = decryptString(encrypted_email)
    except Exception as e:
        raise Http404
    owners = ListOwner.objects.filter(email=email)
    if not owners.exists():
        raise Http404
    m = hashlib.md5()
    m.update(request.META['REMOTE_ADDR'])
    request.session.session_id = m.hexdigest()[:20]
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    site_settings = SiteSettings.objects.get_current()
    initial = {
        'first_name': owners[0].first_name,
        'last_name': owners[0].last_name,
        'email': owners[0].email,
    }
    if request.method == "POST":
        data = request.POST.copy()
        data['email'] = owners[0].email
        form = SimpleRegistrationForm(request, data=request.POST, files=request.FILES, initial=initial)
        form.helper.form_action = request.path
        form.fields['email'].widget = forms.EmailInput(attrs={'readonly': True})
        if form.is_valid():
            user = form.save(activate_immediately=True)
            for owner in owners:
                owner.owner_content_object = user.profile
                owner.email = ''
                owner.first_name = ''
                owner.last_name = ''
                owner.save()
                group = Group.objects.get(name="Curators")
                user.groups.add(group)
            redirect_url = "{}?goto_next={}".format(
                reverse("login"),
                reverse("curated_list_detail", kwargs={'token': owners[0].curated_list.get_token()}),
            )
            return redirect(redirect_url)
    else:
        form = SimpleRegistrationForm(request, initial=initial)
        form.helper.form_action = request.path
        form.fields['email'].widget = forms.EmailInput(attrs={'readonly': True})
    request.session.set_test_cookie()
    return render(request, 'curated_lists/accept_invitation.html', {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'site_name': Site.objects.get_current().name,
        'login_by_email': site_settings.login_by_email,
    })


def register_person_or_institution(request, encrypted_email, *arguments, **keywords):
    """
    The custom registration should do these things:
    - create the user form with the default first_name, last_name, email, institution title values,
    - create the user,
    - optionally create the institution
    - and assign the institution or user.profile to item.content_object.
    """
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    try:
        email = decryptString(encrypted_email)
    except Exception as e:
        raise Http404
    items = ListItem.objects.filter(email=email)
    if not items.exists():
        raise Http404
    m = hashlib.md5()
    m.update(request.META['REMOTE_ADDR'])
    request.session.session_id = m.hexdigest()[:20]
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    site_settings = SiteSettings.objects.get_current()
    initial = {
        'first_name': items[0].first_name,
        'last_name': items[0].last_name,
        'email': items[0].email,
        'institution_title': items[0].institution_title,
    }
    if request.method == "POST":
        data = request.POST.copy()
        data['email'] = items[0].email
        form = PersonAndInstitutionRegistrationForm(request, data=request.POST, files=request.FILES, initial=initial)
        form.helper.form_action = request.path
        form.fields['email'].widget = forms.EmailInput(attrs={'readonly': True})
        if form.is_valid():
            user = form.save(activate_immediately=True)
            institution = form.institution
            for item in items:
                if institution:
                    item.content_object = institution
                else:
                    item.content_object = user.profile
                item.email = ''
                item.first_name = ''
                item.last_name = ''
                item.institution_title = ''
                item.save()
            return redirect('curated_list_detail', token=items[0].curated_list.get_token())
    else:
        form = PersonAndInstitutionRegistrationForm(request, initial=initial)
        form.helper.form_action = request.path
        form.fields['email'].widget = forms.EmailInput(attrs={'readonly': True})
    request.session.set_test_cookie()
    return render(request, 'curated_lists/accept_invitation.html', {
        'form': form,
        settings.REDIRECT_FIELD_NAME: redirect_to,
        'site_name': Site.objects.get_current().name,
        'login_by_email': site_settings.login_by_email,
    })
