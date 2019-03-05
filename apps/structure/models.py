# -*- coding: UTF-8 -*-
import sys
from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.translation import gettext
from django.utils.safestring import mark_safe

from base_libs.models.models import SlugMixin
from base_libs.models.models import SysnameMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField

from filebrowser.fields import FileBrowseField

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey, TreeManyToManyField

verbose_name = _("Structure")


class Vocabulary(SlugMixin(), SysnameMixin()):
    title = MultilingualCharField(_('title'), max_length=255)
    body = MultilingualTextField(_('body'), blank=True)
    image = FileBrowseField(
        _('Image'),
        max_length=255,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
        blank=True
    )
    hierarchy = models.BooleanField(
        _(
            "Will the terms of this vocabulary be used in hierarchical structure?"
        ),
        default=False
    )

    class Meta:
        ordering = ['title']
        verbose_name = _("vocabulary")
        verbose_name_plural = _("vocabularies")

    def __unicode__(self):
        return self.title

    def get_title(self):
        return self.title

    def get_slug(self):
        return self.slug

    def get_body(self):
        return mark_safe(self.body)

    def save(self, *args, **kwargs):
        super(Vocabulary, self).save(*args, **kwargs)
        # update paths in the child terms
        for t in self.term_set.all():
            t.save()

    save.alters_data = True

    def link_add_term(self):
        return """<a class="addlink" href="../term/add/?vocabulary__id__exact=%d">%s</a>""" % (
            self.pk,
            gettext("Add Term"),
        )

    link_add_term.short_description = ""
    link_add_term.allow_tags = True

    def link_change_terms(self):
        return """<a class="changelink" href="../term/?vocabulary__id__exact=%d">%s</a>""" % (
            self.pk,
            gettext("Change Terms"),
        )

    link_change_terms.short_description = ""
    link_change_terms.allow_tags = True


class Term(MPTTModel, SlugMixin(), SysnameMixin()):
    sort_order = models.IntegerField(
        _("sort order"),
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
        'self',
        #related_name="%(class)s_children",
        related_name="child_set",
        blank=True,
        null=True,
    )
    vocabulary = models.ForeignKey(Vocabulary, verbose_name=_("Vocabulary"))
    title = MultilingualCharField(_('title'), max_length=255)
    body = MultilingualTextField(_('body'), blank=True)
    image = FileBrowseField(
        _('Image'),
        max_length=255,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
        blank=True
    )

    objects = TreeManager()

    class Meta:
        verbose_name = _("term")
        verbose_name_plural = _("terms")
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return self.title

    def get_title(self, prefix="", postfix=""):
        return self.title

    def get_slug(self):
        return self.slug

    def get_body(self):
        return mark_safe(self.body)

    def _recurse_for_parents_ids(self, cat_obj):
        #This is used for search path formating
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(str(p.pk))
            more = self._recurse_for_parents_ids(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def save(self, *args, **kwargs):
        if not self.pk:
            Term.objects.insert_node(self, self.parent)
        super(Term, self).save(*args, **kwargs)


class ContextCategory(MPTTModel, SlugMixin(), SysnameMixin()):
    sort_order = models.IntegerField(
        _("sort order"),
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
        'self',
        #related_name="%(class)s_children",
        related_name="child_set",
        blank=True,
        null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)
    creative_sectors = TreeManyToManyField(
        Term,
        verbose_name=_("Available creative sectors"),
        blank=True,
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'}
    )
    body = MultilingualTextField(_('body'), blank=True)
    image = FileBrowseField(
        _('Image'),
        max_length=255,
        extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
        blank=True
    )
    is_applied4person = models.BooleanField(_("for people"), default=True)
    is_applied4institution = models.BooleanField(
        _("for institutions"), default=True
    )
    is_applied4document = models.BooleanField(_("for documents"), default=True)
    is_applied4event = models.BooleanField(_("for events"), default=True)
    is_applied4persongroup = models.BooleanField(
        _("for groups of people"), default=True
    )

    objects = TreeManager()

    class Meta:
        verbose_name = _("context category")
        verbose_name_plural = _("context categories")
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        level = self.get_level()
        return u'{} {}'.format(
            '-' * level,
            self.title.title(),
        )

    def get_title(self, prefix="", postfix=""):
        return self.title

    def get_slug(self):
        return self.slug

    def get_body(self):
        return mark_safe(self.body)

    def _recurse_for_parents_ids(self, cat_obj):
        #This is used for search path formating
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(str(p.pk))
            more = self._recurse_for_parents_ids(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def save(self, *args, **kwargs):
        if not self.pk:
            ContextCategory.objects.insert_node(self, self.parent)

        super(ContextCategory, self).save(*args, **kwargs)

        # update paths in the child terms
        for t in self.child_set.all():
            if not self.is_applied4person:
                t.is_applied4person = False
            if not self.is_applied4institution:
                t.is_applied4institution = False
            if not self.is_applied4document:
                t.is_applied4document = False
            if not self.is_applied4event:
                t.is_applied4event = False
            t.save()
            t.creative_sectors = []
            for ci in self.creative_sectors.all():
                t.creative_sectors.add(ci)

    save.alters_data = True


class Category(MPTTModel, SlugMixin(), SysnameMixin()):
    parent = TreeForeignKey(
        'self',
        related_name="child_set",
        blank=True,
        null=True,
    )
    title = MultilingualCharField(_('title'), max_length=255)

    objects = TreeManager()

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["tree_id", "lft"]

    def __unicode__(self):
        return self.title
