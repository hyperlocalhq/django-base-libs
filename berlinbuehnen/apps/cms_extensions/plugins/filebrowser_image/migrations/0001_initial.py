# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('image_mods', '0003_auto_20180301_2039'),
        ('cms', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilebrowserImage',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='filebrowser_image_filebrowserimage', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
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
