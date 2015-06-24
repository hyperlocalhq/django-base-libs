# -*- coding: utf-8 -*-

from django.shortcuts import render

from forms import DummyForm

def dummy_form(request):
    if request.method == "POST":
        form = DummyForm(request.POST, request.FILES)
        if form.is_valid():
            pass
    else:
        form = DummyForm()
    return render(request, "styleguide/forms.html", {'form': form})
