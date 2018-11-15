# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

"""
Utility functions for parsing XML content in combination with xml.dom.minidom
"""

from xml.dom.minidom import Node
from django.utils.encoding import force_text, force_unicode


def get_first(parent_node, descendant_tagname):
    """
    Returns the first element by a tag name within the given node
    e.g. get_first(item_node, "title") will return title node
    where item_node's xml is
    <item>
        <id>123</id>
        <title>TITLE</title>
    </item>
    """
    nodes = parent_node.getElementsByTagName(descendant_tagname)
    if nodes:
        return nodes[0]
    return None


def get_value(parent_node, descendant_tagname=None):
    """
    Returns the textual value of a node or the first descendant by a tag name
    e.g.get_value(item_node) will return "ITEM"
    and get_value(item_node, "title") will return "TITLE"
    where item_node's xml is
    <item>
        <id>123</id>
        <title>TITLE</title>
        ITEM
    </item>
    """
    if descendant_tagname:
        node = get_first(parent_node, descendant_tagname)
    else:
        node = parent_node
    val = ""
    try:
        val = "".join([
            force_text(n.data.strip())
            for n in node.childNodes
            if n.nodeType in (
                Node.TEXT_NODE,
                Node.CDATA_SECTION_NODE,
            )
        ])
    except:
        pass
    # convert quotes to more usual format
    val = val.replace("", "„")
    val = val.replace("", "“")
    return val


def get_child_text(node, tag, **attrs):
    """
    Returns the text from a child node with tag name and attributes

    Example:
    get_child_text(production_node, "Title", Language="de") == u"Nathan der  Weise"

    :param node: XML node which children to scan
    :param tag: the tag name of the children to get
    :param attrs: attributes of the children to match
    :return: text value of the selected child or empty string otherwise
    """
    for child_node in node.getElementsByTagName(tag):
        all_attributes_match = True
        for name, val in attrs.items():
            if child_node.getAttribute(name) != val:
                all_attributes_match = False
                break
        if all_attributes_match:
            return force_unicode(u''.join([t for t in get_value(child_node)])).replace(r'\n', '\n')
    return u''


def date_de_to_en(date_string):
    """
    Replaces all German-specific date values to English specific ones so that
    dates could be parsed by dateutil.parser
    """
    date_string = date_string.replace("Mo,", "Mon,")
    date_string = date_string.replace("Di,", "Tue,")
    date_string = date_string.replace("Mi,", "Wed,")
    date_string = date_string.replace("Do,", "Thu,")
    date_string = date_string.replace("Fr,", "Fri,")
    date_string = date_string.replace("Sa,", "Sat,")
    date_string = date_string.replace("So,", "Sun,")
    date_string = date_string.replace("Mrz", "Mar")
    date_string = date_string.replace("Mär", "Mar")
    date_string = date_string.replace("Mai", "May")
    date_string = date_string.replace("Okt", "Oct")
    date_string = date_string.replace("Dez", "Dec")
    return date_string

