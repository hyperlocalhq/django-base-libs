# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from models import MenuBlock


@cache_page(60 * 15)  # cache the mega drop-down menu for 15 minutes
def mega_drop_down_menu(request):
    menu_blocks = dict(
        [
            (el.sysname, el)
            for el in MenuBlock.objects.filter(language=request.LANGUAGE_CODE)
        ]
    )
    return render(
        request, "mega_menu/mega_drop_down_menu.html",
        {'menu_blocks': menu_blocks}
    )
