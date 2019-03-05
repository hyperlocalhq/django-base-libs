# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerObjectGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=80, verbose_name='Sysname')),
                ('title', models.CharField(verbose_name='title', max_length=80, null=True, editable=False)),
                ('title_de', models.CharField(max_length=80, verbose_name='title')),
                ('title_en', models.CharField(max_length=80, verbose_name='title', blank=True)),
                ('title_fr', models.CharField(max_length=80, verbose_name='title', blank=True)),
                ('title_pl', models.CharField(max_length=80, verbose_name='title', blank=True)),
                ('title_tr', models.CharField(max_length=80, verbose_name='title', blank=True)),
                ('title_es', models.CharField(max_length=80, verbose_name='title', blank=True)),
                ('title_it', models.CharField(max_length=80, verbose_name='title', blank=True)),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('users', models.ManyToManyField(help_text='In addition to the permissions manually assigned, these users will also get all row level permissions granted to this group.', to=settings.AUTH_USER_MODEL, verbose_name='Users', blank=True)),
            ],
            options={
                'ordering': ('object_id', 'content_type'),
                'db_table': 'auth_perobjectgroup',
                'verbose_name': 'object-specific group',
                'verbose_name_plural': 'object-specific groups',
            },
        ),
        migrations.CreateModel(
            name='RowLevelPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner_object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Owner')),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('negative', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('owner_content_type', models.ForeignKey(related_name='owner', verbose_name="Owner's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('permission', models.ForeignKey(to='auth.Permission')),
            ],
            options={
                'db_table': 'auth_rowlevelpermission',
                'verbose_name': 'row level permission',
                'verbose_name_plural': 'row level permissions',
            },
        ),
    ]
