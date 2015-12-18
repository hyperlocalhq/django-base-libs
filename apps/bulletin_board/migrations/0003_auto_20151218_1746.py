# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0002_auto_20151218_1626'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bulletincontentprovider',
            options={'ordering': ('title',), 'verbose_name': 'bulletin-content provider', 'verbose_name_plural': 'bulletin-content providers'},
        ),
        migrations.AddField(
            model_name='bulletin',
            name='content_provider',
            field=models.ForeignKey(verbose_name='Content provider', blank=True, to='bulletin_board.BulletinContentProvider', null=True),
            preserve_default=True,
        ),
    ]
