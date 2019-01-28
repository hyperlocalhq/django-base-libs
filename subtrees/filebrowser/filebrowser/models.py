# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fields import FileBrowseField

from base_libs.models.fields import MultilingualCharField, MultilingualPlainTextField


class FileDescriptionQuerySet(models.QuerySet):
    def _modify_kwargs(self, kwargs):
        import hashlib
        if 'file_path' in kwargs:
            file_path = kwargs.pop('file_path')
            # if file_path is FileObject, get the path string of it
            if hasattr(file_path, 'path'):
                file_path = file_path.path
            try:
                hash_object = hashlib.sha256(file_path.encode('utf-8'))
                kwargs['file_path_hash'] = hash_object.hexdigest()
            except AttributeError as e:
                pass

    def filter(self, *args, **kwargs):
        self._modify_kwargs(kwargs)
        return super(FileDescriptionQuerySet, self).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        self._modify_kwargs(kwargs)
        return super(FileDescriptionQuerySet, self).exclude(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._modify_kwargs(kwargs)
        return super(FileDescriptionQuerySet, self).get(*args, **kwargs)


class FileDescriptionManager(models.Manager):
    def get_queryset(self):
        return FileDescriptionQuerySet(self.model, using=self._db)  # Important!

    def update_all_hashes(self):
        for obj in self.all():
            obj.save()


class FileDescription(models.Model):
    file_path = FileBrowseField(_("File path"), max_length=500)
    file_path_hash = models.CharField(max_length=64, db_index=True, blank=True, editable=False)
    title = MultilingualCharField(_("Title"), max_length=300, blank=True)
    description = MultilingualPlainTextField(_("Description"), blank=True)
    author = models.CharField(_('Copyright / Photographer'), max_length=300, blank=True)
    copyright_limitations = models.CharField(_('Copyright limitations'), max_length=300, blank=True)

    objects = FileDescriptionManager()

    def __unicode__(self):
        if self.file_path:
            return self.file_path.path
        return u""
        
    class Meta:
        ordering = ['file_path']
        verbose_name = _("File description")
        verbose_name_plural = _("File descriptions")

    def save(self, *args, **kwargs):
        import hashlib
        if self.file_path:
            hash_object = hashlib.sha256(self.file_path.path.encode('utf-8'))
            self.file_path_hash = hash_object.hexdigest()
        super(FileDescription, self).save(*args, **kwargs)
