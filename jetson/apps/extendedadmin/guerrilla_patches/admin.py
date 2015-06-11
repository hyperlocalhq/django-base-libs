# -*- coding: UTF-8 -*-
import re
from django import http, template
from django import forms
from django.db import models
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.helpers import AdminField
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.admin.util import get_model_from_relation
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.admin.forms import ERROR_MESSAGE
from django.contrib.admin.sites import site

def patch_admin():
    def new_admin_field_init(self, form, field, is_first):
        """
        patched AdminField.__init__:
        some stuff for markup_type fields for Textarea fields is added.
        """
        self.field = form[field] # A django.forms.BoundField instance
        self.is_first = is_first # Whether this field is first on the line
        self.is_checkbox = isinstance(self.field.field.widget, forms.CheckboxInput)
        # gather, if a Textarea form field has an attached "markupType" selectbox.
        self.has_markup_type = "hasMarkupType" in self.field.field.widget.attrs.get('class', "")
        self.related_markup_type_field = None
        if self.has_markup_type:
            try:
                self.related_markup_type_field = form['%s_markup_type' % field]
            except:
                pass
        # gather, if a field is! a markup type field. We won't display such fields!!!
        self.is_markup_type = re.search('markup_type$', field) is not None
    AdminField.__init__ = new_admin_field_init
    
    def adminsite_index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site and are listed in settings.ADMIN_APP_INDEX if that is defined.
        
        Structure:
        
        ADMIN_APP_INDEX = (
            {
                'title': _('<group_title>'),
                'apps': (
                    ('<app_label>', app_options),
                    ...
                ),
            },{
                ...
            }
        )
        
        app_options == {
            'verbose_name': _("<App Verbose Name>"),
            'models': (model, ...)
            'classes': ('<css_class>', ...),
            }
        
        model == '<ModelName>'
        """
        app_dict = {}
        user = request.user
        
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)
            
            if has_module_perms:
                perms = model_admin.get_model_perms(request)
                
                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'admin_url': mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                        'perms': perms,
                    }
                    if app_label in app_dict:
                        app_dict[app_label]['model_dict'][model.__name__] = model_dict
                    else:
                        app_verbose_name = getattr(
                            models.get_app(app_label),
                            "verbose_name",
                            app_label.title(),
                            )
                        app_dict[app_label] = {
                            'name': app_verbose_name,
                            'app_url': app_label + '/',
                            'has_module_perms': has_module_perms,
                            'model_dict': {model.__name__: model_dict},
                        }
                        
        app_index = getattr(settings, "ADMIN_APP_INDEX", None)
        if app_index:
            # Sort the apps by the order in ADMIN_APP_INDEX
            app_list = []
            for group in app_index:
                for app_label, app_options in group['apps']:
                    if app_label in app_dict:
                        app = app_dict[app_label]
                        if "verbose_name" in app_options:
                            app['name'] = _(app_options['verbose_name'])
                        if "models" in app_options:
                            app['models'] = []
                            for model_name in app_options["models"]:
                                if model_name in app['model_dict']:
                                    app['models'].append(app['model_dict'][model_name])
                        if "classes" in app_options:
                            app['classes'] = app_options['classes']
                        app['group'] = group['title']
                        app_list.append(app)
        else:
            # Sort the apps alphabetically.
            app_list = app_dict.values()
            app_list.sort(lambda x, y: cmp(x['name'], y['name']))
            
            # Sort the models alphabetically within each app.
            for app in app_list:
                app['models'] = app['model_dict'].values()
                app['models'].sort(lambda x, y: cmp(x['name'], y['name']))
        
        context = {
            'title': _('Site administration'),
            'app_list': app_list,
        }
        context.update(extra_context or {})
        return render_to_response(self.index_template or 'admin/index.html', context,
            context_instance=template.RequestContext(request)
        )
    adminsite_index = never_cache(adminsite_index)
    AdminSite.index = adminsite_index


    def adminsite_app_index(self, request, app_label, extra_context=None):
        user = request.user
        has_module_perms = user.has_module_perms(app_label)
        app_dict = {}
        for model, model_admin in self._registry.items():
            if app_label == model._meta.app_label:
                if has_module_perms:
                    perms = model_admin.get_model_perms(request)
                    
                    # Check whether user has any perm for this module.
                    # If so, add the module to the model_list.
                    if True in perms.values():
                        model_dict = {
                            'name': capfirst(model._meta.verbose_name_plural),
                            'admin_url': '%s/' % model.__name__.lower(),
                            'perms': perms,
                        }
                        if app_dict:
                            app_dict['model_dict'][model.__name__] = model_dict
                        else:
                            # First time around, now that we know there's
                            # something to display, add in the necessary meta
                            # information.
                            app_verbose_name = getattr(
                                models.get_app(app_label),
                                "verbose_name",
                                app_label.title(),
                                )
                            app_dict = {
                                'name': app_verbose_name,
                                'app_url': '',
                                'has_module_perms': has_module_perms,
                                'model_dict': {model.__name__: model_dict},
                            }
        if not app_dict:
            raise http.Http404('The requested admin page does not exist.')
        app_index = getattr(settings, "ADMIN_APP_INDEX", ())
        app_index_dict = {}
        for group in app_index:
            app_index_dict.update(dict(group['apps']))
        if app_label in app_index_dict:
            # Sort the models by the order in ADMIN_APP_INDEX
            app_options = app_index_dict[app_label]
            if "verbose_name" in app_options:
                app_dict['name'] = _(app_options['verbose_name'])
            if "models" in app_options:
                app_dict['models'] = []
                for model_name in app_options["models"]:
                    if model_name in app_dict['model_dict']:
                        app_dict['models'].append(app_dict['model_dict'][model_name])
            if "classes" in app_options:
                app_dict['classes'] = app_options['classes']
        else:
            # Sort the models alphabetically within each app.
            app_dict['models'] = app_dict['model_dict'].values()
            app_dict['models'].sort(lambda x, y: cmp(x['name'], y['name']))
        context = {
            'title': _('%s administration') % app_dict['name'],
            'app_list': [app_dict],
            'root_path': self.root_path,
        }
        context.update(extra_context or {})
        return render_to_response(self.app_index_template or 'admin/app_index.html', context,
            context_instance=template.RequestContext(request)
        )
    AdminSite.app_index = adminsite_app_index

    class AdminAuthenticationForm(AuthenticationForm):
        """
        A custom authentication form used in the admin app.
    
        """
        this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput, initial=1,
            error_messages={'required': _("Please log in again, because your session has expired.")})
    
        def clean(self):
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            message = ERROR_MESSAGE
    
            if username and password:
                self.user_cache = authenticate(username=username, password=password)
                if self.user_cache is None:
                    if u'@' in username:
                        # Mistakenly entered e-mail address instead of username? Look it up.
                        try:
                            user = User.objects.get(email=username)
                        except (User.DoesNotExist, User.MultipleObjectsReturned):
                            raise forms.ValidationError(message)
                        else:
                            self.user_cache = authenticate(email=username, password=password)
                if self.user_cache:
                    if not self.user_cache.is_active or not self.user_cache.is_staff:
                        raise forms.ValidationError(message)
                else:
                    raise forms.ValidationError(message)
            self.check_for_test_cookie()
            return self.cleaned_data
    site.login_form = AdminAuthenticationForm
patch_admin()    
