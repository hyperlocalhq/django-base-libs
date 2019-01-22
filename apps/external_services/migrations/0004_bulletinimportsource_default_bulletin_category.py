# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0009_auto_20160128_1704'),
        ('external_services', '0003_auto_20151218_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulletinimportsource',
            name='default_bulletin_category',
            field=models.ForeignKey(verbose_name='Bulletin category', blank=True, to='bulletin_board.BulletinCategory', null=True),
            preserve_default=True,
        ),
    ]
