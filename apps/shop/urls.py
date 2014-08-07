# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.shop.views',
    url(r'^$', 'shop_product_list', name='shop_product_list'),
    url(r'^(?P<slug>[^/]+)/$', 'shop_product_detail', name='shop_product_detail'),
)
