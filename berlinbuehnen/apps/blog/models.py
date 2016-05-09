# -*- coding: UTF-8 -*-
from datetime import datetime

from django.db import models
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from tagging.fields import TagField
from tagging.models import Tag
from tagging_autocomplete.models import TagAutocompleteField

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models.models import ViewsMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import MultiSiteContainerMixin
from base_libs.models.models import PublishingMixin
from base_libs.models import ExtendedTextField

RowLevelPermission = models.get_model("permissions", "RowLevelPermission")

Comment = models.get_model("comments", "Comment")

verbose_name = _("Blog")

class Blog(MultiSiteContainerMixin, CreationModificationDateMixin):
    """ 
    This is the container for blog posts 
    """
    title = models.CharField(_("title"), blank=True, max_length=255)
    row_level_permissions = True
    
    def __unicode__(self):
        sites_str = ", ".join([str(item.name) for item in self.sites.all()])
        if sites_str != "":
            sites_str = u" (%s)" % sites_str
        return force_unicode(self.title) + sites_str
    
    def save(self, *args, **kwargs):
        content_object = self.content_object
        is_new = not self.id
        # get the title from content object (if there is one)
        if not self.title:
            if content_object:
                self.title = force_unicode(_("Blog for %s") % force_unicode(content_object))
            else:
                self.title = force_unicode(_("Blog"))
            
        super(Blog, self).save(*args, **kwargs)
        if is_new:
            if hasattr(content_object, "get_representatives"):
                owners = content_object.get_representatives()
                for owner in owners:
                    RowLevelPermission.objects.create_row_level_permission(self, owner, "add_blog_posts")
                    RowLevelPermission.objects.create_row_level_permission(self, owner, "change_blog_posts")
                    RowLevelPermission.objects.create_row_level_permission(self, owner, "delete_blog_posts")
                    RowLevelPermission.objects.create_row_level_permission(self, owner, "moderate_blog_comments")
    save.alters_data = True
    
    class Meta(MultiSiteContainerMixin.Meta):
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")
        ordering = ('title',)
        permissions = (
            ("add_blog_posts", "Can add posts"),
            ("change_blog_posts", "Can change posts"),
            ("delete_blog_posts", "Can delete posts"),
            ("moderate_blog_comments", "Can moderate blog comments"),
        )

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)

    def get_url_path(self):
        return reverse('blog_index')

# QUICK HACK: Without the following the Blog.objects.model will be MultiSiteContainerMixin and won't work correctly
Blog.objects.model = Blog

class Post(CreationModificationMixin, PublishingMixin, ViewsMixin, UrlMixin, SlugMixin()):
    title = models.CharField(_("title"), max_length=255)
    tags = TagAutocompleteField(verbose_name=_("tags"))
    body = ExtendedTextField(_("body"))
    blog = models.ForeignKey(Blog, related_name="blog")
    enable_comment_form = models.BooleanField(_('enable comment form'), default=True)
  
    def __unicode__(self):
        return force_unicode(self.title)
        
    def is_rest(self):
        """
        sort of a temp function to allow testing/switching between markdown
        and rest
        """
        return self.body.startswith('..')
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
    
    def get_absolute_url(self):
        return self.get_url_path()

    def get_url_path(self):
        return "%s%s" % (
            self.blog.get_url_path(),
            self.get_relative_url(),
        )

    def get_relative_url(self):
        return "%s/%s/" % (self.published_from.strftime("%Y/%m/%d").lower(), self.slug)
    
    def delete_comments(self):
        table = Comment._meta.db_table
        ctype = ContentType.objects.get_for_model(Post)
        query = """DELETE FROM %s WHERE object_id = %s AND content_type_id = %%s""" % (table, self.id)
        cursor = connection.cursor()
        cursor.execute(query, [ctype.id])
    delete_comments.alters_data = True
                
    def delete_comment(self, id):
        table = Comment._meta.db_table
        query = """DELETE FROM %s WHERE id = %s""" % (table, id)
        cursor = connection.cursor()
        cursor.execute(query)
    delete_comment.alters_data = True

    class Meta:
        verbose_name = _("blog post")
        verbose_name_plural = _("blog posts")
        get_latest_by = 'published_from'
        ordering = ('-published_from',)

    def get_newer_published(self):
        try:
            return Post.published_objects.filter(
                published_from__gt=self.published_from,
                pk__gt=self.pk,
                blog=self.blog,
                ).order_by("published_from")[0]
        except:
            return None
            
    def get_older_published(self):
        try:
            return Post.published_objects.filter(
                published_from__lt=self.published_from,
                pk__lt=self.pk,
                blog=self.blog,
                ).order_by("-published_from")[0]
        except:
            return None
            
    def get_previous_item(self):
        previous_items = Blog.published_objects.filter(
            blog=self.blog,
            published_from__lt=self.published_from,
        ).order_by("-published_from")[:1]
        if previous_items:
            return previous_items[0]
        return None

    def get_next_item(self):
        next_items = Blog.published_objects.filter(
            blog=self.blog,
            published_from__gt=self.published_from,
        ).order_by("published_from")[:1]
        if next_items:
            return next_items[0]
        return None