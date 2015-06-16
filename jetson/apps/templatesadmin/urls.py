from django.conf.urls import *

urlpatterns = patterns('jetson.apps.templatesadmin.views',
    url(r'^$', 'overview', name='templatesadmin-overview'),
    url(r'^edit/(?P<path>.*)/$', 'edit', name='templatesadmin-edit'),
)
