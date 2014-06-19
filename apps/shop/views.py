# -*- coding: utf-8 -*-

from django.db import models


from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.context_processors import prev_next_processor



ShopProductCategory = models.get_model("shop", "ShopProductCategory")
ShopProductType = models.get_model("shop", "ShopProductType")
ShopProduct = models.get_model("shop", "ShopProduct")


def shop_products_list(request):

    qs = ShopProduct.objects.all()
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
    
    
def shop_product(request, product_id):

    qs = ShopProduct.objects.all()

    return object_detail(
        request,
        queryset=qs,
        slug=product_id,
        slug_field="id",
        template_name="shop/product_detail.html",
        context_processors=(prev_next_processor,),
    )

    