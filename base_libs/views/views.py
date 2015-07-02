# -*- coding: UTF-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.template import loader, Template, Context, RequestContext

from base_libs.utils.misc import ExtendedJSONEncoder
from base_libs.utils.misc import get_website_url
from base_libs.utils.misc import get_installed

def access_denied(request):
    t = loader.get_template("403.html")
    return HttpResponseForbidden(t.render(RequestContext(request)))

def get_object(content_type_var, field_name, field_value):
    """
    gets an object from a content_type_var 
    definied as [pkg].[module] and a specific field 
    defining the object.
    Parameters:
        content_type_var    Content Type as a string formatted as
                            [pkg].[module]
        field_name          The name of the field, in which
                            the field value (see below) is stored.
        field_value         The provided field value for looking
                            up the object.
    Returns:
        The found object or None, if no object is found
    """
    #try to resolve the content_type from {package].[module] string
    if not content_type_var:
        return None
    
    try:
        package, module = content_type_var.split('.')
        content_type = ContentType.objects.get(
           app_label__exact=package,model__exact=module
        )
    except:
        raise Http404, "content type for %s could not be resolved" % content_type_var
    
    # ensure the object identified by field_value is valid
    try: 
        obj = content_type.get_object_for_this_type(
            **{field_name:field_value}
        )
    except:
        raise Http404, "object with %s=%s does not exist" % (field_name, field_value)

    return obj

def get_object_from_url(object_url_part, **kwargs):
    """ 
    tries to identify a related object from an "objects url part".
    An url part is formed like 
    
    "<<model_identifier>>/<<object_identifier>>",
    
    for example "person/aidas". In this case, "person" would
    be an identifier for the "Person" model in the "people" app
    and "Aidas" would be the "object identifier". Here, it denotes
    the slug name of Aidas. To identify an object by it's "object_path",
    the application and the object are got from a special map and the
    corresponding model.
    
    kwargs can optionally have two additional key, value pairs:
    
    ('exclude', << a list of model_identifiers to exclude >>)
    ('include', << a list of model_identifiers to include >>)
    
    exclusion and inclusion may not be used together at the moment.  
    
    Additionally, the name of a base template associated with
    the object is got.
    Return value is a tuple (obj, base_template) or (None, None)
    
    """
    obj = None
    base_template = None
     
    if object_url_part is None or object_url_part == "":
        (model_identifier, object_identifier) = (None, None)
    else:
        (model_identifier, object_identifier) = object_url_part.strip('/').split('/')
        try:
            object_url_mapper = getattr(__import__(settings.ROOT_URLCONF, {}, {}, ['']), 'OBJECT_URL_MAPPER')
        except (ImportError, AttributeError):
            raise Http404, "Please specify an OBJECT_URL_MAPPER dict to use this function"
    
        if object_url_mapper.has_key(model_identifier):
            object_props = object_url_mapper[model_identifier]
            try:
                obj = object_props[0].objects.get(**{object_props[1]:object_identifier})
            except:
                raise Http404, "Sorry, requested object '%s' does not exist in the %s model" % (object_identifier, str(object_props[0]))
        
            base_template = object_props[2]
            
    if 'base_template' in kwargs:
        base_template = kwargs['base_template']
            
    # now test, if model is supported and allowed!
    if kwargs.has_key('include'):
        if not model_identifier in kwargs['include']:
            raise Http404, "Sorry, you are not allowed to access object '%s' in the requested application" % object_identifier
    if kwargs.has_key('exclude'):
        if model_identifier in kwargs['exclude']:
            raise Http404, "Sorry, you are not allowed to access object '%s' in the requested application" % object_identifier

    return (obj, base_template)

def get_container(container_model, site, related_obj=None, sysname=None, create=True):
    """
    gets or creates a container object for a specific model, 
    which references another object (related object)
    from a different model.
    
    Parameters:
        container_model      The model for the container
        site                 The current site
        related_object       The related object (if there is one)
        sysname              a sysname to identify the container (optional)
    """
    content_type = None
    object_id = ""
    site_id = None
    if site:
        site_id = site.id
    
    if related_obj:
        try:
            content_type = ContentType.objects.get_for_model(related_obj)
        except:
            return None
        object_id = related_obj._get_pk_val()
        
    qs = container_model.objects.filter(
       content_type__exact=content_type, # None is interpreted as IS NULL
       object_id__exact=object_id, # "" is interpreted as None
       sysname__exact=sysname, # None is interpreted as IS NULL
       )

    """
    if we have not found anything till now, create an object
    for this site!
    """
    if qs.count() == 0:
        obj = container_model(
            content_type=content_type, 
            object_id=object_id,
            sysname=sysname,
            )
        if create:
            if site:
                obj.create_for_site(site)
            else:
                obj.save()
        return obj
        
    # at last filter the site
    if container_model.is_single_site_container():
        if qs.filter(site__id=site_id).count() == 0:
            """
            no specific site found, maybe there is
            an entry with site=None (All sites)
            """
            if qs.filter(site__isnull=True).count() == 0:
                # nothing found, create a new one!
                obj = container_model(
                     content_type=content_type, 
                     object_id=object_id,
                     sysname=sysname,
                     )
                if create:
                    if site:
                        obj.create_for_site(site)
                    else:
                        obj.save()
                return obj
            else:
                return qs.filter(site__isnull=True)[0]
        else:
            return qs.filter(site__id=site_id)[0]
    else:
        # MultiSiteContainer!
        if qs.filter(sites__in=[site_id]).count() == 0:
            """
            no specific site found, maybe there is
            an entry with site=None (All sites)
            """
            if qs.filter(sites__isnull=True).count() == 0:
                """
                nothing found, create a new one!
                TODO I am not really sure, whether it is andgood idea
                to create a new entry with this site. Maybe there is 
                a better solution
                """
                obj = container_model(
                     content_type=content_type, 
                     object_id=object_id,
                     sysname=sysname,
                     )
                if create:
                    if site:
                        obj.create_for_site(site)
                    else:
                        obj.save()
                return obj
            else:
                return qs.filter(sites__isnull=True)[0]
        else:
            return qs.filter(sites__in=[site_id])[0]
        
def json_get_objects_from_contenttype(request, content_type_id):
    """Gets all objects with a given contenttype"""
    json_str = "false"
    if True:
        content_type = ContentType.objects.get(id=content_type_id)
        objs = content_type.model_class().objects.all()
        result = ( # generator of tuples to sort by second value 
            (obj._get_pk_val(), not hasattr(obj, "__unicode__") and obj._get_pk_val() or obj.__unicode__())
            for obj in objs
            )
        result = sorted(result, lambda a, b: cmp(a[1],b[1]))
        json_str = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
    else:
        pass
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')

json_get_objects_from_contenttype = never_cache(json_get_objects_from_contenttype)        

def json_objects_to_select(request, app_name, model_name, obj_pk, field_name, content_type_id):
    """
    Get object_id selection options for selected content_type at the given model editing view"""
    json_str = "false"
    model = get_object_or_404(
        ContentType, 
        app_label=app_name,
        model=model_name,
        ).model_class()
    edited_obj = obj_pk!="add" and get_object_or_404(model, pk=obj_pk) or None
    # the current user should have permission to edit current object
    if request.user.has_perm(
        "%s.change_%s" % (app_name, model_name),
        edited_obj,
        ):
        content_type = get_object_or_404(ContentType, id=content_type_id)
        # the current user should have permission to edit objects of the selected type
        if request.user.has_perm(
            "%s.change_%s" % (content_type.app_label, content_type.model),
            ):
            # get limit_choices_to for object_id from the model directly or from its inline edited children
            field_name_bits = field_name.split("-")
            if len(field_name_bits)==1:
                limit_choices_to = model._meta.get_field(field_name).limit_choices_to
            else:
                limit_choices_to = getattr(model(), field_name_bits[0]).model._meta.get_field(field_name_bits[2]).limit_choices_to
            objs = content_type.model_class().objects
            if isinstance(limit_choices_to, dict):
                objs = objs.filter(**limit_choices_to)
            else:
                objs = objs.filter(limit_choices_to)
            result = ( # generator of tuples to sort by second value 
                (obj._get_pk_val(), (not hasattr(obj, "__unicode__") and ("",) or (obj.__unicode__(),))[0])
                for obj in objs
                )
            result = sorted(result, lambda a, b: cmp(a[1].lower(),b[1].lower()))
            result = [
                (pk, text and ("%s | ID %s" % (text, pk)) or ("ID %s" % pk))
                for pk, text in result
                ]
            json_str = json.dumps(result, ensure_ascii=False, cls=ExtendedJSONEncoder)
    return HttpResponse(json_str, content_type='text/javascript; charset=utf-8')

json_objects_to_select = never_cache(json_objects_to_select)

def ajax_autocomplete(request, app, qs_function, display_attr, add_display_attr=None, limit=1000):
    """
    Method to lookup a model field and return an array. Intended for use 
    in AJAX widgets.
    """
    obj_list = []
    t = Template("")
    if 'q' in request.GET:
        search = request.GET['q']
        
        func = get_installed("%(app)s.ajax.%(func)s" % {
            'app': app,
            'func': qs_function,
            })
        queryset = func(search)

        if add_display_attr == u'None':
            add_display_attr = None
            
        for obj in queryset[:limit]:
            display = getattr(obj, display_attr)
            if callable(display) and not getattr(display, "alters_data", False):
                display = display()
                
            if add_display_attr:
                add_display = getattr(obj, add_display_attr)
                if callable(add_display) and not getattr(add_display, "alters_data", False):
                    add_display = add_display()
                obj_list.append([display, obj.pk, add_display])                                    
            else:
                obj_list.append([display, obj.pk])
                
        if add_display_attr:    
            t = Template('{% autoescape off %}{% for el in obj_list %}{{ el.0 }}|{{ el.1 }}|{{ el.2 }}\n{% endfor %}{% endautoescape %}')
        else:
            t = Template('{% autoescape off %}{% for el in obj_list %}{{ el.0 }}|{{ el.1 }}\n{% endfor %}{% endautoescape %}')
    c = Context({'obj_list': obj_list})
    r = HttpResponse(t.render(c))
    r['Content-Type'] = 'text/plain; charset=UTF-8'
    return r

