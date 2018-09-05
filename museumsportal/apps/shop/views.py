# -*- coding: utf-8 -*-
import os
import shutil

from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache

from base_libs.views import access_denied
from base_libs.forms import dynamicforms
from base_libs.models.base_libs_settings import MARKUP_HTML_WYSIWYG
from base_libs.utils.misc import get_related_queryset

from jetson.apps.utils.decorators import login_required
from jetson.apps.utils.views import object_list, object_detail
from jetson.apps.utils.context_processors import prev_next_processor
from jetson.apps.image_mods.models import FileManager

from datetime import datetime, time

from forms import ShopProductForm

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

ShopProductCategory = models.get_model("shop", "ShopProductCategory")
ShopProductType = models.get_model("shop", "ShopProductType")
ShopProduct = models.get_model("shop", "ShopProduct")


SORT_BY_CHOICES = (
    ('newest', _("By creation date")),
    ('a-z', _("Alphabetically")),
    ('price', _("By price")),
)


class ProductFilterForm(dynamicforms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(),
    )
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

    sort_by = "newest"
    if form.is_valid():

        q = form.cleaned_data['q']
        if q:
            facets['selected']['q'] = q
            qs = qs.filter(
                models.Q(**{'title_%s__icontains' % settings.LANGUAGE_CODE: q}) |
                models.Q(**{'subtitle_%s__icontains' % settings.LANGUAGE_CODE: q}) |
                models.Q(**{'description_%s__icontains' % settings.LANGUAGE_CODE: q}) |
                models.Q(**{'title_%s__icontains' % request.LANGUAGE_CODE: q}) |
                models.Q(**{'subtitle_%s__icontains' % request.LANGUAGE_CODE: q}) |
                models.Q(**{'description_%s__icontains' % request.LANGUAGE_CODE: q})
            )

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
        else:
            sort_by = "newest"

    if sort_by:
        SORT_BY_MAPPER = {
            'newest': '-creation_date',
            'a-z': "title_%s" % request.LANGUAGE_CODE,
            'price': "price",
        }
        qs = qs.order_by(SORT_BY_MAPPER[sort_by])

    extra_context = {}
    extra_context['form'] = form
    extra_context['facets'] = facets

    return object_list(
        request,
        queryset=qs,
        template_name="shop/product_list.html",
        paginate_by=12,
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


@never_cache
@login_required
def add_shop_product(request):
    if not request.user.has_perm("shop.add_shopproduct"):
        return access_denied(request)
        
    if request.method == "POST":
    
        form = ShopProductForm(request.POST, request.FILES)
        
        if 'reset' in request.POST:
            return redirect("dashboard_shopproducts")
            
        if form.is_valid():
        
            instance = form.save(commit=False)
            
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            
            rel_dir = "shop/"
            
            tmp_path = form.cleaned_data['image_path']
            abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
                
            fname, fext = os.path.splitext(tmp_path)
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
            dest_path = "".join((rel_dir, filename))
            FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
            abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
                
            shutil.copy2(abs_tmp_path, abs_dest_path)
                
            os.remove(abs_tmp_path)
            instance.image = dest_path
                
            instance.save()
            form.save_m2m()

            instance.set_owner(request.user)

            return HttpResponseRedirect(reverse("dashboard_shopproducts") + "?status=%s" % instance.status)
    else:
        form = ShopProductForm()
            
    return render(request, "shop/change_product.html", {'form': form})


@never_cache
@login_required
def change_shop_product(request, slug):
    instance = get_object_or_404(ShopProduct, slug=slug)
    can_edit = False
    if request.user.has_perm("shop.change_shopproduct", instance):
        can_edit = True

    for museum in instance.museums.all():
        if request.user.has_perm("museums.change_museum", museum):
            can_edit = True
            break

    if not can_edit:
        return access_denied(request)
        
    if request.method == "POST":
        
        form = ShopProductForm(request.POST, request.FILES, instance=instance)
        
        if 'reset' in request.POST:
            instance = form.save(commit=False)
            return HttpResponseRedirect(reverse("dashboard_shopproducts") + "?status=%s" % instance.status)
        
        if form.is_valid():
        
            instance = form.save(commit=False)
            
            for lang_code, lang_name in FRONTEND_LANGUAGES:
                setattr(instance, 'description_%s_markup_type' % lang_code, MARKUP_HTML_WYSIWYG)
            
            tmp_path = form.cleaned_data['image_path']
            if tmp_path != "preset":
            
                rel_dir = "shop/"
                abs_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
                
                fname, fext = os.path.splitext(tmp_path)
                filename = datetime.now().strftime("%Y%m%d%H%M%S") + fext
                dest_path = "".join((rel_dir, filename))
                FileManager.path_exists(os.path.join(settings.MEDIA_ROOT, rel_dir))
                abs_dest_path = os.path.join(settings.MEDIA_ROOT, dest_path)
                
                shutil.copy2(abs_tmp_path, abs_dest_path)
                
                os.remove(abs_tmp_path)
                instance.image = dest_path
            
            instance.save()
            form.save_m2m()
            
            return HttpResponseRedirect(reverse("dashboard_shopproducts") + "?status=%s" % instance.status)
    else:
        form = ShopProductForm(instance=instance)
        
    return render(request, "shop/change_product.html", {'form': form, 'object': instance})


@never_cache
@login_required
def delete_shop_product(request, slug):
    instance = get_object_or_404(ShopProduct, slug=slug)

    can_delete = False
    if request.user.has_perm("shop.delete_shopproduct", instance):
        can_delete = True

    for museum in instance.museums.all():
        if request.user.has_perm("museums.change_museum", museum):
            can_delete = True
            break

    if not can_delete:
        return access_denied(request)

    if request.method == "POST" and request.is_ajax():
        instance.status = "trashed"
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())


@never_cache
@login_required
def change_shop_product_status(request, slug):
    instance = get_object_or_404(ShopProduct, slug=slug)

    can_edit = False
    if request.user.has_perm("shop.change_shopproduct", instance):
        can_edit = True

    for museum in instance.museums.all():
        if request.user.has_perm("museums.change_museum", museum):
            can_edit = True
            break

    if not can_edit:
        return access_denied(request)

    if request.method == "POST" and request.is_ajax():
        instance.status = request.POST['status']
        instance.save()
        return HttpResponse("OK")
    return redirect(instance.get_url_path())
    
    