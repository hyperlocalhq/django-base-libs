# -*- coding: UTF-8 -*-
import re
import subprocess
import datetime


def get_media_svn_revision(media_root, prefix="", postfix=""):
    from django.utils.version import get_svn_revision
    rev = get_svn_revision(media_root) # "SVN-1234" or "SVN-unknown"
    rev = re.sub(r"[^0-9]+", "", rev) # "1234" or ""
    if rev:
        rev = "".join((prefix, rev, postfix))
    return rev


def get_git_changeset(media_root, prefix="", postfix=""):
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = media_root # os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_show = subprocess.Popen('git show --pretty=format:%ct --quiet HEAD',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=repo_dir, universal_newlines=True)
    timestamp = git_show.communicate()[0].partition('\n')[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
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
