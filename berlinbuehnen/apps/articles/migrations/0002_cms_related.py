# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import filebrowser.fields
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('cms', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSelection',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='articles_articleselection', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
