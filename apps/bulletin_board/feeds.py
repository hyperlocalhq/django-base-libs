# -*- coding: UTF-8 -*-

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from models import Bulletin, TYPE_CHOICES
from forms import BulletinSearchForm


class BulletinFeed(Feed):
    description_template = 'bulletin_board/feeds/bulletin_description.html'

    def __init__(self, category_slug=None, *args, **kwargs):
        super(BulletinFeed, self).__init__(*args, **kwargs)
        self.category_slug = category_slug

    def get_object(self, request):
        form = BulletinSearchForm(data=request.REQUEST)
        context = {}
        if form.is_valid():
            context = {
                'bulletin_type': form.cleaned_data['bulletin_type'],
                'category': form.cleaned_data['category'],
                'query_string': request.META['QUERY_STRING'],
            }
        return context

    def title(self, obj):
        t = u"Kreatives Brandenburg - Projektbörse"
        if obj.get('bulletin_type', False):
            t += u" - %s" % dict(TYPE_CHOICES)[obj['bulletin_type']]
        if obj.get('category', False):
            t += u" - %s" % obj['category'].title
        return t

    def link(self, obj):
        if obj.get('query_string', False):
            return reverse('bulletin_list') + "?" + obj['query_string']
        return reverse('bulletin_list')

    def feed_url(self, obj):
        if obj.get('query_string', False):
            return reverse('bulletin_rss') + "?" + obj['query_string']
        return reverse('bulletin_rss')

    def item_pubdate(self, item):
        return item.published_from or item.creation_date

    def items(self, obj):
        qs = Bulletin.published_objects.order_by("-published_from", "-creation_date")
        if self.category_slug:
            qs = qs.filter(categories__slug=self.category_slug)
        if obj.get('bulletin_type', False):
            qs = qs.filter(
                bulletin_type=obj['bulletin_type'],
            ).distinct()
        if obj.get('category', False):
            qs = qs.filter(
                category=obj['category'],
            ).distinct()
        return qs[:30]