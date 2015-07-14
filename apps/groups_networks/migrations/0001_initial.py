# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import filebrowser.fields
from django.conf import settings
import base_libs.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('i18n', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'members', max_length=30, verbose_name='Role', choices=[(b'owners', 'Owner'), (b'moderators', 'Moderator'), (b'members', 'Member')])),
                ('title', models.CharField(verbose_name='Title', max_length=255, null=True, editable=False, blank=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name='Accepted by user')),
                ('is_blocked', models.BooleanField(default=False, verbose_name='Blocked')),
                ('is_contact_person', models.BooleanField(default=False, verbose_name='Contact Person')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp', null=True)),
                ('activation', models.DateTimeField(verbose_name='Activated', null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('title_en', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('confirmer', models.ForeignKey(related_name='group_confirmer', verbose_name='Confirmer', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('inviter', models.ForeignKey(related_name='group_inviter', verbose_name='Inviter', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Membership at a Group of People',
                'verbose_name_plural': 'Memberships at Groups of People',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('sort_order', models.IntegerField(default=0, verbose_name='sort order', editable=False, blank=True)),
                ('title', models.CharField(verbose_name='title', max_length=255, null=True, editable=False)),
                ('title_de', models.CharField(max_length=255, verbose_name='title')),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='child_set', blank=True, to='groups_networks.GroupType', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'group type',
                'verbose_name_plural': 'group types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(verbose_name='creation date', editable=False)),
                ('modified_date', models.DateTimeField(verbose_name='modified date', null=True, editable=False)),
                ('object_id', models.CharField(default=b'', help_text='Please select the related object.', max_length=255, verbose_name='Related object', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug for URIs')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('title2', models.CharField(max_length=255, verbose_name='Title 2', blank=True)),
                ('description', models.TextField(default=b'', verbose_name='Description', null=True, editable=False, blank=True)),
                ('access_type', models.CharField(default=b'secret', max_length=10, verbose_name='Access Type', choices=[(b'public', 'Public'), (b'private', 'Private'), (b'secret', 'Secret')])),
                ('is_by_invitation', models.BooleanField(default=False, verbose_name='Membership by Invitation')),
                ('is_by_confirmation', models.BooleanField(default=False, verbose_name='Membership by Confirmation')),
                ('status', models.CharField(default=b'draft', max_length=20, verbose_name='Status', blank=True, choices=[(b'draft', 'Draft'), (b'published', 'Published'), (b'not_listed', 'Not Listed')])),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, verbose_name='Image', blank=True)),
                ('description_de', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_de_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('description_en', base_libs.models.fields.ExtendedTextField(default=b'', null=True, verbose_name='Beschreibung', blank=True)),
                ('description_en_markup_type', models.CharField(default=b'pt', help_text='You can select an appropriate markup type here', max_length=10, verbose_name='Markup type', choices=[(b'hw', 'HTML WYSIWYG'), (b'pt', 'Plain Text'), (b'rh', 'Raw HTML'), (b'md', 'Markdown')])),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text='Please select the type (model) for the relation, you want to build.', null=True, verbose_name="Related object's type (model)")),
                ('context_categories', mptt.fields.TreeManyToManyField(to='structure.ContextCategory', verbose_name='Context categories', blank=True)),
                ('creative_sectors', mptt.fields.TreeManyToManyField(related_name='creative_sectors_groups', verbose_name='Creative sectors', to='structure.Term', blank=True)),
                ('group_type', mptt.fields.TreeForeignKey(related_name='type_groups', verbose_name='Group Type', to='groups_networks.GroupType')),
                ('organizing_institution', models.ForeignKey(verbose_name='Organizing institution', blank=True, to='institutions.Institution', null=True)),
                ('preferred_language', models.ForeignKey(verbose_name='Preferred Language', blank=True, to='i18n.Language', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Group of People',
                'verbose_name_plural': 'Groups of People',
                'permissions': (('can_invite', 'Can invite users'), ('can_confirm', 'Can confirm memberships'), ('can_change_members', 'Can change members'), ('can_see_members', 'Can see members'), ('can_see_roles', 'Can see roles of each member')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='person_group',
            field=models.ForeignKey(verbose_name='Group of People', to='groups_networks.PersonGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
