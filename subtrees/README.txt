It is more convenient to use a remote origin for each of the repos that was added to the project with git subtree. To add these origins, just do:

$ git remote add base_libs_origin https://github.com/archatas/django-base-libs

$ git remote add filebrowser_origin https://github.com/archatas/django-filebrowser

$ git remote add jetson_origin https://bitbucket.org/jetson/jetson
# Use the django_1_7 branch

$ git remote add tagging_origin https://github.com/archatas/django-tagging

$ git remote add tagging_autocomplete_origin https://github.com/archatas/django-tagging-autocomplete
