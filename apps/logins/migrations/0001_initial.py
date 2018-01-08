# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginAction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Login date', editable=False)),
                ('user_agent', models.TextField(verbose_name='User Agent', editable=False, blank=True)),
                ('user', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-login_date'],
                'verbose_name': 'Login Action',
                'verbose_name_plural': 'Login Actions',
            },
        ),
        migrations.CreateModel(
            name='WelcomeMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('published_from', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published immediately.", null=True, verbose_name='publishing date', blank=True)),
                ('published_till', models.DateTimeField(help_text="If not provided and the status is set to 'published', the entry will be published forever.", null=True, verbose_name='published until', blank=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Draft'), (1, 'Published')])),
                ('title', models.CharField(verbose_name='Title', max_length=512, null=True, editable=False)),
                ('content', models.TextField(default=b'', verbose_name='Content', null=True, editable=False)),
                ('condition', models.CharField(db_index=True, max_length=1, verbose_name='Condition', choices=[('f', 'First login'), ('m', 'Login after 1 month of inactivity'), ('o', 'Other logins')])),
                ('title_en', models.CharField(max_length=512, verbose_name='Title', blank=True)),
                ('title_de', models.CharField(max_length=512, verbose_name='Title')),
                ('content_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Content', blank=True)),
                ('content_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('content_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Content')),
                ('content_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('author', models.ForeignKey(related_name='welcomemessage_author', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text='If you do not select an author, you will be the author!', null=True, verbose_name='author')),
                ('creator', models.ForeignKey(related_name='welcomemessage_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='welcomemessage_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Welcome Message',
                'verbose_name_plural': 'Welcome Messages',
            },
        ),
    ]
