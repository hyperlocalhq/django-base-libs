# -*- coding: UTF-8 -*-

from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.shop_product_list, name='shop_product_list'),
    url(r'^add/$', views.add_shop_product, name='add_shop_product'),
    url(r'^(?P<slug>[^/]+)/$', views.shop_product_detail, name='shop_product_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', views.change_shop_product, name='change_shop_product'),
    url(r'^(?P<slug>[^/]+)/delete/$', views.delete_shop_product, name='delete_shop_product'),
    url(r'^(?P<slug>[^/]+)/status/$', views.change_shop_product_status, name='change_shop_product_status'),
]