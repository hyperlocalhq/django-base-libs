# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Linked object', blank=True)),
                ('sysname', models.SlugField(help_text='Do not change this value! Sysnames are used to display tree branches of navigation links in templates. Also they are used for binding specific styling or scripts to specific navigation items.', unique=True, max_length=255, verbose_name='Sysname')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('link_url', models.CharField(help_text='It can contain template tags and variables. The link is shown in the navigation menu only if it returns a non-empty string.', max_length=255, verbose_name='Link URL', blank=True)),
                ('related_urls', base_libs.models.fields.PlainTextModelField(help_text='Other URLs for which this link should be highlighted, one per line. It can contain template tags and variables.', verbose_name='Related URLs', blank=True)),
                ('is_group', models.BooleanField(default=False, verbose_name='Group of links')),
                ('is_group_name_shown', models.BooleanField(default=True, verbose_name='Show group name')),
                ('is_shown_for_visitors', models.BooleanField(default=True, verbose_name='Shown for visitors')),
                ('is_shown_for_users', models.BooleanField(default=True, verbose_name='Shown for users')),
                ('is_login_required', models.BooleanField(default=False, verbose_name='Require login')),
                ('is_promoted', models.BooleanField(default=False, verbose_name='Promoted')),
                ('description', models.TextField(default=b'', verbose_name='description', null=True, editable=False, blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Linked object's type (model)")),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='navigation.NavigationLink', null=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', help_text='Restrict this object only for the selected site', null=True, verbose_name='Site')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'navigational menu item',
                'verbose_name_plural': 'navigational menu items',
            },
            bases=(models.Model,),
        ),
    ]
