# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('slideshows', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='description',
            field=models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slide',
            name='description_de',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slide',
            name='description_en',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Beschreibung', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slide',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=200, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slide',
            name='title_de',
            field=models.CharField(max_length=200, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slide',
            name='title_en',
            field=models.CharField(max_length=200, verbose_name='Title', blank=True),
            preserve_default=True,
        ),
    ]
