# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('sender_name', models.CharField(max_length=255, null=True, verbose_name='Sender name', blank=True)),
                ('sender_email', models.EmailField(max_length=254, null=True, verbose_name='Sender email', blank=True)),
                ('recipient_emails', base_libs.models.fields.PlainTextModelField(null=True, verbose_name='Recipient email(s)', blank=True)),
                ('subject', models.CharField(max_length=255, verbose_name='Subject', blank=True)),
                ('body', base_libs.models.fields.PlainTextModelField(verbose_name='Message (Plain text)', blank=True)),
                ('body_html', base_libs.models.fields.ExtendedTextField(verbose_name='Message (HTML)', blank=True)),
                ('is_sent', models.BooleanField(default=False, verbose_name='Sent')),
                ('delete_after_sending', models.BooleanField(default=False, verbose_name='Delete after sending')),
                ('body_html_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('creator', models.ForeignKey(related_name='emailmessage_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
                ('modifier', models.ForeignKey(related_name='emailmessage_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier')),
                ('recipient', models.ForeignKey(related_name='received_by_message_set', verbose_name='Recipient', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('sender', models.ForeignKey(related_name='sent_by_message_set', verbose_name='Sender', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-creation_date', 'subject'),
                'verbose_name': 'email message',
                'verbose_name_plural': 'email messages',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('name', models.CharField(max_length=255, verbose_name='Template Name')),
                ('subject', models.CharField(max_length=255, verbose_name='Subject (English)')),
                ('subject_de', models.CharField(max_length=255, verbose_name='Subject (German)')),
                ('subject_fr', models.CharField(max_length=255, verbose_name='Subject (French)')),
                ('subject_pl', models.CharField(max_length=255, verbose_name='Subject (Polish)')),
                ('subject_tr', models.CharField(max_length=255, verbose_name='Subject (Turkish)')),
                ('subject_es', models.CharField(max_length=255, verbose_name='Subject (Spanish)')),
                ('subject_it', models.CharField(max_length=255, verbose_name='Subject (Italian)')),
                ('body', base_libs.models.fields.PlainTextModelField(verbose_name='Template Text (English)', blank=True)),
                ('body_de', base_libs.models.fields.PlainTextModelField(verbose_name='Template Text (German)', blank=True)),
                ('body_fr', base_libs.models.fields.PlainTextModelField(verbose_name='Template Text (French)', blank=True)),
                ('body_pl', base_libs.models.fields.PlainTextModelField(verbose_name='Template Text (Polish)', blank=True)),
                ('body_tr', base_libs.models.fields.PlainTextModelField(verbose_name='Template Text (Turkish)', blank=True)),
                ('body_es', base_libs.models.fields.PlainTextModelField(verbose_name='Template Text (Spanish)', blank=True)),
                ('body_it', base_libs.models.fields.PlainTextModelField(verbose_name='Template Text (Italian)', blank=True)),
                ('body_html', models.TextField(null=True, verbose_name='Template HTML (English)', blank=True)),
                ('body_html_de', models.TextField(null=True, verbose_name='Template HTML (German)', blank=True)),
                ('body_html_fr', models.TextField(null=True, verbose_name='Template HTML (French)', blank=True)),
                ('body_html_pl', models.TextField(null=True, verbose_name='Template HTML (Polish)', blank=True)),
                ('body_html_tr', models.TextField(null=True, verbose_name='Template HTML (Turkish)', blank=True)),
                ('body_html_es', models.TextField(null=True, verbose_name='Template HTML (Spanish)', blank=True)),
                ('body_html_it', models.TextField(null=True, verbose_name='Template HTML (Italian)', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Written')),
            ],
            options={
                'ordering': ['-timestamp', 'name'],
                'verbose_name': 'email template',
                'verbose_name_plural': 'email templates',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplatePlaceholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sysname', models.SlugField(help_text='Do not change this value!', unique=True, max_length=255, verbose_name='Placeholder Internal Name')),
                ('name', models.CharField(verbose_name='Placeholder Name', max_length=64, null=True, editable=False)),
                ('relates_to', models.IntegerField(default=1, verbose_name='relates to', choices=[(1, 'Recipient'), (2, 'Sender'), (3, 'Object'), (4, 'Global')])),
                ('help_text', models.CharField(max_length=255, null=True, verbose_name='Placeholder Help text', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Written')),
                ('name_de', models.CharField(max_length=64, verbose_name='Placeholder Name')),
                ('name_en', models.CharField(max_length=64, verbose_name='Placeholder Name', blank=True)),
                ('name_fr', models.CharField(max_length=64, verbose_name='Placeholder Name', blank=True)),
                ('name_pl', models.CharField(max_length=64, verbose_name='Placeholder Name', blank=True)),
                ('name_tr', models.CharField(max_length=64, verbose_name='Placeholder Name', blank=True)),
                ('name_es', models.CharField(max_length=64, verbose_name='Placeholder Name', blank=True)),
                ('name_it', models.CharField(max_length=64, verbose_name='Placeholder Name', blank=True)),
            ],
            options={
                'ordering': ['relates_to', 'name'],
                'verbose_name': 'email template placeholder',
                'verbose_name_plural': 'email template placeholders',
            },
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='allowed_placeholders',
            field=models.ManyToManyField(to='mailing.EmailTemplatePlaceholder', verbose_name='Allowed Placeholders', blank=True),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='owner',
            field=models.ForeignKey(verbose_name='Owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='site',
            field=models.ForeignKey(blank=True, to='sites.Site', help_text='Restrict this object only for the selected site', null=True, verbose_name='Site'),
        ),
    ]
