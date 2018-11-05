# -*- coding: UTF-8 -*-
import re
import os
from collections import OrderedDict
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import smart_unicode, force_unicode
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.translation import activate as activate_language

from base_libs.models.models import UrlMixin
from base_libs.models.models import ViewsMixin
from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import CreationModificationMixin
from base_libs.models.models import CreationModificationDateMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import PositionField
from base_libs.models.fields import ExtendedTextField # needed for south to work
from base_libs.models.query import ExtendedQuerySet
from base_libs.utils.misc import is_installed
from base_libs.models.fields import URLField
from base_libs.middleware import get_current_language

from filebrowser.base import FileObject
from filebrowser.settings import MEDIA_ROOT as UPLOADS_ROOT
from filebrowser.settings import MEDIA_URL as UPLOADS_URL
from filebrowser.fields import FileBrowseField


image_mods = models.get_app("image_mods")

verbose_name = _("Media Gallery")


VIDEO_SPLASH_URL = getattr(
    settings,
    "VIDEO_SPLASH_PATH",
    "%ssite/img/media_gallery/default/video.png" % settings.STATIC_URL,
)
VIDEO_SPLASH_TN_URL = getattr(
    settings,
    "VIDEO_SPLASH_TN_PATH",
    "%ssite/img/media_gallery/thumbs/video.png" % settings.STATIC_URL,
)
VIDEO_SPLASH_LIST_URL = getattr(
    settings,
    "VIDEO_SPLASH_LIST_PATH",
    "%ssite/img/media_gallery/list/video.png" % settings.STATIC_URL,
)
AUDIO_SPLASH_URL = getattr(
    settings,
    "AUDIO_SPLASH_PATH",
    "%ssite/img/media_gallery/default/audio.png" % settings.STATIC_URL,
)
AUDIO_SPLASH_TN_URL = getattr(
    settings,
    "AUDIO_SPLASH_TN_PATH",
    "%ssite/img/media_gallery/thumbs/audio.png" % settings.STATIC_URL,
)
AUDIO_SPLASH_LIST_URL = getattr(
    settings,
    "AUDIO_SPLASH_LIST_PATH",
    "%ssite/img/media_gallery/list/audio.png" % settings.STATIC_URL,
)
IMAGE_SPLASH_URL = getattr(
    settings,
    "IMAGE_SPLASH_PATH",
    "%ssite/img/media_gallery/default/image.png" % settings.STATIC_URL,
)
IMAGE_SPLASH_TN_URL = getattr(
    settings,
    "IMAGE_SPLASH_TN_PATH",
    "%ssite/img/media_gallery/thumbs/image.png" % settings.STATIC_URL,
)
IMAGE_SPLASH_LIST_URL = getattr(
    settings,
    "IMAGE_SPLASH_LIST_PATH",
    "%ssite/img/media_gallery/list/image.png" % settings.STATIC_URL,
)

URL_ID_PORTFOLIO = getattr(settings, "URL_ID_PORTFOLIO", "portfolio")

MEDIA_FILE_TYPE_CHOICES = (
    ("-", _("Unknown")),
    ("i", _("Image")),
    ("v", _("Video")),
    ("a", _("Audio")),
    ("y", _("Youtube video")),
    ("m", _("Vimeo video")),
)

MEDIA_FILE_TYPE_RECOGNITION = (
    (re.compile(r"^https?://.*?youtube\.com/watch\?v=|https?://youtu.be/"), "y"),
    (re.compile(r"^https?://.*?vimeo\.com/"), "m"),
    (re.compile(r"\.(jpe?g|png|gif)$"), "i"),
    (re.compile(r"\.(flv|mp4)$"), "v"),
    (re.compile(r"\.mp3$"), "a"),
)

TOKENIZATION_SUMMAND = 56436


class MediaGalleryManager(models.Manager):
    def create_for_object(self, obj, **kwargs):
        return self.create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            **kwargs
        )

    def get_queryset(self):
        q = ExtendedQuerySet(self.model)
        gallery_db_table = self.model._meta.db_table
        ct = ContentType.objects.get_for_model(self.model)
        select = OrderedDict()
        if is_installed("comments.models"):
            Comment = models.get_model("comments", "Comment")
            # we add a field "comments" into the queryset representing the comment count.
            comments_db_table = Comment._meta.db_table
            select['comments'] = """SELECT COUNT(*) from {} WHERE content_type_id = '{}' AND object_id = CAST({}.id AS CHAR)""".format(comments_db_table, ct.id, gallery_db_table)
        if is_installed("favorites.models"):
            Favorite = models.get_model("favorites", "Favorite")
            favorites_db_table = Favorite._meta.db_table
            select['favorite_count'] = """SELECT COUNT(*) from {} WHERE content_type_id = '{}' AND object_id = CAST({}.id AS CHAR)""".format(favorites_db_table, ct.id, gallery_db_table)
        if select:
            q = q.extra(
                select=select,
            )
        return q
    
    def get_sort_order_mapper(self):
        sort_order_mapper = {
            'creation_date_desc': (1, _('Newest Galleries'), ['-creation_date'],),
            'modified_date_desc': (2, _('Lastly Updated'), ['-modified_date'],),
            'discussed_desc': (3, _('Most Discussed'), ['-comments'],),                           
            'favorite_count_desc': (4, _('Most Favored'), ['-favorite_count'],),                           
            'viewed_desc': (5, _('Most Viewed'), ['-views'],),                           
            #'title_asc': (5, _('Name (A-Z)'), ['title'],),
            #'title_desc': (6, _('Name (Z-A)'), ['-title'],),
        }        
        return sort_order_mapper

    def featured(self):
        return self.filter(is_featured=True)
    
    def random_featured(self):
        return self.featured().order_by("?")
        
    def most_commented(self):
        return self.order_by("-comments", "title")
        
    def most_favorite(self):
        return self.order_by("-rating", "title")


class MediaGalleryBase(ObjectRelationMixin(is_required=True), CreationModificationDateMixin, ViewsMixin, UrlMixin):
    title = MultilingualCharField(_("Title"), max_length=100, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    content_object_repr = MultilingualCharField(_("Content object representation"), max_length=100, blank=True, default="", help_text=_("Used for search and ordering in administration."), editable=False)
    content_object_id = models.CharField(_("Content object ID combo"), max_length=100, blank=True, default="", help_text=_("Used for grouping the sortable galleries."), editable=False)
    cover_image = FileBrowseField(_('Cover image'), max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True, default="")
    sort_order = PositionField(_("Sort order"), collection="content_object_id", default=0)
    is_featured = models.BooleanField(_("Featured"), default=False)

    objects = MediaGalleryManager()

    class Meta:
        ordering = ['sort_order', '-creation_date']
        get_latest_by = 'creation_date'
        verbose_name = _('Media Gallery')
        verbose_name_plural = _('Media Galleries')
        abstract = True

    def __unicode__(self):
        value = ugettext("Global gallery")
        if self.content_object:
            value =  ugettext("Gallery of %(content_type)s %(object)s") % {
                'content_type': force_unicode(self.content_type).lower(),
                'object': self.content_object,
            }
        return value
    
    def save(self, **kwargs):
        if self.content_object:
            self.content_object_id = "%s|%s" % (self.content_type.pk, self.object_id)
            current_lang = get_current_language()
            for lang_code, lang_name in settings.LANGUAGES:
                activate_language(lang_code)
                setattr(
                    self,
                    "content_object_repr_%s" % lang_code,
                    unicode(self.content_object)[:100]
                )
            activate_language(current_lang)
        else:
            self.content_object_id = ""
            for lang_code, lang_name in settings.LANGUAGES:
                setattr(self, "content_object_repr_%s" % lang_code, "")
            
        if not self.title:
            current_lang = get_current_language()
            for lang_code, lang_name in settings.LANGUAGES:
                activate_language(lang_code)
                setattr(
                    self,
                    "title_%s" % lang_code,
                    unicode(self.__unicode__())[:100]
                )
            activate_language(current_lang)
            
        super(MediaGalleryBase, self).save(**kwargs)
    save.alters_data = True
        
    def get_title(self, language=None):
        language = language or get_current_language()
        return getattr(self, "title_%s" % language, "") or self.title
        
    def get_absolute_url(self):
        return "%s%s/" % (
            self.content_object.get_absolute_url(),
            URL_ID_PORTFOLIO,
        )

    def get_url_path(self):
        if self.content_object:
            return u"%s%s/album/%s/" % (
                self.content_object.get_url_path(),
                URL_ID_PORTFOLIO,
                self.get_token(),
            )
        else:
            return u""

    def file_count(self, public=True):
        return self.mediafile_set.count()
    file_count.short_description = _('File Count')
    
    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

    def get_recroppable_thumbnail_path(self):
        if self.cover_image:
            return self.cover_image.path
        if self.mediafile_set.count():
            return self.mediafile_set.all()[0].get_recroppable_thumbnail_path()
        return ""
        
    def is_media_gallery(self):
        return True


class MediaFileBase(CreationModificationMixin):
    gallery = models.ForeignKey("media_gallery.MediaGallery", verbose_name=_("Media Gallery"))
    
    path = FileBrowseField(_('File path'), max_length=255, blank=True, help_text=_("A path to a locally stored image, video, or audio file."))
    
    external_url = URLField(_('External URL'), help_text=_("A URL of an external image, video, or audio file."), blank=True)

    splash_image_path = FileBrowseField(_('Splash-image path'), max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'], blank=True, help_text=_("Used for still images in Flash players and for thumbnails."))
    
    file_type=models.CharField(max_length=1, choices=MEDIA_FILE_TYPE_CHOICES, default="-", editable=False)
    
    title = MultilingualCharField(_("Title"), max_length=255, blank=True)
    description = MultilingualTextField(_("Description"), blank=True)
    
    sort_order = PositionField(_("Sort order"), collection="gallery")

    class Meta:
        ordering = ["sort_order", "creation_date"]
        verbose_name = _("Media File")
        verbose_name_plural = _("Media File")
        abstract = True
        
    def __unicode__(self):
        if self.path:
            return self.path.path
        else:
            return self.external_url
    
    def detect_file_type(self):
        result = "-"
        if self.path:
            file_path = self.path.path.lower()
        else:
            file_path = self.external_url.lower()
        for pattern, file_type in MEDIA_FILE_TYPE_RECOGNITION:
            if pattern.search(file_path):
                result = file_type
                break
        return result
        
    def save(self, *args, **kwargs):
        self.file_type = self.detect_file_type()
        super(MediaFileBase, self).save(*args, **kwargs)
    save.alters_data = True
    
    def get_related_file_obj(self):
        return self.path
        
    def get_splash_image_file_obj(self):
        return self.splash_image_path

    def get_thumbnail_url(self):
        if self.splash_image_path:
            abs_path = os.path.join(UPLOADS_ROOT, self.splash_image_path.path)
            if os.path.exists(abs_path):
                try:
                    path, query_params = image_mods.FileManager.modified_path(self.splash_image_path.path, "gt")
                except:
                    pass
                else:
                    url = "".join((UPLOADS_URL, path, query_params))
                    return url
        if self.file_type == "i" and self.path:
            abs_path = os.path.join(UPLOADS_ROOT, self.path.path)
            if os.path.exists(abs_path):
                try:
                    path, query_params = image_mods.FileManager.modified_path(self.path.path, "gt")
                except:
                    pass
                else:
                    url = "".join((UPLOADS_URL, path, query_params))
                    return url
        if self.file_type == "i":
            return IMAGE_SPLASH_TN_URL
        if self.file_type == "a":
            return AUDIO_SPLASH_TN_URL
        if self.file_type in ("v", "y", "m"):
            return VIDEO_SPLASH_TN_URL
        return ""
        
    def get_recroppable_thumbnail_path(self):
        if self.splash_image_path:
            return self.splash_image_path.path
        if self.file_type == "i" and self.path:
            return self.path.path
        return ""
        
    def get_list_image_url(self):
        if self.splash_image_path:
            abs_path = os.path.join(UPLOADS_ROOT, self.splash_image_path.path)
            if os.path.exists(abs_path):
                try:
                    url = "".join((
                        UPLOADS_URL,
                        image_mods.FileManager.modified_path(self.splash_image_path.path, "glist"),
                        ))
                except:
                    pass
                else:
                    return url
        if self.file_type == "i" and self.path:
            abs_path = os.path.join(UPLOADS_ROOT, self.path.path)
            if os.path.exists(abs_path):
                try:
                    path, query_params = image_mods.FileManager.modified_path(self.path.path, "glist")
                except:
                    pass
                else:
                    url = "".join((UPLOADS_URL, path, query_params))
                    return url
        if self.file_type == "i":
            return IMAGE_SPLASH_LIST_URL
        if self.file_type == "a":
            return AUDIO_SPLASH_LIST_URL
        if self.file_type in ("v", "y", "m"):
            return VIDEO_SPLASH_LIST_URL
        return ""
        
    def get_splash_image_url(self):
        if self.splash_image_path:
            abs_path = os.path.join(UPLOADS_ROOT, self.splash_image_path.path)
            if os.path.exists(abs_path):
                try:
                    modified_path, query = image_mods.FileManager.modified_path(self.splash_image_path.path, "gd")
                    url = "".join((UPLOADS_URL, modified_path, query))
                except:
                    pass
                else:
                    return url
        if self.file_type == "i":
            return IMAGE_SPLASH_URL
        if self.file_type == "a":
            return AUDIO_SPLASH_URL
        if self.file_type in ("v", "y", "m"):
            return VIDEO_SPLASH_URL
        return ""
        
    def get_representation(self, suffix=""):
        if suffix:
            suffix = "_%s" % suffix 
        context_dict = {
            'media_file': self,
            'UPLOADS_URL': UPLOADS_URL,
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL,
            'JETSON_MEDIA_URL': settings.JETSON_MEDIA_URL,
            }
        if self.file_type == "i":
            if self.path:
                return render_to_string(
                    "media_gallery/media_file_types/uploaded_image%s.html" % suffix,
                    context_dict,
                    )
            if self.external_url:
                return render_to_string(
                    "media_gallery/media_file_types/external_image%s.html" % suffix,
                    context_dict,
                    )
        if self.file_type == "a":
            if self.path:
                return render_to_string(
                    "media_gallery/media_file_types/uploaded_audio%s.html" % suffix,
                    context_dict,
                    )
            if self.external_url:
                return render_to_string(
                    "media_gallery/media_file_types/external_audio%s.html" % suffix,
                    context_dict,
                    )
        if self.file_type == "v":
            if self.path:
                return render_to_string(
                    "media_gallery/media_file_types/uploaded_video%s.html" % suffix,
                    context_dict,
                    )
            if self.external_url:
                return render_to_string(
                    "media_gallery/media_file_types/external_video%s.html" % suffix,
                    context_dict,
                    )
        if self.file_type == "y":
            if self.external_url:
                match = re.compile(
                    r"^https?://(.*?youtube\.com/watch\?v=|youtu\.be/)([^&]+)",
                    ).match(self.external_url)
                if match:
                    return render_to_string(
                        "media_gallery/media_file_types/youtube_video%s.html" % suffix,
                        dict(youtube_video_id=match.group(2), **context_dict)
                        )
        if self.file_type == "m":
            if self.external_url:
                match = re.compile(
                    r"^https?://.*?vimeo\.com/(\d+)",
                    ).match(self.external_url)
                if match:
                    return render_to_string(
                        "media_gallery/media_file_types/vimeo_video%s.html" % suffix,
                        dict(vimeo_video_id=match.group(1), **context_dict)
                        )
        return ""

    def get_preview_representation(self):
        return self.get_representation(suffix="preview")
        
    def get_token(self):
        if self.pk:
            return int(self.pk) + TOKENIZATION_SUMMAND
        else:
            return None

