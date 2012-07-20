# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from base_libs.models.models import MultiSiteMixin
from base_libs.models.fields import URLField

TWITTER_SEARCH_HELP = """
<div class="twttr-dialog-content">
  <table class="modal-table modal-table-bordered">
  <thead>
    <tr>
      <th>Search operator</th>
      <th>Finds tweets...</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>twitter search</td><td>containing both "twitter" and "search". This is the default operator.</td></tr>
    <tr><td><b>"</b>happy hour<b>"</b></td><td>containing the exact phrase "happy hour".</td></tr>
    <tr><td>love <b>OR</b> hate</td><td>containing either "love" or "hate" (or both).</td></tr>
    <tr><td>beer <b>-</b>root</td><td>containing "beer" but not "root".</td></tr>
    <tr><td><b>#</b>haiku</td><td>containing the hashtag "haiku".</td></tr>
    <tr><td><b>from:</b>alexiskold</td><td>sent from person "alexiskold".</td></tr>
    <tr><td><b>to:</b>techcrunch</td><td>sent to person "techcrunch".</td></tr>
    <tr><td><b>@</b>mashable</td><td>referencing person "mashable".</td></tr>
    <tr><td>"happy hour" <b>near:</b>"san francisco"</td><td>containing the exact phrase "happy hour" and sent near "san francisco".</td></tr>
    <tr><td><b>near:</b>NYC <b>within:</b>15mi</td><td>sent within 15 miles of "NYC".</td></tr>
    <tr><td>superhero <b>since:</b>2010-12-27</td><td>containing "superhero" and sent since date "2010-12-27" (year-month-day).</td></tr>
    <tr><td>ftw <b>until:</b>2010-12-27</td><td>containing "ftw" and sent up to date "2010-12-27".</td></tr>
    <tr><td>movie -scary <b>:)</b></td><td>containing "movie", but not "scary", and with a positive attitude.</td></tr>
    <tr><td>flight <b>:(</b></td><td>containing "flight" and with a negative attitude.</td></tr>
    <tr><td>traffic <b>?</b></td><td>containing "traffic" and asking a question.</td></tr>
    <tr><td>hilarious <b>filter:links</b></td><td>containing "hilarious" and linking to URLs.</td></tr>
    <tr><td>news <b>source:twitterfeed</b></td><td>containing "news" and entered via TwitterFeed</td></tr>
  </tbody>
  </table>
</div>
"""

class SearchSettings(models.Model):
    query = models.CharField(_("Search query"), max_length=140, help_text=TWITTER_SEARCH_HELP)
    sites = models.ManyToManyField(
         Site, 
         verbose_name=_("Site"),
         help_text=_("Show tweets with this hashtag on the selected sites"),
         )
    
    class Meta:
        verbose_name = _("Twitter search settings")
        verbose_name_plural = _("Twitter search settings")

    def __unicode__(self):
        return self.query
        
class UserTimelineSettings(models.Model):
    screen_name = models.CharField(_("Screen name"), max_length=20)
    sites = models.ManyToManyField(
         Site, 
         verbose_name=_("Site"),
         help_text=_("Show tweets from this user on the selected sites"),
         )
    include_rts = models.BooleanField(_("Include retweets"), default=True)
    exclude_replies = models.BooleanField(_("Exclude replies"), default=True)

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



class Tweet(MultiSiteMixin):
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
    
