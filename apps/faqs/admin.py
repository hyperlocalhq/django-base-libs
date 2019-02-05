from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.conf import settings

from base_libs.models import MultiSiteContainerMixinAdminOptions
from base_libs.models import MultiSiteContainerMixinAdminForm
from base_libs.models.admin import get_admin_lang_section
from base_libs.admin import ExtendedModelAdmin
from base_libs.admin import ExtendedStackedInline
from base_libs.admin.tree_editor import TreeEditor
from ccb.apps.faqs.models import FaqContainer, FaqCategory, QuestionAnswer


class FaqContainerAdminForm(MultiSiteContainerMixinAdminForm):
    class Meta:
        model = FaqContainer
        exclude = ()


class FaqContainerOptions(MultiSiteContainerMixinAdminOptions):
    save_on_top = True
    search_fields = ['title']
    list_display = ('id', 'title', 'get_sites', 'get_content_object_display', 'sysname')
    list_display_link = ('id', 'title')
    list_filter = ("creation_date", "modified_date",)

    fieldsets = get_admin_lang_section(_('Title'), ['title'])
    fieldsets += MultiSiteContainerMixinAdminOptions.fieldsets

    form = FaqContainerAdminForm


class QuestionAnswer_Inline(ExtendedStackedInline):
    model = QuestionAnswer
    sortable = True
    sortable_field_name = "sort_order"
    allow_add = True
    extra = 0
    fieldsets = [
        (None, {'fields': ("sort_order",)}),
    ]
    fieldsets += get_admin_lang_section(_("Contents"), ['question', 'answer'], True)
    classes = ('collapse open',)
    inline_classes = ('collapse open',)


class FaqCategoryAdminForm(ModelForm):
    class Meta:
        model = FaqCategory
        exclude = ()

    def __init__(self, *args, **kwargs):
        # hackish way to display markup types for descriptions
        super(FaqCategoryAdminForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.LANGUAGES:
            self.fields['description_%s_markup_type' % lang_code].widget.attrs["class"] = "markupType"


class FaqCategoryOptions(TreeEditor):
    form = FaqCategoryAdminForm
    save_on_top = True
    inlines = [QuestionAnswer_Inline]
    search_fields = ['title', 'short_title_']
    list_display = [
        'actions_column',
        'indented_short_title',
        'container',
        'short_title',
        'questionanswer_count',
        # 'slug',
        'get_url_path'
    ]
    list_filter = ('container', "creation_date", "creator", "modified_date", "modifier")

    fieldsets = [(None, {'fields': ('container', 'parent', 'slug')}), ]
    fieldsets += get_admin_lang_section(_("Contents"), ['title', 'short_title', 'description'])

    _additional_fields = ['children_sort_order_format', 'faqs_on_separate_page', ]
    # hackish way to display markup types for descriptions
    for lang_code, lang_name in settings.LANGUAGES:
        _additional_fields.append('description_%s_markup_type' % lang_code)

    fieldsets += [
        (_('Additional'), {'fields': _additional_fields, 'classes': ("collapse closed",), }),
    ]
    prepopulated_fields = {"slug": ("title_%s" % settings.LANGUAGE_CODE,), }

    def questionanswer_count(self, obj):
        return obj.questionanswer_count

    questionanswer_count.short_description = _('# FAQs')

    def get_queryset(self, request):
        return super(FaqCategoryOptions, self).get_queryset(request).annotate(
            questionanswer_count=models.Count('questionanswer'),
        )


class QuestionAnswerOptions(ExtendedModelAdmin):
    save_on_top = True
    search_fields = ['question', 'answer', 'category__title', ]
    list_display = ('get_question', 'get_category', 'sort_order', 'views',)
    list_filter = ('category', "creation_date", "creator", "modified_date", "modifier")

    fieldsets = [
        (None, {'fields': ('category', 'sort_order')}),
    ]
    fieldsets += get_admin_lang_section(_("Contents"), ['question', 'answer'])
    prepopulated_fields = {"slug": ("question_%s" % settings.LANGUAGE_CODE,), }


admin.site.register(FaqContainer, FaqContainerOptions)
admin.site.register(FaqCategory, FaqCategoryOptions)
# admin.site.register(QuestionAnswer, QuestionAnswerOptions)
