# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin_board', '0009_auto_20160128_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='creator',
            field=models.ForeignKey(related_name='bulletin_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='modifier',
            field=models.ForeignKey(related_name='bulletin_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
    ]
