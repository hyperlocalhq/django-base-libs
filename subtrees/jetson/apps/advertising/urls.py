from django.conf.urls.defaults import *

urlpatterns = patterns(
    'jetson.apps.advertising.views',
    url(r'^view/(?P<id>[\d]+)/$', 'ad_view', name='advertising_ad_view'),
)
