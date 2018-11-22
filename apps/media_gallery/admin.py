# -*- coding: UTF-8 -*-
from copy import deepcopy

from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm
from django.forms.models import BaseModelFormSet
from django.forms.models import BaseInlineFormSet
from django.forms.models import modelformset_factory
from django.forms.models import save_instance
from django.forms.formsets import DELETION_FIELD_NAME
from django.contrib.admin.util import flatten_fieldsets

from base_libs.models.admin import ObjectRelationMixinAdminOptions
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedStackedInline

import filebrowser.settings as filebrowser_settings
URL_FILEBROWSER_MEDIA = getattr(
    filebrowser_settings, "FILEBROWSER_DIRECTORY", 'uploads/'
)
MediaGallery = models.get_model("media_gallery", "MediaGallery")
MediaFile = models.get_model("media_gallery", "MediaFile")

### GENERIC-MEDIA-FILE-INLINE FOR ANY MODEL ###


class MediaFileInlineFormSet(BaseModelFormSet):
    """
    A formset for generic inline objects to a parent.
    """
    model = MediaFile
    obj = None
    parent_model = None

    def __init__(
        self,
        data=None,
        files=None,
        instance=None,
        prefix=None,
        save_as_new=False,
        queryset=None,
        **kwargs
    ):
        self.instance = instance
        self.save_as_new = save_as_new
        super(MediaFileInlineFormSet, self).__init__(
            data=data,
            files=files,
            prefix=prefix,
            queryset=self.get_queryset(),
            **kwargs
        )

    #@classmethod
    def get_default_prefix(cls):
        opts = cls.model._meta
        return '-'.join((
            opts.app_label,
            opts.object_name.lower(),
        ))

    get_default_prefix = classmethod(get_default_prefix)

    def get_queryset(self):
        # Avoid a circular import.
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(self.parent_model)
        pk = self.obj and self.obj._get_pk_val()
        return self.model._default_manager.filter(
            gallery__content_type=ct,
            gallery__object_id=pk,
        ).order_by('sort_order', 'creation_date')

    def save_new_objects(self, commit=True):
        self.new_objects = []
        for form in self.extra_forms:
            if not form.has_changed():
                continue
            # if only sort_order set for the new model, don't save the instance
            if len(
                form.changed_data
            ) == 1 and "sort_order" in form.changed_data:
                continue
            # If someone has marked an add form for deletion, don't save the
            # object.
            if self.can_delete and form.cleaned_data[DELETION_FIELD_NAME]:
                continue
            self.new_objects.append(self.save_new(form, commit=commit))
            if not commit:
                self.saved_forms.append(form)
        return self.new_objects

    def save_new(self, form, commit=True):
        # Avoid a circular import.
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(self.instance)
        gallery, created = MediaGallery.objects.get_or_create(
            content_type=ct,
            object_id=self.instance._get_pk_val(),
        )
        kwargs = {
            'gallery': gallery,
        }
        new_obj = self.model(**kwargs)
        return save_instance(
            form, new_obj, exclude=[self._pk_field.name], commit=commit
        )


def media_file_inlineformset_factory(
    parent_model,
    model,
    obj=None,
    form=ModelForm,
    formset=MediaFileInlineFormSet,
    fields=None,
    exclude=None,
    extra=3,
    can_order=False,
    can_delete=True,
    max_num=None,
    formfield_callback=lambda f: f.formfield(),
):
    """
    Returns an ``MediaFileInlineFormSet`` for the given kwargs.
    """
    # Avoid a circular import.
    if exclude is not None:
        exclude.extend(["gallery"])
    else:
        exclude = ["gallery"]
    FormSet = modelformset_factory(
        model,
        form=form,
        formfield_callback=formfield_callback,
        formset=formset,
        extra=extra,
        can_delete=can_delete,
        can_order=can_order,
        fields=fields,
        exclude=exclude,
        max_num=max_num,
    )
    FormSet.parent_model = parent_model
    FormSet.obj = obj
    return FormSet


class GenericMediaFileInline(ExtendedStackedInline):
    template = 'admin/edit_inline/stacked.html'
    model = MediaFile
    formset = MediaFileInlineFormSet
    sortable_field_name = "sort_order"
    allow_add = True
    fieldsets = [
        (None, {
            'fields': ("path", "external_url", "splash_image_path")
        }),
    ]
    fieldsets += get_admin_lang_section(
        _("Description"), ['title', 'description'], False
    )
    fieldsets += [
        (None, {
            'fields': ("sort_order", )
        }),
    ]
    extra = 0
    classes = ('grp-collapse grp-open', )

    def get_formset(self, request, obj=None):
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        defaults = {
            "obj": obj,
            "form": self.form,
            "formfield_callback": self.formfield_for_dbfield,
            "formset": self.formset,
            "extra": self.extra,
            "can_delete": True,
            "can_order": False,
            "fields": fields,
        }
        return media_file_inlineformset_factory(
            self.parent_model, self.model, **defaults
        )


### NORMAL MEDIA GALLERY ADMIN SETTINGS ###


class MediaFile_FormSet(BaseInlineFormSet):
    def save_new_objects(self, commit=True):
        self.new_objects = []
        for form in self.extra_forms:
            if not form.has_changed():
                continue
            # if only sort_order set for the new model, don't save the instance
            if len(
                form.changed_data
            ) == 1 and "sort_order" in form.changed_data:
                continue
            # If someone has marked an add form for deletion, don't save the
            # object.
            if self.can_delete and form.cleaned_data[DELETION_FIELD_NAME]:
                continue
            self.new_objects.append(self.save_new(form, commit=commit))
            if not commit:
                self.saved_forms.append(form)
        return self.new_objects


class MediaFile_Inline(ExtendedStackedInline):
    model = MediaFile
    formset = MediaFile_FormSet
    sortable = True
    allow_add = True
    extra = 0
    sortable_field_name = "sort_order"
    fieldsets = [
        (
            None, {
                'fields':
                    ["path", "external_url", "splash_image_path"] +
                    get_admin_lang_section(
                        _("Description"), ['title', 'description'], False
                    )
            }
        ),
    ]
    fieldsets += [
        (None, {
            'fields': ("sort_order", )
        }),
    ]


ObjectRelationAdminMixin = ObjectRelationMixinAdminOptions(
    admin_order_field="content_object_repr"
)


class MediaGalleryOptions(ObjectRelationAdminMixin):
    save_on_top = True
    inlines = [MediaFile_Inline]
    list_display = (
        'id', '__unicode__', 'content_type', 'get_content_object_display',
        'creation_date', 'file_count', 'views', 'is_featured'
    )
    list_editable = ('is_featured', )
    list_display_links = (
        'id',
        '__unicode__',
    )
    list_filter = ['creation_date', 'content_type', 'is_featured']
    search_fields = ["title", "content_object_repr"]
    date_hierarchy = 'creation_date'
    fieldsets = deepcopy(ObjectRelationAdminMixin.fieldsets)
    fieldsets += get_admin_lang_section(None, ['title', 'description'])
    fieldsets += [
        (
            _("Cover"), {
                'fields': ("cover_image", ),
                'classes': ["grp-collapse grp-closed"]
            }
        ),
    ]
    fieldsets += [
        (
            _("Details"), {
                'fields': ("is_featured", "sort_order"),
                'classes': ["grp-collapse grp-closed"]
            }
        ),
    ]


admin.site.register(MediaGallery, MediaGalleryOptions)
