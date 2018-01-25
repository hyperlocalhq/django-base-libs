# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from base_libs.admin.options import MarkupTypeOptions

from .models import QuestionAnswer, Document


class QuestionAnswerPlugin(MarkupTypeOptions, CMSPluginBase):
    model = QuestionAnswer
    name = _("Question and Answer")
    render_template = "cms/plugins/question_answer.html"
    change_form_template = "cms/plugins/question_answer_plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder
        })
        return context


plugin_pool.register_plugin(QuestionAnswerPlugin)


class DocumentPlugin(MarkupTypeOptions, CMSPluginBase):
    model = Document
    name = _("Document")
    render_template = "cms/plugins/document.html"
    change_form_template = "cms/plugins/document_plugin_change_form.html"

    filter_horizontal = ["categories"]

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder
        })
        return context


plugin_pool.register_plugin(DocumentPlugin)
