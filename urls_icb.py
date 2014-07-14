# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # root
    (
        r'^$', 
        'ccb.apps.articles.views.article_archive_index', 
        {
            'creative_sector_slug': "games-and-interactive",
            'num_latest': 5, 
            'type_sysname': 'all', 
            'template_name': "articles/articles_overview.html",
            }
        ),
    # the others
    (r'', include('ccb.urls')),
    )
