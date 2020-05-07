# -*- coding: utf-8 -*-
"""
custom model fields
"""
import warnings
import sys
from datetime import datetime

from django.db.models.fields import TextField, NOT_PROVIDED
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.html import escape, linebreaks, urlize
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db import connection, models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import get_language
from django.utils.translation import string_concat

try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from base_libs.middleware import get_current_language
from base_libs.forms.fields import PlainTextFormField
from base_libs.forms.fields import URLField as URLFormField
from base_libs.forms.fields import TemplateChoiceField
from base_libs.models import base_libs_settings as markup_settings

qn = connection.ops.quote_name


class ExtendedTextField(TextField):

    description = _("Text field with additional capabilities for editing.")

    def has_markup_type(self):
        return True
    
    def formfield(self, **kwargs):
        form_field = super(ExtendedTextField, self).formfield(**kwargs)
        widget_attrs = form_field.widget.attrs
        if 'class' not in widget_attrs:
            widget_attrs['class'] = ""
        widget_attrs['class'] += " hasMarkupType"
        return form_field
    
    def contribute_to_class(self, cls, name, virtual_only=False):
        # generate an additional select field for selecting the markup type
        try: # the field shouldn't be already added (for south)
            cls._meta.get_field(name)
        except models.FieldDoesNotExist:
            pass
        else:
            return

        field_class = getattr(self.__class__, '_field_class', None)
        if field_class != PlainTextModelField:
            if not(hasattr(sys, "argv") and "migrate" in sys.argv and sys.argv.index("migrate") == 1):
                # the field shouldn't be added for south,
                # because south will care about it itself
                try:  # the field shouldn't be already added
                    cls._meta.get_field("%s_markup_type" % name)
                except models.FieldDoesNotExist:
                    pass
                else:
                    cls._meta.local_fields.remove(cls._meta.get_field("%s_markup_type" % name))

                editable = not isinstance(self, MultilingualTextField)

                if not hasattr(self, 'related_markup_type_field'):
                    # TODO: find out why the related markup type tries to be added twice
                    self.related_markup_type_field = models.CharField(
                        string_concat(_("Markup type for"), " ", self.verbose_name),
                        max_length=10,
                        blank=False,
                        choices=markup_settings.MARKUP_TYPES,
                        default=markup_settings.DEFAULT_MARKUP_TYPE,
                        help_text=_("You can select an appropriate markup type here"),
                        editable=editable,
                    )
                    self.related_markup_type_field.contribute_to_class(
                        cls,
                        "%s_markup_type" % name
                        )
        # create the field itself
        super(ExtendedTextField, self).contribute_to_class(cls, name)
        
        def get_rendered_wrapper(name):
            import bleach
            _name = name
            def get_rendered(self):
                field_value = getattr(self, _name)
                mt = getattr(self, "%s_markup_type" % name)
                
                if mt == markup_settings.MARKUP_PLAIN_TEXT:
                    field_value = field_value.strip()
                    if field_value:
                        field_value = escape(field_value)
                        try:
                            # try to urlize if there are no invalid IPv6 URLs
                            field_value = bleach.linkify(field_value, parse_email=True)
                        except ValueError:
                            pass
                        field_value = linebreaks(field_value)
                elif mt == markup_settings.MARKUP_RAW_HTML:
                    pass
                elif mt == markup_settings.MARKUP_HTML_WYSIWYG:
                    pass
                elif mt == markup_settings.MARKUP_MARKDOWN:
                    try:
                        import markdown
                    except ImportError:
                        if settings.DEBUG:
                            raise Warning("Error in {% markdown %} filter: The Python markdown library isn't installed.")
                        return field_value
                    else:
                        field_value = markdown.markdown(field_value)

                # remove empty paragraphs
                field_value = field_value.replace('<p></p>', '')

                return mark_safe(field_value)
            get_rendered.needs_autoescape = False
            return get_rendered
        cls.add_to_class("get_rendered_%s" % name, get_rendered_wrapper(name))
        cls.add_to_class("rendered_%s" % name, property(get_rendered_wrapper(name)))


class PlainTextModelField(TextField):

    description = _("Model field for Textarea which won't be converted to RTE")

    def formfield(self, **kwargs):
        defaults = {'form_class': PlainTextFormField}
        defaults.update(kwargs)
        return super(PlainTextModelField, self).formfield(**defaults)
        
    def get_internal_type(self):
        return "TextField"

_language_field_name = lambda name, lang_code: "%s_%s" % (name, lang_code)


class MultilingualProxy(object): 
    def __init__(self, field): 
        self._field = field 

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('MultilingualProxy.__get__ can only be accessed via an instance.')
        language = get_current_language() or settings.LANGUAGE_CODE
        val = obj.__dict__[_language_field_name(self._field.attname, language)]
        if not val:
            val = obj.__dict__[_language_field_name(self._field.attname, settings.LANGUAGE_CODE)]
            if not val and not self._field.blank:
                # No value set for mandatory field for the current language! Has the default language been changed recently?
                return ""
        return val 

    def __set__(self, obj, value):
        """
        sets a multi language value programmatically.
        The value must be provided either by a value or
        by a dictionary with the language code as key and
        a string value as value
        """
        # setting multilingual values via dict!!!
        if isinstance(value, dict):
            for key in value.keys():
                obj.__dict__[_language_field_name(self._field.attname, key)] = value[key]
        # normal setter
        else:
            language = get_current_language() or settings.LANGUAGE_CODE
            obj.__dict__[_language_field_name(self._field.attname, language)] = value


class MultilingualCharField(models.CharField):

    def __init__(self, verbose_name=None, **kwargs):

        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)

        super(MultilingualCharField, self).__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        default = ""
        if self.default != NOT_PROVIDED:
            default = self.default

        # generate language specific fields dynamically
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                _blank = self._blank
            else:
                _blank = True

            localized_field = models.CharField(
                string_concat(self.verbose_name, " (%s)" % lang_code),
                name=self.name,
                primary_key=self.primary_key,
                max_length=self.max_length,
                unique=self.unique,
                blank=_blank,
                null=False,  # we ignore the null argument!
                db_index=self.db_index,
                rel=self.rel,
                default=default,
                editable=self._editable,
                serialize=self.serialize,
                choices=self.choices,
                help_text=self.help_text,
                db_column=None,
                db_tablespace=self.db_tablespace
            )
            localized_field.contribute_to_class(
                cls,
                "%s_%s" % (name, lang_code),
            )

        def translated_value(self):
            language = get_language()
            val = self.__dict__["%s_%s" % (name, language)]
            if not val:
                val = self.__dict__["%s_%s" % (name, settings.LANGUAGE_CODE)]
            return val

        setattr(cls, name, property(translated_value))
    def deconstruct(self):
       name, path, args, kwargs = super(MultilingualCharField, self).deconstruct()
       path = "django.db.models.CharField"
       return name, path, args, kwargs


class MultilingualTextField(models.Field):

    description = _("Multilingual Text")

    _field_class = ExtendedTextField
    
    def __init__(self, verbose_name=None, **kwargs):

        self._blank = kwargs.get("blank", False)
        self._editable = kwargs.get("editable", True)

        super(MultilingualTextField, self).__init__(verbose_name, **kwargs)

    def contribute_to_class(self, cls, name, virtual_only=False):
        # generate language specific fields dynamically

        default = ""
        if self.default != NOT_PROVIDED:
            default = self.default

        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == settings.LANGUAGE_CODE:
                _blank = self._blank
            else:
                _blank = True

            localized_field = self._field_class(
                string_concat(self.verbose_name, " (%s)" % lang_code),
                name=self.name,
                primary_key=self.primary_key,
                max_length=self.max_length,
                unique=self.unique,
                blank=_blank,
                null=False,  # we ignore the null argument!
                db_index=self.db_index,
                rel=self.rel,
                default=default,
                editable=self._editable,
                serialize=self.serialize,
                choices=self.choices,
                help_text=self.help_text,
                db_column=None,
                db_tablespace=self.db_tablespace
            )
            localized_field.contribute_to_class(
                cls,
                "%s_%s" % (name, lang_code),
            )

        def translated_value(self):
            language = get_language()
            val = self.__dict__["%s_%s" % (name, language)]
            if not val:
                val = self.__dict__["%s_%s" % (name, settings.LANGUAGE_CODE)]
            return val

        setattr(cls, name, property(translated_value))

        # overwrite the get_rendered_*
        def get_rendered_wrapper(name):
            import bleach
            _name = name

            def get_rendered(self):
                lang_code = get_current_language() or settings.LANGUAGE_CODE
                return getattr(self, 'get_rendered_%s_%s' % (_name, lang_code))()
            get_rendered.needs_autoescape = False
            return get_rendered
        cls.add_to_class("get_rendered_%s" % name, get_rendered_wrapper(name))
        cls.add_to_class("rendered_%s" % name, property(get_rendered_wrapper(name)))

    def deconstruct(self):
       name, path, args, kwargs = super(MultilingualTextField, self).deconstruct()
       path = "django.db.models.TextField"
       return name, path, args, kwargs


class MultilingualPlainTextField(MultilingualTextField):

    description = _("Plain text Multilingual text fields")

    _field_class = PlainTextModelField


class URLField(models.URLField):
    """
    Model field for URLs
    """
    def formfield(self, **kwargs):
        defaults = {
            'form_class': URLFormField,
            #'verify_exists': self.verify_exists,
            }
        defaults.update(kwargs)
        return super(URLField, self).formfield(**defaults)


class MultilingualURLField(MultilingualCharField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': URLFormField,
            #'verify_exists': self.verify_exists,
            }
        defaults.update(kwargs)
        return super(MultilingualURLField, self).formfield(**defaults)


class TemplatePathField(models.FilePathField):
    def formfield(self, **kwargs):
        defaults = {
            'path': self.path,
            'match': self.match,
            'recursive': self.recursive,
        }
        defaults.update(kwargs)
        defaults['form_class'] = TemplateChoiceField
        return super(TemplatePathField, self).formfield(**defaults)
    

class PositionField(models.IntegerField):
    """
    A slightly modified version of PositionField from http://github.com/jpwatts/django-positions
    """
    def __init__(self, verbose_name=None, name=None, default=None, collection=None, unique_for_field=None, unique_for_fields=None, *args, **kwargs):
        if 'unique' in kwargs:
            raise TypeError("%s can't have a unique constraint." % self.__class__.__name__)
        super(PositionField, self).__init__(verbose_name, name, default=default, *args, **kwargs)

        # Backwards-compatibility mess begins here.
        if collection is not None and unique_for_field is not None:
            raise TypeError("'collection' and 'unique_for_field' are incompatible arguments.")

        if collection is not None and unique_for_fields is not None:
            raise TypeError("'collection' and 'unique_for_fields' are incompatible arguments.")

        if unique_for_field is not None:
            warnings.warn("The 'unique_for_field' argument is deprecated. Please use 'collection' instead.", DeprecationWarning)
            if unique_for_fields is not None:
                raise TypeError("'unique_for_field' and 'unique_for_fields' are incompatible arguments.")
            collection = unique_for_field

        if unique_for_fields is not None:
            warnings.warn("The 'unique_for_fields' argument is deprecated. Please use 'collection' instead.", DeprecationWarning)
            collection = unique_for_fields
        # Backwards-compatibility mess ends here.

        if isinstance(collection, basestring):
            collection = (collection,)
        self.collection = collection

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(PositionField, self).contribute_to_class(cls, name)
        for constraint in cls._meta.unique_together:
            if self.name in constraint:
                raise TypeError("%s can't be part of a unique constraint." % self.__class__.__name__)
        self.auto_now_fields = []
        for field in cls._meta.fields:
            if getattr(field, 'auto_now', False):
                self.auto_now_fields.append(field)
        setattr(cls, self.name, self)
        post_delete.connect(self.update_on_delete, sender=cls)
        post_save.connect(self.update_on_save, sender=cls)

    def get_internal_type(self):
        # pre_save always returns a value >= 0
        return 'PositiveIntegerField'

    def pre_save(self, model_instance, add):
        cache_name = self.get_cache_name()
        current, updated = getattr(model_instance, cache_name)
        
        if add:
            current, updated = None, current

        if updated is None:
            updated = -1

        # existing instance, position not modified; no cleanup required
        if current is not None and updated is None:
            return current

        collection_count = self.get_collection(model_instance).count()
        if current is None:
            max_position = collection_count
        else:
            max_position = collection_count - 1
        min_position = 0

        # new instance; appended; no cleanup required on post_save
        if add and (updated == -1 or updated >= max_position):
            setattr(model_instance, cache_name, (max_position, None))
            return max_position

        if max_position >= updated >= min_position:
            # positive position; valid index
            position = updated
        elif updated > max_position:
            # positive position; invalid index
            position = max_position
        elif abs(updated) <= (max_position + 1):
            # negative position; valid index

            # Add 1 to max_position to make this behave like a negative list index.
            # -1 means the last position, not the last position minus 1

            position = max_position + 1 + updated
        else:
            # negative position; invalid index
            position = min_position

        # instance inserted; cleanup required on post_save
        setattr(model_instance, cache_name, (current, position))

        if position == -1:  # quick fix for data re-imports
            position = 0

        return position

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError("%s must be accessed via instance." % self.name)
        current, updated = getattr(instance, self.get_cache_name())
        if updated is None:
            return current
        else:
            return updated

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError("%s must be accessed via instance." % self.name)
        if value is None:
            value = self.default
        cache_name = self.get_cache_name()
        try:
            current, updated = getattr(instance, cache_name)
        except AttributeError:
            current, updated = value, None
        else:
            updated = value
        setattr(instance, cache_name, (current, updated))

    def get_collection(self, instance):
        filters = {}
        if self.collection:
            for field_name in self.collection:
                field = instance._meta.get_field(field_name)
                field_value = getattr(instance, field.attname)
                if field.null and field_value is None:
                    filters['%s__isnull' % field.name] = True
                else:
                    filters[field.name] = field_value
        return type(instance)._default_manager.filter(**filters)

    def update_on_delete(self, sender, instance, **kwargs):
        current = getattr(instance, self.get_cache_name())[0]
        queryset = self.get_collection(instance)
        updates = {self.name: models.F(self.name) - 1}
        if self.auto_now_fields:
            now = tz_now()
            for field in self.auto_now_fields:
                updates[field.name] = now
        queryset.filter(**{'%s__gt' % self.name: current}).update(**updates)

    def update_on_save(self, sender, instance, created, **kwargs):
        current, updated = getattr(instance, self.get_cache_name())

        if updated is None:
            return None

        queryset = self.get_collection(instance).exclude(pk=instance.pk)

        updates = {}
        if self.auto_now_fields:
            now = tz_now()
            for field in self.auto_now_fields:
                updates[field.name] = now

        if created:
            # increment positions gte updated
            queryset = queryset.filter(**{'%s__gte' % self.name: updated})
            updates[self.name] = models.F(self.name) + 1
        elif updated > current:
            # decrement positions gt current and lte updated
            queryset = queryset.filter(**{'%s__gt' % self.name: current, '%s__lte' % self.name: updated})
            updates[self.name] = models.F(self.name) - 1
        else:
            # increment positions lt current and gte updated
            queryset = queryset.filter(**{'%s__lt' % self.name: current, '%s__gte' % self.name: updated})
            updates[self.name] = models.F(self.name) + 1

        queryset.update(**updates)
        setattr(instance, self.get_cache_name(), (updated, None))

