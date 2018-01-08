# -*- coding: UTF-8 -*-
from django.conf import settings

from apps.bulletin_board.models import URL_ID_BULLETIN_BOARD

def bulletin_board(request=None):
    d = {
        'URL_ID_BULLETIN_BOARD': URL_ID_BULLETIN_BOARD,
        }
    return d

