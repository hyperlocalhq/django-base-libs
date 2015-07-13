# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_app', '0001_initial'),
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpage',
            name='institution',
            field=models.ForeignKey(to='institutions.Institution'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebookpage',
            name='owner_settings',
            field=models.ForeignKey(to='facebook_app.FacebookAppSettings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebookappsettings',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
