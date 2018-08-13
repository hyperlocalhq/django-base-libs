# -*- coding: UTF-8 -*-
import os
import re

from django import template
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from filebrowser.base import FileObject

image_mods = models.get_app("image_mods")

register = template.Library()

### TAGS ###

@register.simple_tag
def cropping_url(path_or_file_object, sysname, request, goto_next):
    """ 
    Returns recropping URL for the user
    
    Usage:
        <a href="{% cropping_url <path> <modification_sysname> <request> <goto_next> %}">
            Adjust Image
        </a>
        or 
        <a href="{% cropping_url <file_object> <modification_sysname> <request> <goto_next> %}">
            Adjust Image
        </a>
        
    Example:
        <a href="{% cropping_url "test/original.png" "gallery_default" request request.path %}">
            Adjust Image
        </a>
        <a href="{% cropping_url person.avatar "gallery_default" request request.path %}">
            Adjust Image
        </a>
        
    """
    if not request.user.is_authenticated():
        return ""
    if isinstance(path_or_file_object, FileObject):
        path = path_or_file_object.path
    else:
        path = path_or_file_object
    return reverse("image_mods_recrop") + "?orig_path=%(orig_path)s&sysname=%(sysname)s&token=%(token)s&goto_next=%(goto_next)s" % {
        'orig_path': path,
        'sysname': sysname,
        'token': image_mods.FileManager.tokenize(request.user.username, path),
        'goto_next': goto_next,
        }


### FILTERS ### 

def modified_path(path_or_file_object, sysname):
    """ 
    Returns the relative filebrowser path to the modified image.
    If the modified image does not exist, it will be created
    
    Usage:
        {{ <path>|modified_path:<modification_sysname> }}
        or 
        {{ <file_object>|modified_path:<modification_sysname> }}
        
    Example:
        {{ "test/original.png"|modified_path:"gallery_default" }}
        {{ person.avatar|modified_path:"gallery_default" }}
        
    """
    if isinstance(path_or_file_object, FileObject):
        path = path_or_file_object.path
    else:
        path = path_or_file_object
    path, query_params = image_mods.FileManager.modified_path(path, sysname)
    return path + query_params

register.filter('modified_path', modified_path)

def mod_exists(path_or_file_object, sysname):
    """ 
    Returns True if relative filebrowser path to the modified image exists,
    or else False.
    
    Usage:
        {% if <path>|mod_exists:<modification_sysname> %}OK{% endif %}
        or 
        {% if <file_object>|mod_exists:<modification_sysname> %}OK{% endif %}
        
    Example:
        {% if "test/original.png"|mod_exists:"gallery_default" %}OK{% endif %}
        {% if person.avatar|mod_exists:"gallery_default" %}OK{% endif %}
        
    """
    if isinstance(path_or_file_object, FileObject):
        path = path_or_file_object.path
    else:
        path = path_or_file_object
    return image_mods.FileManager.mod_exists(path, sysname)

register.filter('mod_exists', mod_exists)

def modified_image(path_or_file_object, sysname):
    """ 
    Returns the FileObject of the modified image.
    
    Usage:
        {% with <path>|modified_image:<modification_sysname> as image %}
            ...
        {% endwith %}
        or 
        {% with <file_object>|modified_image:<modification_sysname> as image %}
            ...
        {% endwith %}
        
    Example:
        {% with "test/original.png"|modified_image:"gallery_default" as image %}
            Filesize: {{ image.filesize|filesizeformat }}
        {% endwith %}
        {% with person.avatar|modified_image:"gallery_default" as image %}
            Filesize: {{ image.filesize|filesizeformat }}
        {% endwith %}
        
    """
    if not mod_exists(path_or_file_object, sysname):
        return None
    if isinstance(path_or_file_object, FileObject):
        path = path_or_file_object.path
    else:
        path = path_or_file_object
    path, query_params = image_mods.FileManager.modified_path(path, sysname)
    if not path:
        return None
    if path.startswith("/"):
        path = path[1:]
    return FileObject(path)
    
register.filter('modified_image', modified_image)
