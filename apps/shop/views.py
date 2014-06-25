# -*- coding: utf-8 -*-

from django.db import models
from django.shortcuts import get_object_or_404

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.context_processors import prev_next_processor



ShopProductCategory = models.get_model("shop", "ShopProductCategory")
ShopProductType = models.get_model("shop", "ShopProductType")
ShopProduct = models.get_model("shop", "ShopProduct")


def shop_products_list(request):

    qs = ShopProduct.objects.filter(status="published")
    qs = qs.order_by("title_%s" % request.LANGUAGE_CODE)
    
    first_page_delta = 0

    return object_list(
        request,
        queryset=qs,
        template_name="shop/products_list.html",
        paginate_by=24,
        httpstate_prefix="products_list",
        context_processors=(prev_next_processor,),
        first_page_delta=first_page_delta,
    )
    
    
def shop_product(request, slug):

    if "preview" in request.REQUEST:
        qs = ShopProduct.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("shop.change_shopProduct", obj):
            return access_denied(request)
    else:
        qs = ShopProduct.objects.filter(status="published")

    return object_detail(
        request,
        queryset=qs,
        slug=slug,
        slug_field="slug",
        template_name="shop/product_detail.html",
        context_processors=(prev_next_processor,),
    )

    