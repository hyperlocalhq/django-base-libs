# -*- coding: UTF-8 -*-
import re
from django import template

register = template.Library()

### FILTERS ###


@register.filter()
def remove_copyright_label(text):
    from ..functions import remove_copyright_label as _remove_copyright_label
    return _remove_copyright_label(text)


### TAGS ###


class EncryptEmail(template.Node):
    def __init__(self, context_var, letter_count=254):
        self.context_var = template.Variable(context_var)
        self.letter_count = template.Variable(letter_count)

    def render(self, context):
        import random
        email_address = self.context_var.resolve(context)
        letter_count = self.letter_count.resolve(context)
        character_set = '+-.0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
        char_list = list(character_set)
        random.shuffle(char_list)

        key = ''.join(char_list)

        cipher_text = ''
        id = 'e' + str(random.randrange(1, 999999999))

        for a in email_address:
            cipher_text += key[character_set.find(a)]

        script = u'var a="' + key + '";var b=a.split("").sort().join("");var c="' + cipher_text + '";var d="";'
        script += u'for(var e=0;e<c.length;e++)d+=b.charAt(a.indexOf(c.charAt(e)));'
        if len(email_address) > letter_count:
            script += u'document.getElementById("' + id + '").innerHTML="<a href=\\"mailto:"+d+"\\">"+d.slice(0,' + unicode(
                letter_count - 1
            ) + u')+"…</a>";'
        else:
            script += u'document.getElementById("' + id + '").innerHTML="<a href=\\"mailto:"+d+"\\">"+d+"</a>";'

        script = u"eval(\"" + script.replace("\\", "\\\\"
                                            ).replace('"', '\\"') + u"\")"
        script = u'<script type="text/javascript">/*<![CDATA[*/' + script + u'/*]]>*/</script>'

        return u'<span id="' + id + u'">[javascript protected email address]</span>' + script


def encrypt_email(parser, token):
    """
        {% encrypt_email user.email 25 %}
    """

    tokens = dict(enumerate(token.contents.split()))
    if len(tokens) > 3:
        raise template.TemplateSyntaxError(
            "%r tag accepts one or two arguments" % tokens[0]
        )
    return EncryptEmail(tokens[1], tokens.get(2, "254"))


register.tag('encrypt_email', encrypt_email)
