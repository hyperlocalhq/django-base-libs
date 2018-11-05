# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('media_gallery', '0003_mediagallery_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='creator',
            field=models.ForeignKey(related_name='mediafile_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='modifier',
            field=models.ForeignKey(related_name='mediafile_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mediagallery',
            name='author',
            field=models.ForeignKey(related_name='mediagallery_author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author'),
            preserve_default=True,
        ),
    ]
