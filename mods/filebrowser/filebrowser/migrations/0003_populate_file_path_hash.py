# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_file_path_hash(apps, schema_editor):
    import hashlib
    FileDescription = apps.get_model('filebrowser', 'FileDescription')
    for fd in FileDescription.objects.all():
        if fd.file_path:
            hash_object = hashlib.sha256(fd.file_path.path.encode('utf-8'))
            fd.file_path_hash = hash_object.hexdigest()
            fd.save()


def depopulate_file_path_hash(apps, schema_editor):
    FileDescription = apps.get_model('filebrowser', 'FileDescription')
    FileDescription.objects.all().update(file_path_hash='')


class Migration(migrations.Migration):

    dependencies = [
        ('filebrowser', '0002_file_path_revisited'),
    ]

    operations = [
        migrations.RunPython(populate_file_path_hash, depopulate_file_path_hash)
    ]
