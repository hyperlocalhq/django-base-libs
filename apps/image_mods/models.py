# -*- coding: UTF-8 -*-
import os
import stat
import time
import sys
import fnmatch
from shutil import rmtree
from datetime import datetime
from inspect import isclass

from django.db import models
from django.core.files import base
from django.conf import settings

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from base_libs.utils.betterslugify import better_slugify

from filebrowser.fields import FileBrowseField
from filebrowser.functions import get_version_path
from filebrowser.settings import *
from filebrowser.base import FileObject

# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    import Image
    import ImageFile
    import ImageOps
    import ImageFilter
    import ImageEnhance
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageFile
        from PIL import ImageOps
        from PIL import ImageFilter
        from PIL import ImageEnhance
    except ImportError:
        raise ImportError(
            _(
                'Filebrowser was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.'
            )
        )

from base_libs.utils.crypt import cryptString

# Modify image file buffer size.
ImageFile.MAXBLOCK = IMAGE_MAXBLOCK

# Prepare a list of image filters
filter_names = []
for n in dir(ImageFilter):
    klass = getattr(ImageFilter, n)
    if isclass(klass) and issubclass(klass, ImageFilter.BuiltinFilter
                                    ) and hasattr(klass, 'name'):
        filter_names.append(klass.__name__)

# The following string made non-translatable, because it messes up the migrations,
# when the default language is not English in the project
image_filters_help_text = (
    'Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE". '
    'Image filters will be applied in order. The following filter are available: %s'
) % ', '.join(filter_names)
# TODO: shouldn't we remove the filters functionality from this app as it is not used anywhere anyway?

# Quality options for JPEG images
JPEG_QUALITY_CHOICES = (
    (30, _('Very Low')),
    (40, _('Low')),
    (50, _('Medium-Low')),
    (60, _('Medium')),
    (70, _('Medium-High')),
    (80, _('High')),
    (90, _('Very High')),
)

# choices for new crop_anchor field in Photo
CROP_ANCHOR_CHOICES = (
    ('top', _('Top')),
    ('right', _('Right')),
    ('bottom', _('Bottom')),
    ('left', _('Left')),
    ('center', _('Center (Default)')),
)

OUTPUT_FORMAT_CHOICES = (
    ('png', 'PNG'),
    ('jpg', 'JPEG'),
    ('gif', 'GIF'),
)

MOD_FOR_FILES = stat.S_IREAD | stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH
MOD_FOR_DIRS = stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH
if settings.FILE_UPLOAD_PERMISSIONS == 0777:
    MOD_FOR_FILES = 0777
    MOD_FOR_DIRS = 0777

verbose_name = _("Image Modifications")


class FileManager:
    _cached_modifications = {}

    @staticmethod
    def tokenize(*args):
        """
        takes any amount of strings as params and makes unique token from that
        """
        return better_slugify(cryptString("".join(args)))[:10]

    @staticmethod
    def path_exists(*args):
        """
        Make sure that a directory at specific path exists. If it doesn't exist, it will be created
        
        For example:
        FileManager.path_exists("/path/to/directory")
        '/path/to/directory'
        FileManager.path_exists("/path/to", "another", "directory")
        '/path/to/another/directory'
        """
        path = os.path.join(*args)
        if not os.path.isdir(path):
            os.makedirs(path)
        directories = path[len(settings.UPLOADS_ROOT):].split("/")
        abs_path = settings.UPLOADS_ROOT
        for d in directories:
            abs_path = os.path.join(abs_path, d)
            #try:
            #    os.chmod(abs_path, MOD_FOR_DIRS)
            #except OSError:
            #    pass
        return path

    @staticmethod
    def locate(pattern, root=os.curdir):
        """
        Locate all files matching supplied filename pattern in and below
        supplied root directory.
        
        For example:
        for f in FileManager.locate("*.html"):
            f
        '/path/to/myproject/templates/a.html'
        '/path/to/myproject/templates/b.html'
        '/path/to/myproject/templates/directory/c.html'
        """
        for path, dirs, files in os.walk(os.path.abspath(root)):
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(path, filename)

    @staticmethod
    def save_file(path, content, **kwargs):
        """
        Save media file and create a thumbnail for the filebrowser
        """
        abs_path = os.path.join(settings.UPLOADS_ROOT, *path.split("/"))
        abs_dir, filename = os.path.split(abs_path)
        FileManager.path_exists(abs_dir)
        filename_base, filename_ext = os.path.splitext(filename)

        f = open(abs_path, 'wb')
        if isinstance(content, base.File):
            for chunk in content.chunks():
                f.write(chunk)
        else:
            f.write(content)
        f.close()
        file_type = ""
        for k, v in EXTENSIONS.iteritems():
            for ext in v:
                if ext == filename_ext:
                    file_type = k
        file_timestamp = datetime.fromtimestamp(os.path.getmtime(abs_path))
        #try:
        #    os.chmod(abs_path, MOD_FOR_FILES)
        #except OSError:
        #    pass
        return True

    @staticmethod
    def delete_file(path):
        """
        Delete media file or directory and all its modifications
        """
        abs_path = os.path.join(settings.UPLOADS_ROOT, *path.split("/"))
        abs_dir, filename = os.path.split(abs_path)

        if os.path.isdir(abs_path):
            rmtree(abs_path)
        else:
            filename_base, filename_ext = os.path.splitext(filename)
            abs_cache_dir = os.path.join(abs_dir, "_cache")
            # delete filebrowser image versions/thumbnails
            for version in VERSIONS:
                relative_server_path = os.path.join(DIRECTORY, path)
                try:
                    os.unlink(
                        os.path.join(
                            settings.UPLOADS_ROOT,
                            get_version_path(relative_server_path, version)
                        )
                    )
                except:
                    pass
            # delete image_mods cached versions
            for mod_file_path in FileManager.locate(
                "%s_*" % filename,
                abs_cache_dir,
            ):
                try:
                    os.unlink(mod_file_path)
                except:
                    pass
            try:
                os.unlink(abs_path)
            except:
                pass

    @staticmethod
    def save_file_for_object(
        obj,
        filename,
        content,
        field_name="image",
        subpath="",  # if not empty, must have a trailing slash
        use_timestamp=True,
        replace_existing=True,
    ):
        """
        Saves media file for an object and assigns the relative
        filebrowser path of the file to the specified field of the object.
        
        The absolute path of the file:
        settings.UPLOADS_ROOT + obj.get_filebrowser_path() + subpath + mediafile.filename        
        """
        if replace_existing:
            FileManager.delete_file_for_object(obj, field_name)
        filename_base, filename_ext = os.path.splitext(filename)
        if use_timestamp:
            now = tz_now()
            filename = "".join(
                (
                    now.strftime("%Y%m%d%H%M%S"),
                    ("000" + str(int(round(now.microsecond / 1000))))[-4:],
                    filename_ext
                )
            )
            # sleep a little bit to ensure that the next file name will be unique
            time.sleep(0.001)

        path = ""
        if hasattr(obj, "get_filebrowser_dir"):
            if callable(obj.get_filebrowser_dir):
                path += obj.get_filebrowser_dir()
        if subpath:
            path += subpath
        path += filename
        FileManager.save_file(path, content)
        setattr(obj, field_name, path)
        if obj.pk:
            # saving without modifying modification dates nor triggering signals
            obj._default_manager.filter(
                pk=obj.pk
            ).update(**{field_name: FileObject(path=path)})
        else:
            obj.save()

    @staticmethod
    def delete_file_for_object(obj, field_name="image"):
        """
        Delete media file for an object
        """
        file_obj = getattr(obj, field_name)
        if file_obj:
            try:
                FileManager.delete_file(file_obj.path)
            except OSError:
                pass

        setattr(obj, field_name, "")
        if obj.pk:
            # saving without modifying modification dates nor triggering signals
            obj._default_manager.filter(pk=obj.pk).update(**{field_name: ""})
        else:
            obj.save()

    @staticmethod
    def mod_exists(rel_orig_path, sysname):
        """ 
        Returns True if relative filebrowser path to the modified image exists,
        or else False.
        """
        orig_path_server = os.path.join(
            settings.UPLOADS_ROOT, *rel_orig_path.split("/")
        )
        if sysname in FileManager._cached_modifications:
            mod = FileManager._cached_modifications[sysname]
        else:
            try:
                mod = ImageModification.objects.get(sysname=sysname)
            except:
                return rel_orig_path
            else:
                FileManager._cached_modifications[sysname] = mod

        mod_path = mod.modified_path(rel_orig_path)
        mod_path_server = os.path.join(
            settings.UPLOADS_ROOT, *mod_path.split("/")
        )

        return os.path.isfile(mod_path_server)

    @staticmethod
    def modified_path(rel_orig_path, sysname):
        """ 
        Returns the relative filebrowser path to the modified image.
        If the modified image does not exist,
            it will be created
        If modification does not exist,
            the original image path will be returned
        If the dimmensions of the image match the dimmensions of the modification,
            the original path will be returned
        
        Example:
            p, query_params = FileManager.modified_path("test/original.png", "gallery_default")
            p == "test/_cache/original.png_gallery_default.jpg"
            query_params == "?t=201710241254"
            
        """
        if rel_orig_path.startswith("/"):
            rel_orig_path = rel_orig_path[1:]
        orig_path_server = os.path.join(
            settings.UPLOADS_ROOT, *rel_orig_path.split("/")
        )
        if sysname in FileManager._cached_modifications:
            mod = FileManager._cached_modifications[sysname]
        else:
            try:
                mod = ImageModification.objects.get(sysname=sysname)
            except:
                return rel_orig_path, ""
            else:
                FileManager._cached_modifications[sysname] = mod

        try:
            im = Image.open(orig_path_server)
        except IOError:
            return "", ""
        cur_width, cur_height = im.size

        if mod.crop:
            if cur_width == mod.width and cur_height == mod.height:
                return rel_orig_path, ""
        else:
            if mod.width == 0 and cur_height == mod.height \
                or mod.height == 0 and cur_width == mod.width:
                return rel_orig_path, ""

        mod_path = mod.modified_path(rel_orig_path)
        mod_path_server = os.path.join(
            settings.UPLOADS_ROOT, *mod_path.split("/")
        )

        if os.path.isfile(orig_path_server):
            if not os.path.isfile(mod_path_server):
                abs_dir, filename = os.path.split(mod_path_server)
                FileManager.path_exists(abs_dir)
                mod.process_image(orig_path_server)

        try:
            mtime = os.path.getmtime(mod_path_server)
        except OSError:
            mtime = 0
        last_modified = datetime.fromtimestamp(mtime)

        return (mod_path, "?t={:%Y%m%d%H%M}".format(last_modified))


class ImageModificationGroup(models.Model):
    """ A pre-defined effect to apply to image files """
    title = models.CharField(_('Title'), max_length=255)

    class Meta:
        verbose_name = _("Image Modification Group")
        verbose_name_plural = _("Image Modification Groups")
        ordering = ("title", )

    def __unicode__(self):
        return self.title


class ImageModificationManager(models.Manager):
    def versions(self):
        return self.exclude(sysname__in=["cropping_preview"], )


class ImageModification(models.Model):
    """ A pre-defined effect to apply to image files """
    sysname = models.SlugField(
        _("Sysname"),
        max_length=255,
        help_text=_(
            "Sysnames are used for cached file suffixes and in the templates"
        )
    )

    title = models.CharField(_('Title'), max_length=255)

    width = models.PositiveIntegerField(
        _('Width'),
        default=0,
        help_text=_('Leave to size the image to the set height')
    )
    height = models.PositiveIntegerField(
        _('Height'),
        default=0,
        help_text=_('Leave to size the image to the set width')
    )
    quality = models.PositiveIntegerField(
        _('Quality'),
        choices=JPEG_QUALITY_CHOICES,
        default=70,
        help_text=_('JPEG image quality.')
    )
    crop = models.BooleanField(
        _('Crop to fit?'),
        default=False,
        help_text=_(
            'If selected the image will be scaled and cropped to fit the supplied dimensions.'
        )
    )
    crop_from = models.CharField(
        _('Crop from'),
        blank=True,
        max_length=10,
        default='center',
        choices=CROP_ANCHOR_CHOICES
    )

    mask = FileBrowseField(
        _("Mask"), max_length=255, extensions=['.png'], blank=True, null=True
    )

    frame = FileBrowseField(
        _("Frame"), max_length=255, extensions=['.png'], blank=True, null=True
    )

    output_format = models.CharField(
        _("Output format"),
        max_length=255,
        default="png",
        choices=OUTPUT_FORMAT_CHOICES
    )

    color = models.FloatField(
        _('Color'),
        default=1.0,
        help_text=_(
            'A factor of 0.0 gives a black and white image, a factor of 1.0 gives the original image.'
        )
    )
    brightness = models.FloatField(
        _('Brightness'),
        default=1.0,
        help_text=_(
            'A factor of 0.0 gives a black image, a factor of 1.0 gives the original image.'
        )
    )
    contrast = models.FloatField(
        _('Contrast'),
        default=1.0,
        help_text=_(
            'A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the original image.'
        )
    )
    sharpness = models.FloatField(
        _('Sharpness'),
        default=1.0,
        help_text=_(
            'A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image.'
        )
    )
    filters = models.CharField(
        _('Filters'),
        max_length=200,
        blank=True,
        help_text=image_filters_help_text
    )

    group = models.ForeignKey(
        ImageModificationGroup,
        verbose_name=_("Image Modification Group"),
        blank=True,
        null=True,
        help_text=_(
            "Assign a group of modifications which will be triggered together while cropping."
        )
    )

    notes = models.TextField(_("Notes"), blank=True)

    objects = ImageModificationManager()

    class Meta:
        verbose_name = _("Image Modification")
        verbose_name_plural = _("Image Modifications")
        ordering = ("sysname", )

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title

    def _related_mods(self):
        if not self.group:
            return ImageModification.objects.none()
        else:
            return self.group.imagemodification_set.exclude(pk=self.pk)

    related_mods = property(_related_mods)

    def delete_cached_images(self):
        """ delete the cached images of this modification """
        for path in FileManager.locate(
            "*_%s.*" % self.sysname, settings.UPLOADS_ROOT
        ):
            file_dir, filename = os.path.split(path)
            if os.path.split(file_dir)[1] == "_cache":
                try:
                    os.unlink(path)
                except OSError:
                    pass

    delete_cached_images.alters_data = True

    def save(self, *args, **kwargs):
        super(type(self), self).save(*args, **kwargs)
        self.delete_cached_images()

    save.alters_data = True

    def delete(self, *args, **kwargs):
        super(type(self), self).delete(*args, **kwargs)
        self.delete_cached_images()

    delete.alters_data = True

    def modified_path(self, path):
        path = path.replace("\\", "/")
        if "/" in path:
            dir_name, filename = path.rsplit("/", 1)
            dir_name += "/"
        else:
            dir_name, filename = "", path
        mod_path = "%s_cache/%s_%s.%s" % (
            dir_name,
            filename,
            self.sysname,
            self.output_format,
        )
        return mod_path

    def process_image(self, absolute_original_path):
        try:
            im = Image.open(absolute_original_path)
        except IOError:
            return False

        try:
            im.load()
        except IOError:
            pass
        except (ValueError, OSError):
            return False

        if im.mode != "RGB":
            im = im.convert("RGB")
        cur_width, cur_height = im.size
        new_width, new_height = self.width, self.height

        try:
            cropping = self.imagecropping_set.get(
                original=FileObject(
                    absolute_original_path[len(settings.UPLOADS_ROOT) + 1:]
                )
            )
        except:
            cropping = None

        if cropping:
            canvas_w = cropping.x2 - cropping.x1
            canvas_h = cropping.y2 - cropping.y1
            box = (
                max(cropping.x1, 0),
                max(cropping.y1, 0),
                min(cropping.x2, cur_width),
                min(cropping.y2, cur_height),
            )
            pos = (
                max(-cropping.x1, 0),
                max(-cropping.y1, 0),
            )
            canvas = Image.new(
                "RGB", (canvas_w, canvas_h), cropping.bgcolor.upper()
            )
            cropped = im.crop(box)
            canvas.paste(cropped, pos)
            im = canvas
            cur_width, cur_height = im.size

        if self.crop:
            ratio = max(
                float(new_width) / cur_width,
                float(new_height) / cur_height
            )
            x = (cur_width * ratio)
            y = (cur_height * ratio)
            xd = abs(new_width - x)
            yd = abs(new_height - y)
            x_diff = int(xd / 2)
            y_diff = int(yd / 2)
            if self.crop_from == 'top':
                box = (int(x_diff), 0, int(x_diff + new_width), new_height)
            elif self.crop_from == 'left':
                box = (0, int(y_diff), new_width, int(y_diff + new_height))
            elif self.crop_from == 'bottom':
                box = (int(x_diff), int(yd), int(x_diff + new_width),
                       int(y))  # y - yd = new_height
            elif self.crop_from == 'right':
                box = (int(xd), int(y_diff), int(x),
                       int(y_diff + new_height))  # x - xd = new_width
            else:
                box = (
                    int(x_diff), int(y_diff), int(x_diff + new_width),
                    int(y_diff + new_height)
                )
            resized = im.resize((int(x), int(y)), Image.ANTIALIAS).crop(box)
        else:
            if not new_width == 0 and not new_height == 0:
                ratio = min(
                    float(new_width) / cur_width,
                    float(new_height) / cur_height,
                )
            else:
                if new_width == 0:
                    ratio = float(new_height) / cur_height
                else:
                    ratio = float(new_width) / cur_width
            resized = im.resize(
                (int(round(cur_width * ratio)), int(round(cur_height * ratio))),
                Image.ANTIALIAS,
            )

        if resized.mode == 'RGB':
            for name in ['Color', 'Brightness', 'Contrast', 'Sharpness']:
                factor = getattr(self, name.lower())
                if factor != 1.0:
                    resized = getattr(ImageEnhance,
                                      name)(resized).enhance(factor)
            for name in self.filters.split('->'):
                image_filter = getattr(ImageFilter, name.upper(), None)
                if image_filter is not None:
                    try:
                        resized = resized.filter(image_filter)
                    except ValueError:
                        pass

        if self.mask:
            try:
                mask = Image.open(
                    os.path.join(
                        settings.UPLOADS_ROOT, *self.mask.path.split("/")
                    ),
                )
            except:
                pass
            else:
                resized = resized.convert("RGBA")
                # resize/crop the image to the size of the mask-image
                resized = ImageOps.fit(
                    resized, mask.size, method=Image.ANTIALIAS
                )
                # get the alpha-channel (used for non-replacement)
                r, g, b, a = mask.split()
                resized.paste(mask, mask=a)

        if self.frame:
            try:
                frame = Image.open(
                    os.path.join(
                        settings.UPLOADS_ROOT, *self.frame.path.split("/")
                    ),
                )
            except:
                pass
            else:
                resized = resized.convert("RGBA")
                # resize/crop the image to the size of the mask-image
                resized = ImageOps.fit(
                    resized, frame.size, method=Image.ANTIALIAS
                )
                # paste the frame mask without replacing the alpha mask of the mask-image
                r, g, b, a = frame.split()
                resized.paste(frame, mask=a)

        absolute_resized_path = self.modified_path(absolute_original_path)

        try:
            if im.format == 'JPEG':
                resized.save(
                    absolute_resized_path,
                    'JPEG',
                    quality=int(self.quality),
                    optimize=True,
                )
            else:
                resized.save(absolute_resized_path)
        except IOError, e:
            if os.path.isfile(absolute_resized_path):
                os.unlink(absolute_resized_path)
            return False  #raise e
        else:
            #try:
            #    os.chmod(absolute_resized_path, MOD_FOR_FILES)
            #except OSError:
            #    pass
            pass

        return True

    process_image.alters_data = True


class ImageCropping(models.Model):
    original = FileBrowseField(
        _("Original"),
        max_length=500,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']
    )
    mods = models.ManyToManyField(
        ImageModification,
        verbose_name=_("Modifications"),
        help_text=_(
            'Modifications with the same ratio which should be used to recrop images together.'
        )
    )
    x1 = models.IntegerField(_('X1'), default=0)
    y1 = models.IntegerField(_('Y1'), default=0)
    x2 = models.IntegerField(_('X2'), default=0)
    y2 = models.IntegerField(_('Y2'), default=0)
    bgcolor = models.CharField(
        _('Canvas color'), max_length=7, default="#ffffff"
    )

    class Meta:
        verbose_name = _("Image Cropping")
        verbose_name_plural = _("Image Croppings")
        ordering = ("original", )

    def __unicode__(self):
        return self.original.path

    def repr(self):
        return "%s (%d,%d)-(%d,%d)" % (
            self.original, self.x1, self.y1, self.x2, self.y2
        )

    def update_versions(self):
        for mod in self.mods.all():
            mod.process_image(
                os.path.join(
                    settings.UPLOADS_ROOT, *self.original.path.split("/")
                )
            )

    update_versions.alters_data = True

    def delete(self, *args, **kwargs):
        # this is not called if you delete objects by admin actions
        mods = list(self.mods.all())
        super(ImageCropping, self).delete(*args, **kwargs)
        for mod in mods:
            abs_path = os.path.join(
                settings.UPLOADS_ROOT, *self.original.path.split("/")
            )
            mod.process_image(abs_path)

    delete.alters_data = True
