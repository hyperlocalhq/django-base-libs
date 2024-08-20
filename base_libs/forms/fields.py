import datetime
import os
import re
import time
from io import BytesIO
from functools import reduce
import binascii

from django import forms
from django.utils.translation import gettext_lazy as _, gettext
from django.utils.encoding import force_str
from django.template.defaultfilters import filesizeformat
from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import Input
from django.forms.widgets import CheckboxInput
from django.forms.widgets import RadioSelect
from django.forms.widgets import CheckboxSelectMultiple
from django.conf import settings

from babel.numbers import parse_number, parse_decimal, NumberFormatError
from babel.dates import format_date, format_time
from babel.dates import parse_date, parse_time
from babel.dates import get_date_format, get_time_format

from base_libs.utils.crypt import cryptString, decryptString
from base_libs.utils.emails import is_valid_email, get_email_and_name
from base_libs.utils.misc import get_installed
from base_libs.middleware.threadlocals import get_current_language
from base_libs.widgets import (
    AutocompleteWidget,
    AutocompleteMultipleWidget,
    SelectToAutocompleteWidget,
    ObjectSelect,
    IntegerWidget,
    DecimalWidget,
    DateWidget,
    TimeWidget,
    URLWidget,
)

SECURITY_FIELD_MIN_TIME = getattr(settings, "SECURITY_FIELD_MIN_TIME", 3)  # 3 seconds
SECURITY_FIELD_MAX_TIME = getattr(settings, "SECURITY_FIELD_MAX_TIME", 3600)  # 1 hour


class IntegerField(forms.IntegerField):
    widget = IntegerWidget

    def clean(self, value):
        locale = get_current_language()
        if value != "":
            try:
                value = force_str(parse_number(value, locale=locale))
            except NumberFormatError:
                raise forms.ValidationError(_("This value is not valid."))
        return super(IntegerField, self).clean(value)


class FloatField(forms.FloatField):
    widget = DecimalWidget

    def __init__(self, format=None, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)
        self.format = self.widget.format = format

    def clean(self, value):
        locale = get_current_language()
        if value != "":
            try:
                value = force_str(parse_decimal(value, locale=locale))
            except NumberFormatError:
                raise forms.ValidationError(self.error_messages["invalid"])
        return super(FloatField, self).clean(value)


class DecimalField(forms.DecimalField):
    widget = DecimalWidget

    def __init__(self, format="#,##0.00", *args, **kwargs):
        super(DecimalField, self).__init__(*args, **kwargs)
        if self.decimal_places:
            format = "#,##0." + self.decimal_places * "0"
        self.format = self.widget.format = format

    def clean(self, value):
        locale = get_current_language()
        if value != "":
            try:
                value = force_str(parse_decimal(value, locale=locale))
            except NumberFormatError:
                raise forms.ValidationError(self.error_messages["invalid"])
        return super(DecimalField, self).clean(value)


class DateField(forms.DateField):
    widget = DateWidget

    def __init__(self, format="medium", *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)
        locale = get_current_language()
        self.format = self.widget.format = format
        self.date_format = get_date_format(locale=locale)
        self.date_example = format_date(datetime.datetime.now(), locale=locale)

    def clean(self, value):
        locale = get_current_language()
        if value != "":
            try:
                value = parse_date(value, locale=locale)
            except:
                raise forms.ValidationError(self.error_messages["invalid"])
        return super(DateField, self).clean(value)


class TimeField(forms.TimeField):
    widget = TimeWidget

    def __init__(self, format="medium", *args, **kwargs):
        super(TimeField, self).__init__(*args, **kwargs)
        locale = get_current_language()
        self.format = self.widget.format = format
        self.time_format = get_time_format(locale=locale)
        self.time_example = format_time(datetime.datetime.now(), locale=locale)

    def clean(self, value):
        locale = get_current_language()
        if value != "":
            try:
                value = parse_time(value, locale=locale)
            except:
                raise forms.ValidationError(self.error_messages["invalid"])
        return super(TimeField, self).clean(value)


class PlainTextFormField(forms.CharField):
    """ a plain text form field """

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.Textarea(attrs={"class": "vPlainTextField"})
        super(PlainTextFormField, self).__init__(*args, **kwargs)


class SecurityField(forms.CharField):
    """
    A field which checks whether the form was filled in within the 
    given range of time
    
    The concept works only for Unbounded forms.
    """

    time_elapsed = 0
    default_error_messages = {
        "invalid": _(
            "The data transfer didn't pass the security test. You are considered as a spambot."
        ),
    }

    def generate_value(self):
        started = cryptString(
            str(int(time.mktime(datetime.datetime.now().timetuple())))
        )
        return started

    def _pass_test(self, value):
        try:
            started = int(decryptString(value))
        except (binascii.Error, ValueError):
            return False
        current = int(time.mktime(datetime.datetime.now().timetuple()))
        self.time_elapsed = current - started
        return self.MIN_TIME < current - started < self.MAX_TIME

    def __init__(self, *args, **kwargs):
        super(SecurityField, self).__init__(*args, **kwargs)
        self.widget = forms.HiddenInput()
        self.initial = self.generate_value
        self.required = True
        self.MIN_TIME = SECURITY_FIELD_MIN_TIME
        self.MAX_TIME = SECURITY_FIELD_MAX_TIME

    def clean(self, value):
        value = super(SecurityField, self).clean(value)
        # python3 wraps value around b"". So we strip those characters
        # in order for the pass_test function to work properly.
        if len(value) == 27:
            value = value[2:-1]
        self._pass_test(value)
        if not self._pass_test(value):
            raise forms.ValidationError(self.error_messages["invalid"])
        return value


class SingleEmailTextField(forms.CharField):
    """
    an email field
    """

    def clean(self, value):
        if not value:
            if self.required:
                raise forms.ValidationError(
                    gettext("Please enter a valid e-mail address")
                )
            else:
                return None

        # TODO here we have to add some mechanism to handle "firstname lastname <email>" format
        email = value
        if not is_valid_email(email):
            raise forms.ValidationError(
                gettext('"%(email)s" is not a valid e-mail address')
                % {"email": email}
            )
        return email


class MultiEmailTextField(forms.Field):
    """
    a "multi-email" email field
    """

    def clean(self, value):
        if not value:
            if self.required:
                raise forms.ValidationError(
                    gettext("Please enter at least one valid e-mail address")
                )
            else:
                return None

        # fist normalize newline characters (windows has '\r\n', unix has '\n')
        # TODO I hope, Mac is like unix!
        recipient_string = re.sub(r"(\r\n|\r|\n)", ",", value)
        # replace all double commas by one comma
        recipient_string = re.sub(
            r"(,\s,|,\s;|;\s,|;\s;|,,|,;|;,|;;)", ",", recipient_string
        )
        recipient_list = re.split(r"[,;]", recipient_string)
        recipient_result_list = []
        for recipient in recipient_list:
            (recipient_email, recipient_name) = get_email_and_name(recipient)

            if not is_valid_email(recipient_email):
                raise forms.ValidationError(
                    gettext('"%(email)s" is not a valid e-mail address')
                    % {"email": recipient_email}
                )

            recipient_result_list.append((recipient_email, recipient_name))
        return recipient_result_list


class AutocompleteField(forms.CharField):
    """ a forms autocomplete field """

    def __init__(
        self,
        app,
        qs_function,
        display_attr,
        add_display_attr=None,
        options=None,
        attrs=None,
        *args,
        **kwargs
    ):

        if not attrs:
            attrs = {}
        if not options:
            options = {}
        self.widget = AutocompleteWidget(
            app, qs_function, display_attr, add_display_attr, options, attrs
        )

        super(AutocompleteField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return super(AutocompleteField, self).clean(value)


class AutocompleteModelChoiceField(AutocompleteField):
    def __init__(
        self,
        app,
        qs_function,
        display_attr,
        add_display_attr=None,
        options=None,
        attrs=None,
        *args,
        **kwargs
    ):
        if not attrs:
            attrs = {}
        if not options:
            options = {}
        super(AutocompleteModelChoiceField, self).__init__(
            app,
            qs_function,
            display_attr,
            add_display_attr,
            options,
            attrs,
            *args,
            **kwargs
        )
        self.app = app
        self.qs_function = qs_function

    def to_python(self, value):
        func = get_installed(
            "%(app)s.ajax.%(func)s" % {"app": self.app, "func": self.qs_function,}
        )
        if value:
            try:
                value = func("all").get(pk=value)
            except:
                raise forms.ValidationError(self.error_messages["invalid"])
        else:
            value = None
        return value

    def prepare_value(self, value):
        if hasattr(value, "pk"):
            return value.pk
        return value


class AutocompleteModelMultipleChoiceField(forms.CharField):
    def __init__(
        self,
        app,
        qs_function,
        display_attr,
        add_display_attr=None,
        options=None,
        attrs=None,
        *args,
        **kwargs
    ):

        if not attrs:
            attrs = {}
        if not options:
            options = {}
        self.widget = AutocompleteMultipleWidget(
            app, qs_function, display_attr, add_display_attr, options, attrs
        )

        super(AutocompleteModelMultipleChoiceField, self).__init__(*args, **kwargs)
        self.app = app
        self.qs_function = qs_function

    def to_python(self, value):
        func = get_installed(
            "%(app)s.ajax.%(func)s" % {"app": self.app, "func": self.qs_function,}
        )
        if value:
            try:
                value = func("all").filter(pk__in=value.split(","))
            except:
                raise forms.ValidationError(self.error_messages["invalid"])
        else:
            value = func("all").none()
        return value


class SelectToAutocompleteField(AutocompleteField):
    """ a forms autocomplete field which renders as select field for non-javascript viewers """

    def __init__(
        self,
        app,
        qs_function,
        display_attr,
        add_display_attr=None,
        options=None,
        attrs=None,
        *args,
        **kwargs
    ):

        if not attrs:
            attrs = {}
        if not options:
            options = {}
        self.app = app
        self.qs_function = qs_function
        self.func = get_installed(
            "%(app)s.ajax.%(func)s" % {"app": self.app, "func": self.qs_function,}
        )
        self.queryset = self.func("all")

        self.widget = SelectToAutocompleteWidget(
            app, qs_function, display_attr, add_display_attr, options, attrs
        )

        forms.CharField.__init__(self, *args, **kwargs)

    def clean(self, value):
        if not value:
            return None
        try:
            value = self.queryset.get(pk=value)
        except:
            raise forms.ValidationError(self.error_messages["invalid"])
        return value


class ObjectChoiceField(forms.Field):
    """
    obj_list should be a list/tuple of querysets each returning instances of
    different models.
    E.g. (User.objects.all(), Group.objects.all())
    """

    widget = ObjectSelect
    default_error_messages = {
        "invalid_choice": _(
            "Select a valid choice. That choice is not one of the available choices."
        ),
    }

    def __init__(
        self,
        choices=(),
        obj_list=(),
        default_text="",
        required=True,
        widget=None,
        label=None,
        initial=None,
        help_text=None,
        *args,
        **kwargs
    ):
        super(ObjectChoiceField, self).__init__(
            required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs
        )
        self.choices = choices
        self.obj_list = obj_list
        self.widget.default_text = default_text

    def _get_obj_list(self):
        return self._obj_list

    def _set_obj_list(self, value):
        self._obj_list = value
        choice_list = []
        for q in self._obj_list:
            object_choice = [
                (ObjectChoiceField.returnKey(o), force_str(o)) for o in q
            ]
            choice_list.append(
                (force_str(q.model._meta.verbose_name).title(), object_choice)
            )
        self.choices = choice_list

    obj_list = property(_get_obj_list, _set_obj_list)

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        # Setting choices also sets the choices on the widget.
        # choices can be any iterable, but we call list() on it because
        # it will be consumed more than once.
        self._choices = self.widget.choices = list(value)

    choices = property(_get_choices, _set_choices)

    def clean(self, value):
        """
        Validates that the input is in self.choices.
        """
        if value in forms.fields.EMPTY_VALUES:
            value = ""
        if not isinstance(value, str):
            value = ObjectChoiceField.returnKey(value)
        value = force_str(value)
        value = super(ObjectChoiceField, self).clean(value)
        if value == "":
            return value
        # flatten key choices
        valid_values = set(
            reduce(
                lambda a, b: a + b,
                [list(dict(group).keys()) for group in dict(self.widget.choices).values()],
            )
        )
        if value not in valid_values:
            raise forms.ValidationError(
                self.error_messages["invalid_choice"] % {"value": value}
            )
        if value:
            value = ObjectChoiceField.returnObject(value)
        return value

    @staticmethod
    def returnObject(data):
        app_label, model, pk = data.split("/")
        ct = ContentType.objects.get(app_label__exact=app_label, model__exact=model,)
        obj = ct.get_object_for_this_type(pk=pk)
        return obj

    @staticmethod
    def returnKey(obj):
        ct = ContentType.objects.get_for_model(obj)
        return "/".join((ct.app_label, ct.model, str(obj.pk)))


class ImageField(forms.FileField):
    """
    Form field handling image uploads
    """

    default_error_messages = {
        "invalid_image": _(
            "The file you uploaded was either not an image, was corrupted, or contained unsupported properties. Please save it for web without interlacing and try again."
        ),
        "invalid_extension": _("File type of the uploaded file is invalid."),
    }

    def __init__(
        self,
        valid_file_extensions=("bmp", "gif", "jpeg", "jpg", "png", "tif", "tiff",),
        max_file_size=5 * 1024 * 1024,  # 5 MB
        min_dimensions=(480, 480),
        max_ratio=5,
        *args,
        **kwargs
    ):
        self.default_error_messages.update(
            {
                "too_small_dimensions": _(
                    "The media file is too small. The minimal dimensions are %(width)dx%(height)d."
                )
                % {"width": min_dimensions[0], "height": min_dimensions[1],},
                "too_large_ratio": _(
                    "The ratio of the dimensions is too large. The maximal allowed ratio is %d:1."
                )
                % max_ratio,
                "too_large_file": _(
                    "The media file is too large. The maximal allowed file size is %s."
                )
                % filesizeformat(max_file_size),
            }
        )
        self.min_dimensions = min_dimensions
        self.max_ratio = max_ratio
        self.valid_file_extensions = valid_file_extensions
        self.max_file_size = max_file_size
        super(ImageField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports).
        """
        f = super(ImageField, self).clean(data, initial)
        if f is None:
            return None
        elif not data and initial:
            return initial

        # if the FILES were already used outside of the form,
        # let's move the cursor back to the beginning of the file
        data.seek(0)

        if data.name.split(".")[-1].lower() not in self.valid_file_extensions:
            raise forms.ValidationError(self.error_messages["invalid_extension"],)

        if data.size > self.max_file_size:
            raise forms.ValidationError(self.error_messages["too_large_file"])

        from PIL import Image

        # We need to get a file object for PIL. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, "temporary_file_path"):
            file = data.temporary_file_path()
        else:
            if hasattr(data, "read"):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data["content"])

        try:
            # load() is the only method that can spot a truncated JPEG,
            #  but it cannot be called sanely after verify()
            trial_image = Image.open(file)
            trial_image.load()
            # Since we're about to use the file again we have to reset the
            # file object if possible.
            if hasattr(file, "reset"):
                file.reset()

            # verify() is the only method that can spot a corrupt PNG,
            #  but it must be called immediately after the constructor
            trial_image = Image.open(file)
            trial_image.verify()
        except IndexError:
            raise forms.ValidationError(self.error_messages["invalid_image"])
        else:
            width, height = trial_image.size
            if width < self.min_dimensions[0] or height < self.min_dimensions[1]:
                raise forms.ValidationError(
                    self.error_messages["too_small_dimensions"],
                )
            if 1.0 * max(width, height) / min(width, height) > self.max_ratio:
                raise forms.ValidationError(self.error_messages["too_large_ratio"],)
        if hasattr(data, "seek") and callable(data.seek):
            data.seek(0)
        return data


class VideoField(forms.FileField):
    """
    Form field handling video uploads
    """

    default_error_messages = {
        "invalid_video": _(
            "Upload a valid video. The file you uploaded was either not a video or a corrupted video."
        ),
        "invalid_extension": _("File type of the uploaded file is invalid."),
    }

    def __init__(
        self,
        valid_file_extensions=(
            "3gp",
            "asf",
            "asx",
            "avi",
            "flv",
            "mov",
            "mp4",
            "mpg",
            "qt",
            "rm",
            "swf",
            "wmv",
        ),
        max_file_size=10 * 1024 * 1024,  # 10 MB
        *args,
        **kwargs
    ):
        self.default_error_messages.update(
            {
                "too_large_file": _(
                    "The media file is too large. The maximal allowed file size is %s."
                )
                % filesizeformat(max_file_size),
            }
        )
        self.valid_file_extensions = valid_file_extensions
        self.max_file_size = max_file_size
        super(VideoField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """
        Checks that the file-upload field data contains a valid video.
        """
        f = super(VideoField, self).clean(data, initial)
        if f is None:
            return None
        elif not data and initial:
            return initial

        if data.name.split(".")[-1].lower() not in self.valid_file_extensions:
            raise forms.ValidationError(self.error_messages["invalid_extension"],)

        if data.size > self.max_file_size:
            raise forms.ValidationError(self.error_messages["too_large_file"])

        if hasattr(f, "seek") and callable(f.seek):
            f.seek(0)
        return f


class AudioField(forms.FileField):
    """
    Form field handling audio uploads
    """

    default_error_messages = {
        "invalid_audio": _(
            "Upload a valid audio file. The file you uploaded was either not an audio or a corrupted audio."
        ),
        "invalid_extension": _("File type of the uploaded file is invalid."),
    }

    def __init__(
        self,
        valid_file_extensions=(
            "aac",
            "aif",
            "iff",
            "mid",
            "midi",
            "mp3",
            "mpa",
            "ra",
            "ram",
            "wav",
            "wma",
        ),
        max_file_size=5 * 1024 * 1024,  # 5 MB
        *args,
        **kwargs
    ):
        self.default_error_messages.update(
            {
                "too_large_file": _(
                    "The media file is too large. The maximal allowed file size is %s."
                )
                % filesizeformat(max_file_size),
            }
        )
        self.valid_file_extensions = valid_file_extensions
        self.max_file_size = max_file_size
        super(AudioField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """
        Checks that the file-upload field data contains a valid audio.
        """
        f = super(AudioField, self).clean(data, initial)
        if f is None:
            return None
        elif not data and initial:
            return initial

        if data.name.split(".")[-1].lower() not in self.valid_file_extensions:
            raise forms.ValidationError(self.error_messages["invalid_extension"],)

        if data.size > self.max_file_size:
            raise forms.ValidationError(self.error_messages["too_large_file"])

        if hasattr(f, "seek") and callable(f.seek):
            f.seek(0)
        return f


class URLField(forms.URLField):
    """
    Form field for URLs
    """

    widget = URLWidget

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = URLWidget
        super(URLField, self).__init__(*args, **kwargs)


class TemplateChoiceField(forms.ChoiceField):
    """
    Form field for selecting a template
    """

    def __init__(
        self,
        path,
        match=None,
        recursive=False,
        allow_files=True,
        allow_folders=False,
        required=True,
        widget=None,
        label=None,
        initial=None,
        help_text=None,
        *args,
        **kwargs
    ):
        """
        path is a relative template path where the templates should be checked
        """
        self.path, self.match, self.recursive = path, match, recursive
        self.allow_files, self.allow_folders = allow_files, allow_folders

        super(TemplateChoiceField, self).__init__(
            choices=(),
            required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            *args,
            **kwargs
        )

        if self.match is not None:
            self.match_re = re.compile(self.match)

        choices = set()
        for templates_root in settings.TEMPLATES[0]["DIRS"]:
            path = os.path.join(templates_root, self.path)
            if recursive:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if self.match is None or self.match_re.search(f):
                            f = os.path.join(root, f)
                            choices.add(
                                (
                                    f.replace(templates_root + "/", "", 1),
                                    f.replace(path, "", 1),
                                )
                            )
            else:
                try:
                    for f in os.listdir(path):
                        full_file = os.path.join(path, f)
                        if os.path.isfile(full_file) and (
                            self.match is None or self.match_re.search(f)
                        ):
                            choices.add(
                                (full_file.replace(templates_root + "/", "", 1), f,)
                            )
                except OSError:
                    pass
        self.choices = sorted(choices)
        if not self.required:
            self.choices.insert(0, ("", "---------"))

        self.widget.choices = self.choices


class HierarchicalModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        prefix = (obj.path_search.count("/") - 2) * "-"
        if prefix:
            prefix += " "
        return prefix + force_str(obj)
