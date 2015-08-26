# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from base_libs.models.models import UrlMixin
from base_libs.models import ViewsMixin
from base_libs.models import CreationModificationDateMixin
from jetson.apps.comments.models import Comment
from base_libs.utils.misc import get_website_url
from base_libs.models.query import ExtendedQuerySet
from base_libs.models.fields import URLField
from ccb.apps.external_services.jovoto.default_settings import JOVOTO_ROOT_DIR

verbose_name = _("Jovoto")


class IdeaManager(models.Manager):
    def get_queryset(self):
        q = ExtendedQuerySet(self.model)

        # we add a field "comments" into the queryset representing the comment count.
        idea_db_table = self.model._meta.db_table
        comment_db_table = Comment._meta.db_table
        ct = ContentType.objects.get_for_model(self.model)
        q = q.extra(
            select={
                'comments': 'SELECT COUNT(*) from %s WHERE content_type_id=%d AND object_id=%s.id' % \
                            (comment_db_table, ct.id, idea_db_table)
            }
        )
        return q

    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'published_date_desc': (1, _('Published'), ['-pubdate'],),
            'rating_desc': (2, _('Rating'), ['-rating'],),
            'discussed_desc': (3, _('Most discussed'), ['-comments'],),
            'name_asc': (4, _('Name (A-Z)'), ['name'],),
            'name_desc': (5, _('Name (Z-A)'), ['-name'],),
        }
        return sort_order_mapper

    def latest_published(self):
        return self.order_by("-pubdate", "name")

    def most_commented(self):
        return self.order_by("-comments", "name")

    def best_rated(self):
        return self.order_by("-rating", "name")


class Idea(CreationModificationDateMixin, ViewsMixin, UrlMixin):
    """
    Model to store Jovoto logo ideas in our database
    """
    ext_id = models.IntegerField(_("id"))
    name = models.CharField(_("name"), max_length=256)
    description = models.TextField(_("description"))
    pubdate = models.DateTimeField(_("publishing date"))
    link = URLField(_("link"))
    guid = URLField(_("guid"))

    author_username = models.CharField(_("author username"), max_length=256, blank=True)
    author_city = models.CharField(_("author city"), max_length=256, blank=True)
    author_country = models.CharField(_("author country"), max_length=256, blank=True)
    author_icon = models.CharField(_("author icon"), max_length=256, blank=True)

    media0_type = models.CharField(_("first media type"), max_length=256)
    media0_thumb = models.CharField(_("first media thumbnail"), max_length=256, blank=True, null=True)
    media0_medium = models.CharField(_("first media medium sized"), max_length=256, blank=True, null=True)
    media0_big = models.CharField(_("first media big sized"), max_length=256, blank=True, null=True)
    media0_path = models.CharField(_("first media originally sized"), max_length=256, blank=True, null=True)

    rating = models.DecimalField(_("rating"), max_digits=5, decimal_places=2, blank=True, null=True)

    objects = IdeaManager()

    def __unicode__(self):
        return force_unicode(self.name)

    def get_author_icon_path(self):
        return "%s%s" % (JOVOTO_ROOT_DIR, self.author_icon)

    def get_media0_thumb_path(self):
        return "%s%s" % (JOVOTO_ROOT_DIR, self.media0_thumb)

    def get_media0_medium_path(self):
        return "%s%s" % (JOVOTO_ROOT_DIR, self.media0_medium)

    def get_media0_big_path(self):
        return "%s%s" % (JOVOTO_ROOT_DIR, self.media0_big)

    def get_media0_path(self):
        return "%s%s" % (JOVOTO_ROOT_DIR, self.media0_path)

    def get_media0_thumb_image(self):
        return """<img src="%s" alt="%s" />""" % (
            self.get_media0_thumb_path(),
            self.name,
        )

    get_media0_thumb_image.allow_tags = True
    get_media0_thumb_image.short_description = _("Thumbnail")

    def get_absolute_url(self):
        # get the idea from the guid and form the link
        return "%slogo_contest/ideas/idea/%s/" % (
            get_website_url(),
            self.ext_id
        )

    def get_url_path(self):
        # get the idea from the guid and form the link
        return "%slogo_contest/ideas/idea/%s/" % (
            settings.ROOT_DIR,
            self.ext_id
        )

    def delete(self):
        """deletes the idea and all underlying comments and ratings"""
        super(Idea, self).delete()

    class Meta:
        ordering = ('-pubdate',)
