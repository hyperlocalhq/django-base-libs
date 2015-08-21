# As of version 3.5.3, most functions are now in base and sites ... remaining functions are in utils.py
# This file will be removed with version 3.6
import os

# filebrowser imports
from filebrowser.settings import *

def path_strip(path, root):
    if not path or not root:
        return path
    path = os.path.normcase(path)
    root = os.path.normcase(root)
    if path.startswith(root):
        return path[len(root):]
    return path


def get_version_path(value, version_prefix, site=None):
    """
    Construct the PATH to an Image version.
    value has to be a path relative to the location of
    the site's storage.

    version_filename = filename + version_prefix + ext
    Returns a relative path to the location of the site's storage.
    """

    if site.storage.isfile(value):
        path, filename = os.path.split(value)
        relative_path = path_strip(os.path.join(path,''), site.directory)
        filename, ext = os.path.splitext(filename)
        version_filename = filename + "_" + version_prefix + ext
        if VERSIONS_BASEDIR:
            return os.path.join(VERSIONS_BASEDIR, relative_path, version_filename)
        else:
            return os.path.join(site.directory, relative_path, version_filename)
    else:
        return None

