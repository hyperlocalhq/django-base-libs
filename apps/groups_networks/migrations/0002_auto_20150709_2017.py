# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('i18n', '__first__'),
        ('groups_networks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persongroup',
            name='organizing_institution',
            field=models.ForeignKey(verbose_name='Organizing institution', blank=True, to='institutions.Institution', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='persongroup',
            name='preferred_language',
            field=models.ForeignKey(verbose_name='Preferred Language', blank=True, to='i18n.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grouptype',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='groups_networks.GroupType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='confirmer',
            field=models.ForeignKey(related_name='group_confirmer', verbose_name='Confirmer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='inviter',
            field=models.ForeignKey(related_name='group_inviter', verbose_name='Inviter', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='person_group',
            field=models.ForeignKey(verbose_name='Group of People', to='groups_networks.PersonGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
