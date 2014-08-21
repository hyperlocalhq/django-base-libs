# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import get_object_or_404
from django import forms
from django.utils.translation import ugettext_lazy as _

from base_libs.views import access_denied
from base_libs.forms import dynamicforms

from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from base_libs.utils.misc import get_related_queryset

ShopProductCategory = models.get_model("shop", "ShopProductCategory")
ShopProductType = models.get_model("shop", "ShopProductType")
ShopProduct = models.get_model("shop", "ShopProduct")


SORT_BY_CHOICES = (
    ('a-z', _("Alphabetically")),
    ('price', _("By price")),
    ('newest', _("By creation date")),
)


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
    is_featured = forms.BooleanField(
        required=False,
    )
    is_new = forms.BooleanField(
        required=False,
    )
    is_for_children = forms.BooleanField(
        required=False,
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=SORT_BY_CHOICES,
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
            'is_featured': _("Featured"),
            'is_for_children': _("For Children"),
            'is_new': _("New"),
            'sort_by': SORT_BY_CHOICES,
        },
    }

    sort_by = "a-z"
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

        cat = form.cleaned_data['is_featured']
        if cat:
            facets['selected']['is_featured'] = cat
            qs = qs.filter(
                is_featured=cat,
            ).distinct()

        cat = form.cleaned_data['is_for_children']
        if cat:
            facets['selected']['is_for_children'] = cat
            qs = qs.filter(
                is_for_children=cat,
            ).distinct()

        cat = form.cleaned_data['is_new']
        if cat:
            facets['selected']['is_new'] = cat
            qs = qs.filter(
                is_new=cat,
            ).distinct()

        sort_by = form.cleaned_data['sort_by']
        if sort_by:
            facets['selected']['sort_by'] = (sort_by, dict(SORT_BY_CHOICES)[sort_by])

    if sort_by:
        SORT_BY_MAPPER = {
            'a-z': "title_%s" % request.LANGUAGE_CODE,
            'price': "price",
            'newest': '-creation_date',
        }
        qs = qs.order_by(SORT_BY_MAPPER[sort_by])

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
