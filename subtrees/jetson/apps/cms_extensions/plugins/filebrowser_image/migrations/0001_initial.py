# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('image_mods', '0001_initial'),
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilebrowserImage',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image')),
                ('alt', models.CharField(max_length=200, verbose_name='Alternative text', blank=True)),
                ('css_class', models.CharField(max_length=200, verbose_name='CSS class', blank=True)),
                ('mod', models.ForeignKey(verbose_name='Apply modification', blank=True, to='image_mods.ImageModification', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
