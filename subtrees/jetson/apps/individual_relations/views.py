# -*- coding: UTF-8 -*-
import datetime
import json

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.conf import settings

from base_libs.utils.misc import ExtendedJSONEncoder, get_related_queryset
from base_libs.utils.crypt import decryptString
from base_libs.utils.misc import get_installed
from base_libs.views import access_denied

from jetson.apps.individual_relations.forms import IndividualRelationForm, InvitationConfirmation
from jetson.apps.individual_relations.models import IndividualRelation

Person = models.get_model("people", "Person")
Recipient = get_installed("mailing.recipient.Recipient")
send_email_using_template = get_installed("mailing.views.send_email_using_template")


def json_manage_individual_relation(request, username):
    """Sets the object as a favorite for the current user"""
    json_str = "false"
    try:
        to_user = User.objects.get(username=username)
    except:
        to_user = None
    if request.user.is_authenticated() and to_user:
        relation, is_created = IndividualRelation.objects.get_or_create(
            user=request.user,
            to_user=to_user,
        )
        if not is_created:
            relation.delete()
        result = relation.__dict__
        result = dict(
            [
                (item[0], unicode(item[1]))
                for item in result.items() if not item[0].startswith("_")
            ]
        )
        # ("waiting", "to_confirm", "active", "removed")
        result['status'] = is_created and "added" or "removed"
        json_str = json.dumps(
            result, ensure_ascii=False, cls=ExtendedJSONEncoder
        )
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')


json_manage_individual_relation = never_cache(json_manage_individual_relation)


def manage_individual_relationship(request, action="edit", username=None):
    """
    Shows the content of POPUP window and manipulates forms in POPUPS
    returns 
    1. HTML with a form to show
    2. Empty string for closing popup
    3. "reload" for reloading the page
    """
    # edit | invite | accept | deny | cancel | block | unblock | remove

    user_1 = request.user
    try:
        user_2 = User.objects.get(username=username, )
    except:
        raise Http404()

    # check privileges
    if not user_1.is_authenticated():
        return access_denied(request)

    #if not user_1.has_perm(
    #    "groups_networks.can_add_individualrelation",
    #    ):
    #    return access_denied(request)

    #if not user_1.has_perm(
    #    "groups_networks.can_change_individualrelation",
    #    ):
    #    return access_denied(request)

    person = user_2.profile
    if (
        action == "edit" and not person.is_contact_editable() or
        action == "invite" and not person.is_contact_addable() or
        action == "accept" and not person.is_contact_acceptable() or
        action == "deny" and not person.is_contact_denyable() or
        action == "block" and not person.is_contact_blockable() or
        action == "unblock" and not person.is_contact_unblockable() or
        action == "cancel" and not person.is_contact_cancelable() or
        action == "remove" and not person.is_contact_removable()
    ):
        return access_denied(request)

    if request.method == 'POST':
        data = request.POST.copy()
        form = IndividualRelationForm(
            relation_action=action,
            user_1=user_1,
            user_2=user_2,
            data=data,
            files=request.FILES,
        )
        if form.is_valid():
            form.save()
            return HttpResponse("reload")
    else:
        form = IndividualRelationForm(
            relation_action=action,
            user_1=user_1,
            user_2=user_2,
        )

    return render_to_response(
        "individual_relations/individual_relation_%s.html" % action,
        {
            'form': form,
            'user': user_2,
        },
        RequestContext(request),
    )


manage_individual_relationship = never_cache(manage_individual_relationship)


def confirm_invitation(request, slug, encrypted_email):
    """Displays the registration completion form and handles the registration action
    slug - institution slug
    encrypted_email - the email of the invited user
    """
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    email = decryptString(encrypted_email)
    user = authenticate(email=email)
    if not user:
        raise Http404()
    person = user.profile
    obj = Person.objects.get(user__username=slug)
    inviter = obj
    if not user:
        return HttpResponseRedirect('/register/')
    if request.method == "POST":
        if "deny_invitation" in request.POST:
            user.delete()
            return HttpResponseRedirect("/")
        d = {
            'login_email': user.email,
            'username': user.username,
        }
        f = InvitationConfirmation(request.POST, initial=d)
        if f.is_valid():
            cleaned = f.cleaned_data
            user.is_active = True
            user.email = cleaned['login_email']
            user.first_name = cleaned['first_name']
            user.last_name = cleaned['last_name']
            user.username = cleaned['username']
            user.set_password(cleaned['password'])
            user.save()
            person.status = get_related_queryset(
                Person,
                "status",
            ).get(sysname="published")
            person.prefix_id = cleaned['prefix']
            person.occupation = cleaned['occupation']
            person.birthday_yyyy = cleaned['birthday_yyyy']
            person.birthday_mm = cleaned['birthday_mm']
            person.birthday_dd = cleaned['birthday_dd']
            person.save()
            contact = person.get_contacts()[0]
            contact.phone0_country = cleaned['phone_country']
            contact.phone0_area = cleaned['phone_area']
            contact.phone0_number = cleaned['phone_number']
            contact.phone1_country = cleaned['fax_country']
            contact.phone1_area = cleaned['fax_area']
            contact.phone1_number = cleaned['fax_number']
            contact.phone2_country = cleaned['mobile_country']
            contact.phone2_area = cleaned['mobile_area']
            contact.phone2_number = cleaned['mobile_number']
            contact.save()

            from django.contrib.auth import login
            login(request, user)

            if cleaned['accept_inviter']:
                owner = user.groupmembership_set.get().person_group.get_owners(
                )[0]
                IndividualRelation.objects.accept(user, owner)

            if cleaned['accept_membership']:
                membership = user.groupmembership_set.get()
                membership.is_accepted = True
                membership.title = person.occupation
                membership.title_de = person.occupation
                membership.save()
            else:
                membership = user.groupmembership_set.delete()

            current_site = Site.objects.get_current()
            sender_name = ''
            sender_email = settings.DEFAULT_FROM_EMAIL
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
            return HttpResponseRedirect('/register/alldone/')
    else:
        d = {
            'prefix': person.prefix_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'individual_type': person.individual_type_id,
            'login_email': user.email,
            'login_email_confirm': user.email,
            'username': user.username,
            'occupation': person.occupation,
            'accept_inviter': True,
            'accept_membership': True,
        }
        contact = person.get_primary_contact()
        if contact.get("phone_number", False):
            d["phone_country"] = contact.get("phone_country", "")
            d["phone_area"] = contact.get("phone_area", "")
            d["phone_number"] = contact.get("phone_number", "")
        if contact.get("fax_number", False):
            d["fax_country"] = contact.get("fax_country", "")
            d["fax_area"] = contact.get("fax_area", "")
            d["fax_number"] = contact.get("fax_number", "")
        if contact.get("mobile_number", False):
            d["mobile_country"] = contact.get("mobile_country", "")
            d["mobile_area"] = contact.get("mobile_area", "")
            d["mobile_number"] = contact.get("mobile_number", "")

        f = InvitationConfirmation(initial=d)
    t = loader.get_template(
        "individual_relations/confirm_invitation_to_contacts.html"
    )
    c = RequestContext(
        request, {
            'form': f,
            'object': obj,
            'inviter': inviter,
        }
    )
    return HttpResponse(t.render(c))


confirm_invitation = never_cache(confirm_invitation)
