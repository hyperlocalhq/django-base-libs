# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# possible markup types for TextFields. Those 
# settings apply to all models with Textfields.
MARKUP_PLAIN_TEXT =     'pt'
MARKUP_RAW_HTML =       'rh'
MARKUP_HTML_WYSIWYG =   'hw'
MARKUP_MARKDOWN =       'md'

MARKUP_TYPES = (
    (MARKUP_HTML_WYSIWYG, _('HTML WYSIWYG')),                
    (MARKUP_PLAIN_TEXT,   _('Plain Text')),
    (MARKUP_RAW_HTML,     _('Raw HTML')),
    (MARKUP_MARKDOWN,     _('Markdown')),
) 

DEFAULT_MARKUP_TYPE = getattr(settings, "DEFAULT_MARKUP_TYPE", MARKUP_PLAIN_TEXT)

STATUS_CODE_DRAFT = 0
STATUS_CODE_PUBLISHED = 1

JQUERY_URL = getattr(
    settings,
    "JQUERY_URL",
    "http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js",
    )

JQUERY_UI_URL = getattr(
    settings,
    "JQUERY_UI_URL",
    "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/jquery-ui.min.js",
    )
