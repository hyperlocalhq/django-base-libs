# -*- coding: utf-8 -*-

from django.db import models
from django.shortcuts import get_object_or_404
from django import forms

from base_libs.views import access_denied
from base_libs.forms import dynamicforms

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from base_libs.utils.misc import get_related_queryset

ShopProductCategory = models.get_model("shop", "ShopProductCategory")
ShopProductType = models.get_model("shop", "ShopProductType")
ShopProduct = models.get_model("shop", "ShopProduct")


class ProductFilterForm(dynamicforms.Form):
    category = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(ShopProduct, "product_categories"),
        to_field_name="slug",
    )
    product_type = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(ShopProduct, "product_types").filter(parent=None),
        to_field_name="slug",
    )
    product_subtype = forms.ModelChoiceField(
        required=False,
        queryset=get_related_queryset(ShopProduct, "product_types").exclude(parent=None),
        to_field_name="slug",
    )


def shop_product_list(request):
    qs = ShopProduct.objects.filter(status="published")
    qs = qs.order_by("title_%s" % request.LANGUAGE_CODE)

    form = ProductFilterForm(data=request.REQUEST)

    facets = {
        'selected': {},
        'categories': {
            'categories': get_related_queryset(ShopProduct, "product_categories"),
            'product_types': get_related_queryset(ShopProduct, "product_types").filter(parent=None),
            'product_subtypes': get_related_queryset(ShopProduct, "product_types").exclude(parent=None),
        },
    }

    if form.is_valid():

        cat = form.cleaned_data['category']
        if cat:
            facets['selected']['category'] = cat
            qs = qs.filter(
                product_categories=cat,
            ).distinct()

        cat = form.cleaned_data['product_type']
        if cat:
            facets['selected']['product_type'] = cat
            qs = qs.filter(
                product_types=cat,
            ).distinct()

        cat = form.cleaned_data['product_subtype']
        if cat:
            facets['selected']['product_subtype'] = cat
            qs = qs.filter(
                product_types=cat,
            ).distinct()

    extra_context = {}
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="shop/product_list.html",
        paginate_by=24,
        httpstate_prefix="products_list",
        context_processors=(prev_next_processor,),
        extra_context=extra_context,
    )
    
    
def shop_product_detail(request, slug):
    if "preview" in request.REQUEST:
        qs = ShopProduct.objects.all()
        obj = get_object_or_404(qs, slug=slug)
        if not request.user.has_perm("shop.change_shopproduct", obj):
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
