# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Sysname')),
                ('title', models.CharField(verbose_name='title', max_length=512, null=True, editable=False, blank=True)),
                ('content', models.TextField(default=b'', help_text='It can contain template tags and variables', null=True, editable=False, verbose_name='content')),
                ('title_de', models.CharField(max_length=512, verbose_name='title', blank=True)),
                ('title_en', models.CharField(max_length=512, verbose_name='title', blank=True)),
                ('content_de', base_libs.models.fields.ExtendedTextField(default=b'', help_text='It can contain template tags and variables', null=True, verbose_name='Inhalt')),
                ('content_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('content_en', base_libs.models.fields.ExtendedTextField(default=b'', help_text='It can contain template tags and variables', null=True, verbose_name='Inhalt', blank=True)),
                ('content_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('author', models.ForeignKey(related_name='infoblock_author', blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
                ('site', models.ForeignKey(blank=True, to='sites.Site', help_text='Restrict this object only for the selected site', null=True, verbose_name='Site')),
            ],
            options={
                'ordering': ['sysname'],
                'verbose_name': 'information block',
                'verbose_name_plural': 'information blocks',
            },
            bases=(models.Model,),
        ),
    ]
