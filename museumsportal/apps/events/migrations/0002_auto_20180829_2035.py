# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('exhibitions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museums', '0001_initial'),
        ('i18n', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='exhibition',
            field=models.ForeignKey(verbose_name='Related exhibition', blank=True, to='exhibitions.Exhibition', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='languages',
            field=models.ManyToManyField(to='i18n.Language', verbose_name='Languages', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='modifier',
            field=models.ForeignKey(related_name='event_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
        ),
        migrations.AddField(
            model_name='event',
            name='museum',
            field=models.ForeignKey(verbose_name='Museum', blank=True, to='museums.Museum', null=True),
        ),
    ]
