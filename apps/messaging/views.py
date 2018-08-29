# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db import models
from django.core.urlresolvers import reverse

from base_libs.utils.misc import ExtendedJSONEncoder

from jetson.apps.messaging.models import InternalMessage
from jetson.apps.messaging.forms import InternalMessageForm
from jetson.apps.messaging.forms import ContactForm
from jetson.apps.mailing.views import do_generic_mail, Recipient
from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list
from jetson.apps.utils.views import object_detail

Person = models.get_model("people", "Person")

def json_change_message(request):
    """changes or deletes a message given by primary key"""
    result = {}
    
    data = {
        'action': '',
        'idlist': '',
    }
    data.update(dict([(item[0], item[1]) for item in request.GET.items()]))
    action = data['action']
    
    idlist = data['idlist'].split()
    for pk in idlist:
        try:
            message = InternalMessage.objects.get(pk=pk)
        except:
            result['error'] = _("message cannot be found")
            message = None

        if message is not None and request.user.is_authenticated():
            # simple security check!
            if request.user == message.sender or request.user == message.recipient:
                if action == "delete_forever":
                    message.delete()
                if action == "delete":
                    message.is_deleted = True
                    message.save()
                if action == "restore":
                    message.is_deleted = False
                    message.save()
                elif action == "is_read":
                    message.is_read = True
                    message.save()
                elif action == "is_unread":
                    message.is_read = False
                    message.save()
                elif action == "is_spam":
                    message.is_spam = True
                    message.save()
                elif action == "is_nospam":
                    message.is_spam = False
                    message.save()
            else:
                result['error'] = _("You are not allowed to perform this operation")
            
    # currently, no data is returned, a page reload should be performed....  
    json_str = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')

json_change_message = never_cache(json_change_message)


def messages_list(request, box=None, **kwargs):
    """Displays the list of personal messages in inbox, sent messages, drafts, deleted maeeages, etc."""
    person = get_object_or_404(Person, user=request.user)
    if box is None:
        return HttpResponseRedirect(reverse("messages_list") + "inbox/")
        
    if box == "inbox":
        queryset = InternalMessage.objects.filter(
            recipient=request.user,
            is_draft=False,
            ).exclude(
                is_deleted=True,
                ).order_by("-creation_date")
    elif box == "sent":
        queryset = InternalMessage.objects.filter(
            sender=request.user,
            is_draft=False,
            ).exclude(
                is_deleted=True,
                ).order_by("-creation_date")
    elif box == "drafts":
        queryset = InternalMessage.objects.filter(
            sender=request.user,
            is_draft=True,
            ).exclude(
                is_deleted=True,
                ).order_by("-creation_date")
    elif box == "deleted":
        queryset = InternalMessage.objects.filter(
            models.Q(is_deleted=True) &
            (models.Q(sender=request.user) | models.Q(recipient=request.user))
            ).order_by("-creation_date")
    else:
        raise Http404
    
    kwargs['extra_context'] = {'object': person, 'box' : box}
    kwargs['queryset'] = queryset
    kwargs['template_name'] = "messaging/messages_list.html"
    kwargs['paginate_by'] = 10
    kwargs['allow_empty'] = True
    request.httpstate['last_url'] = request.get_full_path()
    return object_list(request, **kwargs)
messages_list = login_required(messages_list)

def view_message(request, pk):
    person = get_object_or_404(Person, user=request.user)
    message = get_object_or_404(InternalMessage, pk=pk)
    
    # check, if I am privileged to display the message 
    # TODO: this may be done in another way...
    if not (message.sender == request.user or message.recipient == request.user):
        raise Http404
        
    t = loader.get_template("messaging/view_message.html")
    c = RequestContext(request, {
        'object': person,
        'message': message,
        'last_url': request.httpstate.get("last_url", reverse("messages_list")),
    })
    # mark mesage as read
    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        message.save()
    return HttpResponse(t.render(c))
view_message = login_required(view_message)

def reply_message(request, pk, **kwargs):
    message = get_object_or_404(InternalMessage, pk=pk)
    if not (message.recipient == request.user):
        raise Http404
        
    if request.method == 'POST':
        form = InternalMessageForm(request.user, None, request.POST)
        
        if form.is_valid():
            if request.POST.has_key("send"):
                form.send()
                message.is_replied = True
                message.save()
                return HttpResponseRedirect(reverse("messages_list") + "sent/")
            elif request.POST.has_key("save_as_draft"):
                form.save_as_draft()
                return HttpResponseRedirect(reverse("messages_list") + "drafts/")
            return HttpResponseRedirect(reverse("messages_list") + "inbox/")
    else:
        form = InternalMessageForm(request.user, None)
        form.fields['recipients_email_list'].choices = (
            (message.sender.pk, message.sender.profile.get_title()),
            )
        form.fields['recipients_email_list'].initial = [message.sender.pk]
    
    context = {
        'object' : request.user.profile,
        'form': form,
    }
    return render_to_response(
        'messaging/new_message.html',
        context, 
        context_instance=RequestContext(request)
    )
    
reply_message = login_required(never_cache(reply_message))

def forward_message(request, pk, **kwargs):
    message = get_object_or_404(InternalMessage, pk=pk)
    
    if not (message.recipient == request.user
        or message.sender == request.user):
        raise Http404
        
    if request.method == 'POST':
        form = InternalMessageForm(request.user, None, request.POST)
        
        if form.is_valid():
            if request.POST.has_key("send"):
                form.send()
                return HttpResponseRedirect(reverse("messages_list") + "sent/")
            elif request.POST.has_key("save_as_draft"):
                form.save_as_draft()
                return HttpResponseRedirect(reverse("messages_list") + "drafts/")
            return HttpResponseRedirect(reverse("messages_list") + "inbox/")
    else:
        form = InternalMessageForm(request.user, None, initial=message.__dict__)
    
    context = {
        'object' : request.user.profile,
        'form': form,
    }
    return render_to_response(
        'messaging/new_message.html',
        context, 
        context_instance=RequestContext(request)
    )
    
forward_message = login_required(never_cache(forward_message))

def send_draft_message(request, pk, **kwargs):
    message = get_object_or_404(InternalMessage, pk=pk)
    if not (message.sender == request.user):
        raise Http404
        
    if request.method == 'POST':
        form = InternalMessageForm(request.user, message, request.POST)
        
        if form.is_valid():
            if request.POST.has_key("send"):
                form.send()
                return HttpResponseRedirect(reverse("messages_list") + "sent/")
            elif request.POST.has_key("save_as_draft"):
                form.save_as_draft()
                return HttpResponseRedirect(reverse("messages_list") + "drafts/")
            return HttpResponseRedirect(reverse("messages_list") + "inbox/")
    else:
        form = InternalMessageForm(request.user, message)
    
    context = {
        'object' : request.user.profile,
        'form': form,
    }
    return render_to_response(
        'messaging/new_message.html',
        context, 
        context_instance=RequestContext(request)
    )
send_draft_message = login_required(never_cache(send_draft_message))

def new_message(request, **kwargs):
    if request.method == 'POST':
        form = InternalMessageForm(request.user, None, request.POST)
        
        if form.is_valid():
            if request.POST.has_key("send"):
                form.send()
                return HttpResponseRedirect(reverse("messages_list") + "sent/")
            elif request.POST.has_key("save_as_draft"):
                form.save_as_draft()
                return HttpResponseRedirect(reverse("messages_list") + "drafts/")
            return HttpResponseRedirect(reverse("messages_list") + "inbox/")
    else:
        form = InternalMessageForm(request.user, None)
    
    context = {
        'object' : request.user.profile,
        'form': form,
    }
    return render_to_response(
        'messaging/new_message.html',
        context, 
        context_instance=RequestContext(request)
    )  
    
new_message = login_required(never_cache(new_message))

def delete_message(request, pk, **kwargs):
    redirect_to = request.httpstate.get("last_url", reverse("messages_list"))
    person = get_object_or_404(Person, user=request.user)
    
    # first get the message from the slug
    message = get_object_or_404(InternalMessage, pk=pk)
    
    if not (message.sender == request.user or message.recipient == request.user):
        raise Http404
    
    if request.method == 'POST':
        # cancel the whole action
        if request.POST.has_key('cancel'):
            return HttpResponseRedirect(redirect_to)
        
        elif request.POST.has_key('delete'):
            message.delete()
            return HttpResponseRedirect(redirect_to)
         
    context = {
        'message' : message,
        'object' : person, 
        'last_url': redirect_to,
    }
    return render_to_response(
        'messaging/delete_message.html',
        context, 
        context_instance=RequestContext(request)
    )  
delete_message = login_required(delete_message)

def contact(request, **kwargs):
    """
    Displays and manages a contact form for an object
    """
    kwargs['slug'] = kwargs['slug'].lower()
    obj = get_object_or_404(
        kwargs['queryset'],
        **{kwargs['slug_field']: kwargs['slug']}
        )
    if hasattr(obj, "content_object"): # if the obj is ContextItem or alike, then use its related object
        obj = obj.content_object

    if not obj.is_contactable(): # checking the permissions or blocking
        raise Http404

    if request.method == 'POST':
        form = ContactForm(request.user, obj, request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('%smessage/alldone/' % obj.get_url_path())
    else:
        form = ContactForm(request.user, obj)

    kwargs['extra_context'] = kwargs.get("extra_context", {})
    
    kwargs['extra_context']['object'] = obj
    kwargs['extra_context']['form'] = form
    
    return object_detail(request, **kwargs)
    
contact = login_required(never_cache(contact))

def contact_done(request, **kwargs):
    """
    Display the confirmation page after submitting a contact form
    """
    kwargs['slug'] = kwargs['slug'].lower()
    obj = get_object_or_404(
        kwargs['queryset'],
        **{kwargs['slug_field']: kwargs['slug']}
        )
    if hasattr(obj, "content_object"): # if the obj is ContextItem or alike, then use its related object
        obj = obj.content_object

    kwargs['extra_context'] = kwargs.get("extra_context", {})
    kwargs['extra_context']['object'] = obj
    
    return object_detail(request, **kwargs)
