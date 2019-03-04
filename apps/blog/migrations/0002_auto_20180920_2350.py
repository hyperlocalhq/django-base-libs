# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='sites',
            field=models.ManyToManyField(help_text='Please select some sites, this container relates to. If you do not select any site, the container applies to all sites.', to='sites.Site', verbose_name='Sites', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='post_author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(related_name='post_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modifier',
            field=models.ForeignKey(related_name='post_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
        ),
    ]
