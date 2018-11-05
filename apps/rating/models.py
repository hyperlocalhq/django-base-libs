from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import EmptyQuerySet

from base_libs.models import CreationDateMixin, ObjectRelationMixin

verbose_name = _("Ratings")

# a "default" key for ratings, when a key is not relevant
DEFAULT_KEY = "RATING"

class UserRatingManager(models.Manager):

    def _votes(self, obj, user, key=DEFAULT_KEY):
        """
        returns a queryset holding votes for an object and a user.
        """
        try:
            ct = ContentType.objects.get_for_model(obj)
            return self.filter(
                user__pk=user.id, 
                content_type=ct, 
                object_id=obj.id, 
                key=key,
                )
        except:
            return EmptyQuerySet()
    
    def can_rate(self, obj, user, key=DEFAULT_KEY):
        """
        returns False, if a user has given 
        a vote for a spcified key on a specific
        object, True otherwise
        """
        if not user or not user.is_authenticated():
            return False
        return self._votes(obj, user, key).count() == 0

    def has_rated(self, obj, user, key=DEFAULT_KEY):
        """
        True, if the user has already rated for a 
        specific object, False otherwise
        """
        if not user or not user.is_authenticated():
            return False
        return self._votes(obj, user, key).count() != 0

    def is_aggregated(self, obj, user, key=DEFAULT_KEY):
        """
        True, if the user has already rated 
        for a specific object and the object 
        is aggregated yet, False otherwise
        """
        if not user or not user.is_authenticated():
            return False
        
        votes = self._votes(obj, user, key)
        if votes.count() == 0:
            return False
        else:
            return votes[0].is_aggregated
    
    def rate(self, obj, user, score, key=DEFAULT_KEY):
        """
        Rates an object
        """
        if self.can_rate(obj, user, key):
            ct = ContentType.objects.get_for_model(obj)
            rating = self.model(
              content_type=ct,
              object_id=obj.id,
              user=user,
              key=key,
              score=score
              )
            rating.save()

class UserRating(CreationDateMixin, ObjectRelationMixin()):
    """
    Holds user votes for a specific object
    
    Remarks:
        key: is used for rating an object for different keys. 
        usually, only one key is provided. If for a rating 
        system only one key is used, it has a default value
        "RATING" 
        is_aggregated: can be used for indicating, that the current
        score is already aggregated by external system and should 
        not be taken into account any more.
    """
    user            = models.ForeignKey(User, related_name="rating_userrating_user")
    key             = models.CharField(_('key'), max_length=32, default=DEFAULT_KEY)
    score           = models.IntegerField()
    is_aggregated   = models.BooleanField(_('is aggregated'), default=False)
    objects         = UserRatingManager()

    class Meta:
        unique_together = ('content_type', 'object_id', 'user', 'key')
