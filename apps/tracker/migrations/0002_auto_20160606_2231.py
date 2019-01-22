# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='modifier',
            field=models.ForeignKey(related_name='ticket_modifier', on_delete=django.db.models.deletion.SET_NULL, verbose_name='modifier', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='submitter',
            field=models.ForeignKey(related_name='ticket_submitter', on_delete=django.db.models.deletion.SET_NULL, verbose_name='submitter', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
