# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('curated_lists', '0003_curatedlist_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='curatedlist',
            name='description',
            field=models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='description_de_markup_type',
            field=models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='description_en_markup_type',
            field=models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='curatedlist',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Profile image', blank=True),
            preserve_default=True,
        ),
    ]
