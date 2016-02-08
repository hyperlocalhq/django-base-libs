from django.conf.urls import *
from base_libs.models.base_libs_settings import STATUS_CODE_PUBLISHED

all_dict = dict(
    # include=['member'],
    # only_for_this_site=True,
    slug='kreativwirtschaftsberatung_berlin',
    status=STATUS_CODE_PUBLISHED,
    # url_identifier=u'blog',
)

urlpatterns = patterns(
    # public posts
    (r'^$', 'jetson.apps.blog.views.handle_request', all_dict),
)