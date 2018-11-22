# -*- coding: UTF-8 -*-
import sys

from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import force_unicode
from django.conf import settings
from django.utils.html import strip_tags

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models import ViewsMixin
from base_libs.models import CreationModificationMixin
from base_libs.models import CreationModificationDateMixin
from base_libs.models import MultiSiteContainerMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models import ExtendedTextField
from base_libs.utils.misc import get_translation
from base_libs.utils.misc import truncwords

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey

verbose_name = _("Forum")

STATUS_CODE_DRAFT = 1
STATUS_CODE_PUBLIC = 0

STATUS_CODES_CHOICES = (
    (STATUS_CODE_DRAFT, _("Draft")),
    (STATUS_CODE_PUBLIC, _("Published")),
)

#TODO
FORUM_PERMISSIONS = (
    (
        'can_apply_forum_options',
        'Can apply global options to all forums under the forum container'
    ),
    ('can_set_forum_status', 'Can set the status of a forum'),
    ('can_moderate', 'Can moderate the forum'),
    ('can_set_sticky', 'Can set specific threads sticky'),
    ('can_add_forum', 'Can add a forum'),
    ('can_change_forum', 'Can edit a forum'),
    ('can_delete_forum', 'Can delete a forum'),
    ('can_start_thread', 'Can start a thread'),
    (
        'can_change_self_post',
        'Can edit a self written post (thread starting post or reply)'
    ),
    ('can_change_any_post', 'Can edit any post'),
    ('can_reply', 'Can reply'),
    ('can_read_forum', 'Can read any thread or reply of the forum'),
)

FORUM_ROLE_PERMISSIONS = {
    'members': (),
    'moderators': (),
    'owners': (),
}

FORUM_ROLE_PERMISSIONS['members'] = \
    FORUM_ROLE_PERMISSIONS['members'] + (
       'can_start_thread',
       'can_reply',
       'can_change_self_post',
       'can_read_forum',
)

FORUM_ROLE_PERMISSIONS['moderators'] = \
    FORUM_ROLE_PERMISSIONS['members'] + (
       'can_set_forum_status',
       'can_moderate',
       'can_set_sticky',
       'can_add_forum',
       'can_change_forum',
       'can_delete_forum',
       'can_change_any_post'
    )

FORUM_ROLE_PERMISSIONS['owners'] = \
    FORUM_ROLE_PERMISSIONS['moderators'] + (
       'can_apply_forum_options',
    )


class ForumContainer(MultiSiteContainerMixin, CreationModificationDateMixin):
    """
    The container model holding (nested) Forums
    """
    title = MultilingualCharField(
        _('title'),
        blank=True,
        max_length=255,
    )

    allow_bumping = models.BooleanField(
        _("allow bumping"),
        default=False,
        help_text=_(
            "check this field, if you want to allow your threads be displayed at the top again, if nobody has answered yet. So, every thread should get a chance to be heard, even if the forum is highly frequented. 'Bumping' is done by posting a second time to the (not yet answered) thread."
        ),
    )

    max_level = models.IntegerField(
        _("max nesting level"),
        default=1,
        help_text=_(
            "the maximum nesting level. As forums can contain forums, restrict the nesting level here. If the maximum nesting level is set to 0, only one default forum is allowed."
        ),
    )

    def __unicode__(self):
        sites_str = ", ".join([str(item.name) for item in self.sites.all()])
        if sites_str != "":
            sites_str = u" (%s)" % sites_str
        return force_unicode(self.title) + sites_str

    def save(self, *args, **kwargs):
        content_object = self.content_object
        if not self.title:
            title_dict = {}
            if content_object:
                for key in settings.LANGUAGES:
                    title_dict[key[0]] = \
                        get_translation('Forum Container for %(obj)s', language=key[0]) %\
                            {'obj': force_unicode(content_object)}
                self.title = title_dict
            else:
                for key in settings.LANGUAGES:
                    title_dict[key[0]] = \
                        get_translation('General Forum Container', language=key[0])
                self.title = title_dict

        super(ForumContainer, self).save(*args, **kwargs)

    save.alters_data = True

    # deprecated
    def get_absolute_url(self):
        return self.get_url_path()

    class Meta(MultiSiteContainerMixin.Meta):
        ordering = ('title', )
        verbose_name = _("Forum Container")
        verbose_name_plural = _("Forum Containers")


# QUICK HACK:
ForumContainer.objects.model = ForumContainer


class ForumManager(TreeManager):
    def get_roots(self, container, status):
        return self.get_queryset().filter(
            container=container,
            parent__isnull=True,
            status=status,
        )


class Forum(MPTTModel, CreationModificationMixin, UrlMixin, SlugMixin()):
    """
    A forum is a collection of threads. A forum may contain a forum
    """
    container = models.ForeignKey(
        ForumContainer,
        verbose_name=_('container'),
    )

    sort_order = models.IntegerField(
        _("sort order"),
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
        'self',
        #related_name="%(class)s_children",
        related_name="child_set",
        blank=True,
        null=True,
    )
    """ 
    no multilingual fields in this case, as it is "managed" by users, not
    by admins. users should not be forced to supply multilingual text!
    """
    title = models.CharField(_('title'), max_length=512)
    short_title = models.CharField(
        _('short title'),
        help_text=_(
            "a short title to be displayed in page breadcrumbs and headline. If left blank, short title is derived from title."
        ),
        max_length=32,
        blank=True,
    )
    description = ExtendedTextField(_('description'), blank=True)

    status = models.IntegerField(
        _("status"), default=STATUS_CODE_PUBLIC, choices=STATUS_CODES_CHOICES
    )

    objects = ForumManager()

    class Meta:
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return self.title

    def short_str(self):
        return self.short_title

    def save(self, *args, **kwargs):
        if not self.pk:
            Forum.objects.insert_node(self, self.parent)
        self.populate_short_title()
        # if self has a parent, set the container of the parent!!!!
        if self.parent:
            self.container = self.parent.container
        super(Forum, self).save(*args, **kwargs)

    save.alters_data = True

    def delete(self, *args, **kwargs):
        """ delete forum and all its descendants """
        forum_list = self.get_children()
        for forum in forum_list:
            for thread in self.get_threads(exclude_is_sticky=False):
                thread.delete()
            forum.delete()
        super(Forum, self).delete(*args, **kwargs)

    delete.alters_data = True

    def populate_short_title(self):
        short_title = self.short_title
        if not short_title or len(short_title) == 0:
            short_title = ""
            for word in self.title.split(' '):
                if len(short_title) + len(word) < 32:
                    if len(short_title) != 0:
                        short_title += " "
                    short_title += word
                else:
                    break
            self.short_title = short_title

    def get_verbose(self):
        """
        returns a verbose representation of the path
        this is also used as a callback for admin list_filters.
        """
        path = ""
        parent = self
        while parent:
            indented = parent.short_title
            if parent.path:
                indented = "%s %s" % (
                    "-" * (parent.path.count("/") - 1),
                    parent.short_title,
                )
            if len(path) > 0:
                path = '%s<br />%s' % (indented, path)
            else:
                path = indented
            parent = parent.parent
        path = '%s<br /><br />' % path
        return path

    # deprecated
    def get_absolute_url(self):
        return self.get_url_path()

    def get_url_path(self):
        return "%s%s/" % (
            self.container.get_url_path(),
            self.slug,
        )

    def is_public(self):
        return self.status == STATUS_CODE_PUBLIC

    def get_children_latest_threads(self, exclude_is_sticky=True):
        """
        gets the latest threads for all child forums as a queryset.
        TODO SORTING ORDER!!!!!
        """
        forum_list = self.get_descendants()
        qs = ForumThread.objects.filter(
            forum__in=forum_list,
            status=STATUS_CODE_PUBLIC,
        ).distinct()
        if exclude_is_sticky:
            qs = qs.filter(is_sticky=False)

        return qs.order_by(
            '-is_sticky', '-forumreply__creation_date', '-creation_date'
        )

    def get_threads(self, exclude_is_sticky=True):
        """ gets all threads (or all non sticky threads) of the forum"""
        qs = ForumThread.objects.filter(status=STATUS_CODE_PUBLIC, forum=self)
        if exclude_is_sticky:
            qs = qs.filter(is_sticky=False)
        return qs.order_by(
            '-is_sticky', '-forumreply__creation_date', '-creation_date'
        )

    def has_threads(self):
        return self.get_threads().count() > 0

    def get_nof_threads(self):
        return self.get_threads().count()

    get_nof_threads.short_description = _('# threads')

    def get_nof_threads_recursive(self):
        count = self.get_nof_threads()
        for forum in self.get_descendants():
            count += forum.get_nof_threads()
        return count

    def get_nof_replies(self):
        count = 0
        for thread in self.get_threads():
            count = count + thread.get_nof_replies()
        return count

    get_nof_replies.short_description = _('# replies')

    def get_nof_replies_recursive(self):
        count = self.get_nof_replies()
        for forum in self.get_descendants():
            count += forum.get_nof_replies()
        return count

    def get_nof_views(self):
        count = 0
        for thread in self.get_threads():
            count += thread.views
        return count

    def get_latest_post(self):
        """ 
        returns the thread with the latest post
        """
        threads = self.get_threads()
        if threads:
            return threads[0].get_latest_post()
        return None


class ForumThread(
    CreationModificationMixin, ViewsMixin, UrlMixin,
    SlugMixin(proposal="thread")
):
    """
    A forum thread defines a new thread
    """
    forum = TreeForeignKey(Forum, verbose_name=_('forum'))
    subject = models.CharField(_('subject'), max_length=255)
    message = ExtendedTextField(_('message'))
    is_sticky = models.BooleanField(
        _("is sticky"),
        default=False,
        help_text=_(
            "check this field, if you want your thread to appear continually at the top of the forum."
        ),
    )
    status = models.IntegerField(
        _("status"), default=STATUS_CODE_PUBLIC, choices=STATUS_CODES_CHOICES
    )

    class Meta:
        verbose_name = _('Thread')
        verbose_name_plural = _('Threads')
        ordering = ['forum', '-is_sticky', 'creation_date']

    def __unicode__(self):
        return self.subject

    # just for admin
    is_sticky.boolean = True

    def delete(self, *args, **kwargs):
        """ delete thread with all it's replies """
        for reply in self.get_replies():
            reply.delete()
        super(ForumThread, self).delete(*args, **kwargs)

    delete.alters_data = True

    # deprecated
    def get_absolute_url(self):
        return self.get_url_path()

    def get_url_path(self):
        return "%s%s/" % (
            self.forum.get_url_path(),
            self.slug,
        )

    def is_public(self):
        return self.status == STATUS_CODE_PUBLIC

    def get_replies(self):
        """ get all replies including recursive replies! """
        return ForumReply.objects.filter(thread=self)

    def has_replies(self):
        return self.get_replies().count() > 0

    def get_nof_replies(self):
        return self.get_replies().count()

    get_nof_replies.short_description = _('# replies')

    def get_latest_reply(self):
        """
        gets the latest reply (by creation_date)
        """
        replies = self.get_replies().order_by('-creation_date')
        if replies.count() > 0:
            return replies[0]
        return None

    def get_latest_post(self):
        """
        gets the latest reply or, if the thread has no replies yet,
        the thread itself
        """
        return self.get_latest_reply() or self


class ForumReply(
    MPTTModel, CreationModificationMixin, UrlMixin, SlugMixin(proposal="reply")
):
    """
    A forum replies defines a reply to a thread
    """
    sort_order = models.IntegerField(
        _("sort order"),
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
        'self',
        #related_name="%(class)s_children",
        related_name="child_set",
        blank=True,
        null=True,
    )
    thread = models.ForeignKey(ForumThread, verbose_name=_('thread'))
    subject = models.CharField(_('subject'), max_length=255, blank=True)
    message = ExtendedTextField(_('message'))

    objects = TreeManager()

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return self.subject

    def short_str(self):
        return truncwords(strip_tags(self.subject), 3)

    def save(self, *args, **kwargs):
        if not self.pk:
            ForumReply.objects.insert_node(self, self.parent)
        # subject is just derived from the message!
        self.subject = truncwords(strip_tags(self.message), 10)
        if self.parent:
            self.thread = self.parent.thread
        super(ForumReply, self).save(*args, **kwargs)

    save.alters_data = True

    def delete(self, *args, **kwargs):
        """ delete reply and its descendants """
        reply_list = self.get_children()
        for reply in reply_list:
            reply.delete()
        super(ForumReply, self).delete(*args, **kwargs)

    delete.alters_data = True

    #deprecated
    def get_absolute_url(self):
        return self.get_url_path()

    def get_url_path(self):
        return self.thread.get_url_path()
        #return "%s%s/" % (
        #    self.thread.get_url_path(),
        #    self.slug,
        #    )

    def get_nof_replies(self):
        """ get nof replies to this reply"""
        return len(self.get_descendants())
