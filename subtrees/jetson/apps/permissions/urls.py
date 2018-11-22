from django.conf import settings
from django.conf.urls import *

from base_libs.utils.misc import path_in_installed_app

urlpatterns = patterns(
    '',
    url(
        '',
        path_in_installed_app('permissions.views.manage_row_level_permissions'),
        name="manage_row_level_permissions",
    ),
)
