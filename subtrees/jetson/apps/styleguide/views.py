# -*- coding: utf-8 -*-
from django.shortcuts import render

from .forms import DummyForm


def page(request, page=None):

    if not page or "/" in page:
        page = "base"

    # if template for page doesn't exist, fallback to styleguide/base.html
    return render(
        request, ["styleguide/{}.html".format(page), "styleguide/base.html"]
    )


def dummy_form(request):
    if request.method == "POST":
        form = DummyForm(request.POST, request.FILES)
        if form.is_valid():
            pass
    else:
        form = DummyForm()
    return render(request, "styleguide/forms.html", {'form': form})
