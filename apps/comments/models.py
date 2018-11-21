# -*- coding: UTF-8 -*-
from datetime import datetime

from django.apps import apps
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.functional import lazy
from django.utils.encoding import smart_str, force_unicode
from django.conf import settings
try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from base_libs.models.models import UrlMixin
from base_libs.models.models import ObjectRelationMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField  # needed for south to work
from base_libs.models.fields import URLField

from base_libs.middleware import get_current_user, get_current_language
from base_libs.utils.user import get_user_title

verbose_name = _("Comments")

MIN_PHOTO_DIMENSION = 5
MAX_PHOTO_DIMENSION = 1000

# option codes for comment-form hidden fields
PHOTOS_REQUIRED = 'pr'
PHOTOS_OPTIONAL = 'pa'
RATINGS_REQUIRED = 'rr'
RATINGS_OPTIONAL = 'ra'
IS_PUBLIC = 'ip'

# what users get if they don't have any karma
DEFAULT_KARMA = 5
KARMA_NEEDED_BEFORE_DISPLAYED = 3


class CommentManager(models.Manager):
    def get_security_hash(self, options, photo_options, rating_options, target):
        """
        Returns the MD5 hash of the given options (a comma-separated string such as
        'pa,ra') and target (something like 'lcom.eventtimes:5157'). Used to
        validate that submitted form options have not been tampered-with.
        """
        from hashlib import md5
        return md5(
            options + photo_options + rating_options + target +
            settings.SECRET_KEY
        ).hexdigest()

    def get_rating_options(self, rating_string):
        """
        Given a rating_string, this returns a tuple of (rating_range, options).
        >>> s = "scale:1-10|First_category|Second_category"
        >>> Comment.objects.get_rating_options(s)
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['First category', 'Second category'])
        """
        rating_range, options = rating_string.split('|', 1)
        rating_range = range(
            int(rating_range[6:].split('-')[0]),
            int(rating_range[6:].split('-')[1]) + 1
        )
        choices = [c.replace('_', ' ') for c in options.split('|')]
        return rating_range, choices

    def get_list_with_karma(self, **kwargs):
        """
        Returns a list of Comment objects matching the given lookup terms, with
        _karma_total_good and _karma_total_bad filled.
        """
        extra_kwargs = {}
        extra_kwargs.setdefault('select', {})
        extra_kwargs['select'][
            '_karma_total_good'
        ] = 'SELECT COUNT(*) FROM comments_karmascore, comments_comment WHERE comments_karmascore.comment_id=comments_comment.id AND score=1'
        extra_kwargs['select'][
            '_karma_total_bad'
        ] = 'SELECT COUNT(*) FROM comments_karmascore, comments_comment WHERE comments_karmascore.comment_id=comments_comment.id AND score=-1'
        return self.filter(**kwargs).exclude(is_spam=True).extra(**extra_kwargs)

    def user_is_moderator(self, user):
        if user.is_superuser:
            return True
        for g in user.groups.all():
            if g.id == settings.COMMENTS_MODERATORS_GROUP:
                return True
        return False


class Comment(ObjectRelationMixin(is_required=True), UrlMixin):
    """
    one of the fields,  user or name is mandatory. If a user is logged in,
    commentators name is filled in as the logged in user, otherwise,
    the "commentator" must provide a 
    name (see the save method below).  
    """
    user = models.ForeignKey("auth.User", blank=True, null=True)
    name = models.CharField(_('name'), max_length=80)
    email = models.EmailField(_('email'), blank=True, null=True)
    url_link = URLField(_("URL"), blank=True, null=True)

    headline = models.CharField(
        _('headline'), max_length=255, blank=True, null=True
    )
    comment = models.TextField(_('comment'), max_length=3000)
    rating1 = models.PositiveSmallIntegerField(
        _('rating #1'), blank=True, null=True
    )
    rating2 = models.PositiveSmallIntegerField(
        _('rating #2'), blank=True, null=True
    )
    rating3 = models.PositiveSmallIntegerField(
        _('rating #3'), blank=True, null=True
    )
    rating4 = models.PositiveSmallIntegerField(
        _('rating #4'), blank=True, null=True
    )
    rating5 = models.PositiveSmallIntegerField(
        _('rating #5'), blank=True, null=True
    )
    rating6 = models.PositiveSmallIntegerField(
        _('rating #6'), blank=True, null=True
    )
    rating7 = models.PositiveSmallIntegerField(
        _('rating #7'), blank=True, null=True
    )
    rating8 = models.PositiveSmallIntegerField(
        _('rating #8'), blank=True, null=True
    )
    # This field designates whether to use this row's ratings in aggregate
    # functions (summaries). We need this because people are allowed to post
    # multiple reviews on the same thing, but the system will only use the
    # latest one (with valid_rating=True) in tallying the reviews.
    valid_rating = models.BooleanField(_('is valid rating'), default=False)
    submit_date = models.DateTimeField(
        _('date/time submitted'), auto_now_add=True
    )
    is_public = models.BooleanField(_('is public'), default=False)
    ip_address = models.GenericIPAddressField(
        _('IP address'), blank=True, null=True
    )
    is_removed = models.BooleanField(
        _('is removed'),
        default=False,
        help_text=_(
            'Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.'
        )
    )
    is_spam = models.BooleanField(
        _('is spam'),
        default=False,
        help_text=_(
            'Check this box if the comment should be marked as spam. The comment will not be displayed in this case.'
        )
    )
    site = models.ForeignKey("sites.Site")
    objects = CommentManager()

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('-submit_date', )

    def __repr__(self):
        if self.user:
            return "%s: %s..." % (
                smart_str(self.user.username), smart_str(self.comment[:100])
            )
        else:
            return "%s: %s..." % (
                smart_str(self.name), smart_str(self.comment[:100])
            )

    def __unicode__(self):
        if self.user:
            return "%s: %s..." % (
                force_unicode(self.user.username),
                force_unicode(self.comment[:100])
            )
        else:
            return "%s: %s..." % (
                force_unicode(self.name), force_unicode(self.comment[:100])
            )

    def get_comment(self):
        """ 
        returns the comment contents or a message, if the comment was refused
        """
        if self.is_removed:
            m = ModeratorDeletion.objects.get(comment=self)
            return m.get_reason()
        else:
            return self.comment

    get_comment.is_safe = True

    def get_absolute_url(self):
        return self.content_object.get_absolute_url() + "#c" + str(self.id)

    def get_url_path(self):
        return self.content_object.get_url_path() + "#c" + str(self.id)

    def get_crossdomain_url(self):
        return "/r/%d/%d/" % (self.content_type_id, self.object_id)

    def get_flag_url(self):
        return "/comments/flag/%s/" % self.id

    def get_deletion_url(self):
        return "/comments/delete/%s/" % self.id

    def _fill_karma_cache(self):
        """Helper function that populates good/bad karma caches"""
        good, bad = 0, 0
        for k in self.karmascore_set:
            if k.score == -1:
                bad += 1
            elif k.score == 1:
                good += 1
        self._karma_total_good, self._karma_total_bad = good, bad

    def get_good_karma_total(self):
        if not hasattr(self, "_karma_total_good"):
            self._fill_karma_cache()
        return self._karma_total_good

    def get_bad_karma_total(self):
        if not hasattr(self, "_karma_total_bad"):
            self._fill_karma_cache()
        return self._karma_total_bad

    def get_karma_total(self):
        if not hasattr(self, "_karma_total_good"
                      ) or not hasattr(self, "_karma_total_bad"):
            self._fill_karma_cache()
        return self._karma_total_good + self._karma_total_bad

    def get_as_text(self):
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % \
            {'user': self.user.username, 'date': self.submit_date,
            'comment': self.comment, 'domain': self.site.domain, 'url': self.get_absolute_url()}

    def can_rate(self):
        """
        returns a dictionary containing values for each rating index, 
        if the logged in user can rate the comment.
        """
        user = get_current_user()
        can_rate_dict = {}
        for i in range(1, 9):
            #can_rate_dict.update((i, UserRating.objects.can_rate(self, user, i)))
            l = UserRating.objects.can_rate(self, user, i)
            can_rate_dict[i] = l
        return can_rate_dict


class KarmaScoreManager(models.Manager):
    def vote(self, user_id, comment_id, score):
        try:
            karma = self.get(comment__pk=comment_id, user__pk=user_id)
        except self.model.DoesNotExist:
            karma = self.model(
                None,
                user_id=user_id,
                comment_id=comment_id,
                score=score,
                scored_date=tz_now()
            )
            karma.save()
        else:
            karma.score = score
            karma.scored_date = tz_now()
            karma.save()

    def get_pretty_score(self, score):
        """
        Given a score between -1 and 1 (inclusive), returns the same score on a
        scale between 1 and 10 (inclusive), as an integer.
        """
        if score is None:
            return DEFAULT_KARMA
        return int(round((4.5 * score) + 5.5))


class KarmaScore(models.Model):
    user = models.ForeignKey("auth.User")
    comment = models.ForeignKey("comments.Comment")
    score = models.SmallIntegerField(_('score'), db_index=True)
    scored_date = models.DateTimeField(_('score date'), auto_now=True)
    objects = KarmaScoreManager()

    class Meta:
        verbose_name = _('karma score')
        verbose_name_plural = _('karma scores')
        unique_together = (('user', 'comment'), )

    def __repr__(self):
        return smart_str(
            _("%(score)d rating by %(user)s") % {
                'score': self.score,
                'user': self.user
            }
        )

    def __unicode__(self):
        return force_unicode(
            _("%(score)d rating by %(user)s") % {
                'score': self.score,
                'user': self.user
            }
        )


class UserFlagManager(models.Manager):
    def flag(self, comment, user):
        """
        Flags the given comment by the given user. If the comment has already
        been flagged by the user, or it was a comment posted by the user,
        nothing happens.
        """
        if int(comment.user_id) == int(user.id):
            return  # A user can't flag his own comment. Fail silently.
        try:
            f = self.objects.get(user__pk=user.id, comment__pk=comment.id)
        except self.model.DoesNotExist:
            from django.core.mail import mail_managers
            f = self.model(None, user.id, comment.id, None)
            message = _('This comment was flagged by %(user)s:\n\n%(text)s') % {
                'user': user.username,
                'text': comment.get_as_text()
            }
            mail_managers('Comment flagged', message, fail_silently=True)
            f.save()


class UserFlag(models.Model):
    user = models.ForeignKey("auth.User")
    comment = models.ForeignKey("comments.Comment")
    flag_date = models.DateTimeField(_('flag date'), auto_now_add=True)
    objects = UserFlagManager()

    class Meta:
        verbose_name = _('user flag')
        verbose_name_plural = _('user flags')
        unique_together = (('user', 'comment'), )

    def __repr__(self):
        return smart_str(_("Flag by %s") % self.user)

    def __unicode__(self):
        return force_unicode(_("Flag by %s") % self.user)


class ModeratorDeletionReason(models.Model):

    title = MultilingualCharField(_('title'), max_length=255)
    reason = MultilingualTextField(_('reason'))

    def get_title(self):
        return self.title

    def get_reason(self):
        return self.reason

    class Meta:
        verbose_name = _('moderator deletion reason')
        verbose_name_plural = _('moderator deletion reasons')

    def __repr__(self):
        return self.get_title()

    def __unicode__(self):
        return self.get_title()


class ModeratorDeletion(models.Model):
    user = models.ForeignKey("auth.User", verbose_name='moderator')
    comment = models.ForeignKey("comments.Comment")
    deletion_date = models.DateTimeField(_('deletion date'), auto_now_add=True)
    deletion_reason = models.ForeignKey(
        "comments.ModeratorDeletionReason", verbose_name='deletion reason'
    )

    class Meta:
        verbose_name = _('moderator deletion')
        verbose_name_plural = _('moderator deletions')
        unique_together = (('user', 'comment'), )

    def __unicode__(self):
        return ugettext('moderator deletion')
        #return force_unicode(_("Moderator deletion by %r") % self.user)

    def get_reason(self):
        return self.deletion_reason.get_reason()


class UserRatingManager(models.Manager):
    def can_rate(self, comment, user, rate_index):
        """
        returns False, if a user has given a rate for a spcified 
        index already or user is None or the rating user has written the
        comment, True otherwise
        """
        if not user or not user.is_authenticated():
            return False
        # A user can't rate his own comment.
        if comment.user.id == user.id:
            return False
        try:
            # user has done a rating already!!!
            f = self.get(
                user__pk=user.id, comment__pk=comment.id, rate_index=rate_index
            )
            return False
        except:
            pass
        return True

    def rate(self, comment, user, rate_index):
        """
        Remembers that a user has rated a comment. If the comment has already
        been rated by the user, or it was a comment posted by the user,
        nothing happens. "Self rating" is not allowed!
        """
        if self.can_rate(comment, user, rate_index):
            f = self.model(None, user.id, comment.id, None, rate_index)
            # do the rating itself!!!
            rating = None
            exec "rating = comment.rating" + str(rate_index)
            if rating:
                rating += 1
            else:
                rating = 1

            exec "comment.rating" + str(rate_index) + " = rating"

            #from django.core.mail import mail_managers
            #message = _('This comment was rated by %(user)s:\n\n%(text)s with rating index %(index)s') % {'user': user.username, 'text': comment.get_as_text(), 'index': str(rate_index)}
            #mail_managers('Comment flagged', message, fail_silently=True)

            comment.save()
            f.save()


class UserRating(models.Model):
    user = models.ForeignKey("auth.User")
    comment = models.ForeignKey("comments.Comment")
    rate_date = models.DateTimeField(_('rate date'), auto_now_add=True)
    rate_index = models.SmallIntegerField(_('rate index'))
    objects = UserRatingManager()

    class Meta:
        verbose_name = _('user rating')
        verbose_name_plural = _('user ratings')
        unique_together = (('user', 'comment', 'rate_index'), )

    def __repr__(self):
        return smart_str(
            _("Rating with index %(rate_index)d by %(user)r") % {
                "rate_index": self.rate_index,
                "user": self.user
            }
        )

    def __unicode__(self):
        return force_unicode(
            _("Rating with index %(rate_index)d by %(user)r") % {
                "rate_index": self.rate_index,
                "user": self.user
            }
        )


def comment_added(sender, instance, **kwargs):
    """
    Notify appropriate users about comments for their entries
    """
    if not models.get_model("notification", "Notice"):
        # if notification not install, exit function
        return
    from jetson.apps.notification import models as notification

    commented_object = instance.content_object
    creator = getattr(commented_object, "creator", None)

    if creator:
        if instance.email:
            submitter_email = instance.email
        else:
            submitter_email = instance.user.email
        if instance.name:
            submitter_name = instance.name
        else:
            submitter_name = get_user_title(instance.user)
        notification.send(
            creator,
            "comment_added",
            {
                "object_creator_title":
                    submitter_name,
                "object_url":
                    "".join(
                        (
                            commented_object.get_url(),
                            "#c",
                            str(instance.pk),
                        )
                    ),
            },
            instance=instance,
        )
        if apps.is_installed("actstream"):
            from actstream import action
            action.send(
                instance.user, verb="added comment", action_object=instance
            )


#models.signals.post_save.connect(comment_added, sender=Comment)
