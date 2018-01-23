# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base_libs.models.fields import URLField

TWITTER_SEARCH_HELP = """
A comma-separated list of phrases which will be used to determine what Tweets will be delivered on the stream.
A phrase may be one or more terms separated by spaces, and a phrase will match if all of the terms in the phrase
are present in the Tweet, regardless of order and ignoring case.
"""


class SearchSettings(models.Model):
    query = models.CharField(_("Search query"), max_length=140, help_text=TWITTER_SEARCH_HELP)

    class Meta:
        verbose_name = _("Twitter search settings")
        verbose_name_plural = _("Twitter search settings")

    def __unicode__(self):
        return self.query


class UserTimelineSettings(models.Model):
    screen_name = models.CharField(_("Screen name"), max_length=20)

    class Meta:
        verbose_name = _("Twitter user timeline settings")
        verbose_name_plural = _("Twitter user timeline settings")

    def __unicode__(self):
        return self.screen_name


LANGUAGE_CHOICES = (
    ("ar", _("Arabic")),
    ("ca", _("Catalan")),
    ("da", _("Danish")),
    ("nl", _("Dutch")),
    ("en", _("English")),
    ("fa", _("Farsi")),
    ("fil", _("Filipino")),
    ("fi", _("Finnish")),
    ("fr", _("French")),
    ("de", _("German")),
    ("he", _("Hebrew")),
    ("hi", _("Hindi")),
    ("hu", _("Hungarian")),
    ("id", _("Indonesian")),
    ("it", _("Italian")),
    ("ja", _("Japanese")),
    ("ko", _("Korean")),
    ("msa", _("Malay")),
    ("no", _("Norwegian")),
    ("pl", _("Polish")),
    ("pt", _("Portuguese")),
    ("ru", _("Russian")),
    ("zh-cn", _("Simplified Chinese")),
    ("es", _("Spanish")),
    ("sv", _("Swedish")),
    ("th", _("Thai")),
    ("zh-tw", _("Traditional Chinese")),
    ("tr", _("Turkish")),
    ("uk", _("Ukrainian")),
    ("ur", _("Urdu")),
)

STATUS_CHOICES = (
    ('published', _("Published")),
    ('not_listed', _("Not Listed")),
)


class TwitterUser(models.Model):
    id = models.CharField(_("ID"), primary_key=True, max_length=20)
    id_str = models.CharField(_("ID String"), help_text=_("Used in URLs"), max_length=20)
    screen_name = models.CharField(_("Screen name"), max_length=20)
    name = models.CharField(_("Name"), max_length=20, blank=True)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    profile_image_url = URLField(_("Profile image URL"), max_length=255)
    url = URLField(_("URL"), max_length=255, blank=True)
    description = models.TextField(_("Description"), blank=True)
    language = models.CharField(_("Language"), max_length=5, blank=True, choices=LANGUAGE_CHOICES)
    
    class Meta:
        verbose_name = _("Twitter user")
        verbose_name_plural = _("Twitter users")
        ordering = ("screen_name",)
    
    def __unicode__(self):
        return self.screen_name


class Tweet(models.Model):
    id = models.CharField(_("ID"), primary_key=True, max_length=20)
    id_str = models.CharField(_("ID String"), help_text=_("Used in URLs"), max_length=20)
    creation_date = models.DateTimeField(_("Creation date"),)
    user = models.ForeignKey(TwitterUser, verbose_name=_("Twitter user"))
    text = models.TextField(_("Text"), help_text=_("Text as imported from twitter"))
    html = models.TextField(_("HTML"))
    latitude = models.FloatField(_("Latitude"), help_text=_("Latitude (Lat.) is the angle between any point and the equator (north pole is at 90; south pole is at -90)."), blank=True, null=True)
    longitude = models.FloatField(_("Longitude"), help_text=_("Longitude (Long.) is the angle east or west of an arbitrary point on Earth from Greenwich (UK), which is the international zero-longitude point (longitude=0 degrees). The anti-meridian of Greenwich is both 180 (direction to east) and -180 (direction to west)."), blank=True, null=True)
    from_search = models.BooleanField(_("from search by query"))
    by_user = models.BooleanField(_("by twitter user from user timeline settings"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, blank=True, default="published")

    class Meta:
        verbose_name = _("Tweet")
        verbose_name_plural = _("Tweets")
        ordering = ("-creation_date",)
        
    def __unicode__(self):
        return "%s: %s" % (self.user.screen_name, self.text)


class TweetMedia(models.Model):
    tweet = models.ForeignKey(Tweet, verbose_name=_("Tweet"))
    media_url = URLField(_("Media URL"))
    media_type = models.CharField(_("MediaType"), choices=(('photo', _("Photo")),), default="photo", max_length=20)
    
    class Meta:
        verbose_name = _("Tweet media")
        verbose_name_plural = _("Tweet media")
        ordering = ("id",)
        
    def __unicode__(self):
        return self.media_url
