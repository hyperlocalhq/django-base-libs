# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filebrowser', '0005_auto_20180619_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedescription',
            name='description_es',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='description_fr',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='description_it',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='description_pl',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='description_tr',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='title_es',
            field=models.CharField(max_length=300, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='title_fr',
            field=models.CharField(max_length=300, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='title_it',
            field=models.CharField(max_length=300, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='title_pl',
            field=models.CharField(max_length=300, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='filedescription',
            name='title_tr',
            field=models.CharField(max_length=300, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='copyright_limitations',
            field=models.CharField(help_text='If this field does not contain precise restrictions or if no restrictions are set, the rights of use are granted non-exclusively, and unrestricted in terms of time, place and content.', max_length=300, verbose_name='Copyright limitations', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_de',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='filedescription',
            name='description_en',
            field=base_libs.models.fields.PlainTextModelField(default=b'', null=True, verbose_name='Description', blank=True),
        ),
    ]
