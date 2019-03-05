# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields
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
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('sender_name', models.CharField(default='Berlin B\xfchnen', max_length=255, verbose_name='Sender name')),
                ('sender_email', models.EmailField(default='berlin-buehnen@kulturprojekte-berlin.de', max_length=254, verbose_name='Sender email')),
                ('subject', models.CharField(max_length=255, verbose_name='Subject')),
                ('body_html', base_libs.models.fields.ExtendedTextField(verbose_name='Message', blank=True)),
                ('image', filebrowser.fields.FileBrowseField(help_text='A path to a locally stored image.', max_length=255, verbose_name='Image')),
                ('template', base_libs.models.fields.TemplatePathField(path=b'mailchimp/campaign/', max_length=150, verbose_name='Template', match=b'\\.html$')),
                ('sent', models.BooleanField(default=False, verbose_name='Sent', editable=False)),
                ('body_html_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('creator', models.ForeignKey(related_name='campaign_creator', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='creator')),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'Campaign',
                'verbose_name_plural': 'Campaigns',
            },
        ),
        migrations.CreateModel(
            name='MailingContentBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.CharField(blank=True, max_length=40, verbose_name=b'Content Type', choices=[('authorship', 'Image authorship'), ('locations', 'Theaters'), ('productions', 'Productions'), ('festivals', 'Festivals'), ('educational_departments', 'Educational Departments'), ('educational_projects', 'Educational Projects'), ('article', 'News'), ('banner', 'Banner'), ('image_and_text', 'Image and Text'), ('headline', 'Headline'), ('text', 'Text only'), ('page_teaser', 'Page Teaser')])),
                ('content', base_libs.models.fields.ExtendedTextField(verbose_name='Content', blank=True)),
                ('sort_order', base_libs.models.fields.PositionField(default=None, verbose_name='Sort order')),
                ('content_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('campaign', models.ForeignKey(to='mailchimp.Campaign')),
            ],
            options={
                'ordering': ('sort_order',),
                'verbose_name': 'Content Block',
                'verbose_name_plural': 'Content Blocks',
            },
        ),
        migrations.CreateModel(
            name='MList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False)),
                ('is_public', models.BooleanField(default=True, help_text='Will this mailing list be displayed in the public settings of subscriptions?', verbose_name='Public')),
                ('last_sync', models.DateTimeField(null=True, verbose_name='Last sync', blank=True)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('site', models.ForeignKey(blank=True, to='sites.Site', help_text='Restrict this object only for the selected site', null=True, verbose_name='Site')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Mailing List',
                'verbose_name_plural': 'Mailing Lists',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('api_key', models.CharField(max_length=200, verbose_name='API key', blank=True)),
                ('double_optin', models.BooleanField(default=True, help_text='Flag to control whether a double opt-in confirmation message is sent. ABUSING THIS MAY CAUSE YOUR ACCOUNT TO BE SUSPENDED.', verbose_name='Double Optin')),
                ('update_existing', models.BooleanField(default=False, help_text='Flag to congtrol whether the existing subscribers should be updated instead of throwing an error.', verbose_name='Update existing')),
                ('send_welcome', models.BooleanField(default=False, help_text='If double optin is false and this is true, MailChimp will send a welcome message to new subscribers.', verbose_name='Send welcome')),
                ('delete_member', models.BooleanField(default=False, help_text='Flag to completely delete the member from the list instead of just unsubscribing', verbose_name='Delete member')),
                ('send_goodbye', models.BooleanField(default=True, help_text='Flag to send the goodbye message to the email address.', verbose_name='Send goodbye')),
            ],
            options={
                'ordering': ['api_key'],
                'verbose_name': 'MailChimp Settings',
                'verbose_name_plural': 'MailChimp Settings',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('first_name', models.CharField(max_length=200, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=200, verbose_name='Last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email address', blank=True)),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='IP Address', blank=True)),
                ('status', models.CharField(blank=True, max_length=200, verbose_name='Status', choices=[(b'pending', 'Pending'), (b'subscribed', 'Subscribed'), (b'unsubscribed', 'Unsubscribed')])),
                ('mailinglist', models.ForeignKey(verbose_name='Mailing list', to='mailchimp.MList')),
                ('subscriber', models.ForeignKey(verbose_name='Subscriber', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['email'],
                'verbose_name': 'subscription',
                'verbose_name_plural': 'subscriptions',
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='mailinglist',
            field=models.ForeignKey(verbose_name='Mailing list', to='mailchimp.MList'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='modifier',
            field=models.ForeignKey(related_name='campaign_modifier', on_delete=django.db.models.deletion.SET_NULL, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modifier'),
        ),
    ]
