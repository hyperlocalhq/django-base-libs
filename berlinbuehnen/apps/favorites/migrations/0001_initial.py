# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('user', models.ForeignKey(verbose_name='Preferrer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'favorite',
                'verbose_name_plural': 'favorites',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FavoriteListOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='My Favorites title', blank=True)),
                ('description', models.TextField(verbose_name='My Favorites description', blank=True)),
                ('user', models.ForeignKey(verbose_name='Preferrer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'favorite list options',
                'verbose_name_plural': 'favorite list options',
            },
            bases=(models.Model,),
        ),
    ]
