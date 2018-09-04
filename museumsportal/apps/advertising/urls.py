from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^view/(?P<id>[\d]+)/$', views.ad_view, name='advertising_ad_view'),
]
