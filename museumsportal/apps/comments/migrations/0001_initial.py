# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('name', models.CharField(max_length=80, verbose_name='name')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email', blank=True)),
                ('url_link', base_libs.models.fields.URLField(null=True, verbose_name='URL', blank=True)),
                ('headline', models.CharField(max_length=255, null=True, verbose_name='headline', blank=True)),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('rating1', models.PositiveSmallIntegerField(null=True, verbose_name='rating #1', blank=True)),
                ('rating2', models.PositiveSmallIntegerField(null=True, verbose_name='rating #2', blank=True)),
                ('rating3', models.PositiveSmallIntegerField(null=True, verbose_name='rating #3', blank=True)),
                ('rating4', models.PositiveSmallIntegerField(null=True, verbose_name='rating #4', blank=True)),
                ('rating5', models.PositiveSmallIntegerField(null=True, verbose_name='rating #5', blank=True)),
                ('rating6', models.PositiveSmallIntegerField(null=True, verbose_name='rating #6', blank=True)),
                ('rating7', models.PositiveSmallIntegerField(null=True, verbose_name='rating #7', blank=True)),
                ('rating8', models.PositiveSmallIntegerField(null=True, verbose_name='rating #8', blank=True)),
                ('valid_rating', models.BooleanField(verbose_name='is valid rating')),
                ('submit_date', models.DateTimeField(auto_now_add=True, verbose_name='date/time submitted')),
                ('is_public', models.BooleanField(verbose_name='is public')),
                ('ip_address', models.GenericIPAddressField(null=True, verbose_name='IP address', blank=True)),
                ('is_removed', models.BooleanField(default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.', verbose_name='is removed')),
                ('is_spam', models.BooleanField(default=False, help_text='Check this box if the comment should be marked as spam. The comment will not be displayed in this case.', verbose_name='is spam')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('site', models.ForeignKey(to='sites.Site')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-submit_date',),
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='KarmaScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.SmallIntegerField(verbose_name='score', db_index=True)),
                ('scored_date', models.DateTimeField(auto_now=True, verbose_name='score date')),
                ('comment', models.ForeignKey(to='comments.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'karma score',
                'verbose_name_plural': 'karma scores',
            },
        ),
        migrations.CreateModel(
            name='ModeratorDeletion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deletion_date', models.DateTimeField(auto_now_add=True, verbose_name='deletion date')),
                ('comment', models.ForeignKey(to='comments.Comment')),
            ],
            options={
                'verbose_name': 'moderator deletion',
                'verbose_name_plural': 'moderator deletions',
            },
        ),
        migrations.CreateModel(
            name='ModeratorDeletionReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('reason', models.TextField(default=b'', verbose_name='reason', null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_fr', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_pl', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_tr', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_es', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_it', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('reason_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason')),
                ('reason_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('reason_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason', blank=True)),
                ('reason_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('reason_fr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason', blank=True)),
                ('reason_fr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('reason_pl', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason', blank=True)),
                ('reason_pl_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('reason_tr', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason', blank=True)),
                ('reason_tr_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('reason_es', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason', blank=True)),
                ('reason_es_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('reason_it', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='reason', blank=True)),
                ('reason_it_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
            ],
            options={
                'verbose_name': 'moderator deletion reason',
                'verbose_name_plural': 'moderator deletion reasons',
            },
        ),
        migrations.CreateModel(
            name='UserFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flag_date', models.DateTimeField(auto_now_add=True, verbose_name='flag date')),
                ('comment', models.ForeignKey(to='comments.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user flag',
                'verbose_name_plural': 'user flags',
            },
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate_date', models.DateTimeField(auto_now_add=True, verbose_name='rate date')),
                ('rate_index', models.SmallIntegerField(verbose_name='rate index')),
                ('comment', models.ForeignKey(to='comments.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user rating',
                'verbose_name_plural': 'user ratings',
            },
        ),
        migrations.AddField(
            model_name='moderatordeletion',
            name='deletion_reason',
            field=models.ForeignKey(verbose_name=b'deletion reason', to='comments.ModeratorDeletionReason'),
        ),
        migrations.AddField(
            model_name='moderatordeletion',
            name='user',
            field=models.ForeignKey(verbose_name=b'moderator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userrating',
            unique_together=set([('user', 'comment', 'rate_index')]),
        ),
        migrations.AlterUniqueTogether(
            name='userflag',
            unique_together=set([('user', 'comment')]),
        ),
        migrations.AlterUniqueTogether(
            name='moderatordeletion',
            unique_together=set([('user', 'comment')]),
        ),
        migrations.AlterUniqueTogether(
            name='karmascore',
            unique_together=set([('user', 'comment')]),
        ),
    ]
