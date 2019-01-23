# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0001_initial'),
        ('multiparts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='production',
            field=models.ForeignKey(to='productions.Production'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parent',
            name='creator',
            field=models.ForeignKey(related_name='parent_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parent',
            name='modifier',
            field=models.ForeignKey(related_name='parent_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parent',
            name='production',
            field=models.OneToOneField(related_name='multipart', verbose_name='Production', to='productions.Production'),
            preserve_default=True,
        ),
    ]
