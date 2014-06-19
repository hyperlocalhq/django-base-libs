# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.shop.views',
    url(r'^$', 'shop_products_list', name='shop_products_list'),
    url(r'^(?P<product_id>\d+)/$', 'shop_product', name='shop_product'),
)
