# -*- coding: utf-8 -*-
from datetime import datetime
from django.template import loader
from django.template import RequestContext
from django.template import Template

from django.http import Http404
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import EmptyQuerySet
from django.utils.translation import force_unicode, ugettext_lazy as _

from base_libs.views import get_object_from_url
from base_libs.views import get_container
from base_libs.utils.loader import get_template_name_list_for_object
from base_libs.utils.misc import get_or_404
from base_libs.forms.formprocessing import FormHandler, FormPreviewHandler
from base_libs.forms.formprocessing import ID_ACTION_NEW
from base_libs.forms.formprocessing import ID_ACTION_EDIT
from base_libs.forms.formprocessing import ID_ACTION_DELETE

from base_libs.utils.misc import get_website_url
from jetson.apps.utils.views import object_list
from jetson.apps.forum.models import ForumContainer, Forum, ForumThread, ForumReply
from jetson.apps.forum.models import STATUS_CODE_PUBLIC, STATUS_CODE_DRAFT
from jetson.apps.utils.decorators import login_required

def get_forum_params(object_url_part, url_identifier, forum_slug=None, 
                     thread_slug=None, reply_slug=None, **kwargs):
    """
    gets some parameters. 
    It is used by the view functions and for form processing.
    Returns the parsed and calculated parameters as a 
    dictionary. This later can be used is extra_context
    in the rendered templates or for other purposes.
    """
    current_forum = None
    current_thread = None
    current_reply = None
        
    # first of all, object and container stuff!
    (obj, base_template) = get_object_from_url(object_url_part, **kwargs)
    site = None
    if kwargs.has_key('only_for_this_site'):
        if kwargs['only_for_this_site']:
            site = Site.objects.get_current()
            
    container = get_container(ForumContainer, site, obj, url_identifier)
    
    """
    here we must handle a special case (Reinhards decision, 30-01-2009):
    if container.max_level == 0, only one! forum is allowed, we call that
    "the discussion board". So, if there is no forum yet, create one on default
    and set it to current_forum! If there is one already, set current_forum to the
    "discussion board". This is maybe a little weird, but ...
    """
    if container.max_level == 0:
        # try to get the only forum!
        forums = Forum.objects.filter(container=container)
        nof_forums = forums.count()
        if nof_forums > 1:
            raise RuntimeError, "Database integrity corrupted. For container '%s' with max_level=0, there must not be more than one forum. %d forums detected. Please check that!" %(str(container), nof_forums)
        elif nof_forums == 1:
            current_forum = forums[0]
        else:
            current_forum = Forum(container=container, title=force_unicode("Discussion Board"))
            current_forum.save()
    
    # try to resolve forum, thread and reply from slug
    if forum_slug:
        current_forum = get_or_404(Forum, slug=forum_slug)
    if thread_slug:
        current_thread = get_or_404(ForumThread, slug=thread_slug)
    if reply_slug:
        current_reply = get_or_404(ForumReply, slug=reply_slug)

    # we need the path to the root for the breadcrumbs
    forum_path = []
    if current_forum:
        forum = current_forum
        while forum:
            forum_path.append(forum)
            forum = forum.parent    
    forum_path.reverse()  
    
    extra_context = {'container': container, 'object': obj, 'current_forum': current_forum, 'forum_path': forum_path,
                     'current_thread': current_thread, 'current_reply': current_reply,
                     'base_template': base_template or "forum/base.html"}

    return extra_context
    
def handle_request(request, object_url_part, url_identifier, 
     status=STATUS_CODE_PUBLIC, forum_slug=None, thread_slug=None,
     paginate_by=None, page=None, allow_empty=True, extra_context=None,
     context_processors=None, **kwargs):
    """
    handles a request for a forum or a thread.
    We do not provide separate view functions for 
    forums and threads, special needs are handled
    by template tags. This method avoids code redundancy! 

    These cases are handled by the view function:
    1. Just a related object (given by object_url_part)
       is provided -> all root forums are displayed.
    2. A forum is given additionally -> child forums and
       threads of the given forum are displayed.
    3. A thread is also given -> replies of the given thread 
       are displayed.
       
    Context (provided as extra_context):
    
    object           The object related to the forum container (or None)
    container        The forum container (defined by the rel. object)
    current_forum    The "current forum": Children of that forum should be 
                     displayed (or None)
    forum_path       The "Path" from the root_forum through all its parents.
                     We need that for the breadcrumbs.
    current_thread   the (current) thread to display (or a list of all threads, 
                     if this is None) 
    """
    queryset = EmptyQuerySet()
        
    # first of all, get forum parameters from the url parts...
    extra_context = get_forum_params(
         object_url_part, url_identifier, 
         forum_slug, thread_slug, **kwargs
         )
    
    current_thread = extra_context['current_thread']
    if current_thread:
        #queryset is a list of replies
        template_object_name = 'reply'
        current_thread.increase_views()
        queryset = current_thread.get_replies().order_by('-creation_date')
    else:
        #queryset is a list of threads
        template_object_name = 'thread'
        current_forum = extra_context['current_forum']
        # get queryset for threads: depends on being a leaf forum or not
        if current_forum:
            if current_forum.is_leaf():
                queryset = current_forum.get_threads(exclude_is_sticky=False)
            else: 
                queryset = current_forum.get_children_latest_threads()   
        
    obj = extra_context['object']
    template_name_list = get_template_name_list_for_object("forum", obj, "forum")
    
    return object_list(request, queryset, 
        paginate_by=paginate_by, page=page, allow_empty=True, 
        template_name=template_name_list, template_loader=loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=None)

class ForumOptionsFormHandler(FormHandler):
    """
    Handler for forum options form
    """   
    def parse_extra_params(self, *args, **kwargs):
        extra_context = get_forum_params(*args, **kwargs)
        self.container = extra_context['container']
        return extra_context
    
    def get_form_params(self):
        return {'container' : self.container}
    
    def get_form_template(self, use_ajax):
        return get_template_name_list_for_object("forum_options", self.container, "forum/forms", use_ajax)
        
    def check_allowed(self, request, action):
        pass
    check_allowed = login_required(check_allowed)

    def get_object(self):
        return self.container
        
    def get_edit_data(self, object):
        return {
            'title' : object.title, 
            'allow_bumping' : object.allow_bumping,
            #'max_level' : object.max_level,
        }
        
    def cancel(self, action):
        return HttpResponseRedirect(self.container.get_url())
    
    def save_edit(self, object, cleaned):
        container = self.container
        container.title = cleaned['title']
        container.allow_bumping = cleaned['allow_bumping']
        #container.max_level = cleaned['max_level']
        container.save()
        return HttpResponseRedirect(container.get_url())

class ForumFormPreviewHandler(FormPreviewHandler):    
    """
    Handler for new/edit/delete forum form
    """              
    def parse_extra_params(self, *args, **kwargs):
        extra_context = get_forum_params(*args, **kwargs)
        self.container = extra_context['container']
        self.current_forum = extra_context['current_forum']
        return extra_context
    
    def get_form_params(self):
        return {
            'container' : self.container,
            'current_forum' : self.current_forum,
            }
    
    def get_form_template(self, use_ajax):
        return get_template_name_list_for_object("forum", self.container, "forum/forms", use_ajax)
        
    def get_confirm_delete_template(self, use_ajax):
        return get_template_name_list_for_object("confirm_delete", self.container, "forum/forms", use_ajax)
    
    def check_allowed(self, request, action):
        # TODO privilege checks go here!
        container = self.container
        forum = self.current_forum
        
        # check, if you may create a forum here!
        if action == ID_ACTION_NEW:
            if container.max_level == 0:
                return self.redirect(action)
            if forum and forum.get_level() + 1 >= container.max_level:
                return self.redirect(action)
    check_allowed = login_required(check_allowed)
    
    def check_warnings(self, request, action):
        # check, if you may create a forum here!
        if action == ID_ACTION_NEW:
            if self.current_forum and self.current_forum.has_threads():
                return _("WARNING! You want to create a new forum under the '%(current_forum)s' forum, which already have threads. All threads of '%(current_forum)s' will be moved to your new forum!") % {'current_forum': unicode(self.current_forum)} 
        return None
    
    def get_object(self):
        return self.current_forum
        
    def get_edit_data(self, object):
        if object.parent:
            parent_id = object.parent.id
        else:
            parent_id = None
        return {
            'title' : object.title, 
            'short_title' : object.short_title,
            'description' : object.description,
            'parent' : parent_id,
            'status' : object.status,
        }

    def redirect(self, action):
        if action != ID_ACTION_DELETE:
            if self.current_forum and self.current_forum.is_public():
                return HttpResponseRedirect(self.current_forum.get_url())
        return HttpResponseRedirect(self.container.get_url())
        
    def cancel(self, action):
        return self.redirect(action)
    
    def save_new(self, cleaned):
        forum = Forum(
            container=self.container,
            parent=self.current_forum,
            title=cleaned['title'],
            short_title=cleaned['short_title'],
            description=cleaned['description'],
            status=cleaned['status'],
            )
        forum.save()
        # move threads from parent forum
        if self.current_forum:
            for thread in self.current_forum.get_threads(exclude_is_sticky=False):
                thread.forum = forum
                thread.save()
                
        return self.redirect(ID_ACTION_NEW)
        
    def save_edit(self, object, cleaned):
        forum = object
        forum.title = cleaned['title']
        forum.short_title = cleaned['short_title']
        forum.description = cleaned['description']
        if cleaned['parent']:
            forum.parent = Forum.objects.get(id=cleaned['parent'])
        else:
            forum.parent = None
        forum.status = cleaned['status']
        forum.save()
        return self.redirect(ID_ACTION_EDIT)
            
    def delete(self, object):
        object.delete()
        return self.redirect(ID_ACTION_DELETE)                    
   
class ThreadFormPreviewHandler(FormPreviewHandler):    
    """
    Handler for new/edit/delete thread form
    """    
    def parse_extra_params(self, *args, **kwargs):
       extra_context = get_forum_params(*args, **kwargs)
       self.container = extra_context['container']
       self.current_forum = extra_context['current_forum']
       self.current_thread = extra_context['current_thread']
       return extra_context

    def get_form_params(self):
       return {'container' : self.container}

    def get_form_template(self, use_ajax):
        return get_template_name_list_for_object("thread", self.container, "forum/forms", use_ajax)
        
    def get_confirm_delete_template(self, use_ajax):
        return get_template_name_list_for_object("confirm_delete", self.container, "forum/forms", use_ajax)
        
    def check_allowed(self, request, action):
        # TODO privilege checks go here!
        current_forum = self.current_forum
        # check, if you may create a thread here!
        if action == ID_ACTION_NEW:
            if current_forum.has_children():
                return self.redirect(action)
    check_allowed = login_required(check_allowed)

    def get_object(self):
        return self.current_thread
        
    def get_edit_data(self, object):
        return {
            'subject' : object.subject, 
            'message' : object.message,
            'forum' : object.forum.id,            
            'is_sticky' : object.is_sticky 
        }
        
    def redirect(self, action):
        if action != ID_ACTION_DELETE:
            if self.current_thread and self.current_thread.is_public():
                return HttpResponseRedirect(self.current_thread.get_url())
                        
        if self.current_forum and self.current_forum.is_public():
            return HttpResponseRedirect(self.current_forum.get_url())
        else:
            return HttpResponseRedirect(self.container.get_url())        
        
    def cancel(self, action):
        return self.redirect(action)
    
    def save_new(self, cleaned):
        thread = ForumThread(
                    forum=self.current_forum,
                    subject=cleaned['subject'],
                    message=cleaned['message'],
                    is_sticky=cleaned['is_sticky'],
                )
        thread.save()
        return self.redirect(ID_ACTION_NEW)
    
    def save_edit(self, object, cleaned):
        thread = object
        
        thread.subject = cleaned['subject']
        thread.message = cleaned['message']
        thread.is_sticky=cleaned['is_sticky'],
        #thread.status = cleaned['status']
        thread.save()
        return self.redirect(ID_ACTION_EDIT)
  
    def delete(self, object):
        object.delete()
        return self.redirect(ID_ACTION_DELETE)

class ReplyFormPreviewHandler(FormPreviewHandler):
    """
    Handler for new/edit/delete reply form
    """    
    def parse_extra_params(self, *args, **kwargs):
        extra_context = get_forum_params(*args, **kwargs)
        self.container = extra_context['container']
        self.current_forum = extra_context['current_forum']
        self.current_thread = extra_context['current_thread']
        self.current_reply = extra_context['current_reply']
        extra_context['reply_to'] = self.current_reply or self.current_thread 
        return extra_context

    def get_form_template(self, use_ajax):
        return get_template_name_list_for_object("reply", self.container, "forum/forms", use_ajax)
        
    def get_confirm_delete_template(self, use_ajax):
        return get_template_name_list_for_object("confirm_delete", self.container, "forum/forms", use_ajax)

    def check_allowed(self, request, action):
        pass
    check_allowed = login_required(check_allowed)

    def get_object(self):
        """ sets the current object to edit (or delete) """
        return self.current_reply
        
    def get_edit_data(self):
        """ returns the form data used for editing """
        return { 'message' : self.get_object().message }
    
    def redirect(self):
        if self.current_thread and self.current_thread.is_public():
            return HttpResponseRedirect(self.current_thread.get_url())
        if self.current_forum and self.current_forum.is_public():
            return HttpResponseRedirect(self.current_forum.get_url())
        return HttpResponseRedirect(self.container.get_url())    
        
    def cancel(self, action):
        return self.redirect()
    
    def save_new(self, cleaned):
        thread = self.current_thread
        parent = self.current_reply
        reply = ForumReply(thread=thread, parent=parent, message=cleaned['message'])
        reply.save()
        return self.redirect()
    
    def save_edit(self, object, cleaned):
        reply = object
        reply.message = cleaned['message']
        reply.save()
        return self.redirect()
    
    def delete(self, object):
        """ on delete. """
        object.delete()
        return self.redirect()

        
