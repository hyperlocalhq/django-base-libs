# -*- coding: UTF-8 -*-
from datetime import datetime
from rest.client import webcall

from django.conf import settings
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from django.db.models import Q
from django.views.decorators.cache import never_cache

from base_libs.utils.misc import string_to_datetime
from base_libs.views import access_denied

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.decorators import login_required
from jetson.apps.comments.views.comments import post_comment, refuse_comment
from jetson.apps.comments.views.comments import accept_comment, mark_as_spam_comment

from ccb.apps.external_services.jovoto.models import Idea
from ccb.apps.external_services.jovoto.xmlparse import parse_idea_list
from ccb.apps.external_services.jovoto.xmlparse import parse_idea_details
from ccb.apps.external_services.jovoto.default_settings import JOVOTO_ROOT_DIR
from ccb.apps.external_services.jovoto.default_settings import JOVOTO_NOF_REQUEST_RETRIES
from ccb.apps.external_services.jovoto.default_settings import IDEA_DATE_FORMAT
from ccb.apps.external_services.jovoto.default_settings import JOVOTO_SERVICE_USERNAME
from ccb.apps.external_services.jovoto.default_settings import JOVOTO_SERVICE_PASSWORD
from ccb.apps.external_services.jovoto.default_settings import JOVOTO_WEBSERVICE

def get_idea_list():
    """
    gets the list of ideas from the jovoto webservices
    and update the model. (This should be called by a cron job)
    """
    # the webservice client
    @webcall(url=JOVOTO_WEBSERVICE)
    def rest_get_all_ideas(): 
        pass
    xml = smart_str(rest_get_all_ideas())
    idea_list = parse_idea_list(xml)
    
    before_modify_date = datetime.now()
    
    # update the model
    for idea_data in idea_list:
        try:
            idea = Idea.objects.get(guid=idea_data['guid'])
        except:
            idea = Idea(guid = idea_data['guid'])

        # the ext_id represents the external idea id and is parsed from the guid
        idea.ext_id = int((idea_data['guid'].split('/')[-1].split('.'))[-2])
        idea.name = idea_data['name']
        idea.description = idea_data['description']
        
        idea.pubdate = string_to_datetime(idea_data['pubdate'], IDEA_DATE_FORMAT)
        
        idea.link = idea_data['link']
        
        if idea_data['rating'] == "":
            idea.rating = None
        else:
            idea.rating = idea_data['rating']
        
        idea.author_username = idea_data['author_username']
        idea.author_city = idea_data['author_city']
        idea.author_country = idea_data['author_country']
        idea.author_icon = idea_data['author_icon']
        
        idea.media0_type = idea_data['media0_type']
        idea.media0_thumb = idea_data['media0_thumb']
        idea.media0_medium = idea_data['media0_medium']
        idea.media0_big = idea_data['media0_big']
        idea.media0_path = idea_data['media0_path']
        idea.save()

    # delete ideas, which are no longer in the idea list.
    # we conclude that from "before_modify_date" (see above)
    ideas_to_delete = Idea.objects.filter(
        (Q(modified_date__isnull=False) & Q(modified_date__lt=before_modify_date)) |
        (Q(modified_date__isnull=True) & Q(creation_date__lt=before_modify_date))
    )

    for idea in ideas_to_delete:
        idea.delete()

def get_all_ideas(request, **kwargs):
    """
    get all ideas from the jovoto rest web services
    """
    queryset = Idea.objects.all()
    
    extra_context = kwargs.get('extra_context', {})
    extra_context['source_list'] = "logo_contest/ideas"
    
    kwargs["extra_context"] = extra_context  
    kwargs['queryset'] = queryset
    
    return object_list(request, **kwargs)

def get_idea(request, ext_id, retry_count=0, **kwargs):
    """
    gets the details of an idea directly from 
    the jovoto web services.
    """
    try:
        idea = get_object_or_404(Idea, ext_id=ext_id)
    
        # we must form the correct url for the idea details here!
        url_part = idea.guid.split("http://")[1]
        url = 'http://%s:%s@%s' % (JOVOTO_SERVICE_USERNAME, JOVOTO_SERVICE_PASSWORD, url_part)
    
        extra_context = kwargs.get('extra_context', {})
        
        @webcall(url=url)
        def rest_get_idea_details(): 
            pass
        
        xml = smart_str(rest_get_idea_details().strip())
        if xml and xml != "HTTP Basic: Access denied.":
            idea_details = parse_idea_details(xml)
            idea_details['pubdate'] = string_to_datetime(idea_details['pubdate'], IDEA_DATE_FORMAT)
            extra_context['idea_details'] = idea_details
        
        extra_context['jovoto_root_dir'] = JOVOTO_ROOT_DIR
        
        kwargs['queryset'] = Idea.objects.all()
        kwargs['extra_context'] = extra_context
    
        # object_id is needed for the generic object_detail view
        kwargs['object_id'] = idea.id
        return object_detail(request, **kwargs)        
        
    except:
        if retry_count >= JOVOTO_NOF_REQUEST_RETRIES:
            #raise Http404, "The requested object is not available"
            raise 
        else:
            return get_idea(request, ext_id, retry_count+1, **kwargs)
            
@never_cache
def idea_post_comment(request, ext_id, template_name=None, extra_context=None, use_ajax=False, **kwargs):
    """
    handles posting a comment
    """
    obj = Idea.objects.get(ext_id=ext_id)
    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj
        
    extra_context[settings.REDIRECT_FIELD_NAME] = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    
    if template_name is None:
        template_name='external_services/jovoto/comments/form.html'
    
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')

    if request.method == 'POST':
        if request.POST.has_key('post'):
            post_comment(request, template_name=template_name, use_ajax=use_ajax)
            if not use_ajax:
                redirect_to = redirect_to + "#comments"
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse("reload")
                
        # the normal preview is done ...
        elif request.POST.has_key('preview'):
            return post_comment(request, template_name=template_name, use_ajax=use_ajax, extra_context=extra_context)
            
        #cancel
        else:
            if not use_ajax:
                redirect_to = redirect_to + "#comments"
                return HttpResponseRedirect(redirect_to)
            
    from django.template import Template
    # we need to get the post from the post_slug ...
    extra_context['idea'] = Idea.objects.get(ext_id=ext_id)   
    t = Template("""
        {% load comments %}
        {% comment_form using template_name for external_services.jovoto.idea idea.id %}
        """)
    c = RequestContext(request, extra_context)
    return HttpResponse(t.render(c))

def idea_refuse_comment(
        request, ext_id, comment_id, template_name=None, 
        extra_context=None, use_popup=False, **kwargs):
    """
    Displays the delete comment form and handles the associated action
    """
    # TODO check permissions

    # currently, we only check for "user is staff"
    if not request.user.is_staff:
        return access_denied(request)
    
    obj = Idea.objects.get(ext_id=ext_id)
    
    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj
        
    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if redirect_to == '':
        redirect_to = request.path.split('comment')[0]        
    
    extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
    extra_context['object'] = obj
    
    if template_name is None:
        template_name='external_services/jovoto/comments/refuse.html'
    return refuse_comment(request, comment_id, template_name, redirect_to, extra_context, use_popup)   

def idea_accept_comment(
        request, ext_id, comment_id, template_name=None, 
        extra_context=None, use_popup=False, **kwargs):
    """
    Displays the accept comment form and handles the associated action
    """
  
    # check permissions
    if not request.user.is_staff:
        return access_denied(request)

    
    obj = Idea.objects.get(ext_id=ext_id)
    
    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj

    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if redirect_to == '':
        redirect_to = request.path.split('comment')[0]        
    
    extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
    extra_context['object'] = obj
    
    if template_name is None:
        template_name='external_services/jovoto/comments/accept.html'    
    return accept_comment(request, comment_id, template_name, redirect_to, extra_context, use_popup)

def idea_mark_as_spam_comment(
        request, ext_id, comment_id, template_name=None, 
        extra_context=None, use_popup=False, **kwargs):
    """
    Displays the "mark as spam" comment form and handles the associated action
    """
    # check permissions
    if not request.user.is_staff:
        return access_denied(request)
    
    obj = Idea.objects.get(ext_id=ext_id)
    
    if extra_context is None:
        extra_context = {}
    if obj:
        extra_context['object'] = obj

    redirect_to = request.REQUEST.get(settings.REDIRECT_FIELD_NAME, '')
    if redirect_to == '':
        redirect_to = request.path.split('comment')[0]        
    
    extra_context[settings.REDIRECT_FIELD_NAME] = redirect_to
    extra_context['object'] = obj
    
    if template_name is None:
        template_name='external_services/jovoto/comments/markasspam.html'    
    
    return mark_as_spam_comment(request, comment_id, template_name, redirect_to, extra_context, use_popup)     
 