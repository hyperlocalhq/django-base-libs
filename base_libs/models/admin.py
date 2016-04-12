# -*- coding: UTF-8 -*-
import json

from django.contrib import admin
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django import forms, template
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.contrib.admin.views.main import ERROR_FLAG
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.exceptions import PermissionDenied
from django.conf import settings

from base_libs.views.hierarchy import HierarchyChangeList
from base_libs.widgets import TreeSelectWidget
from base_libs.middleware import get_current_user
from base_libs.admin.options import ExtendedModelAdmin
from base_libs.models import ContentBaseMixin
from base_libs.models.base_libs_settings import JQUERY_URL
from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

# "save" buttons for ContentBaseMixin extending models
CONTENT_BASE_SUBMIT_CHOICES = (
    ('save', _("Save")),
    ('save-add', _("Save and Add Another")),
    ('hello', _("Hello")),
)

ADMIN_MEDIA_URL = getattr(
    settings,
    "JETSON_MEDIA_URL",
    settings.ADMIN_MEDIA_PREFIX,
)


def get_admin_lang_section(heading, field_list, default_expanded=True):
    """
    function that returns a fieldset section 
    with specified multilingual fields
    """
    
    get_admin_lang_section.count = getattr(get_admin_lang_section, 'count', 0) + 1
    
    fieldset = []
    for lang_code, lang_verbose in settings.LANGUAGES:
        
        if len(settings.LANGUAGES) > 1:
            if heading is not None:
                section = string_concat(heading, " (", lang_verbose, ")")
            else:
                section = lang_verbose
        else:
            if heading is not None:
                section = heading
            else:
                section = None
            
        
        if default_expanded:
            if lang_code == settings.LANGUAGE_CODE:
                classes = ["grp-collapse grp-open"]
            else:
                classes = ["grp-collapse grp-closed"]
        else:
            classes = ["grp-collapse grp-closed"]
        
        classes.append("multilingual")
        classes.append("multilingual-set-%d" % get_admin_lang_section.count)
        classes.append("multilingual-language-%s" % lang_code)
        fields = ()
        for field_name in field_list:
            fields = fields + ("%s_%s" % (field_name, lang_code),)
        fieldset.append(
            (section, {
                'fields': fields,
                'classes': classes,
            }),
        )
    return fieldset


class PublishingMixinAdminOptions(ExtendedModelAdmin):
    """
    admin options for PublishingMixin
    """
    list_filter = ('author', 'status', 'published_from', 'published_till')   
    
    fieldsets = [(_('Publish Status'), {
        'fields': ('author', 'status', 'published_from', 'published_till',),
        'classes': ("collapse closed",),
        }),
    ]
    
    def is_published(self, obj):
        return obj.is_published()
    is_published.boolean = True
    
        
    def is_draft(self, obj):
        return obj.is_draft()
    is_draft.boolean = True
        
    # currently logged in user cannot set as default in the model definition. so we do that here!
    #prepopulated_fields = {'author': ('get_current_user',),}


def ObjectRelationMixinAdminOptions(
    prefix="",
    prefix_verbose="",
    admin_order_field="",
    extending=ExtendedModelAdmin
    ):
    """
    returns an admin.ModelAdmin extending class used 
    for the newforms admin. Some custom widgets
    for selecting contenttype and object id are provided!
    "extending" defines what model to extend:
        admin.ModelAdmin, admin.StackedInline, admin.TabularInline, or other
    """
    if prefix:
        prefix = "%s_" % prefix
    content_type_field = "%scontent_type" % prefix
    object_id_field = "%sobject_id" % prefix
    content_object_field = "%scontent_object" % prefix
    
    # here is the class itself
    class klass(extending):
        fieldsets = [
            (
                prefix_verbose or _('Related object'), {
                     'classes': ('collapse open',), 
                     'fields': [content_type_field, object_id_field],
                }
            ),
        ]
        
        def formfield_for_dbfield(self, db_field, **kwargs):
            """ applying custom widgets here! """
            field = super(klass, self).formfield_for_dbfield(db_field, **kwargs)
            if db_field.name == content_type_field:
                # we add a special class for javascript capturing events her.
                # do not edit the name of this class!!!!
                field.widget.attrs['class'] ='related_object_ct_select'
            if db_field.name == object_id_field:
                # we add a special class for javascript capturing events her.
                # do not edit the name of this class!!!!
                field.widget.attrs['class'] ='related_object_obj_id_select'
            return field
            
    def get_content_object_display(self, obj):
        """this method is just used for display in the admin"""
        co = getattr(obj, content_object_field)
        if not co:
            return "-------"
        user = get_current_user()
        app_name = co._meta.app_label
        model_name = co.__class__.__name__.lower()
        co_unicode = hasattr(co, "__unicode__") and co.__unicode__() or co._get_pk_val()
        if user.has_perm("%s.change_%s" % (app_name, model_name), co):
            return u"""<a href="/admin/%s/%s/%s/" class="content_object">%s</a>""" % (
                app_name,
                model_name,
                co._get_pk_val(),
                co_unicode,
                )
        else:
            return co_unicode
    get_content_object_display.allow_tags = True
    get_content_object_display.short_description = prefix_verbose or _("Content Object")
    if admin_order_field:
        get_content_object_display.admin_order_field = admin_order_field
    
    setattr(
        klass,
        "get_%scontent_object_display" % prefix,
        get_content_object_display,
        )
            
    return klass


def ObjectRelationMixinAdminForm(prefix=None):
    """
    returns a ModelForm extending class used for model
    validation. In this case,it has to implemented as a factory.
    (for more details, see base_libs.models.ObjectRelationMixin)
    """
    if prefix:
        content_type_field = "%s_content_type" % prefix
        object_id_field = "%s_object_id" % prefix
    else:
        content_type_field = "content_type" 
        object_id_field = "object_id"
        
    class klass(forms.ModelForm):
        class Media:
            js = (
                "%sjs/admin/RelatedObjectSelect.js" % ADMIN_MEDIA_URL,
            )
            
    def clean_object_id(self):
        """
        Validator. Checks, whether the object Id is correct
        for the given ContentType.
        """
        if self.cleaned_data.has_key(content_type_field):
            content_type_value = self.cleaned_data[content_type_field]
        else:
            content_type_value = None

        if self.cleaned_data.has_key(object_id_field):
            object_id_value = self.cleaned_data[object_id_field]
        else:
            object_id_value = None
        
        if object_id_value and not content_type_value:
            raise forms.ValidationError(
                 _("If you provide an object ID, you must specify a content type.")
            )    

        if content_type_value:
            if not object_id_value:
                raise forms.ValidationError(
                     _("For a given content type, you must specify an object id.")
                )    
            try:
                # check for correct object!
                content_type_value.get_object_for_this_type(pk=object_id_value)
            except:
                raise forms.ValidationError(
                     _("No object with the given content type, object id exists.")
                )
        return object_id_value
        
    def clean_content_type(self):        
        """
        Checks, whether the content type is correct for the given object id.
        """
        if self.cleaned_data.has_key(content_type_field):
            content_type_value = self.cleaned_data[content_type_field]
        else:
            content_type_value = None

        if self.cleaned_data.has_key(object_id_field):
            object_id_value = self.cleaned_data[object_id_field]
        else:
            object_id_value = None

        if object_id_value and not content_type_value:
            raise forms.ValidationError(
                 _("If you provide an object ID, you must choose a content type.")
            )    
        return content_type_value
    
    # apply methods
    setattr(klass, 'clean_%s' % object_id_field, clean_object_id)
    setattr(klass, 'clean_%s' % content_type_field, clean_content_type)
    return klass


class SingleSiteContainerMixinAdminOptions(ObjectRelationMixinAdminOptions()):
    """
    newforms admin options for SingleSiteContainers
    """
    fieldsets = [
         (
              _("Related Object, Sites and URL Identifier"), {
                    'classes': ('collapse open',), 
                    'fields': ['site', 'content_type', 'object_id', 'sysname'],
              }
          ),
    ]
    pass


class SingleSiteContainerMixinAdminForm(ObjectRelationMixinAdminForm()):

    def clean(self):
        """
        The uniqueness of site, content_type, object_id and sysname 
        guarantees the uniqueness of a container. 
        """
        model = self.Meta.model
        qs = model.objects.all()
        # exclude myself from query!
        if self.instance._get_pk_val():
            qs = qs.exclude(id__exact=self.instance._get_pk_val())

        if self.cleaned_data.has_key('content_type'):
            content_type_value = self.cleaned_data['content_type']
        else:
            content_type_value = None

        if self.cleaned_data.has_key('object_id'):
            object_id_value = self.cleaned_data['object_id']
        else:
            object_id_value = None
        
        if self.cleaned_data.has_key('site'):
            site_value = self.cleaned_data['site']
        else:
            site_value = None
        
        if content_type_value and object_id_value:
            qs = qs.filter(
                   content_type=content_type_value,
                   object_id=int(object_id_value)
                )
        else:
            qs = qs.filter(content_type__isnull=True, object_id__isnull=True)
    
        if site_value:
            qs = qs.filter(site=site_value)
        else:
            qs = qs.filter(site__isnull=True)
    
        qs = qs.filter(sysname__exact=self.cleaned_data['sysname'])
    
        if qs.count() > 0:
            raise forms.ValidationError(_("There already exists a container with these properties."))
        
        return super(SingleSiteContainerMixinAdminForm, self).clean()


class MultiSiteContainerMixinAdminOptions(ObjectRelationMixinAdminOptions()):
    """
    newforms admin options for SingleSiteContainers
    """
    fieldsets = [
         (
              _("Related Object, Sites and URL Identifier"), {
                    'classes': ('collapse open',), 
                    'fields': ['sites', 'content_type', 'object_id', 'sysname'],
              }
          ),
    ]
    pass


class MultiSiteContainerMixinAdminForm(ObjectRelationMixinAdminForm()):

    def clean(self):
        """
        The uniqueness of site, content_type, object_id and sysname 
        guarantees the uniqueness of a container. 
        """
        self.cleaned_data = super(MultiSiteContainerMixinAdminForm, self).clean()
        model = self.Meta.model
        qs = model.objects.all()
        # exclude myself from query!
        if self.instance._get_pk_val():
            qs = qs.exclude(pk__exact=self.instance._get_pk_val())

        if self.cleaned_data.has_key('content_type'):
            content_type_value = self.cleaned_data['content_type']
        else:
            content_type_value = None

        if self.cleaned_data.has_key('object_id'):
            object_id_value = self.cleaned_data['object_id']
        else:
            object_id_value = None
        
        if self.cleaned_data.has_key('sites'):
            sites_value = self.cleaned_data['sites']
        else:
            sites_value = None
        
        if content_type_value and object_id_value:
            qs = qs.filter(
                content_type=content_type_value,
                object_id=object_id_value,
            )
        else:
            qs = qs.filter(content_type__isnull=True, object_id__isnull=True)
    
        if sites_value:
            #site_list = [int(site) for site in sites_value]
            qs = qs.filter(sites__in=sites_value)
        else:
            qs = qs.filter(sites__isnull=True)
    
        qs = qs.filter(sysname__exact=self.cleaned_data.get('sysname', None))
    
        if qs.count() > 0:
            raise forms.ValidationError(_("There already exists a container with these properties."))
        return self.cleaned_data


class HierarchyMixinAdminOptions(ExtendedModelAdmin):
    """
    newforms admin options for Hierarchy based models
    """
    # determines, if drag&drop is allowed
    dragdrop_allowed = True
    
    def changelist_view(self, request, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label
        
        # save changes ....
        if request.method == 'POST':
            tree_data = request.POST.get('tree_data')
            if tree_data:
                tree_list = json.loads(tree_data)
                sort_order_list = []
                for item in tree_list:
                    node = self.model.objects.get(pk=item['id'])
                    sort_order_list.append(node.sort_order)
                sort_order_list = sorted(sort_order_list)
                counter = 0
                for item in tree_list:
                    node = self.model.objects.get(pk=item['id'])
                    if item['parent']:
                        node.parent = self.model.objects.get(pk=item['parent'])
                    else:
                        node.parent = None
                    node.sort_order = sort_order_list[counter]
                    node.save() 
                    counter += 1
            return HttpResponseRedirect('.')
        
        # here the normal procedure for change list
        # views go. we just took that part from
        # django.contrib.admin.options.changelist_view

        # suppress pagination TODO: This is not the best solution, but it works :)
        self.list_per_page = 100000000
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        try:
            cl = HierarchyChangeList(request, self.model, self.list_display, self.list_display_links, self.list_filter,
                self.date_hierarchy, self.search_fields, self.list_select_related, self.list_per_page,
                self.list_max_show_all, self.list_editable, self)
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return render_to_response('admin/invalid_setup.html', {'title': _('Database error')})
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        # additional JS
        media = self.media
        media.add_js((
            JQUERY_URL,
            "%sjs/json/json2.js" % ADMIN_MEDIA_URL,
            "%sjs/admin/Trees.js" % ADMIN_MEDIA_URL,
        ))

        context = {
            'dragdrop_allowed': self.dragdrop_allowed,       
            'title': cl.title,
            'is_popup': cl.is_popup,
            'cl': cl,
            'has_add_permission': self.has_add_permission(request),
            'app_label': app_label,
            'media': mark_safe(media),
        }
        
        return render_to_response(
            'admin/tree_change_list.html',
            context,
            context_instance=template.RequestContext(request)
        ) 
        
    def formfield_for_dbfield(self, db_field, **kwargs):
        """ applying custom widgets here! """
        field = super(HierarchyMixinAdminOptions, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'parent':
            field.widget = TreeSelectWidget(self.model, choices = field.widget.choices)
        return field        


class HierarchyMixinAdminForm(forms.ModelForm):
    """
    a validator for checking infinite loops in 
    hierarchical data defined below!
    """
    def clean_parent(self):
        # for new objects or objects with no parent, this does not matter
        parent = self.cleaned_data['parent']
        if not self.instance._get_pk_val():
            return parent

        # so this is to do when changing objects
        cid = self.instance._get_pk_val()
        if parent:
            pid = parent._get_pk_val()
        else:
            return parent
        model = self.Meta.model
        while pid:
            if pid == cid:
                raise forms.ValidationError(_("This parent is not allowed, as it creates a cyclical reference. Please select a different parent."))
            new_parent = model.objects.get(pk=pid)
            pid = new_parent.parent_id
            if pid is None:
                return parent


class ContentBaseMixinAdminOptions(PublishingMixinAdminOptions):
    save_on_top = True
    list_display = ('get_id', 'title', 'author', 'status', 'published_from', 'published_till')
    list_filter =  ('sites', 'creation_date', 'modified_date', 'creator', 'modifier')
    
    fieldsets = get_admin_lang_section(
        _("Content"),
        ['title', 'subtitle', 'short_title', 'content'],
        )
    fieldsets += [
        (_("Sites"), {
            'classes': ("collapse open",),                                             
            'fields': ('sites',),
            }),
        ]
 
    fieldsets += PublishingMixinAdminOptions.fieldsets
    
    list_display_links = ('title',)

    # callback for the additional buttons (overwritten method)
    def add_get_additional_buttons_callback(self):
        return self.change_get_additional_buttons_callback()
    
    # callback for the additional buttons actions (overwritten method)
    def add_handle_button_action_callback(self, action, obj):
        self.change_handle_button_action_callback(action, obj)

    # callback for the additional buttons (overwritten method)
    def change_get_additional_buttons_callback(self):
        return [('publish', _('Publish'))]
    
    # callback for the additional buttons actions (overwritten method)
    def change_handle_button_action_callback(self, action, obj):
        if obj:
            if action == 'publish':
                obj.status = STATUS_CODE_PUBLISHED
            # apply other actions here
            obj.save()
            
    def get_id(self, obj):
        return obj._get_pk_val()
    get_id.short_description = "ID"


class MetaTagsMixinAdminOptions(ExtendedModelAdmin):
    fieldsets = (
        (_("Meta tags"), {
            'classes': ("collapse open",),                                             
            'fields': ['meta_keywords_{}'.format(lang_code) for lang_code, lang_name in settings.LANGUAGES] +
                ['meta_description_{}'.format(lang_code) for lang_code, lang_name in settings.LANGUAGES] +
                ['meta_author', 'meta_copyright'],
        }),
    )


class SEOMixinAdminOptions(ExtendedModelAdmin):
    fieldsets = (
        (_("SEO"), {
            'classes': ("collapse closed",),                                             
            'fields': ['page_title_{}'.format(lang_code) for lang_code, lang_name in settings.LANGUAGES] +
                ['meta_keywords_{}'.format(lang_code) for lang_code, lang_name in settings.LANGUAGES] +
                ['meta_description_{}'.format(lang_code) for lang_code, lang_name in settings.LANGUAGES] +
                ['meta_author', 'meta_copyright']
        }),
    )

