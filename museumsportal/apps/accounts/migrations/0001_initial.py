# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacySettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_to_public', models.BooleanField(default=True, verbose_name='Display profile to public')),
                ('display_username', models.BooleanField(default=False, verbose_name='Display username instead of full name')),
                ('user', models.OneToOneField(verbose_name='Benutzer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
                'verbose_name': 'Privacy Settings',
                'verbose_name_plural': 'Privacy Settings',
            },
        ),
    ]
