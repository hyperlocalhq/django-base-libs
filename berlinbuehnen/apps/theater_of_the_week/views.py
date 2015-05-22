# -*- coding: UTF-8 -*-
import datetime, time

from django.db import models
from django.template import loader
from django.http import Http404
from django.db.models.fields import DateTimeField
from django.core.urlresolvers import reverse
from django.utils.timezone import now as tz_now
from django.shortcuts import render

from base_libs.models.settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED
from base_libs.middleware import get_current_language
from base_libs.views import access_denied

from jetson.apps.utils.views import object_list

Theater = models.get_model("theater_of_the_week", "TheaterOfTheWeek")


def get_theaters(
    type_sysname=None,
    status=STATUS_CODE_PUBLISHED,
    only_features=False,
):
    """
    forms a queryset for Articles using some optional filters
    """
    if status == STATUS_CODE_PUBLISHED:
        queryset = Theater.published_objects.select_related()
    elif status == STATUS_CODE_DRAFT:
        queryset = Theater.draft_objects.select_related()
    else:
        raise NotImplementedError, "You provided an unknown status. Cannot continue."
    
    if type_sysname and type_sysname != 'all':
        queryset = queryset.filter(article_type__slug=type_sysname)
        
    if only_features:
        queryset = queryset.filter(is_featured=True)
        
    queryset = queryset.filter(models.Q(language=get_current_language()) | models.Q(language="") | models.Q(language=None))
    
    return queryset
    

def get_most_read_articles(
    type_sysname=None,
    status=STATUS_CODE_PUBLISHED,
    date_field='published_from',
    allow_future=False,
    num_latest=5
):
    """
    forms a queryset for Articles using some optional filters
    """
    queryset = get_theaters(type_sysname, status)
    queryset = queryset.exclude(views=0)
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: tz_now()})
  
    if num_latest:
        queryset = queryset.order_by('-views')[:num_latest]
    else:
        queryset = queryset.order_by('-views')
    return queryset
    

    
def theater_of_the_week_archive_index(
    request,
    type_sysname=None,
    status=STATUS_CODE_PUBLISHED,
    only_features=False,
    date_field='published_from',
    num_latest=15,
    paginate_by=None,
    page=None,
    allow_empty=True,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    context_processors=None,
    template_object_name='article',
    mimetype=None,
    allow_future=False,
    **kwargs
):
    """
    Top-level archive of article objects.

    Context:
        date_list      List of years
        article_list   List of requested articles         
    
    Paramters:
        status = (STATUS_CODE_DRAFT|STATUS_CODE_PUBLISHED)
                
    """
    queryset = get_theaters(type_sysname, status, only_features=only_features)
    
    # TODO!!!! check some permissions
    #if extra_context.has_key('article_filter'):
        #if extra_context['article_filter'] == 'drafts':
            #if not request.user.has_perm("blog.change_blog_posts", blog):
            #    return access_denied(request)
        
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = 'latest'
    try:
        extra_context['rel_root_dir'] = reverse("%s:theater_of_the_week_archive" % request.LANGUAGE_CODE)
    except:
        extra_context['rel_root_dir'] = reverse("theater_of_the_week_archive")
    
    extra_context['most_read_articles'] = get_most_read_articles(
        type_sysname,
        status,
        )
    
    if template_name is None:
        template_name = 'theater_of_the_week/theater_of_the_week_overview.html'
    
    # this part is taken from django/views/generic/date_based.py, 
    # function "archive_index" 
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: tz_now()})

    date_list = queryset.dates(date_field, 'year')[::-1]
    if not date_list and not allow_empty:
        raise Http404, "No object available"

    if date_list:
        if num_latest:
            queryset = queryset.order_by('-'+date_field)[:num_latest]
        else:
            queryset = queryset.order_by('-'+date_field)
    else:
        queryset = Theater.objects.none()
        
    extra_context['date_list'] = date_list
    
    return object_list(request, queryset, 
       paginate_by=paginate_by, page=page, allow_empty=allow_empty, 
       template_name=template_name, template_loader=template_loader,
       extra_context=extra_context, context_processors=context_processors,
       template_object_name=template_object_name, mimetype=mimetype)  
       
    
    
def theater_of_the_week_object_detail(
    request,
    year,
    month,
    day,
    theater_of_the_week_slug,
    type_sysname=None,
    status=STATUS_CODE_DRAFT,
    date_field='published_from',
    month_format='%m',
    day_format='%d',
    template_name=None,
    template_loader=loader,
    template_name_field=None,
    extra_context={},
    context_processors=None,
    template_object_name='article',
    mimetype=None,
    allow_future=False,
    **kwargs
):
    
    """
    Detail view from year/month/day/slug 

    Context:
        article:      the article to be detailed
    """
    queryset = get_theaters(type_sysname, status)
    
    # get the requested article
    try:
        article = queryset.get(slug=theater_of_the_week_slug)
    except:
        raise Http404
    else:
        #update the "views field"
        article.increase_views()
    
    context_dict = extra_context

    try:
        context_dict['rel_root_dir'] = reverse("%s:theater_of_the_week" % request.LANGUAGE_CODE)
    except:
        context_dict['rel_root_dir'] = reverse("theater_of_the_week")
    
    context_dict['links_to_articles'] = queryset.exclude(
        slug=theater_of_the_week_slug
        ).order_by("-published_from")[0:5]
    
    if template_name is None:
        template_name = 'theater_of_the_week/theater_of_the_week_object_detail.html' 

    context_dict[template_object_name] = article

    return render(request, template_name, context_dict)
    
    
    
def theater_of_the_week(request, template_name=None, template_object_name='article', type_sysname=None, status=STATUS_CODE_PUBLISHED, extra_context={}):    

    queryset = get_theaters(type_sysname, status)
    article = queryset.order_by('-published_from')[0]
    
    context_dict = extra_context
    
    if template_name is None:
        template_name = 'theater_of_the_week/theater_of_the_week_object_detail.html' 

    context_dict[template_object_name] = article

    return render(request, template_name, context_dict)
    
    

def theater_of_the_week_feed(
    request,
    feed_type,
    theater_of_the_week_feeds={},
    type_sysname=None,
    status=STATUS_CODE_PUBLISHED,
    num_latest=5,
    date_field='published_from',
    **kwargs
):
    """
    wrapper for feeds
    """
    queryset = get_theaters(type_sysname, status)
    queryset = queryset.order_by('-' + date_field)[:num_latest]

    if not kwargs:
        kwargs = {}
        
    feed = kwargs[feed_type]

    kwargs['queryset'] = queryset
    
    return feed(**kwargs)(request)