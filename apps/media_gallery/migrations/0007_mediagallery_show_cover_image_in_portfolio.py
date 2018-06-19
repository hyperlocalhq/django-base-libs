# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_gallery', '0006_adding_photocredtis_to_media_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediagallery',
            name='show_cover_image_in_portfolio',
            field=models.BooleanField(default=False, verbose_name='Show image in portfolio'),
        ),
    ]
