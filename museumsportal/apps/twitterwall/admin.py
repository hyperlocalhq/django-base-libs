# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base_libs.admin import ExtendedModelAdmin

SearchSettings = models.get_model("twitterwall", "SearchSettings")
UserTimelineSettings = models.get_model("twitterwall", "UserTimelineSettings")
TwitterUser = models.get_model("twitterwall", "TwitterUser")
Tweet = models.get_model("twitterwall", "Tweet")
TweetMedia = models.get_model("twitterwall", "TweetMedia")

class SearchSettingsAdmin(ExtendedModelAdmin):
    pass

class UserTimelineSettingsAdmin(ExtendedModelAdmin):
    pass

class TwitterUserAdmin(ExtendedModelAdmin):
    pass

class TweetMediaAdminInline(admin.StackedInline):
    model = TweetMedia
    extra = 0

class TweetAdmin(ExtendedModelAdmin):
    list_display = ('creation_date', 'user', 'get_text', 'is_geoposition_set', 'status')
    list_filter = ('status', 'by_user', 'from_search', 'creation_date')
    search_fields = ('id_str', 'text')
    inlines = [TweetMediaAdminInline]
    fieldsets = [
        (_("Main data"), {'fields': ('id', 'id_str', 'creation_date', 'user', 'text', 'html')}),
        (_("Geoposition"), {'fields': ('latitude', 'longitude')}),
        (_("Publishing"), {'fields': ('from_search', 'by_user', 'status')}),
    ]
    def get_text(self, obj):
        return obj.text
    get_text.allow_tags = True
    get_text.short_description = _("Text")
    
    def is_geoposition_set(self, obj):
        if obj.latitude:
            return '<img alt="True" src="%sgrappelli/img/admin/icon-yes.gif" />' % settings.STATIC_URL
        return '<img alt="False" src="%sgrappelli/img/admin/icon-no.gif">' % settings.STATIC_URL
    is_geoposition_set.allow_tags = True
    is_geoposition_set.short_description = _("Geoposition?")

admin.site.register(SearchSettings, SearchSettingsAdmin)
admin.site.register(UserTimelineSettings, UserTimelineSettingsAdmin)
admin.site.register(TwitterUser, TwitterUserAdmin)
admin.site.register(Tweet, TweetAdmin)

