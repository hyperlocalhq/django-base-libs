# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSelection',
            fields=[
                ('cmsplugin_ptr',
                 models.OneToOneField(parent_link=True, related_name='articles_articleselection', auto_created=True,
                                      primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('article', models.ForeignKey(to='articles.Article')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
