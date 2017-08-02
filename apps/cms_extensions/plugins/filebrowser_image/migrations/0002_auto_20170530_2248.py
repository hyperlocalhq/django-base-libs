# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filebrowser_image', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filebrowserimage',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='filebrowser_image_filebrowserimage', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]
