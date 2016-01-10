# -*- coding: utf-8 -*-
import re

from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import QuestionAnswer, Document


class QuestionAnswerPlugin(CMSPluginBase):
    model = QuestionAnswer
    name = _("Question and Answer")
    render_template = "cms/plugins/question_answer.html"
    change_form_template = "cms/plugins/question_answer_plugin_change_form.html"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(QuestionAnswerPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder
        })
        return context


plugin_pool.register_plugin(QuestionAnswerPlugin)


class DocumentPlugin(CMSPluginBase):
    model = Document
    name = _("Document")
    render_template = "cms/plugins/document.html"
    change_form_template = "cms/plugins/document_plugin_change_form.html"

    filter_horizontal = ["categories"]

    def formfield_for_dbfield(self, db_field, **kwargs):
        # add .markupType to body_markup_type
        field = super(DocumentPlugin, self).formfield_for_dbfield(db_field, **kwargs)
        if re.search('markup_type$', db_field.name):
            field.widget.attrs['class'] = "markupType"
        return field

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder
        })
        return context


plugin_pool.register_plugin(DocumentPlugin)
