# -*- coding: UTF-8 -*-
import datetime, time

from django.db import models
from django.template import loader
from django.http import Http404
from django.db.models.fields import DateTimeField
from django.core.urlresolvers import reverse
from django.utils.timezone import now as tz_now
from django.shortcuts import render

from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED
from base_libs.middleware import get_current_language
from base_libs.views import access_denied

from jetson.apps.utils.views import object_list

Article = models.get_model("articles", "Article")
ArticleType = models.get_model("articles", "ArticleType")

def get_articles(
    type_sysname=None,
    status=STATUS_CODE_PUBLISHED,
    only_features=False,
):
    """
    forms a queryset for Articles using some optional filters
    """
    if status == STATUS_CODE_PUBLISHED:
        queryset = Article.published_objects.select_related()
    elif status == STATUS_CODE_DRAFT:
        queryset = Article.draft_objects.select_related()
    else:
        # any status
        queryset = Article.objects.select_related()

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
    queryset = get_articles(type_sysname, status)
    queryset = queryset.exclude(views=0)
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: tz_now()})
  
    if num_latest:
        queryset = queryset.order_by('-views')[:num_latest]
    else:
        queryset = queryset.order_by('-views')
    return queryset
    
def article_archive_index(
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
    content_type=None,
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
    queryset = get_articles(type_sysname, status, only_features=only_features)
    
    # TODO!!!! check some permissions
    #if extra_context.has_key('article_filter'):
        #if extra_context['article_filter'] == 'drafts':
            #if not request.user.has_perm("blog.change_blog_posts", blog):
            #    return access_denied(request)
        
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = 'latest'
    try:
        extra_context['rel_root_dir'] = reverse("%s:article_archive" % request.LANGUAGE_CODE)
    except:
        extra_context['rel_root_dir'] = reverse("article_archive")
    
    try:
        extra_context['type'] = ArticleType.objects.get(slug=type_sysname)
    except:
        pass
    
    extra_context['most_read_articles'] = get_most_read_articles(
        type_sysname,
        status,
        )
    
    if template_name is None:
        template_name = 'articles/articles_archive.html' 
    
    # this part is taken from django/views/generic/date_based.py, 
    # function "archive_index" 
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: tz_now()})

    date_list = queryset.datetimes(date_field, 'year')[::-1]
    if not date_list and not allow_empty:
        raise Http404, "No object available"

    if date_list:
        if num_latest:
            queryset = queryset.order_by('-'+date_field)[:num_latest]
        else:
            queryset = queryset.order_by('-'+date_field)
    else:
        queryset = Article.objects.none()
        
    extra_context['date_list'] = date_list
    
    return object_list(request, queryset, 
       paginate_by=paginate_by, page=page, allow_empty=allow_empty, 
       template_name=template_name, template_loader=template_loader,
       extra_context=extra_context, context_processors=context_processors,
       template_object_name=template_object_name, content_type=content_type)

def article_archive_year(
    request,
    year,
    type_sysname=None,
    status = STATUS_CODE_PUBLISHED,
    date_field='published_from',
    paginate_by=None,
    page=None,
    allow_empty=True,
    template_name=None,
    template_loader=loader,
    extra_context=None,
    context_processors=None,
    template_object_name='article',
    content_type=None,
    allow_future=False,
    make_object_list=True,
    **kwargs
):

    """
    Context:
        date_list
            List of months in this year as a tuple: (month(datetime), has_posts(boolean))
        year
            This year
        article_list
            List of objects published in the given year
            (Only available if make_object_list argument is True)
    
     Paramters:
        status = (STATUS_CODE_DRAFT|STATUS_CODE_PUBLISHED)
                
    """
    queryset = get_articles(type_sysname, status)
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = year
    try:
        extra_context['rel_root_dir'] = reverse("%s:article_archive" % request.LANGUAGE_CODE)
    except:
        extra_context['rel_root_dir'] = reverse("article_archive")
        
    try:
        extra_context['type'] = ArticleType.objects.get(slug=type_sysname)
    except:
        pass
    
    if template_name is None:
        template_name = 'articles/articles_archive_year.html'
    
    # this part is taken from django/views/generic/date_based.py, 
    # function "archive_year" 
    now = tz_now()
    lookup_kwargs = {'%s__year' % date_field: year}

    # Only bother to check current date if the year isn't in the past and future objects aren't requested.
    if int(year) >= now.year and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    date_list = queryset.filter(**lookup_kwargs).datetimes(date_field, 'month')
    
    # build up month list for posts
    month_has_posts_list = []
    for month in date_list:
        month_has_posts_list.append((datetime.datetime(int(year), month.month, 1), True))
    
    if not date_list and not allow_empty:
        raise Http404
    if make_object_list:
        queryset = queryset.filter(**lookup_kwargs)
    else:
        queryset = Article.objects.none()

    queryset = queryset.order_by('-'+date_field)        
    
    extra_context['date_list'] = month_has_posts_list
    extra_context['year'] = year

    return object_list(request, queryset, 
        paginate_by=paginate_by, page=page, allow_empty=allow_empty,
        template_name=template_name, template_loader=template_loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=content_type,
    )

def article_archive_month(
    request,
    year,
    month,
    type_sysname=None,
    status = STATUS_CODE_PUBLISHED,
    date_field='published_from',
    paginate_by=None,
    page=None,
    allow_empty=True,
    month_format='%m',
    template_name=None,
    template_loader=loader,
    extra_context=None,
    context_processors=None,
    template_object_name='article',
    content_type=None,
    allow_future=False,
    **kwargs
):
    
    """
    Context:
        month:            (date) this month
        next_month:       (date) the first day of the next month, or None if the next month is in the future
        previous_month:   (date) the first day of the previous month
        day_list          list of days with posts
        article_list:     list of articles published in the given month
    """
    queryset = get_articles(type_sysname, status)
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = str(year)+str(month)
    try:
        extra_context['rel_root_dir'] = reverse("%s:article_archive" % request.LANGUAGE_CODE)
    except:
        extra_context['rel_root_dir'] = reverse("article_archive")
             
    try:
        extra_context['type'] = ArticleType.objects.get(slug=type_sysname)
    except:
        pass
    
    if template_name is None:
        template_name = 'articles/articles_archive_month.html'
    
    # this part is taken from django/views/generic/date_based.py, 
    # function "archive_month" 
    try:
        date = datetime.date(*time.strptime(year+month, '%Y'+month_format)[:3])
    except ValueError:
        raise Http404
    
    now = tz_now()

    # Calculate first and last day of month, for use in a date-range lookup.
    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)
    lookup_kwargs = {'%s__range' % date_field: (first_day, last_day)}

    # Only bother to check current date if the month isn't in the past and future objects are requested.
    if last_day >= now.date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    queryset = queryset.filter(**lookup_kwargs)
    if not queryset and not allow_empty:
        raise Http404

    # Calculate the next month, if applicable.
    if allow_future:
        next_month = last_day + datetime.timedelta(days=1)
    elif last_day < datetime.date.today():
        next_month = last_day + datetime.timedelta(days=1)
    else:
        next_month = None
        
    day_list = queryset.filter(**lookup_kwargs).datetimes(date_field, 'day')
    queryset = queryset.order_by('-'+date_field)      

    extra_context['month'] = date
    extra_context['next_month'] = next_month
    extra_context['previous_month'] = first_day - datetime.timedelta(days=1),
    extra_context['day_list'] = day_list

    return object_list(request, queryset, 
       paginate_by=paginate_by, page=page, allow_empty=allow_empty, 
       template_name=template_name, template_loader=template_loader,
       extra_context=extra_context, context_processors=context_processors,
       template_object_name=template_object_name, content_type=content_type)

def article_archive_day(
    request,
    year,
    month,
    day,
    type_sysname=None,
    status = STATUS_CODE_PUBLISHED,
    date_field='published_from',
    paginate_by=None,
    page=None,
    allow_empty=True,
    month_format='%m',
    day_format='%d',
    template_name=None,
    template_loader=loader,
    extra_context=None,
    context_processors=None,
    template_object_name='article',
    content_type=None,
    allow_future=False,
    **kwargs
):
    
    """
    Article daily archive view.
    
    Context:
        day:            (datetime) the day
        previous_day:   (datetime) the previous day
        next_day:       (datetime) the next day, or None if the current day is today
        article_list:   list of articles published at the given day
    """
    queryset = get_articles(type_sysname, status)
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = str(year)+str(month)        

    try:
        extra_context['rel_root_dir'] = reverse("%s:article_archive" % request.LANGUAGE_CODE)
    except:
        extra_context['rel_root_dir'] = reverse("article_archive")

    try:
        extra_context['type'] = ArticleType.objects.get(slug=type_sysname)
    except:
        pass
    
    if template_name is None:
        template_name = 'articles/articles_archive_day.html' 
    
    try:
        date = datetime.date(int(year), int(month), int(day))
    except ValueError:
        raise Http404

    model = queryset.model
    now = tz_now()

    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {'%s__range' % date_field: (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max))}
    else:
        lookup_kwargs = {date_field: date}

    # Only bother to check current date if the date isn't in the past and future objects aren't requested.
    if date >= now.date() and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    queryset = queryset.filter(**lookup_kwargs)
    if not allow_empty and not queryset:
        raise Http404

    # Calculate the next day, if applicable.
    if allow_future:
        next_day = date + datetime.timedelta(days=1)
    elif date < datetime.date.today():
        next_day = date + datetime.timedelta(days=1)
    else:
        next_day = None
        
    queryset = queryset.order_by('-'+date_field)        

    extra_context['day'] = date
    extra_context['next_day'] = next_day
    extra_context['previous_day'] = date - datetime.timedelta(days=1)

    return object_list(request, queryset, 
        paginate_by=paginate_by, page=page, allow_empty=allow_empty,
        template_name=template_name, template_loader=template_loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=content_type)


def article_object_detail(request, year, month, day, article_slug, type_sysname=None, status=STATUS_CODE_PUBLISHED,
                          date_field='published_from', month_format='%m', day_format='%d', template_name=None,
                          template_loader=loader, template_name_field=None, extra_context=None, context_processors=None,
                          template_object_name='article', content_type=None, allow_future=False, **kwargs):
    
    """
    Detail view from year/month/day/slug 

    Context:
        article:      the article to be detailed
    """
    if not extra_context:
        extra_context = {}
    queryset = get_articles(type_sysname=type_sysname, status=None)
    
    # get the requested article
    try:
        article = queryset.get(slug=article_slug)
    except:
        raise Http404
    else:
        #update the "views field"
        article.increase_views()

    if not article.is_published() and not request.user.has_perm("articles.change_article"):
        return access_denied(request)

    context_dict = extra_context

    try:
        context_dict['rel_root_dir'] = reverse("%s:article_archive" % request.LANGUAGE_CODE)
    except:
        context_dict['rel_root_dir'] = reverse("article_archive")
    
    context_dict['links_to_articles'] = queryset.exclude(
        slug=article_slug
        ).order_by("-published_from")[0:5]
        
    try:
        context_dict['type'] = ArticleType.objects.get(slug=type_sysname)
    except:
        pass
    
    if template_name is None:
        template_name = 'articles/articles_detail.html' 

    context_dict[template_object_name] = article

    return render(request, template_name, context_dict)


def article_feed(request, feed_type, article_feeds=None, type_sysname=None, status=STATUS_CODE_PUBLISHED, num_latest=5,
                 date_field='published_from', **kwargs):
    """
    wrapper for feeds
    """
    if not article_feeds:
        article_feeds = {}
    queryset = get_articles(type_sysname, status)
    queryset = queryset.order_by('-' + date_field)[:num_latest]

    if not kwargs:
        kwargs = {}
        
    feed = kwargs[feed_type]

    kwargs['queryset'] = queryset
    try:
        kwargs['type'] = ArticleType.objects.get(slug=type_sysname)
    except:
        pass
    
    return feed(**kwargs)(request)
