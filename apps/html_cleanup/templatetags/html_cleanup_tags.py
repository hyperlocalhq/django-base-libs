# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup

from django.conf import settings
from django import template

register = template.Library()


@register.filter(is_safe=True)
def remove_empty_paragraphs(fragment):
    soup = BeautifulSoup(fragment, "html.parser")
    for tag in soup.findAll(lambda t: t.name == 'p' and t.find(True) is None and (t.string is None or t.string.strip() == "")):
        tag.extract()
    return unicode(soup)


ACCEPTABLE_TAGS = getattr(
    settings, "HTML_CLEANUP_ACCEPTABLE_TAGS", [
        'a',
        'abbr',
        'acronym',
        'address',
        'area',
        'b',
        'big',
        'blockquote',
        'br',
        'button',
        'caption',
        'center',
        'cite',
        'code',
        'col',
        'colgroup',
        'dd',
        'del',
        'dfn',
        'dir',
        'div',
        'dl',
        'dt',
        'em',
        'font',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'hr',
        'i',
        'img',
        'ins',
        'kbd',
        'label',
        'legend',
        'li',
        'map',
        'menu',
        'ol',
        'p',
        'pre',
        'q',
        's',
        'samp',
        'small',
        'span',
        'strike',
        'strong',
        'sub',
        'sup',
        'table',
        'tbody',
        'td',
        'tfoot',
        'th',
        'thead',
        'tr',
        'tt',
        'u',
        'ul',
        'var',
    ]
)

ACCEPTABLE_ATTRS = getattr(
    settings, "HTML_CLEANUP_ACCEPTABLE_ATTRS", [
        'abbr',
        'accept',
        'accept-charset',
        'accesskey',
        'action',
        'align',
        'alt',
        'axis',
        'border',
        'cellpadding',
        'cellspacing',
        'char',
        'charoff',
        'charset',
        'checked',
        'cite',
        'clear',
        'cols',
        'colspan',
        'color',
        'compact',
        'coords',
        'datetime',
        'dir',
        'enctype',
        'for',
        'headers',
        'height',
        'href',
        'hreflang',
        'hspace',
        'id',
        'ismap',
        'label',
        'lang',
        'longdesc',
        'maxlength',
        'method',
        'multiple',
        'name',
        'nohref',
        'noshade',
        'nowrap',
        'prompt',
        'rel',
        'rev',
        'rows',
        'rowspan',
        'rules',
        'scope',
        'shape',
        'size',
        'span',
        'src',
        'start',
        'summary',
        'tabindex',
        'target',
        'title',
        'type',
        'usemap',
        'valign',
        'value',
        'vspace',
        'width',
    ]
)


@register.filter(is_safe=True)
def clean_html(fragment):
    while True:
        soup = BeautifulSoup(fragment, "html.parser")
        removed = False
        for tag in soup.findAll(True):  # find all tags
            if tag.name not in ACCEPTABLE_TAGS:
                tag.extract()  # remove the bad ones
                removed = True
            else:
                for attr in tag.attrs.keys():
                    if attr not in ACCEPTABLE_ATTRS:
                        del tag[attr]

        # turn it back to html
        fragment = unicode(soup)

        if removed:
            # we removed tags and tricky can could exploit that!
            # we need to reparse the html until it stops changing
            continue  # next round

        return fragment
