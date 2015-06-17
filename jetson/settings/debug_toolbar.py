# -*- coding: utf-8 -*-
def custom_show_toolbar(request):
    return "1" == request.COOKIES.get("DjDT", False)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': True,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'HIDE_DJANGO_SQL': True,
    'SHOW_TEMPLATE_CONTEXT': True,
    }

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    #'debug_toolbar.panels.cache.CacheDebugPanel'
    # 'memcache_toolbar.panels.memcache.MemcachePanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    )
