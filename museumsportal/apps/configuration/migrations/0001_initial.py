# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PageSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(help_text="All that goes after '/', for example: 'about/contact/'. Make sure to have trailing slash. Use '*' for all pages.", max_length=100, verbose_name='Path', blank=True)),
                ('pickled_settings', models.TextField(verbose_name='Settings', editable=False)),
                ('site', models.ForeignKey(verbose_name='Site', to='sites.Site')),
                ('user', models.ForeignKey(verbose_name='Viewer', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('path',),
                'abstract': False,
                'verbose_name': 'page settings',
                'verbose_name_plural': 'page settings',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_keywords', models.CharField(editable=False, max_length=255, blank=True, help_text='Separate keywords by comma.', null=True, verbose_name='Keywords')),
                ('meta_description', models.CharField(verbose_name='Description', max_length=255, null=True, editable=False, blank=True)),
                ('meta_author', models.CharField(max_length=255, verbose_name='Author', blank=True)),
                ('meta_copyright', models.CharField(max_length=255, verbose_name='Copyright', blank=True)),
                ('registration_type', models.CharField(default=b'simple', max_length=10, verbose_name='Registration type', choices=[(b'simple', 'Simple'), (b'advanced', 'Advanced')])),
                ('login_by_email', models.BooleanField(verbose_name='Login by email')),
                ('extra_head', base_libs.models.fields.PlainTextModelField(help_text='Third-party code snippets to be added to the end of the HEAD section.', verbose_name='Extra head', blank=True)),
                ('extra_body', base_libs.models.fields.PlainTextModelField(help_text='Third-party code snippets to be added to the end of the BODY section.', verbose_name='Extra body', blank=True)),
                ('meta_keywords_de', models.CharField(help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords', blank=True)),
                ('meta_keywords_en', models.CharField(help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords', blank=True)),
                ('meta_keywords_fr', models.CharField(help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords', blank=True)),
                ('meta_keywords_pl', models.CharField(help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords', blank=True)),
                ('meta_keywords_tr', models.CharField(help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords', blank=True)),
                ('meta_keywords_es', models.CharField(help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords', blank=True)),
                ('meta_keywords_it', models.CharField(help_text='Separate keywords by comma.', max_length=255, verbose_name='Keywords', blank=True)),
                ('meta_description_de', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('meta_description_en', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('meta_description_fr', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('meta_description_pl', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('meta_description_tr', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('meta_description_es', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('meta_description_it', models.CharField(max_length=255, verbose_name='Description', blank=True)),
                ('site', models.OneToOneField(verbose_name='Site', to='sites.Site')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'site settings',
                'verbose_name_plural': 'site settings',
            },
        ),
        migrations.AlterUniqueTogether(
            name='pagesettings',
            unique_together=set([('site', 'user')]),
        ),
    ]
