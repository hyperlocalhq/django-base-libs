# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('curated_lists', '0006_auto_20180625_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='description',
            field=models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='description_de',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='description_de_markup_type',
            field=models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')]),
        ),
        migrations.AddField(
            model_name='listitem',
            name='description_en',
            field=base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='description_en_markup_type',
            field=models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')]),
        ),
        migrations.AddField(
            model_name='listitem',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=255, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='title_de',
            field=models.CharField(max_length=255, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='listitem',
            name='title_en',
            field=models.CharField(max_length=255, verbose_name='Title', blank=True),
        ),
    ]
