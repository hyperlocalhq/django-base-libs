# -*- coding: UTF-8 -*-
import os, fnmatch


def path_exists(*args):
    path = os.path.join(*args)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def locate(pattern, root=os.curdir):
    """Locate all files matching supplied filename pattern in and below
    supplied root directory."""
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)
