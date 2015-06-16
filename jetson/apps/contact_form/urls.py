# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.conf import settings
from django.views.generic import TemplateView

from base_libs.utils.misc import path_in_installed_app

contact_form_done_dict = {'template': 'contact_form/contact_form_done.html'}

urlpatterns = patterns('',
    (
        r'^alldone/$',
        TemplateView.as_view(template_name='contact_form/contact_form_done.html'),
    ),
    (
        r'^(?P<slug>[-\w]+)/$',
        path_in_installed_app("contact_form.views.process_contact_form"),
    ),
    (
        r'^(?P<slug>[-\w]+)/alldone/$',
        TemplateView.as_view(template_name='contact_form/contact_form_done.html'),
    ),
    (
        r'^$',
        path_in_installed_app("contact_form.views.process_contact_form"),
    ),
)
