# -*- coding: UTF-8 -*-
import datetime
import time

from django.apps import apps
from django.template import loader
from django.http import Http404
from django.db.models.fields import DateTimeField
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.contenttypes.models import ContentType
from base_libs.models.base_libs_settings import STATUS_CODE_DRAFT, STATUS_CODE_PUBLISHED
from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_related_queryset
from base_libs.views import access_denied
from jetson.apps.utils.views import object_list, object_detail, feed
from jetson.apps.structure.models import Term

from .forms import ArticleSearchForm

Article = apps.get_model("articles", "Article")
ArticleType = apps.get_model("articles", "ArticleType")
Category = apps.get_model("structure", "Category")


def get_articles(
        creative_sector_slug='all',
        type_sysname=None,
        status=STATUS_CODE_PUBLISHED,
        only_features=False,
        ignore_language=False,
):
    """
    forms a queryset for Articles using some optional filters
    """
    current_language = get_current_language()

    if status == STATUS_CODE_PUBLISHED:
        if current_language == "de" and not ignore_language:
            queryset = Article.site_published_objects.select_related()
        else:
            queryset = Article.site_published_objects_all_languages.select_related()
    elif status == STATUS_CODE_DRAFT:
        queryset = Article.site_draft_objects.select_related()
    else:
        raise NotImplementedError("You provided an unknown status. Cannot continue.")

    if creative_sector_slug and creative_sector_slug != 'all':
        queryset = queryset.filter(creative_sectors__slug=creative_sector_slug)

    if type_sysname and type_sysname != 'all':
        article_type = get_object_or_404(ArticleType, slug=type_sysname)
        if article_type.is_root_node():
            queryset = queryset.filter(article_type__tree_id=article_type.tree_id)
        else:
            queryset = queryset.filter(article_type=article_type)

    if only_features:
        queryset = queryset.filter(is_featured=True)

    return queryset


def get_archives(queryset):
    """
    returns a list of tuples with years and tuples of months for article archives
    e.g., (2009, ((2, "Feb"),(1, "Jan"),)),(2008, ((3, "Mar"),))
    """
    months = [_('Jan'), _('Feb'), _('Mar'), _('Apr'), _('May'), _('Jun'),
              _('Jul'), _('Aug'), _('Sep'), _('Oct'), _('Nov'), _('Dec')]
    archives = {}
    for i in queryset.dates('published_from', 'month', order="DESC"):
        year = i.year
        month = i.month
        if year not in archives:
            archives[year] = []
            archives[year].append((month, months[month - 1]))
        else:
            if month not in archives[year]:
                archives[year].append((month, months[month - 1]))
    return sorted(archives.items(), reverse=True)


def get_creative_sectors():
    """
    returns a queryset of creative sectors
    """
    return get_related_queryset(Article, "creative_sectors").filter(
        parent=None
    ).order_by("title_%s" % get_language()[:2])


def get_most_read_articles(
        creative_sector_slug,
        type_sysname=None,
        status=STATUS_CODE_PUBLISHED,
        date_field='published_from',
        allow_future=False,
        num_latest=5,
):
    """
    forms a queryset for Articles using some optional filters
    """
    queryset = get_articles(creative_sector_slug, type_sysname, status)
    queryset = queryset.exclude(views=0)
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: datetime.datetime.now()})

    if num_latest:
        queryset = queryset.order_by('-views')[:num_latest]
    else:
        queryset = queryset.order_by('-views')
    return queryset


def article_archive_index(
        request,
        creative_sector_slug,
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
        show="all",
        category_slug="",
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
    if "queryset" in kwargs:
        queryset = kwargs.pop("queryset")
    else:
        queryset = get_articles(creative_sector_slug, type_sysname, status, only_features=only_features)

    category = None
    if category_slug:
        category = Category.objects.get(slug=category_slug)

    form = ArticleSearchForm(data=request.REQUEST)
    if category:
        queryset = queryset.filter(
            categories__lft__gte=category.lft,
            categories__rght__lte=category.rght,
            categories__tree_id=category.tree_id,
        ).distinct()
    elif form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            queryset = queryset.filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()

    archives = get_archives(queryset)

    if show == "favorites":
        if not request.user.is_authenticated():
            return access_denied(request)
        tables = ["favorites_favorite"]
        condition = [
            "favorites_favorite.user_id = %d" % request.user.id,
            "favorites_favorite.object_id = articles_article.id",
            "favorites_favorite.content_type_id = %d" % ContentType.objects.get_for_model(Article).pk,
        ]
        queryset = queryset.extra(
            tables=tables,
            where=condition,
        ).distinct()


    # TODO!!!! check some permissions
    # if extra_context.has_key('article_filter'):
    # if extra_context['article_filter'] == 'drafts':
    # if not request.user.has_perm("blog.change_blog_posts", blog):
    #    return access_denied(request)

    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = 'latest'

    root_article_type = article_type = None
    try:
        article_type = extra_context['article_type'] = ArticleType.objects.get(slug=type_sysname)
        root_article_type = extra_context['root_article_type'] = extra_context['article_type'].get_root()
    except Exception:
        pass
    if root_article_type and root_article_type.slug == "interviews":
        extra_context['rel_root_dir'] = reverse("article_archive_for_interviews")
    else:
        extra_context['rel_root_dir'] = reverse("article_archive_for_news")

    try:
        extra_context['creative_sector'] = Term.objects.get(slug=creative_sector_slug)
    except Exception:
        pass

    extra_context['most_read_articles'] = get_most_read_articles(creative_sector_slug, type_sysname, status)

    if template_name is None:
        template_name = 'articles/articles_archive.html'

    # this part is taken from django/views/generic/date_based.py,
    # function "archive_index" 
    if not allow_future:
        queryset = queryset.filter(**{'%s__lte' % date_field: datetime.datetime.now()})

    date_list = queryset.dates(date_field, 'year')[::-1]
    if not date_list and not allow_empty:
        raise Http404("No object available")

    if date_list:
        queryset = queryset.order_by('-' + date_field)
        if num_latest:
            queryset = queryset[:num_latest]
    else:
        queryset = Article.objects.none()

    extra_context['form'] = form
    extra_context['archives'] = archives
    extra_context['creative_sectors'] = get_creative_sectors()
    extra_context['date_list'] = date_list
    extra_context['category'] = category
    extra_context['show'] = show
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"

    return object_list(
        request, queryset,
        paginate_by=paginate_by, page=page, allow_empty=allow_empty,
        template_name=template_name, template_loader=template_loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=content_type,
        **kwargs
    )


def article_archive_news(request, creative_sector_slug, **kwargs):
    if request.LANGUAGE_CODE == "en":
        kwargs['queryset'] = Article.site_published_objects_all_languages.news()
    else:
        kwargs['queryset'] = Article.site_published_objects.news()
    if "type_sysname" in kwargs and kwargs['type_sysname'] != 'news':
        kwargs['queryset'] = kwargs['queryset'].filter(article_type__slug=kwargs['type_sysname'])
    kwargs['httpstate_prefix'] = "news"
    return article_archive_index(request, creative_sector_slug, **kwargs)


def article_archive_interviews(request, creative_sector_slug, **kwargs):
    if request.LANGUAGE_CODE == "en":
        kwargs['queryset'] = Article.site_published_objects_all_languages.interviews()
    else:
        kwargs['queryset'] = Article.site_published_objects.interviews()
    if "type_sysname" in kwargs and kwargs['type_sysname'] != 'interviews':
        kwargs['queryset'] = kwargs['queryset'].filter(article_type__slug=kwargs['type_sysname'])
    kwargs['httpstate_prefix'] = "interviews"
    return article_archive_index(request, creative_sector_slug, **kwargs)


def article_archive_non_interviews(request, creative_sector_slug, **kwargs):
    if request.LANGUAGE_CODE == "en":
        kwargs['queryset'] = Article.site_published_objects_all_languages.non_interviews()
    else:
        kwargs['queryset'] = Article.site_published_objects.non_interviews()
    return article_archive_index(request, creative_sector_slug, **kwargs)


def article_archive_year(
        request,
        year,
        creative_sector_slug,
        type_sysname=None,
        status=STATUS_CODE_PUBLISHED,
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
    queryset = get_articles(creative_sector_slug, type_sysname, status)

    form = ArticleSearchForm(data=request.REQUEST)
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            queryset = queryset.filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()

    archives = get_archives(queryset)
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = year

    root_article_type = article_type = None
    try:
        article_type = extra_context['article_type'] = ArticleType.objects.get(slug=type_sysname)
        root_article_type = extra_context['root_article_type'] = extra_context['article_type'].get_root()
    except Exception:
        pass
    if root_article_type and root_article_type.slug == "interviews":
        extra_context['rel_root_dir'] = reverse("article_archive_for_interviews")
    else:
        extra_context['rel_root_dir'] = reverse("article_archive_for_news")

    try:
        extra_context['creative_sector'] = Term.objects.get(slug=creative_sector_slug)
    except Exception:
        pass

    if template_name is None:
        template_name = 'articles/articles_archive_year.html'

    # this part is taken from django/views/generic/date_based.py, 
    # function "archive_year" 
    now = datetime.datetime.now()
    lookup_kwargs = {'%s__year' % date_field: year}

    # Only bother to check current date if the year isn't in the past and future objects aren't requested.
    if int(year) >= now.year and not allow_future:
        lookup_kwargs['%s__lte' % date_field] = now
    date_list = queryset.filter(**lookup_kwargs).dates(date_field, 'month')

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

    queryset = queryset.order_by('-' + date_field)

    extra_context['form'] = form
    extra_context['archives'] = archives
    extra_context['creative_sectors'] = get_creative_sectors()
    extra_context['date_list'] = month_has_posts_list
    extra_context['year'] = year
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"

    kwargs.setdefault('httpstate_prefix', type_sysname)

    return object_list(
        request, queryset,
        paginate_by=paginate_by, page=page, allow_empty=allow_empty,
        template_name=template_name, template_loader=template_loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=content_type,
        **kwargs
    )


def article_archive_month(
        request,
        year,
        month,
        creative_sector_slug,
        type_sysname=None,
        status=STATUS_CODE_PUBLISHED,
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
    queryset = get_articles(creative_sector_slug, type_sysname, status)

    form = ArticleSearchForm(data=request.REQUEST)
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            queryset = queryset.filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()

    archives = get_archives(queryset)
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = str(year) + str(month)

    root_article_type = article_type = None
    try:
        article_type = extra_context['article_type'] = ArticleType.objects.get(slug=type_sysname)
        root_article_type = extra_context['root_article_type'] = extra_context['article_type'].get_root()
    except Exception:
        pass
    if root_article_type and root_article_type.slug == "interviews":
        extra_context['rel_root_dir'] = reverse("article_archive_for_interviews")
    else:
        extra_context['rel_root_dir'] = reverse("article_archive_for_news")

    try:
        extra_context['creative_sector'] = Term.objects.get(slug=creative_sector_slug)
    except Exception:
        pass

    if template_name is None:
        template_name = 'articles/articles_archive_month.html'

    # this part is taken from django/views/generic/date_based.py, 
    # function "archive_month" 
    try:
        date = datetime.date(*time.strptime(year + month, '%Y' + month_format)[:3])
    except ValueError:
        raise Http404

    now = datetime.datetime.now()

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

    day_list = queryset.filter(**lookup_kwargs).dates(date_field, 'day')
    queryset = queryset.order_by('-' + date_field)

    extra_context['form'] = form
    extra_context['archives'] = archives
    extra_context['creative_sectors'] = get_creative_sectors()
    extra_context['month'] = date
    extra_context['next_month'] = next_month
    extra_context['previous_month'] = first_day - datetime.timedelta(days=1),
    extra_context['day_list'] = day_list
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"

    kwargs.setdefault('httpstate_prefix', type_sysname)

    return object_list(
        request, queryset,
        paginate_by=paginate_by, page=page, allow_empty=allow_empty,
        template_name=template_name, template_loader=template_loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=content_type,
        **kwargs
    )


def article_archive_day(
        request,
        year,
        month,
        day,
        creative_sector_slug,
        type_sysname=None,
        status=STATUS_CODE_PUBLISHED,
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
    queryset = get_articles(creative_sector_slug, type_sysname, status)

    form = ArticleSearchForm(data=request.REQUEST)
    if form.is_valid():
        cat = form.cleaned_data['category']
        if cat:
            queryset = queryset.filter(
                categories__lft__gte=cat.lft,
                categories__rght__lte=cat.rght,
                categories__tree_id=cat.tree_id,
            ).distinct()

    archives = get_archives(queryset)
    if not extra_context:
        extra_context = {}
    extra_context['article_filter'] = str(year) + str(month)

    root_article_type = article_type = None
    try:
        article_type = extra_context['article_type'] = ArticleType.objects.get(slug=type_sysname)
        root_article_type = extra_context['root_article_type'] = extra_context['article_type'].get_root()
    except Exception:
        pass
    if root_article_type and root_article_type.slug == "interviews":
        extra_context['rel_root_dir'] = reverse("article_archive_for_interviews")
    else:
        extra_context['rel_root_dir'] = reverse("article_archive_for_news")

    try:
        extra_context['creative_sector'] = Term.objects.get(slug=creative_sector_slug)
    except Exception:
        pass

    if template_name is None:
        template_name = 'articles/articles_archive_day.html'

    try:
        date = datetime.date(int(year), int(month), int(day))
    except ValueError:
        raise Http404

    model = queryset.model
    now = datetime.datetime.now()

    if isinstance(model._meta.get_field(date_field), DateTimeField):
        lookup_kwargs = {'%s__range' % date_field: (
            datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max))}
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

    queryset = queryset.order_by('-' + date_field)

    extra_context['form'] = form
    extra_context['archives'] = archives
    extra_context['creative_sectors'] = get_creative_sectors()
    extra_context['day'] = date
    extra_context['next_day'] = next_day
    extra_context['previous_day'] = date - datetime.timedelta(days=1)
    if request.is_ajax():
        extra_context['base_template'] = "base_ajax.html"

    kwargs.setdefault('httpstate_prefix', type_sysname)

    return object_list(
        request, queryset,
        paginate_by=paginate_by, page=page, allow_empty=allow_empty,
        template_name=template_name, template_loader=template_loader,
        extra_context=extra_context, context_processors=context_processors,
        template_object_name=template_object_name, content_type=content_type,
        **kwargs
    )


def article_object_detail(
        request,
        year,
        month,
        day,
        creative_sector_slug,
        article_slug,
        type_sysname=None,
        status=STATUS_CODE_PUBLISHED,
        date_field='published_from',
        month_format='%m',
        day_format='%d',
        template_name=None,
        template_loader=loader,
        template_name_field=None,
        extra_context=None,
        context_processors=None,
        template_object_name='article',
        content_type=None,
        allow_future=False,
        **kwargs
):
    """
    Detail view from year/month/day/slug 

    Context:
        article:      the article to be detailed
    """
    queryset = get_articles(creative_sector_slug, type_sysname, status, ignore_language=True)
    archives = get_archives(queryset)

    # get the requested article to update the "views field"
    try:
        article = queryset.get(slug=article_slug)
    except Exception:
        return redirect("article_archive_for_news")
    else:
        article.increase_views()

    if not extra_context:
        extra_context = {}

    extra_context['links_to_articles'] = queryset.filter(
        article_type=article.article_type,
    ).exclude(
        slug=article_slug,
    ).order_by("-published_from")[0:5]

    root_article_type = article_type = None
    try:
        article_type = extra_context['article_type'] = ArticleType.objects.get(slug=type_sysname)
        root_article_type = extra_context['root_article_type'] = extra_context['article_type'].get_root()
    except Exception:
        pass
    if root_article_type and root_article_type.slug == "interviews":
        extra_context['rel_root_dir'] = reverse("article_archive_for_interviews")
    else:
        extra_context['rel_root_dir'] = reverse("article_archive_for_news")

    try:
        extra_context['creative_sector'] = Term.objects.get(slug=creative_sector_slug)
    except Exception:
        pass
    extra_context['archives'] = archives
    extra_context['creative_sectors'] = get_creative_sectors()

    if template_name is None:
        template_name = 'articles/articles_detail.html'

    kwargs.setdefault('httpstate_prefix', type_sysname)

    return object_detail(
        request, queryset, year, month, day,
        object_id=None,
        slug=article_slug,
        slug_field='slug',
        template_name=template_name,
        template_name_field=template_name_field,
        template_loader=template_loader,
        extra_context=extra_context,
        context_processors=context_processors,
        template_object_name=template_object_name,
        content_type=content_type,
        **kwargs
    )


def article_feed(
        request,
        feed_type,
        creative_sector_slug,
        type_sysname=None,
        status=STATUS_CODE_PUBLISHED,
        num_latest=20,
        date_field='published_from',
        category_slug="",
        **kwargs
):
    """
    wrapper for feeds
    """
    queryset = get_articles(creative_sector_slug, type_sysname, status)

    category = None
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        kwargs['category'] = category

    if category:
        queryset = queryset.filter(
            categories__lft__gte=category.lft,
            categories__rght__lte=category.rght,
            categories__tree_id=category.tree_id,
        ).distinct()

    try:
        kwargs['article_type'] = ArticleType.objects.get(slug=type_sysname)
        kwargs['root_article_type'] = kwargs['article_type'].get_root()
    except Exception:
        pass

    try:
        kwargs['creative_sector'] = Term.objects.get(slug=creative_sector_slug)
    except Exception:
        pass

    queryset = queryset.order_by('-' + date_field)[:num_latest]
    kwargs['queryset'] = queryset

    return feed(request, feed_type, **kwargs)


def magazine_overview(request):
    from ccb.apps.blog.models import Post
    context = {
        'articles_under_player_of_the_week': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="player-of-the-week",
        ).order_by("-importance_in_magazine"),
        'articles_under_when_i_moved_to_berlin': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="when-i-moved-to-berlin",
        ).order_by("-importance_in_magazine"),
        'articles_under_innovation_and_vision': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="innovation-and-vision",
        ).order_by("-importance_in_magazine"),
        'articles_under_at_home_with': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="at-home-with",
        ).order_by("-importance_in_magazine"),
        'articles_under_knowledge_and_analysis': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="knowledge-and-analysis",
        ).order_by("-importance_in_magazine"),
        'articles_under_specials': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="specials",
        ).order_by("-importance_in_magazine"),
        'articles_under_articles_from_our_network_partners': get_articles().filter(
            featured_in_magazine=True,
            article_type__slug="articles-from-our-network-partners",
        ).order_by("-importance_in_magazine"),
        'blog_posts': Post.published_objects.featured_in_magazine(),
    }
    return render(request, "articles/magazine_overview.html", context)


def magazine_blog_posts(request):
    from ccb.apps.blog.models import Post
    queryset = Post.published_objects.order_by("-published_from")
    article_type = ArticleType.objects.get(slug="interviews")
    form = ArticleSearchForm(data=request.REQUEST)
    context = {
        'root_article_type': article_type,
        'article_type': article_type,
        'form': form,
    }
    return object_list(
        request, queryset,
        paginate_by=24,
        allow_empty=True,
        template_name="articles/magazine_blog_posts.html",
        extra_context=context,
        template_object_name='blog_post',
    )
