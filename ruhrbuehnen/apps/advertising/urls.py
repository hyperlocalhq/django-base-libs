from django.conf.urls import *

urlpatterns = patterns('ruhrbuehnen.apps.advertising.views',
    url(r'^view/(?P<id>[\d]+)/$', 'ad_view', name='advertising_ad_view'),
)
