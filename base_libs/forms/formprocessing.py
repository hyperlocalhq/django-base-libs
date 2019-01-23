# -*- coding: utf-8 -*-
import re

from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

from formtools.utils import form_hmac

from django.utils.translation import ugettext_lazy as _

# action names for standard actions. Do not Edit!!!
ID_ACTION_NEW = "new"
ID_ACTION_EDIT = "edit"
ID_ACTION_DELETE = "delete"
ALLOWED_ACTIONS = [ID_ACTION_NEW, ID_ACTION_EDIT, ID_ACTION_DELETE]

AUTO_ID = 'form_%s' # Each form here uses this as its auto_id parameter.


def methodNotImplementedError(method, instance):
    raise NotImplementedError, 'You must define a %s method on your %s subclass.' % (method, instance.__class__.__name__)


class FormHandler(object):
    """
    A class managing general form processing 
    for all, new, edit and delete operations. 
    """
    form_template = "form.html"
    form_template_ajax = None
    confirm_delete_template = "confirm_delete.html"
    confirm_delete_template_ajax = None

    def __init__(self, form, confirm_delete=True, use_ajax=False):
        """ 
        The init method. Do not override in your subclasses. 
        The 'confirm_delete' parameter should be true, if you 
        want to set a "do you really want to delete ..." form
        before deleting the object. 
        """
        self.form = form
        self.use_ajax = use_ajax
        self.confirm_delete = confirm_delete
        
        # context for templates
        self.context = {
            'cancel_stage_field': self._check_name('submit_cancel'),
            'delete_stage_field': self._check_name('submit_delete'),
            'post_stage_field': self._check_name('submit_post'),
        }
        self.extra_context = {}
        
    def __call__(self, request, *args, **kwargs):
        """ 
        The call method acts as an action dispatcher. 
        """
        # first, parse the desired action from the kwargs.
        if kwargs.has_key('action'):
            action = kwargs['action']
            """ Checks for allowed actions """
            if action not in ALLOWED_ACTIONS:
                raise AttributeError, "You have defined an invalid action '%s' in your %s form call. Allowed actions are %s." % (action, self.__class__.__name__, str(ALLOWED_ACTIONS))
            self.context['form_handler_action'] = self.context['form_action'] = self._check_name(action)
            # TODO: self.context['form_action'] is deprecated as it is conflicting with crispy forms
            self.action = action
        else:
            raise AttributeError, "You must provide an 'action' parameter in your %s call. Please correct." % self.__class__.__name__

        self.request = request  # the request might be necessary when saving objects or redirecting

        # get extra params and extra inits        
        self.extra_context = self.parse_extra_params(*args, **kwargs)
        
        # check, if the whole action is allowed!
        check = self.check_allowed(request, action)
        if isinstance(check, (HttpResponseRedirect, HttpResponse, HttpResponseForbidden)):
            return check
        
        warnings = self.check_warnings(request, action)
        if warnings:
            self.context['warnings'] = warnings

        # get the submit_action from the post (or default to 'start')
        submit_action = 'start'
        for key, val in request.POST.items():
            regex = re.match('submit_(.*)', key)
            if regex:
                submit_action = regex.group(1)
                break

        # delete action is detached from the others!
        if action == ID_ACTION_DELETE:
            if not self.confirm_delete or submit_action == 'delete':
                return self.delete(self.get_object())

        if submit_action == 'cancel':
            return self.cancel(self.action)
        else: # the rest of the actions: 'post' and others defined in subclasses ('preview', etc.)
            try:
                method = getattr(self, submit_action)
            except AttributeError:
                raise AttributeError, "Tried to call non existent method '%s' in the %s form subclass. Please correct." % (submit_action, self.__class__.__name__)
            return method(request, action)
    
    def _check_name(self, name):
        """
        Checks, if a submit value name clashes with a form field.
        If so, give an error. You must not name any form field
        'delete', 'cancel' 'post' or 'preview' etc.
        This method is private and should not be used by subclasses.
        """
        while 1:
            try:
                f = self.form.base_fields[name]
                raise AttributeError, "You have defined a field '%s' in your %s form subclass. This name clashes with an internally defined context variable. Please correct." % (name, self.__class__.__name__)
            except KeyError:
                return name
            
    def start(self, request, action):
        """ Initially displays the form """
        template = self.get_form_template(self.use_ajax)

        if action == ID_ACTION_NEW:
            form = self.form(auto_id=AUTO_ID, **self.get_form_params())
        elif action == ID_ACTION_EDIT:
            form = self.form(
                         auto_id=AUTO_ID, 
                         data=self.get_edit_data(self.get_object()),
                         **self.get_form_params()
                         )
        else: # ID_ACTION_DELETE
            form = None
            template = self.get_confirm_delete_template(self.use_ajax)
            self.extra_context['delete_object'] = self.get_object()
        
        context = {}
        if isinstance(template, (tuple, list)):
            t = loader.select_template(template)
        else:
            t = loader.get_template(template)

        context['form'] = form
        context.update(self.context)
        context.update(self.extra_context)
        return HttpResponse(t.render(RequestContext(request, context)))   
                
    def post(self, request, action):
        """
        Validates the POST data. If valid, calls save_new()
        ore save_edit(). If none of them is provided, call
        save(). If the form is not valid, redisplay the form
        with its errors.
        """
        form = self.form(
                 data=request.POST,
                 files=request.FILES,
                 auto_id=AUTO_ID, 
                 **self.get_form_params()
                 )
        context = { 'form': form, }
        if form.is_valid():
            # encode cleaned data
            cleaned = form.cleaned_data
            if action == ID_ACTION_NEW:
                return self.save_new(cleaned)
            else: #ID_ACTION_EDIT:
                return self.save_edit(self.get_object(), cleaned)
        else:
            template_name = self.get_form_template(self.use_ajax)
            if isinstance(template_name, (tuple, list)):
                t = loader.select_template(template_name)
            else:
                t = loader.get_template(template_name)
            context.update(self.context)
            context.update(self.extra_context)
            return HttpResponse(t.render(RequestContext(request, context)))   
        
    # METHODS SUBCLASSES MAY OVERRIDE
    
    def parse_extra_params(self, *args, **kwargs):
        """
        Given captured args and kwargs from the URLconf, 
        saves something in self.extra_context.
        """
        pass
    
    def get_form_params(self):
        """
        maybe, you want to pass some kwargs to your forms custom
        init method used for validation or anything else in the 
        form. In this case, just overwrite this function. Must
        return a dictionary.
        """
        return {}
    
    def get_form_template(self, use_ajax):
        """ specifies a template to use for the form """
        if use_ajax:
            template = self.__class__.form_template_ajax
        else:
            template = self.__class__.form_template
        if not template:
            raise AttributeError, "You must define a form template for your %s form call." % self.__class__.__name__
        return template
    
    def get_confirm_delete_template(self, use_ajax):
        """ specifies a template to use for delete confirmation """
        if use_ajax:
            template = self.__class__.confirm_delete_template_ajax
        else:
            template = self.__class__.confirm_delete_template
        if not template:
            raise AttributeError, "You must define a form template for your %s form call." % self.__class__.__name__
        return template
    
    def check_allowed(self, request, action):
        """
        optional check before the form is displayed. If that
        check fails, this method should return a HttpResponse
        or HttpResponseRedirect object. This method can also 
        be decorated (by login_required) or something else  
        """
        pass
   
    def check_warnings(self, request, action):
        """
        optional check before the form is displayed. Any warning
        as a string can be placed here. The warning will be 
        displayed at the form template, when it is rendered!
        """
        pass
    # METHODS SUBCLASSES MUST OVERRIDE
     
    def cancel(self, action):
        """ Cancels the action and returns an HttpResponseRedirect. """
        return methodNotImplementedError('cancel()', self)
    
    # METHODS SUBCLASSES MUST OVERRIDE FOR SPECIFIC CASES
    def delete(self, object):
        """ Cancels the action and returns an HttpResponseRedirect. """
        return methodNotImplementedError('delete()', self)

    def save_new(self, cleaned):
        """
        Does something with the cleaned_data for "new" forms 
        and returns an HttpResponseRedirect. This method must
        be overwritten, if you want to provide a "new" action.
        """
        return methodNotImplementedError('save_new()', self)

    def save_edit(self, object, cleaned):
        """
        Does something with the cleaned_data for "edit" forms 
        and returns an HttpResponseRedirect. This method must
        be overwritten, if you want to provide a "edit" action.
        """
        return methodNotImplementedError('save_edit()', self)
    
    def get_edit_data(self, object):
        """ gets the data to be edited. """
        return methodNotImplementedError('get_edit_date()', self)
     
    def get_object(self):
        """ gets the object to be edited or deleted. """
        return methodNotImplementedError('get_object()', self)


class FormPreviewHandler(FormHandler):
    """
    A class managing new,edit and delete operations
    with preview, both, non ajax and ajax.
    """
    preview_template = 'preview.html'
    preview_ajax_template = 'ajax_preview.html'

    def __init__(self, form, confirm_delete=True, use_ajax=True):
        """ 
        The init method. Do not override in your subclasses!
        """
        super(FormPreviewHandler, self).__init__(form, confirm_delete, use_ajax)
        # additional context for templates
        self.context.update({
            'preview_stage_field': self._check_name('submit_preview'),
        })

    def preview(self, request, action):
        """
        Validates the POST data. If valid, displays 
        the preview. Otherwise, redisplays form.
        """
        self.extra_context['hash_failed'] = False
        
        if self.context.has_key('warnings'):
            self.context['warnings'] = None
        
        form = self.form(data=request.POST, files=request.FILES, auto_id=AUTO_ID, **self.get_form_params())
        context = {
           'form': form,
        }
        if form.is_valid():
            context['hash_field'] = self._check_name('hash')
            context['hash_value'] = self.security_hash(request, form)
            context['form_preview'] = True
            template_name = self.get_preview_template(self.use_ajax)
        else:
            template_name = self.get_form_template(self.use_ajax)

        if isinstance(template_name, (tuple, list)):
            t = loader.select_template(template_name)
        else:
            t = loader.get_template(template_name)

        context.update(self.context)
        context.update(self.extra_context)
            
        return HttpResponse(t.render(RequestContext(request, context)))
    
    def post(self, request, action):
        form = self.form(data=request.POST, files=request.FILES, auto_id=AUTO_ID, **self.get_form_params())
        if form.is_valid():
            if self.security_hash(request, form) != request.POST.get(self._check_name('hash')):
                return self.failed_hash(request, action) # Security hash failed.
        return super(FormPreviewHandler, self).post(request, action)
    
    # METHODS SUBCLASSES MAY OVERRIDE
    
    def security_hash(self, request, form):
        """
        Calculates the security hash for the given HttpRequest
        and Form instances. Subclasses may want to take into 
        account request-specific information, such as the IP 
        address.
        """
        return form_hmac(form)

    def failed_hash(self, request, action):
        """Returns an HttpResponse in the case of an invalid security hash."""
        self.extra_context['hash_failed'] = True
        self.extra_context['hash_failed_message'] = _("Security check failed. Maybe your form has been tampered. Please try again.")
        return self.preview(request, action)
    
    def get_preview_template(self, use_ajax):
        """ specifies a template to use for the form preview """
        return self.get_form_template(use_ajax)
