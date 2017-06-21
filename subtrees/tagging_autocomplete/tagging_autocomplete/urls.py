from django.conf.urls import *

urlpatterns = patterns('tagging_autocomplete.views',
    url(r'^list/$', 'list_tags', name='tagging_autocomplete-list'),
)
