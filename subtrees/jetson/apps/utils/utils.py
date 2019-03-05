# -*- coding: UTF-8 -*-

import re
import subprocess
import datetime


def get_media_svn_revision(media_root, prefix="", postfix=""):
    repo_dir = media_root
    svn_revision = subprocess.Popen(
        'svn info | grep "Revision" | awk \'{print $2}\'',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=repo_dir,
        universal_newlines=True
    )
    rev = svn_revision.communicate()[0].partition('\n')[0]
    if rev:
        rev = "".join((prefix, rev, postfix))
    return rev


def get_git_changeset(media_root, prefix="", postfix=""):
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = media_root  # os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_show = subprocess.Popen(
        'git show --pretty=format:%ct --quiet HEAD',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=repo_dir,
        universal_newlines=True
    )
    timestamp = git_show.communicate()[0].partition('\n')[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return "".join((prefix, "0", postfix))
    changeset = timestamp.strftime('%Y%m%d%H%M%S')
    if changeset:
        changeset = "".join((prefix, changeset, postfix))
    return changeset


def any(S):
    for x in S:
        if x:
            return True
    return False


def all(S):
    for x in S:
        if not x:
            return False
    return True


def custom_show_toolbar(request):
    return "1" == request.COOKIES.get("DjDT", False)
