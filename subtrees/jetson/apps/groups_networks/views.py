# -*- coding: UTF-8 -*-
import datetime
import json

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import get_object_or_404

from base_libs.utils.misc import ExtendedJSONEncoder, get_related_queryset
from base_libs.utils.crypt import decryptString
from base_libs.views import access_denied

from jetson.apps.utils.decorators import login_required
from jetson.apps.groups_networks.forms import EditMemberForm, GroupMembershipForm, ADD_GROUP_FORM_STEPS, INVITATION_FORM_STEPS

from jetson.apps.utils.views import object_list, show_form_step, get_abc_list, filter_abc
from jetson.apps.mailing.views import do_generic_mail, send_email_using_template, Recipient
from jetson.apps.memos.models import Memo, MEMO_TOKEN_NAME

Person = models.get_model("people", "Person")
Institution = models.get_model("institutions", "Institution")

app = models.get_app("groups_networks")
PersonGroup, GroupMembership, URL_ID_PERSONGROUP, URL_ID_PERSONGROUPS = (
    app.PersonGroup, app.GroupMembership,
    app.URL_ID_PERSONGROUP, app.URL_ID_PERSONGROUPS
    )

def json_manage_ss_membership(request, slug):
    """Sets the object as a favorite for the current user"""
    json_str = "false"
    person_group = None
    try:
        institution = Institution.objects.get(slug=slug)
        person_group, is_created = PersonGroup.objects.get_or_create(
            place = institution,
            defaults = {
                'title': institution.title,
                'slug': institution.slug,
                }
            )
    except:
        pass
    # TODO: what to do if the person_group has just been created and has no owner set?
    if request.user.is_authenticated() and person_group:
        """
        RS15112007 added
        groupmembership.is_accepted is set to true, if a user wants to join the group. 
        we use this to be able to distinguish between invited users and
        users, whose membership must be confirmed.
        """
        relation, is_created = GroupMembership.objects.get_or_create(
            user=request.user,
            person_group=person_group,
            is_accepted=True,
            )
        if not is_created:
            relation.delete()
        result = relation.__dict__
        result = dict([(item[0], unicode(item[1])) for item in result.items() if not item[0].startswith("_")])
        result['action'] = is_created and "added" or "removed"
        json_str = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')
json_manage_ss_membership = never_cache(json_manage_ss_membership)

def manage_group_membership(request, action="edit", slug=None, username=""):
    """
    Shows the content of POPUP window and manipulates forms in POPUPS
    returns 
    1. HTML with a form to show
    2. Empty string for closing popup
    3. "reload" for reloading the page
    """
    # edit | request | cancel | remove | accept-group | deny-group
    # accept-user | deny-user | invite-user | remove-user
    
    if username:
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404()
    else:
        user = request.user
        
    try:
        group = PersonGroup.objects.get(
            slug=slug,
            )
    except:
        raise Http404()

    # check privileges
    if not user.is_authenticated():
        return access_denied(request)
    
    if (
        action=="edit" and not group.is_membership_editable()
        or action=="request" and not group.is_membership_requestable()
        or action=="cancel" and not group.is_member_request_cancelable()
        or action=="remove" and not group.is_membership_removable()
        or action=="invite" and not group.is_member_invitable()
        or action=="accept-%s" % URL_ID_PERSONGROUP and not group.is_member_invitation_acceptable()
        or action=="deny-%s" % URL_ID_PERSONGROUP and not group.is_member_invitation_denyable()
        or action=="cancel-user" and not group.is_member_invitation_cancelable(user)
        or action=="accept-user" and not group.is_member_request_acceptable(user)
        or action=="deny-user" and not group.is_member_request_denyable(user)
        or action=="remove-user" and not group.is_member_removable(user)
        ):
        return access_denied(request)

    if request.method == 'POST':
        data = request.POST.copy()
        form = GroupMembershipForm(
            relation_action=action,
            user=user,
            group=group,
            data=data,
            files=request.FILES,
            )
        if form.is_valid():
            form.save()
            return HttpResponse("reload")
    else:
        form = GroupMembershipForm(
            relation_action=action,
            user=user,
            group=group,
            )

    return render_to_response(
        "groups_networks/group_membership_%s.html" % action,
        {
            'form' : form,
            'person' : user.profile,
            'group' : group,
            },
        RequestContext(request),
        )
manage_group_membership = never_cache(manage_group_membership)

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
    obj = Institution.objects.get(slug=slug)
    inviter = None
    try:
        inviter = obj.get_groups()[0].get_owners()[0].profile.get_title()
    except:
        pass
    if not user:
        return HttpResponseRedirect('/register/')
    if request.method=="POST":
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
            person.status = "published"
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
            
            if "jetson.apps.individual_relations" in settings.INSTALLED_APPS:
                from jetson.apps.individual_relations.models import IndividualRelation
                if cleaned['accept_inviter']:
                    owner = user.groupmembership_set.get(
                        ).person_group.get_owners()[0]
                    IndividualRelation.objects.accept(user, owner)
                
            if cleaned['accept_membership']:
                membership = user.groupmembership_set.get()
                membership.is_accepted = True
                membership.title_en = person.occupation
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
    t = loader.get_template("groups_networks/confirm_invitation_to_institution.html")
    c = RequestContext(request, {
        'form': f,
        'object': obj,
        'inviter': inviter,
    })
    return HttpResponse(t.render(c))
confirm_invitation = never_cache(confirm_invitation)

# the decorator checking the privileges of a specific institutional group of people
def check_persongroup_privilege(function, required_permission):
    def new_function(request, slug, **kwargs):
        if request.user.is_authenticated():
            from jetson.apps.groups_networks.models import PersonGroup
            try:
                institution = Institution.objects.get(slug=slug)
                person_group = PersonGroup.objects.get(place=institution)
            except:
                raise Http404, "You entered an invalid institution slug name"
    
            if request.user.has_perm("groups_networks.%s" % required_permission, object=person_group):
                return function(request, slug, **kwargs)
            
        raise Http404, "You are not allowed to perform the requested operation"

    return new_function

@never_cache
def persongroup_list(request, criterion="", slug="", show="", **kwargs):
    
    abc_list = None
    abc_filter = request.GET.get('by-abc', None)
    
    if show=="favorites":
        if not request.user.is_authenticated():
            return access_denied(request)
        ContextItem = models.get_model("site_specific", "ContextItem")
        
        tables = ["favorites_favorite"]
        condition = ["favorites_favorite.user_id = %d" % request.user.id,
                     "favorites_favorite.object_id = system_contextitem.id"]
        ct = ContentType.objects.get_for_model(kwargs['queryset'].model)
        fav_inst_ids = [
            el['object_id'] for el in ContextItem.objects.filter(
                content_type=ct
            ).extra(
                tables=tables,
                where=condition,
            ).distinct().values("object_id")
            ]
        kwargs['queryset'] = kwargs['queryset'].filter(pk__in=fav_inst_ids)
    elif show=="memos":
        ct = ContentType.objects.get_for_model(kwargs['queryset'].model)
        memos_ids = map(int, Memo.objects.filter(
            collection__token=request.COOKIES.get(MEMO_TOKEN_NAME, None),
            content_type=ct,
        ).values_list("object_id", flat=True))
        kwargs['queryset'] = kwargs['queryset'].filter(
            pk__in=memos_ids,
        )
    elif show=="own-%s" % URL_ID_PERSONGROUPS:
        if not request.user.is_authenticated():
            return access_denied(request)
        kwargs['queryset'] = kwargs['queryset'].filter(
            groupmembership__user=request.user,
            ).exclude(
                groupmembership__activation__isnull=True,
                )
    elif show=="requested":
        if not request.user.is_authenticated():
            return access_denied(request)
        kwargs['queryset'] = kwargs['queryset'].filter(
            groupmembership__user=request.user,
            groupmembership__is_accepted=True,
            groupmembership__confirmer__isnull=True,
            groupmembership__activation__isnull=True,
            ).distinct()
    elif show=="invitations":
        if not request.user.is_authenticated():
            return access_denied(request)
        kwargs['queryset'] = kwargs['queryset'].filter(
            groupmembership__user=request.user,
            groupmembership__is_accepted=False,
            groupmembership__activation__isnull=True,
            ).exclude(
                groupmembership__inviter__isnull=True,
                ).distinct()
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(status="published")
        
    "Displays the list of accounts"
    persongroup_filters = {}
    for var in ("type", "commerciality", "location-type", "actuality", "neighborhood"):
        if var in request.GET:
            persongroup_filters[var] = request.GET[var]
    if not persongroup_filters:
        persongroup_filters = request.httpstate.get('persongroup_filters', {})
        
    if slug=="all":
        try:
            del(persongroup_filters[criterion])
        except:
            pass
    else:
        if persongroup_filters.get('criterion', '') != slug:
            persongroup_filters[criterion] = slug
    request.httpstate['persongroup_filters'] = persongroup_filters
    
    if len(persongroup_filters) == 0 and criterion:
        return HttpResponseRedirect('/%s/' % URL_ID_PERSONGROUPS)
    elif len(persongroup_filters) == 1 and criterion != persongroup_filters.keys()[0]:
        for k, v in persongroup_filters.items():
            page = 'page' in request.GET and "?page=%s" % request.GET.get('page', "") or ""
            return HttpResponseRedirect('/%s/by-%s/%s/%s' % (URL_ID_PERSONGROUPS, k, v, page))
    elif not len(request.GET) and len(persongroup_filters) > 1:
        query_vars = "?" + "&".join(["%s=%s" % (k, v) for k, v in persongroup_filters.items()])
        page = 'page' in request.GET and "?page=%s" % request.GET.get("page", "") or ""
        return HttpResponseRedirect('/%s/%s%s' % (URL_ID_PERSONGROUPS, page, query_vars))
    else:
        queryset = kwargs['queryset']
        for k, v in persongroup_filters.items():
            if k=="type":
                pass
            elif k=="commerciality":
                queryset = queryset.filter(is_non_profit = True)
            elif k=="location-type" and request.user.is_authenticated():
                q = None
                for n in request.user.get_persongroup().get_neighborhoods():
                    if not q:
                        q = models.Q(neighborhoods__icontains=n)
                    else:
                        q |= models.Q(neighborhoods__icontains=n)
                if q:
                    queryset = queryset.filter(q)
            elif k=="actuality":
                if v=="activity":
                    queryset = queryset.order_by("-last_activity_timestamp")
                elif v=="rating":
                    queryset = queryset.order_by("rating")
                elif v=="new":
                    queryset = queryset.order_by("-creation_date")
                elif v=="my-contacts":
                    persongroup_ids = [p.id for p in PersonGroup.objects.filter(user__to_user__user=request.user).distinct()]
                    persongroup_ctype = ContentType.objects.get_for_model(PersonGroup)
                    institution_ids = [i.id for i in Institution.objects.filter(persongroup__groupmembership__user=request.user).distinct()]
                    institution_ctype = ContentType.objects.get_for_model(Institution)
                    queryset = queryset.filter(models.Q(object_id__in=persongroup_ids) & models.Q(content_type=persongroup_ctype) | models.Q(object_id__in=institution_ids) & models.Q(content_type=institution_ctype))
            
        abc_list = get_abc_list(queryset, "title", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "title", abc_filter)

        extra_context = {'abc_list': abc_list, 'show': ("", "/%s" % show)[bool(show)],
                         'source_list': URL_ID_PERSONGROUPS}
        kwargs['extra_context'] = extra_context
        kwargs['httpstate_prefix'] = URL_ID_PERSONGROUPS  
        kwargs['queryset'] = queryset  
        return object_list(request, **kwargs)

def persongroup_invitation_list(request, group_ind="", show="", **kwargs):
    extra_context = {}
    abc_list = None
    abc_filter = request.GET.get('by-abc', None)
    status_filter = request.GET.get('by-status', None)
    if status_filter:
        extra_context['active_status_filter'] = status_filter
    # just "invitations" makes a redirection to default (my-groups)
    if group_ind=="" and show=="":
        if not status_filter:
            status_filter = "pending"
        return HttpResponseRedirect('/%s/invitations/my-groups/?by-status=%s' % (URL_ID_PERSONGROUPS, status_filter))
    elif group_ind=="my-%s" % URL_ID_PERSONGROUPS and show=="":
        if not status_filter:
            status_filter = "pending"
        return HttpResponseRedirect('/%s/invitations/my-groups/invitations/?by-status=%s' % (URL_ID_PERSONGROUPS, status_filter))
    elif group_ind=="other-%s" % URL_ID_PERSONGROUPS and show=="":
        if not status_filter:
            status_filter = "pending"
        return HttpResponseRedirect('/%s/invitations/other-%s/invitations/?by-status=%s' % (URL_ID_PERSONGROUPS, URL_ID_PERSONGROUPS, status_filter))
    
    # ok, redirection is finished, so we can get data ...
    if show=="invitations":
        extra_context['active_link'] = 'invitations'
        # those filters are not yet implemented because we do not have any "denied" at the moment
        if status_filter == "pending":
            filter_by = "NOT_YET_IMPLEMENTED"
        elif status_filter == "denied":
            filter_by = "NOT_YET_IMPLEMENTED"
        else:
            filter_by = None
    elif show=="requests":
        extra_context['active_link'] = 'requests'
        # those filters are not yet implemented because we do not have any "denied" at the moment
        if status_filter == "pending":
            filter_by = "NOT_YET_IMPLEMENTED"
        elif status_filter == "denied":
            filter_by = "NOT_YET_IMPLEMENTED"
        else:
            filter_by = None       
    else:
        raise Http404, "show must be one of 'invitations', 'requests'"
    
    # ok, now for the groups ...
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # TODO apply pending and denied filters
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if group_ind=="my-%s" % URL_ID_PERSONGROUPS:
        if show=="invitations":
            queryset = request.user.profile.get_my_groups_invitations()
        else:
            queryset = request.user.profile.get_my_groups_requests()
        abc_list = get_abc_list(queryset, "user__last_name", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "user__last_name", abc_filter)
    elif group_ind=="other-%s" % URL_ID_PERSONGROUPS:
        if show=="invitations":
            queryset = request.user.profile.get_other_groups_invitations()
        else:
            queryset = request.user.profile.get_other_groups_requests()
        abc_list = get_abc_list(queryset, "title", abc_filter)
        if abc_filter:
            queryset = filter_abc(queryset, "title", abc_filter)
    elif group_ind=="invite-to-%s" % URL_ID_PERSONGROUP:
        raise Http404, "Not implemented"        
    else:
        raise Http404, "group_ind parameter must be 'my-%s' or 'invite-to-%s" % (URL_ID_PERSONGROUPS, URL_ID_PERSONGROUP)
        
    extra_context['abc_list'] = abc_list
    # Ruper20032008 that show stuff gives anb error in the produced pagination url ...
    #extra_context["show"] = ("", "/%s" % show)[bool(show)]
    extra_context['source_list'] = URL_ID_PERSONGROUPS
    extra_context['group_ind'] = group_ind          
    kwargs['extra_context'] = extra_context  
    kwargs['queryset'] = queryset  
    return object_list(request, **kwargs)    

persongroup_invitation_list = login_required(never_cache(persongroup_invitation_list))  

@never_cache
def view_persongroup_members(request, slug, section="members", **kwargs):
    group = PersonGroup.objects.get(slug=slug)
    #check privileges
    #if not request.user.has_perm("groups_networks.can_see_members", persongroup):
    if not group.is_forum_shown():
        return access_denied(request)
    
    kwargs['template_name'] = "groups_networks/persongroups/group_members.html"
    kwargs['extra_context'] = {
        "object": group
        }
    if section == "moderators":
        kwargs['queryset'] = group.get_moderators()
    elif section == "admins":
        kwargs['queryset'] = group.get_owners()
    elif section == "unconfirmed":
        kwargs['queryset'] = group.get_unconfirmed()
    elif section == "invited":
        kwargs['queryset'] = group.get_invited()
    else: # members
        kwargs['queryset'] = group.get_all_members()
    return object_list(request, **kwargs)

@never_cache
def invite_persongroup_members(request, slug, **kwargs):
    group = PersonGroup.objects.get(slug=slug)
    def save_invitations(recipients_list):
        for recipient in recipients_list:
            try:
                membership = group.groupmembership_set.get(user=user)
            except:
                membership = group.groupmembership_set.create(
                    inviter=request.user,
                    user=recipient.user,
                    )
            membership.save()
            
            pass # do some saving
    #check privileges
    if not group.are_members_invitable(request.user):
        return access_denied(request)
    recipients_list = [
        Recipient(id=rel.to_user.id, user=rel.to_user)
        for rel in request.user.profile.get_individual_relations().filter(
            status="confirmed",
            )
        if group.is_member_invitable(rel.to_user)
        ]
    if recipients_list:
        return do_generic_mail(
            request,
            template_name='groups_networks/persongroups/invite_group_members.html',
            redirect_to=None,
            success_template=None,
            extra_context=None,
            recipients_list=recipients_list, # list of Recipient instances
            display_recipients_list=True,
            display_recipients_input=False,
            display_en=group.preferred_language.iso2_code=="en",
            display_de=group.preferred_language.iso2_code=="de",
            email_template_slug="invite_to_group",
            obj=group,
            obj_placeholders=None,
            delete_after_sending=False,
            reply_to=None,
            forward=None,
            draft=None,
            is_html=False,
            onbeforesend=save_invitations,
            onsend=None,
            onaftersend=None,
            )
    else:
        kwargs['template_name'] = 'groups_networks/persongroups/invite_group_members.html'
        kwargs['extra_context'] = {
            "object": group,
            "no_contacts_to_invite": True,
            }
        kwargs['queryset'] = group.get_all_members()
        return object_list(request, **kwargs)

def invite_institution_members(request, slug, **kwargs):
    institution = get_object_or_404(Institution, slug=slug)
    group = get_object_or_404(PersonGroup,
        object_id=institution.id,
        content_type=ContentType.objects.get_for_model(institution),
    )
    #check privileges
    if not group.are_members_invitable(request.user):
        return access_denied(request)
    form_steps = INVITATION_FORM_STEPS.copy()
    form_steps['name'] = "_".join((
        form_steps['name'],
        institution.slug,
        ))
    form_steps['institution'] = institution
    form_steps['user'] = request.user
    return show_form_step(
        request,
        form_steps,
        extra_context={
            'object': institution,
            'user': request.user,
            })


invite_institution_members = login_required(never_cache(invite_institution_members))

@never_cache
def edit_group_member(request, slug, user_id):
    """
    Shows the content of POPUP window and manipulates forms in POPUPS
    returns 
    1. HTML with a form to show
    2. Empty string for closing popup
    3. "reload" for reloading the page
    """
    try:
        person_group = PersonGroup.objects.get(slug=slug)
        user = User.objects.get(id=user_id)
        group_membership = GroupMembership.objects.get(user=user, person_group=person_group)
    except:
        raise Http404()

    #check privileges
    if not request.user.has_perm("groups_networks.can_see_members", person_group):
        return access_denied(request)

    if not request.user.has_perm("groups_networks.can_change_members", person_group):
        return access_denied(request)

    if request.method == 'POST':
        data = request.POST.copy()
        data.update(request.FILES)
        form = EditMemberForm(data)
        
        if form.is_valid():
            # do character encoding
            cleaned = form.cleaned_data
            #for key, value in cleaned.items():
            #    if type(value).__name__ == "unicode":
            #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)

            role = cleaned["role"]
            group_membership.role = role
            group_membership.save()
            return HttpResponse("reload")
    else:
       form = EditMemberForm(data = {'role': group_membership.role})

    return render_to_response(
        "groups_networks/persongroups/popups/edit_member.html",
        {
            'user': user,
            'person_group': person_group,
            'form' : form,
            },
        RequestContext(request),
        )

@never_cache
@transaction.atomic
@login_required
def add_group(request):
    return show_form_step(request, ADD_GROUP_FORM_STEPS, extra_context={})
