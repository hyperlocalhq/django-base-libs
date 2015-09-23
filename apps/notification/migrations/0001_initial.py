# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Digest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('frequency', models.CharField(max_length=15, verbose_name='frequency', choices=[(b'daily', 'Daily'), (b'weekly', 'Weekly')])),
                ('is_sent', models.BooleanField(default=False, verbose_name='sent?')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'digest',
                'verbose_name_plural': 'digests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DigestNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('message', models.TextField(verbose_name='message')),
                ('digest', models.ForeignKey(verbose_name='digest', to='notification.Digest')),
            ],
            options={
                'ordering': ['creation_date'],
                'verbose_name': 'notice of a digest',
                'verbose_name_plural': 'notices of digests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(verbose_name='message')),
                ('added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added')),
                ('unseen', models.BooleanField(default=True, verbose_name='unseen')),
                ('archived', models.BooleanField(default=False, verbose_name='archived')),
            ],
            options={
                'ordering': ['-added'],
                'verbose_name': 'notice',
                'verbose_name_plural': 'notices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeEmailTemplate',
            fields=[
                ('emailtemplate_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mailing.EmailTemplate')),
            ],
            options={
                'abstract': False,
            },
            bases=('mailing.emailtemplate',),
        ),
        migrations.CreateModel(
            name='NoticeSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('medium', models.CharField(max_length=1, verbose_name='medium', choices=[(b'1', 'Email')])),
                ('frequency', models.CharField(max_length=15, verbose_name='sending frequency', choices=[(b'never', "Don't send notifications"), (b'immediately', 'Send immediately'), (b'daily', 'Send in a daily digest'), (b'weekly', 'Send in a weekly digest')])),
            ],
            options={
                'verbose_name': 'notice setting',
                'verbose_name_plural': 'notice settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='should match the slug of an associated EmailTemplate object', unique=True, max_length=255, verbose_name='Sysname')),
                ('display', models.CharField(verbose_name='display', max_length=50, null=True, editable=False)),
                ('description', models.CharField(verbose_name='description', max_length=100, null=True, editable=False)),
                ('message_template', models.TextField(default=b'', help_text='This message will be shown in the website. Accepted template variables: {{ notified_user }}, {{ object }}, and specific extra context.', null=True, editable=False, verbose_name='Message Template')),
                ('default', models.IntegerField(help_text='How will the notices be reported to users by default?', verbose_name='default media', choices=[(0, 'Not reported'), (1, 'Shown in the website'), (2, 'Shown in the website and sent by email')])),
                ('is_public', models.BooleanField(default=True, help_text='is this notice type displayed in the public notification settings?', verbose_name='public')),
                ('description_de', models.CharField(max_length=100, verbose_name='description')),
                ('description_en', models.CharField(max_length=100, verbose_name='description', blank=True)),
                ('message_template_de', base_libs.models.fields.PlainTextModelField(default=b'', help_text='This message will be shown in the website. Accepted template variables: {{ notified_user }}, {{ object }}, and specific extra context.', null=True, verbose_name='Nachrichten Vorlage')),
                ('message_template_en', base_libs.models.fields.PlainTextModelField(default=b'', help_text='This message will be shown in the website. Accepted template variables: {{ notified_user }}, {{ object }}, and specific extra context.', null=True, verbose_name='Nachrichten Vorlage', blank=True)),
                ('display_de', models.CharField(max_length=50, verbose_name='display')),
                ('display_en', models.CharField(max_length=50, verbose_name='display', blank=True)),
            ],
            options={
                'ordering': ('category__title', 'display'),
                'verbose_name': 'notice type',
                'verbose_name_plural': 'notice types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoticeTypeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='display', max_length=50, null=True, editable=False)),
                ('is_public', models.BooleanField(default=True, help_text='is this category displayed in the public notification settings?', verbose_name='public')),
                ('title_de', models.CharField(max_length=50, verbose_name='display')),
                ('title_en', models.CharField(max_length=50, verbose_name='display', blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'notice-type category',
                'verbose_name_plural': 'notice-type categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ObservedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object')),
                ('added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added')),
                ('signal', models.CharField(max_length=255, verbose_name='signal')),
                ('content_type', models.ForeignKey(verbose_name="Related object's type (model)", to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.')),
                ('notice_type', models.ForeignKey(verbose_name='notice type', to='notification.NoticeType')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-added'],
                'verbose_name': 'observed item',
                'verbose_name_plural': 'observed items',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='noticetype',
            name='category',
            field=models.ForeignKey(verbose_name='Category', blank=True, to='notification.NoticeTypeCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noticesetting',
            name='notice_type',
            field=models.ForeignKey(verbose_name='notice type', to='notification.NoticeType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noticesetting',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notice',
            name='notice_type',
            field=models.ForeignKey(verbose_name='notice type', to='notification.NoticeType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notice',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='digestnotice',
            name='notice_type',
            field=models.ForeignKey(verbose_name='notice type', to='notification.NoticeType'),
            preserve_default=True,
        ),
    ]
