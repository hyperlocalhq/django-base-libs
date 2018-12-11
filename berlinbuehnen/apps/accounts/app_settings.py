# -*- coding: UTF-8 -*-
from django.conf import settings

DASHBOARD_USER_GROUPS = getattr(settings, "ACCOUNTS_DASHBOARD_USER_GROUPS", [])