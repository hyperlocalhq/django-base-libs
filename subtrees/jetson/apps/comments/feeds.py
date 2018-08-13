from django.conf import settings
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site

from jetson.apps.comments.models import Comment

class LatestCommentsFeed(Feed):
    """Feed of latest comments on the current site."""

    comments_class = Comment

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "%s comments" % self._site.name

    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % self._site.domain

    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "Latest comments on %s" % self._site.name

    def get_queryset(self):
        qs = self.comments_class.objects.filter(site__pk=settings.SITE_ID, is_public=True)
        qs = qs.filter(is_removed=False)
        group = getattr(settings, 'COMMENTS_BANNED_USERS_GROUP', '')
        if group:
            where = ['user_id NOT IN (SELECT user_id FROM auth_users_group WHERE group_id = %s)']
            params = [group]
            qs = qs.extra(where=where, params=params)
        return qs

    def items(self):
        return self.get_queryset()[:40]
    
    def item_pubdate(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return obj.submit_date
