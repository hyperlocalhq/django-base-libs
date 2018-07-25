# -*- coding: UTF-8 -*-

"""
ANSI escape codes
http://en.wikipedia.org/wiki/ANSI_escape_code
"""


EFFECTS = {
    'reset': "\x1b[0m",
    'gray': "\033[1;30m",
    'red': "\033[1;31m",
    'green': "\033[1;32m",
    'yellow': "\033[1;33m",
    'blue': "\033[1;34m",
    'magenta': "\033[1;35m",
    'cyan': "\033[1;36m",
    'white': "\033[1;37m",
    'crimson': "\033[1;38m",
    'bg_red': "\033[1;41m",
    'bg_green': "\033[1;42m",
    'bg_brown': "\033[1;43m",
    'bg_blue': "\033[1;44m",
    'bg_magenta': "\033[1;45m",
    'bg_cyan': "\033[1;46m",
    'bg_gray': "\033[1;47m",
    'bg_crimson': "\033[1;48m",
    'bold': "\x1b[1m",
    'not_bold': "\x1b[22m",
    'italic': "\x1b[23m",
    'not_italic': "\x1b[23m",
    'underline': "\x1b[4m",
    'not_underline': "\x1b[24m",
    'strikethrough': "\x1b[9m",
    'not_strikethrough': "\x1b[29m",
    'inverse': "\x1b[7m",
    'not_inverse': "\x1b[27m",
    }

def colored(text, color):
    return "".join((EFFECTS[color], str(text), EFFECTS['reset']))
    
def bold(text):
    return "".join((EFFECTS['bold'], str(text), EFFECTS['not_bold']))
    
def italic(text):
    return "".join((EFFECTS['italic'], str(text), EFFECTS['not_italic']))

def underlined(text):
    return "".join((EFFECTS['underline'], str(text), EFFECTS['not_underline']))

def strikedthrough(text):
    return "".join((EFFECTS['strikethrough'], str(text), EFFECTS['not_strikethrough']))

def inversed(text):
    return "".join((EFFECTS['inverse'], str(text), EFFECTS['not_inverse']))


