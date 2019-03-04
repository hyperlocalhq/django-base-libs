# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib.sites.models import Site
from django.contrib import messages
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from base_libs.middleware import get_current_user
from base_libs.utils.misc import get_website_url
from base_libs.utils.user import get_user_title

from jetson.apps.people.functions import get_user_language
from museumsportal.apps.mailing.forms import GenericMailForm
from museumsportal.apps.mailing.models import EmailTemplate
from museumsportal.apps.mailing.models import EmailMessage
from museumsportal.apps.mailing.recipient import Recipient


def get_global_placeholders(placeholders={}, language="en"):
    """
    sets up the global and object placeholders
    The keys used here are the "sysname" values from
    the EmailTemplatePlaceholder Model.
    These values must not be changed!!!
    """
    placeholders['site_name'] = Site.objects.get_current().name
    placeholders['website_url'] = get_website_url()
    if settings.MEDIA_URL.startswith("/"):
        placeholders['media_url'] = placeholders['website_url'] + settings.MEDIA_URL[1:]
    else:
        placeholders['media_url'] = settings.MEDIA_URL
    return placeholders


def get_sender_placeholders(placeholders={}, language="en", sender_name="", sender_email=""):
    """
    sets up the sender placeholders
    The keys used here are the "sysname" values from
    the EmailTemplatePlaceholder Model.
    These values must not be changed!!!
    """
    user = get_current_user()
    placeholders['sender_slug'] = ""
    placeholders['sender_url'] = ""
    if user and user.is_authenticated():
        placeholders['sender_name'] = sender_name or get_user_title(user)
        placeholders['sender_email'] = sender_email or user.email
        placeholders['sender_slug'] = user.username
        if getattr(settings, 'AUTH_PROFILE_MODULE', False):
            placeholders['sender_url'] = user.get_profile().get_absolute_url()
    else:
        placeholders['sender_name'] = sender_name
        placeholders['sender_email'] = sender_email
    if placeholders['sender_url']:
        placeholders['sender_link'] = u'<a href="%s">%s</a>' % (force_unicode(placeholders['sender_url']), force_unicode(placeholders['sender_name']))
    else:
        placeholders['sender_link'] = ""

    return placeholders


def get_object_placeholders(placeholders={}, obj=None, obj_placeholders={}, language="en"):
    """
    sets up the object placeholders. 
    The keys used here are the "sysname" values from
    the EmailTemplatePlaceholder Model.
    The values are filled with the values from the obj_placeholders dict.
    If not available there, defualt methods are used for the values.
    Hopefully, every object supports these methods. 
    If the object does not have such attributes or methods, 
    the values remain empty. This is used just for 
    simplicity - Maybe we can ommit the specific view functions
    one day!!!
    
    placeholders :    A dictionary holding placeholders. 
                      This dictionary will be returned with
                      some fields appended
    obj:              the object to get default placeholders from.
    obj_placeholders: object placeholders explicitely passed in.
                      Those values have precedence against the 
                      default values.
                
    """
    try:
        placeholders['object_title'] = obj.get_title(language=language)
    except:
        try:
            # maybe there is no title method with a language?
            placeholders['object_title'] = obj.get_title()
        except:
            placeholders['object_title'] = ""

    try:    
        placeholders['object_description'] = obj.get_description(language=language)
    except:        
        placeholders['object_description'] = ""
            
    try:        
        placeholders['object_slug'] = obj.slug
    except:
        placeholders['object_slug'] = ""
    
    try:
        placeholders['object_url'] = obj.get_absolute_url()
    except:
        placeholders['object_url'] = ""
        
    if placeholders['object_url']:
        placeholders['object_link'] = '<a href="%s">%s</a>' % (placeholders['object_url'], placeholders['object_title'])
    else:
        placeholders['object_link'] = ""
    try:
        placeholders['object_creation'] = obj.creation_date.strftime(_("LOCALE_DATETIME")),
    except:
        placeholders['object_creation'] = ""
            
    # overwrite all values with the additionally passed ones
    if obj_placeholders:
        for key,value in obj_placeholders.items():
            placeholders[key] = value
    
    return placeholders


def create_message(
    sender, 
    recipient, 
    sender_name, 
    sender_email, 
    recipient_email, 
    subject, 
    subject_de,
    body,
    body_de,
    delete_after_sending=False,
    is_html=True,
):
    """
    creates the email message depending on language information:
    English or german depends on the recipient, but:
    If the body or subject of the correct one is empty, take the other one
    we alwaws default to german!!!!!
    """
    # we default to german
    language = "de"
    if recipient:
        if get_user_language(recipient) == 'en':
            language = 'en'

    the_subject = subject
    the_body = body
    if language == "de":
        if len(subject_de) > 0 and len(body_de) > 0:
            the_subject = subject_de
            the_body = body_de
    if is_html:
        message = EmailMessage.objects.create(
            sender=sender,
            recipient=recipient,
            sender_name=sender_name,
            sender_email=sender_email,
            recipient_emails=recipient_email,
            subject=the_subject,
            body_html=the_body,
            delete_after_sending=delete_after_sending
        )
    else:
        message = EmailMessage.objects.create(
            sender=sender,
            recipient=recipient,
            sender_name=sender_name,
            sender_email=sender_email,
            recipient_emails=recipient_email,
            subject=the_subject,
            body=the_body,
            delete_after_sending=delete_after_sending
        )
    message.save()
    return message


@never_cache
def do_generic_mail(
    request,
    template_name='mailing/generic_mail.html',
    redirect_to=None,
    success_template=None,
    extra_context=None,
    recipients_list=(),  # list/tuple of Recipient instances
    preselect_recipients_list=False,
    display_recipients_list=False,
    display_recipients_input=False,
    display_en=True,
    display_de=False,
    email_template_slug=None,
    obj=None,
    obj_placeholders=None,
    delete_after_sending=False,
    reply_to=None,
    forward=None,
    draft=None,
    is_html=True,
    onbeforesend=None,
    onsend=None,
    onaftersend=None,
):
    """
    do_generic_mail opens an email form and saves specific email messages to the database
    
    template_name:            Path to a django template used to render the email
                              form (optional)
    redirect_to:              Redirection URL after completing the form
                              (optional)
    success_template:         Redirection Template after completing the form.
                              This parameter should not be set, if the
                              redirect_to parameter is set. (optional)
    extra_context:            extra context to be passed to the django template
                              (optional) 
    recipients_list:          A list of predefined recipients: This list
                              contains instances of class Recipient  (optional)
    preselect_recipients_list Flag indicating, if the recipients list should be 
                              preselected.
    display_recipients_list   Boolean value: If True, a list of recipients
                              (registered users) is displayed in the form.
                              (optional) 
    display_recipients_input  Boolean value: If True, a TextField with
                              recipients, who are not registered users is
                              displayed in the form. (optional)
    display_en                Boolean value: If True, the subject and body field
                              to input English text is displayed. (optional)
    display_de                Boolean value: If True, the subject and body field
                              to input German text is displayed. (optional)                             
    email_template_slug       The name of an email template (see EmailTemplate
                              model) with predefined body and subject.
                              (optional)
    obj                       an object related to the Email. (optional)
    obj_placeholders          any placeholders (see EmailTemplatePlaceholders)
                              according to the object. (optional)
    delete_after_sending      Boolean value: If True, the generated emails will
                              be deleted immediately after sending.
    reply_to                  an email message, which is "replied" (optional)
    forward                   an email message, which is forwarded (optional)
    draft                     an email message to be sent from drafts (optional)
    is_html                   is html used for email templates (optional)
    onbeforesend              event handler for doing something with recipients
                              before sending emails
    onsend                    event handler for overwriting the sending itself
    onaftersend               event handler for doing something with recipients
                              after sending emails
    """
    
    if not redirect_to:
        redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    
    # get the email Body template (if there is one given)
    try:
        email_template = EmailTemplate.objects.get(slug=email_template_slug)
    except:
        email_template = None
    
    # set up the global, sender and object placeholders
    
    user = get_current_user()
    
    rec_list = []
    if recipients_list != None:
        for item in recipients_list:
            rec_list.append((item.id, item.display_name))
    
    if request.method == 'POST':
        
        data = request.POST.copy()
        form = GenericMailForm(data, request.FILES)
        
        #subject and body for de and en:
        form.fields["subject"].required = display_en
        form.fields["body"].required = display_en
        form.fields["subject_de"].required = display_de
        form.fields["body_de"].required = display_de

            
        # sender is required, if user is not logged in
        form.fields["sender_name"].required = not(
            user and user.is_authenticated()
            )
        form.fields["sender_email"].required = not(
            user and user.is_authenticated()
            )
        
        # for sending the message, these fields are required!!!
        if data.has_key("send"):   
            # if there is a recipient_email_list available, you have to choose something
            if display_recipients_list:
                form.fields["recipients_email_list"].required = display_recipients_list and recipients_list and not display_recipients_input
            if display_recipients_input:
                form.fields["recipients_email_input"].required = display_recipients_input and not display_recipients_list

        if data.has_key("save_as_draft"):
            if display_recipients_list:
                form.fields["recipients_email_list"].required = False
            if display_recipients_input:
                form.fields["recipients_email_input"].required = False
            
        form.fields['recipients_email_list'].choices = rec_list                    
        
        if form.is_valid():
            # do character encoding
            cleaned = form.cleaned_data
            #for key, value in cleaned.items():
            #    if type(value).__name__ == "unicode":
            #        cleaned[key] = value.encode(settings.DEFAULT_CHARSET)

            # sender specific stuff ....
            if user and user.is_authenticated():
                sender_name = cleaned.get("sender_name", "") or get_user_language(user)
                sender_email = cleaned.get("sender_email", "") or user.email
            else:
                sender_name = cleaned["sender_name"]
                sender_email = cleaned["sender_email"]

            # recipients is a list of Recipient instances
            recipients = []
            
            # testmail recipient is just the sender!
            if data.has_key('send_test_mail'):
                tester_email = cleaned["tester_email"]
                recipients.append(
                    Recipient(
                        user=user.is_authenticated() and user or None,
                        name=sender_name,
                        email=tester_email,
                        )
                    )
            else:
                # recipient list is displayed, so get only selected items
                if display_recipients_list:
                    recipients_email_list = cleaned['recipients_email_list']
                    for item in recipients_list:
                        if item.id in recipients_email_list:
                            recipients.append(item)
                # recipient list is not displayed, so get all from the list!
                else:
                    for item in recipients_list:
                        recipients.append(item)
                            
                        
                if display_recipients_input:
                    recipients_email_input = cleaned["recipients_email_input"]
                    if recipients_email_input:
                        for rec_email, rec_name in recipients_email_input:
                            recipients.append(Recipient(user=None, name=rec_name, email=rec_email))
                    
            # at last, send the message or save it as draft!!! 
            placeholders = get_global_placeholders()
            placeholders = get_sender_placeholders(placeholders, sender_name=sender_name, sender_email=sender_email)
            
            if data.has_key("save_as_draft"):
                if email_template:
                    subject = email_template.render_template(
                        placeholders,
                        cleaned["subject"],
                    )
                    body = email_template.render_template(
                        placeholders,
                        cleaned["body"],
                        is_html=False,
                    )
                    subject_de = email_template.render_template(
                        placeholders,
                        cleaned["subject_de"],
                    )
                    body_de = email_template.render_template(
                        placeholders,
                        cleaned["body_de"],
                    )
                else:
                    subject = cleaned["subject"]
                    body = cleaned["body"]
                    subject_de = cleaned["subject_de"]
                    body_de = cleaned["body_de"]

                message = create_message(
                    sender=user,
                    recipient=None,
                    sender_name=sender_name,
                    sender_email=sender_email,
                    recipient_email=None,
                    subject=subject,
                    subject_de=subject_de,
                    body=body,
                    body_de=body_de,
                    delete_after_sending=delete_after_sending,
                    is_html=is_html,
                )
            else:       
                if len(recipients) > 0:
                    if callable(onbeforesend):
                        onbeforesend(recipients)
                    if callable(onsend):
                        onsend(recipients)
                    else:
                        for recipient in recipients:
                            
                            if recipient.name != None:
                                recipient_email = '%s <%s>' % (recipient.name, recipient.email)
                            else:
                                recipient_email = recipient.email
                            
                            # get the recipient placeholders
                            if email_template:
                                placeholders = recipient.get_placeholders(
                                    placeholders,
                                    language="en",
                                )
                                placeholders = get_object_placeholders(
                                    placeholders,
                                    obj,
                                    obj_placeholders,
                                    language="en",
                                )
                                subject = email_template.render_template(
                                    placeholders,
                                    cleaned["subject"],
                                )
                                body = email_template.render_template(
                                    placeholders,
                                    cleaned["body"],
                                    is_html=is_html,
                                )
                                # the german ones!
                                placeholders = recipient.get_placeholders(
                                    placeholders,
                                    language="de",
                                )
                                placeholders = get_object_placeholders(
                                    placeholders,
                                    obj,
                                    obj_placeholders,
                                    language="de",
                                )
                                subject_de = email_template.render_template(
                                    placeholders,
                                    cleaned["subject_de"],
                                )
                                body_de = email_template.render_template(
                                    placeholders,
                                    cleaned["body_de"],
                                    is_html=is_html,
                                )
                            else:
                                subject = cleaned["subject"]
                                body = cleaned["body"]
                                subject_de = cleaned["subject_de"]
                                body_de = cleaned["body_de"]
                            
                            message = create_message(
                                sender=user,
                                recipient=recipient.user,
                                sender_name=sender_name,
                                sender_email=sender_email,
                                recipient_email=recipient_email,
                                subject=subject,
                                subject_de=subject_de,
                                body=body,
                                body_de=body_de,
                                delete_after_sending=delete_after_sending,
                                is_html=is_html,
                            )
                            
                            # if reply_to, update the replied message
                            if reply_to:
                                reply_to.save()
                                
                            if data.has_key('send_test_mail'):        
                                message.send()
                            
                    if callable(onaftersend):
                        onaftersend(recipients)
                    messages.success(request, _("Your message has been sent."))
            
            # this is just for testing. must be done by a cron job! 
            #EmailMessage.objects.send_mails()    
            
            if not data.has_key('send_test_mail'):
                # mesage is finished ...
                if success_template is not None:
                    context = {}
                    if extra_context:
                        context.update(extra_context)
                    return render_to_response(
                        success_template,
                        context,
                        context_instance=RequestContext(request)
                    )
                else:
                    return HttpResponseRedirect(redirect_to)
    else:
        form = GenericMailForm()
        #subject and body for de and en:
        form.fields["subject"].required = display_en
        form.fields["body"].required = display_en
        form.fields["subject_de"].required = display_de
        form.fields["body_de"].required = display_de
                
        # sender is required, if user is not logged in
        form.fields["sender_name"].required = not(
            user and user.is_authenticated()
        )
        form.fields["sender_email"].required = not(
            user and user.is_authenticated()
        )
        
        # if there is a recipient_email_list available, you have to choose something
        if display_recipients_list:
            form.fields["recipients_email_list"].required = display_recipients_list and recipients_list and not display_recipients_input

        if display_recipients_input:
            form.fields["recipients_email_input"].required = display_recipients_input and not display_recipients_list
        
        # fill the choices for the recipients_email_list MultSelectionField 
        form.fields['recipients_email_list'].choices = rec_list
        if preselect_recipients_list:
            form.fields['recipients_email_list'].initial = [item[0] for item in rec_list]
        
                
        # fill the template
        if user and user.is_authenticated():
            form.fields['sender_name'].initial = get_user_title(user)
            form.fields['sender_email'].initial = user.email
            form.fields['tester_email'].initial = user.email

        if email_template:
            form.fields['subject'].initial = email_template.subject
            form.fields['subject_de'].initial = email_template.subject_de
            if is_html:
                form.fields['body'].initial = BeautifulSoup(email_template.body_html, "html.parser").prettify()
                form.fields['body_de'].initial = BeautifulSoup(email_template.body_html_de, "html.parser").prettify()
            else:
                form.fields['body'].initial = email_template.body
                form.fields['body_de'].initial = email_template.body_de
            
        if reply_to:
            form.fields['subject'].initial = "RE: %s" % reply_to.subject
            form.fields['subject_de'].initial = "AW: %s" % reply_to.subject
            if is_html:
                form.fields['body'].initial = BeautifulSoup(reply_to.body_html, "html.parser").prettify()
                form.fields['body_de'].initial = BeautifulSoup(reply_to.body_html, "html.parser").prettify()
            else:
                form.fields['body'].initial = reply_to.body
                form.fields['body_de'].initial = reply_to.body
            
        if forward:
            #TODO We could add some forward info such as "from", "sent to" etc.
            form.fields['subject'].initial = "FW: %s" % forward.subject
            form.fields['subject_de'].initial = "WG: %s" % forward.subject
            if is_html:
                form.fields['body'].initial = BeautifulSoup(forward.body_html,"html.parser").prettify()
                form.fields['body_de'].initial = BeautifulSoup(forward.body_html, "html.parser").prettify()
            else:
                form.fields['body'].initial = forward.body
                form.fields['body_de'].initial = forward.body
        if draft:
            #TODO We could add some forward info such as "from", "sent to" etc.
            form.fields['subject'].initial = draft.subject
            form.fields['subject_de'].initial = draft.subject
            if is_html:
                form.fields['body'].initial = BeautifulSoup(draft.body_html, "html.parser").prettify()
                form.fields['body_de'].initial = BeautifulSoup(draft.body_html, "html.parser").prettify()
            else:
                form.fields['body'].initial = draft.body
                form.fields['body_de'].initial = draft.body
                
    context = {
        'form': form,
        'object': obj,
        'display_recipients_list': display_recipients_list,
        'display_recipients_input': display_recipients_input,
        'display_en' : display_en,
        'display_de' : display_de,
        settings.REDIRECT_FIELD_NAME: redirect_to,
    }
        
    if extra_context:
        context.update(extra_context)
    return render_to_response(template_name, context, context_instance=RequestContext(request))


def send_email_using_template(
    recipients_list,  # list of Recipient instances
    email_template_slug,
    obj=None,
    obj_placeholders=None,
    delete_after_sending=False,
    sender=None,
    sender_name="",
    sender_email="",
    send_immediately=False,
):
    """
    send_mail sends an email to certain recipients without displaying the generic mail form 
      
    recipients_list:            A list of predefined recipients: This list
                                contains instances of class Recipient
                                (mandatory)
    email_template_slug         The name of an email template (see EmailTemplate
                                model) with predefined body and subject.
                                (mandatory)
    obj                         an object related to the Email. (optional)
    obj_placeholders            any placeholders (see EmailTemplatePlaceholders)
                                according to the object. (optional)
    delete_after_sending        Boolean value: If True, the generated emails
                                will be deleted immediately after sending.
    sender                      User who sends the message. (optional)
    sender_name                 The name of the sender (optional)
    sender_email                The email of the sender (optional)
    send_immediately            Send not by cron job, but directly
    """
    # get the email Body template (if there is one given)
    try:
        email_template = EmailTemplate.objects.get(slug=email_template_slug)
    except:
        raise Http404, "You must specify a valid email template, '%s' is not valid" % email_template_slug
    
    # set up the global, sender and object placeholders
    if not (sender_name and sender_email or sender):
        sender = get_current_user()
    if not sender_name:
        sender_name = get_user_title(sender)
    if not sender_email:
        sender_email = sender.email
    
    # recipients is a list of Recipient instances
    recipients = []
    for item in recipients_list:
        recipients.append(item)
                    
    # at last, send the message!!!        
    if len(recipients) == 0:
        raise Http404, "You must specify a recipients list"
    placeholders = get_global_placeholders()
    placeholders = get_sender_placeholders(
        placeholders,
        sender_name=sender_name,
        sender_email=sender_email,
    )
    for recipient in recipients:
        
        if recipient.name != None:
            recipient_email = '%s <%s>' % (recipient.name, recipient.email)
        else:
            recipient_email = recipient.email
        
        # get the recipient placeholders

        placeholders = recipient.get_placeholders(
            placeholders,
            language="en",
        )
        placeholders = get_object_placeholders(
            placeholders,
            obj,
            obj_placeholders,
            language="en",
        )
        subject = email_template.render_template(
            placeholders,
            email_template.subject,
        )
        body = email_template.render_template(
            placeholders,
            email_template.body,
            is_html=False,
        )
        body_html = email_template.render_template(
            placeholders,
            email_template.body_html,
        )
        # the german ones!
        placeholders = recipient.get_placeholders(
            placeholders,
            language="de",
        )
        placeholders = get_object_placeholders(
            placeholders,
            obj,
            obj_placeholders,
            language="de",
        )
        subject_de = email_template.render_template(
            placeholders,
            email_template.subject_de,
        )
        body_de = email_template.render_template(
            placeholders,
            email_template.body_de,
            is_html=False,
        )
        body_html_de = email_template.render_template(
            placeholders,
            email_template.body_html_de,
        )
        
        language = "de"
        if recipient.user:
            if get_user_language(recipient.user) == 'en':
                language = 'en'

        the_subject = subject
        the_body = body
        the_body_html = body_html
        if language == "de":
            if len(subject_de) > 0 and len(body_de) > 0:
                the_subject = subject_de
                the_body = body_de
                the_body_html = body_html_de
        message = EmailMessage.objects.create(
            sender=sender,
            recipient=recipient.user,
            sender_name=sender_name,
            sender_email=sender_email,
            recipient_emails=recipient_email,
            subject=the_subject,
            body_html=the_body_html,
            body=the_body,
            delete_after_sending=delete_after_sending
        )
        message.save()
        
        if send_immediately:
            message.send()
