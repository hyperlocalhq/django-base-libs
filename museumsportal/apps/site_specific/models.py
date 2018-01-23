# -*- coding: UTF-8 -*-

def patch_filebrowser():
    from django.conf import settings
    from django.utils.translation import ugettext_lazy as _
    from filebrowser.models import FileDescription
    
    FileDescription._meta.get_field('copyright_limitations').verbose_name = _('Details of any restrictions on use (time limit) for the disclosure to third parties (Cinemarketing, Berlin online, etc.)')
    FileDescription._meta.get_field('copyright_limitations').help_text = _('If this field does not contain precise restrictions or if no restrictions are set, the rights of use are granted non-exclusively, and unrestricted in terms of time, place and content.')

    for lang_code, lang_name in settings.LANGUAGES: 
        FileDescription._meta.get_field('title_%s' % lang_code).verbose_name = _('Caption')
        FileDescription._meta.get_field('description_%s' % lang_code).verbose_name = _('Description (will be used as alt attribute)')

patch_filebrowser()
