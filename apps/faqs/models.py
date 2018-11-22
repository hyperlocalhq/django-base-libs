# -*- coding: UTF-8 -*-
import sys

from django.db import models

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _

from django.utils.encoding import force_unicode
from django.conf import settings

from base_libs.models.models import UrlMixin
from base_libs.models.models import SlugMixin
from base_libs.models import ViewsMixin
from base_libs.models import CreationModificationMixin
from base_libs.models import CreationModificationDateMixin
from base_libs.models import MultiSiteContainerMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField
from base_libs.models.fields import ExtendedTextField  # needed for south to work
from base_libs.utils.misc import get_translation

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey

verbose_name = _("FAQ")


class FaqContainer(
    MultiSiteContainerMixin,
    CreationModificationDateMixin,
):
    """
    The container model holding FaqCategories
    """
    title = MultilingualCharField(
        _('title'),
        blank=True,
        max_length=255,
    )

    def __unicode__(self):
        sites_str = ", ".join([str(item.name) for item in self.sites.all()])
        if sites_str != "":
            sites_str = u" (%s)" % sites_str
        return force_unicode(self.title) + sites_str

    def save(self, *args, **kwargs):
        content_object = self.content_object
        if not self.title:
            title_dict = {}
            if content_object:
                for key in settings.LANGUAGES:
                    title_dict[key[0]] = \
                        get_translation('Faqs for %(obj)s', language=key[0]) %\
                            {'obj': force_unicode(content_object)}
                self.title = title_dict
            else:
                for key in settings.LANGUAGES:
                    title_dict[key[0]] = \
                        get_translation('General Faqs', language=key[0])
                self.title = title_dict

        super(FaqContainer, self).save(*args, **kwargs)

    save.alters_data = True

    class Meta(MultiSiteContainerMixin.Meta):
        ordering = ('title', )
        verbose_name = _("FAQ Container")
        verbose_name_plural = _("FAQ Containers")


# QUICK HACK: Without the following the FaqContainer.objects.model will be MultiSiteContainerMixin and won't work correctly
FaqContainer.objects.model = FaqContainer


class FaqCategoryManager(TreeManager):
    def get_roots(self, container):
        return self.get_queryset().filter(
            container=container, parent__isnull=True
        )


class FaqCategory(MPTTModel, CreationModificationMixin, UrlMixin, SlugMixin()):
    container = models.ForeignKey(
        FaqContainer,
        verbose_name=_('container'),
    )
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
    title = MultilingualCharField(_('title'), max_length=512)
    short_title = MultilingualCharField(
        _('short title'),
        help_text=_(
            "a short title to be displayed in page breadcrumbs and headline."
        ),
        max_length=80,
    )
    description = MultilingualTextField(
        _('description'),
        blank=True,
        max_length=8192,
    )

    # python format for displaying the sort_order of the child nodes
    children_sort_order_format = models.CharField(
        _('format for child categories'),
        max_length=20,
        help_text=_("sort order format for children (python style, e.g '%d')"),
        blank=True,
        null=True,
        default='%02d',
    )

    faqs_on_separate_page = models.BooleanField(
        _('separate page'),
        help_text=_(
            "check, if you want to display relating faqs on a separate page. If this category is not a 'leaf category', it has no effect."
        ),
        default=False,
    )

    objects = FaqCategoryManager()

    class Meta:
        verbose_name = _('FAQ Category')
        verbose_name_plural = _('FAQ Categories')
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    def __unicode__(self):
        return force_unicode(self.title)

    def short_str(self):
        return self.short_title

    def populate_short_title(self):
        for language in dict(settings.LANGUAGES).keys():
            short_title = getattr(self, 'short_title_%s' % language)
            if not short_title or len(short_title) == 0:
                short_title = ""
                for word in getattr(self, 'title_%s' % language).split(' '):
                    if len(short_title) + len(word) < 32:
                        if len(short_title) != 0:
                            short_title += " "
                        short_title = short_title + word
                    else:
                        break
                setattr(self, 'short_title_%s' % language, short_title)
        return

    def get_verbose(self):
        """
        returns a verbose representation of the category path
        this is also used as a callback for admin list_filters.
        For further info, 
        see base_libs.monkeypatches.admin_patches.py
        """
        path = ""
        parent = self
        while parent:
            indented = parent.short_title
            if parent.path:
                indented = "%s %s" % (
                    "-" * (parent.path.count("/") - 1),
                    parent.short_title,
                )
            if len(path) > 0:
                path = '%s<br />%s' % (indented, path)
            else:
                path = indented
            parent = parent.parent
        path = '%s<br /><br />' % path
        return path

    def save(self, *args, **kwargs):
        if not self.pk:
            FaqCategory.objects.insert_node(self, self.parent)
        self.populate_short_title()
        # if self has a parent, set the container of the parent!!!!
        if self.parent:
            self.container = self.parent.container
        super(FaqCategory, self).save(*args, **kwargs)

    save.alters_data = True

    def get_formatted_sort_order(self):
        if self.parent:
            if self.parent.children_sort_order_format:
                try:
                    return self.parent.children_sort_order_format %\
                        self.sort_order
                except:
                    pass
        return "%s" % self.sort_order

    def get_absolute_url(self):
        return self.get_url_path()

    def get_url_path(self):
        container = self.container
        prefix = "/"
        rel_obj = container.content_object
        if rel_obj and hasattr(rel_obj, "get_url_path"):
            prefix = rel_obj.get_url_path()
        return "%s%s/%s" % (
            prefix,
            container.sysname,
            self.get_relative_url(),
        )

    def get_relative_url(self):
        category = self
        if not self.faqs_on_separate_page and category.parent:
            category = category.parent
        return "%s/" % category.slug

    def get_faqs(self):
        return QuestionAnswer.objects.filter(category=self
                                            ).order_by('sort_order')

    def has_faqs(self):
        return self.get_faqs().count() > 0

    def get_nof_faqs(self):
        return self.get_faqs().count()

    get_nof_faqs.short_description = _('# Faqs')

    def has_link(self):
        """
        just for usage in templates: determines, if an faq category 
        has a "link" to a separate page: This is true, if and only 
        if the category has children or (the category has faqs and
        the category's faqs are displayed on a separate page!)
        """
        #return self.has_children() or\
        # (self.has_faqs() and self.faqs_on_separate_page)
        return not self.is_leaf_node() or (
            self.has_faqs() and self.faqs_on_separate_page
        )


class QuestionAnswer(CreationModificationMixin, ViewsMixin, UrlMixin):

    category = TreeForeignKey(FaqCategory, verbose_name=_('category'))
    sort_order = models.IntegerField(_('sort order'))
    #question = MultilingualCharField(_('question'), max_length=2048)
    question = MultilingualCharField(_('question'), max_length=255)
    answer = MultilingualTextField(_('answer'), max_length=16384)

    class Meta:
        verbose_name = _('Question-Answer')
        verbose_name_plural = _('Questions-Answers')
        ordering = ['category']

    def __unicode__(self):
        return force_unicode(self.get_question())

    def get_url(self):
        return "%s#qa-%s" % (self.category.get_absolute_url(), self.pk)

    def get_answer_links_targeted_to_blank(self):
        """
        all external links should have target=blank.
        We do just some naive replacement
        """
        replaced_answer = self.answer
        replaced_answer = replaced_answer.replace('<a ', '<a target="blank" ')
        return replaced_answer

    def get_question(self):
        from base_libs.utils.misc import truncwords
        return truncwords(self.question, 10)

    get_question.short_description = _('question')
    get_question.allow_tags = True
    get_question.admin_order_field = 'question'

    def get_answer(self):
        # we need a method here just to use 'allow_tags'!
        #from base_libs.utils.misc import truncwords
        #return truncwords(self.answer, 10)
        return self.answer

    get_answer.short_description = _('answer')
    get_answer.allow_tags = True
    get_answer.admin_order_field = 'answer'

    def get_formatted_sort_order(self):
        if self.category.children_sort_order_format:
            try:
                return self.category.children_sort_order_format % self.sort_order
            except:
                pass
        return "%s" % self.sort_order

    def get_category(self):
        return self.category.get_verbose()

    get_category.short_description = _('category')
    get_category.allow_tags = True
    get_category.admin_order_field = 'category'
