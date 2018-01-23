# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('museumsportal.apps.shop.views',
    url(r'^$', 'shop_product_list', name='shop_product_list'),
    url(r'^add/$', 'add_shop_product', name='add_shop_product'),
    url(r'^(?P<slug>[^/]+)/$', 'shop_product_detail', name='shop_product_detail'),
    url(r'^(?P<slug>[^/]+)/change/$', 'change_shop_product', name='change_shop_product'),
    url(r'^(?P<slug>[^/]+)/delete/$', 'delete_shop_product', name='delete_shop_product'),    
    url(r'^(?P<slug>[^/]+)/status/$', 'change_shop_product_status', name='change_shop_product_status'), 
)
