from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.advertising.views',
    url(r'^view/(?P<id>[\d]+)/$', 'ad_view', name='advertising_ad_view'),
)
