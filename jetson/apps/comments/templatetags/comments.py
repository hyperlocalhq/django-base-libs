import re

from django import template
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from base_libs.middleware import get_current_user
from base_libs.forms.fields import SecurityField

from jetson.apps.comments.models import Comment
from jetson.apps.comments.models import PHOTOS_REQUIRED, PHOTOS_OPTIONAL, RATINGS_REQUIRED, RATINGS_OPTIONAL, IS_PUBLIC
from jetson.apps.comments.models import MIN_PHOTO_DIMENSION, MAX_PHOTO_DIMENSION
from jetson.apps.comments.views.comments import PublicCommentForm

register = template.Library()

COMMENT_FORM = 'form.html'

class CommentFormNode(template.Node):
    def __init__(self, template_dir_lookup_var, content_type_lookup_var, content_type, obj_id_lookup_var, obj_id, 
        photos_optional=False, photos_required=False, photo_options='',
        ratings_optional=False, ratings_required=False, rating_options='',
        is_public=True):
        
        self.content_type_lookup_var, self.content_type = content_type_lookup_var, content_type
        self.obj_id_lookup_var, self.obj_id = obj_id_lookup_var, obj_id 
        self.template_dir_lookup_var = template_dir_lookup_var
        self.photos_optional, self.photos_required = photos_optional, photos_required
        self.ratings_optional, self.ratings_required = ratings_optional, ratings_required
        self.photo_options, self.rating_options = photo_options, rating_options
        self.is_public = is_public
        self.template_path = COMMENT_FORM
            
    def render(self, context):
        #from django.conf import settings
        from django.utils.text import normalize_newlines
        import base64
        context.push()
        
        """ try to resolve template_dir var name:
        The "using" part can have the following form (example):
        {% comment_form using template_dir+"comments/form.html" for people.person object.id %}
        {% comment_form using "comments/form.html" for people.person object.id %}
        """
        if self.template_dir_lookup_var is not None:
            parts = self.template_dir_lookup_var.split('+')
            parsed_parts = []
            for part in parts:
                try:
                    parsed_parts.append(
                        template.resolve_variable(part, context)
                        )
                except:
                    pass
            self.template_path = "".join(parsed_parts)
        
        # try to resolve content_type var name 
        if self.content_type_lookup_var is not None:
            try:
                ct_string = template.resolve_variable(self.content_type_lookup_var, context)
                package, module = ct_string.split('.')
                ct = ContentType.objects.get(
                    app_label__exact=package,
                    model__exact=module,
                    )
                self.content_type = ct
            except:
                return ''
        
        # try to resolve object var name
        if self.obj_id_lookup_var is not None:
            try:
                self.obj_id = template.resolve_variable(self.obj_id_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''
            # Validate that this object ID is valid for this content-type.
            # We only have to do this validation if obj_id_lookup_var is provided,
            # because do_comment_form() validates hard-coded object IDs.
            try:
                self.content_type.get_object_for_this_type(pk=self.obj_id)
            except ObjectDoesNotExist:
                context['display_form'] = False
            else:
                context['display_form'] = True
        else:
            context['display_form'] = True
            
        context['target'] = '%s:%s' % (self.content_type.id, self.obj_id)
        options = []
        for var, abbr in (('photos_required', PHOTOS_REQUIRED),
                          ('photos_optional', PHOTOS_OPTIONAL),
                          ('ratings_required', RATINGS_REQUIRED),
                          ('ratings_optional', RATINGS_OPTIONAL),
                          ('is_public', IS_PUBLIC)):
            context[var] = getattr(self, var)
            if getattr(self, var):
                options.append(abbr)
        context['options'] = ','.join(options)
        context['photo_options'] = self.photo_options
        context['rating_options'] = normalize_newlines(base64.encodestring(self.rating_options).strip())
        if self.rating_options:
            context['rating_range'], context['rating_choices'] = Comment.objects.get_rating_options(self.rating_options)
        context['hash'] = Comment.objects.get_security_hash(context['options'], context['photo_options'], context['rating_options'], context['target'])
        context['logout_url'] = settings.LOGOUT_URL
        comment_form = PublicCommentForm(user=get_current_user() or None)

        # we need to initialize the prevent spam field here, because "SecurityField" only works for unbound forms        
        security_field = SecurityField()
        comment_form.fields['prevent_spam'].initial = security_field.generate_value()

        context['comment_form'] = comment_form

        default_form = loader.get_template(self.template_path)
        output = default_form.render(context)
        context.pop()
        return output

class CommentCountNode(template.Node):
    def __init__(self, package, module, context_var_name, obj_id, var_name):
        self.package, self.module = package, module
        self.context_var_name, self.obj_id = context_var_name, obj_id
        self.var_name = var_name

    def render(self, context):
        #from django.conf import settings
        manager = Comment.objects
        if self.context_var_name is not None:
            self.obj_id = template.resolve_variable(self.context_var_name, context)
        comment_count = manager.filter(object_id__exact=self.obj_id,
            content_type__app_label__exact=self.package,
            content_type__model__exact=self.module, site__id__exact=settings.SITE_ID, is_spam=False).count()
        context[self.var_name] = comment_count
        return ''

class CommentLatestNode(template.Node):
    def __init__(self, package, module, context_var_name, obj_id, var_name):
        self.package, self.module = package, module
        self.context_var_name, self.obj_id = context_var_name, obj_id
        self.var_name = var_name

    def render(self, context):
        #from django.conf import settings
        manager = Comment.objects
        if self.context_var_name is not None:
            self.obj_id = template.resolve_variable(self.context_var_name, context)
        comment_latest = manager.filter(object_id__exact=self.obj_id,
            content_type__app_label__exact=self.package,
            content_type__model__exact=self.module, site__id__exact=settings.SITE_ID, is_spam=False).latest('submit_date')
        context[self.var_name] = comment_latest
        return ''

class CommentListNode(template.Node):
    def __init__(self, package, module, context_var_name, obj_id, var_name, sort_order, extra_kwargs=None):
        self.package, self.module = package, module
        self.context_var_name, self.obj_id = context_var_name, obj_id
        self.var_name = var_name
        self.sort_order = sort_order
        self.extra_kwargs = extra_kwargs or {}

    def render(self, context):
        #from django.conf import settings
        get_list_function = Comment.objects.get_list_with_karma
        if self.context_var_name is not None:
            try:
                self.obj_id = template.resolve_variable(self.context_var_name, context)
            except template.VariableDoesNotExist:
                return ''
        kwargs = {
            'object_id__exact': self.obj_id,
            'content_type__app_label__exact': self.package,
            'content_type__model__exact': self.module,
            'site__id__exact': settings.SITE_ID,
        }
        kwargs.update(self.extra_kwargs)
        if settings.COMMENTS_BANNED_USERS_GROUP:
            kwargs['select'] = {'is_hidden': 'user_id IN (SELECT user_id FROM auth_user_groups WHERE group_id = %s)' % settings.COMMENTS_BANNED_USERS_GROUP}
        comment_list = get_list_function(**kwargs).order_by(self.sort_order + 'submit_date').select_related()
        
        if 'user' in context and context['user'].is_authenticated():
            user_id = context['user'].id
            context['user_can_moderate_comments'] = Comment.objects.user_is_moderator(context['user'])
        else:
            user_id = None
            context['user_can_moderate_comments'] = False
        # Only display comments by banned users to those users themselves.
        if settings.COMMENTS_BANNED_USERS_GROUP:
            comment_list = [c for c in comment_list if not c.is_hidden or (user_id == c.user_id)]

        context[self.var_name] = comment_list
        return ''

class DoCommentForm:
    """
    Displays a comment form for the given params.

    Syntax::

        {% comment_form [using <template_path>] for [pkg].[py_module_name] [context_var_containing_obj_id] with [list of options] %}

    Example usage::

        {% comment_form for lcom.eventtimes event.id with is_public yes photos_optional thumbs,200,400 ratings_optional scale:1-5|first_option|second_option %}

    ``[context_var_containing_obj_id]`` can be a hard-coded integer or a variable containing the ID.
    """
    def __init__(self):
        pass
    
    def __call__(self, parser, token):
        kwargs = {}
        tokens = token.contents.split()
        if len(tokens) < 4:
            raise template.TemplateSyntaxError, "%r tag requires at least 3 arguments" % tokens[0]
        token_index = 1
        
        template_dir_lookup_var = None
        if tokens[1] == 'using':
            token_index = 3;
            template_dir_lookup_var = tokens[2]
        
        if tokens[token_index] != 'for':
            raise template.TemplateSyntaxError, "Argument %d in %r tag must be 'for'" % (token_index + 1, tokens[0])
        
        # ok, maybe the content_type is in the form [pkg].[py_module_name] 
        # or it is a context variable name!!!
        content_type_lookup_var, content_type = None, None
        try:
            package, module = tokens[token_index+1].split('.')
            content_type = ContentType.objects.get(
                app_label__exact=package,
                model__exact=module,
                )
        except ValueError: 
            content_type_lookup_var = tokens[token_index+1]
            content_type = None
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError, "%r tag has invalid content-type '%s.%s'" % (tokens[0], package, module)
        
        obj_id_lookup_var, obj_id = None, None
        if tokens[token_index + 2].isdigit():
            obj_id = tokens[token_index + 2]
            try: # ensure the object ID is valid
                content_type.get_object_for_this_type(pk=obj_id)
            except ObjectDoesNotExist:
                raise template.TemplateSyntaxError, "%r tag refers to %s object with ID %s, which doesn't exist" % (tokens[0], content_type.name, obj_id)
        else:
            obj_id_lookup_var = tokens[token_index + 2]
        
        if (tokens[1] == 'using' and len(tokens) > 6) or (tokens[1] != 'using' and len(tokens) > 4):
            if tokens[token_index + 3] != 'with':
                raise template.TemplateSyntaxError, "Fourth argument in %r tag must be 'with'" % tokens[0]
            for option, args in zip(tokens[token_index + 4::2], tokens[token_index + 5::2]):
                if option in ('photos_optional', 'photos_required'):
                    # VALIDATION ##############################################
                    option_list = args.split(',')
                    if len(option_list) % 3 != 0:
                        raise template.TemplateSyntaxError, "Incorrect number of comma-separated arguments to %r tag" % tokens[0]
                    for opt in option_list[::3]:
                        if not opt.isalnum():
                            raise template.TemplateSyntaxError, "Invalid photo directory name in %r tag: '%s'" % (tokens[0], opt)
                    for opt in option_list[1::3] + option_list[2::3]:
                        if not opt.isdigit() or not (MIN_PHOTO_DIMENSION <= int(opt) <= MAX_PHOTO_DIMENSION):
                            raise template.TemplateSyntaxError, "Invalid photo dimension in %r tag: '%s'. Only values between %s and %s are allowed." % (tokens[0], opt, MIN_PHOTO_DIMENSION, MAX_PHOTO_DIMENSION)
                    # VALIDATION ENDS #########################################
                    kwargs[option] = True
                    kwargs['photo_options'] = args
                elif option in ('ratings_optional', 'ratings_required'):
                    # VALIDATION ##############################################
                    if 2 < len(args.split('|')) > 9:
                        raise template.TemplateSyntaxError, "Incorrect number of '%s' options in %r tag. Use between 2 and 8." % (option, tokens[0])
                    if re.match('^scale:\d+\-\d+\:$', args.split('|')[0]):
                        raise template.TemplateSyntaxError, "Invalid 'scale' in %r tag's '%s' options" % (tokens[0], option)
                    # VALIDATION ENDS #########################################
                    kwargs[option] = True
                    kwargs['rating_options'] = args
                elif option in ('is_public'):
                    kwargs[option] = (args == 'true')
                else:
                    raise template.TemplateSyntaxError, "%r tag got invalid parameter '%s'" % (tokens[0], option)
        return CommentFormNode(template_dir_lookup_var, content_type_lookup_var, content_type, obj_id_lookup_var, obj_id, **kwargs)

class DoCommentCount:
    """
    Gets comment count for the given params and populates the template context
    with a variable containing that value, whose name is defined by the 'as'
    clause.

    Syntax::

        {% get_comment_count for [pkg].[py_module_name] [context_var_containing_obj_id] as [varname]  %}

    Example usage::

        {% get_comment_count for lcom.eventtimes event.id as comment_count %}

    Note: ``[context_var_containing_obj_id]`` can also be a hard-coded integer, like this::

        {% get_comment_count for lcom.eventtimes 23 as comment_count %}
    """
    def __init__(self):
        pass

    def __call__(self, parser, token):
        tokens = token.contents.split()
        # Now tokens is a list like this:
        # ['get_comment_list', 'for', 'lcom.eventtimes', 'event.id', 'as', 'comment_list']
        if len(tokens) != 6:
            raise template.TemplateSyntaxError, "%r tag requires 5 arguments" % tokens[0]
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[0]
        try:
            package, module = tokens[2].split('.')
        except ValueError: # unpack list of wrong size
            raise template.TemplateSyntaxError, "Third argument in %r tag must be in the format 'package.module'" % tokens[0]
        try:
            content_type = ContentType.objects.get(
                app_label__exact=package,
                model__exact=module,
                )
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError, "%r tag has invalid content-type '%s.%s'" % (tokens[0], package, module)
        var_name, obj_id = None, None
        if tokens[3].isdigit():
            obj_id = tokens[3]
            try: # ensure the object ID is valid
                content_type.get_object_for_this_type(pk=obj_id)
            except ObjectDoesNotExist:
                raise template.TemplateSyntaxError, "%r tag refers to %s object with ID %s, which doesn't exist" % (tokens[0], content_type.name, obj_id)
        else:
            var_name = tokens[3]
        if tokens[4] != 'as':
            raise template.TemplateSyntaxError, "Fourth argument in %r must be 'as'" % tokens[0]
        return CommentCountNode(package, module, var_name, obj_id, tokens[5])

class DoGetCommentLatest:
    """
    Gets latest comment for the given params and populates the template context
    with a variable containing that value, whose name is defined by the 'as'
    clause.

    Syntax::

        {% get_comment_latest for [pkg].[py_module_name] [context_var_containing_obj_id] as [varname]  %}

    Example usage::

        {% get_comment_latest for lcom.eventtimes event.id as comment_count %}

    Note: ``[context_var_containing_obj_id]`` can also be a hard-coded integer, like this::

        {% get_comment_latest for lcom.eventtimes 23 as comment_count %}
    """
    def __init__(self):
        pass

    def __call__(self, parser, token):
        tokens = token.contents.split()
        # Now tokens is a list like this:
        # ['get_comment_latest', 'for', 'lcom.eventtimes', 'event.id', 'as', 'comment_list']
        if len(tokens) != 6:
            raise template.TemplateSyntaxError, "%r tag requires 5 arguments" % tokens[0]
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[0]
        try:
            package, module = tokens[2].split('.')
        except ValueError: # unpack list of wrong size
            raise template.TemplateSyntaxError, "Third argument in %r tag must be in the format 'package.module'" % tokens[0]
        try:
            content_type = ContentType.objects.get(
                app_label__exact=package,
                model__exact=module,
                )
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError, "%r tag has invalid content-type '%s.%s'" % (tokens[0], package, module)
        var_name, obj_id = None, None
        if tokens[3].isdigit():
            obj_id = tokens[3]
            try: # ensure the object ID is valid
                content_type.get_object_for_this_type(pk=obj_id)
            except ObjectDoesNotExist:
                raise template.TemplateSyntaxError, "%r tag refers to %s object with ID %s, which doesn't exist" % (tokens[0], content_type.name, obj_id)
        else:
            var_name = tokens[3]
        if tokens[4] != 'as':
            raise template.TemplateSyntaxError, "Fourth argument in %r must be 'as'" % tokens[0]
        return CommentLatestNode(package, module, var_name, obj_id, tokens[5])

class DoGetCommentList:
    """
    Gets comments for the given params and populates the template context with a
    special comment_package variable, whose name is defined by the ``as``
    clause.

    Syntax::

        {% get_comment_list for [pkg].[py_module_name] [context_var_containing_obj_id] as [varname] (reversed) %}

    Example usage::

        {% get_comment_list for lcom.eventtimes event.id as comment_list %}

    Note: ``[context_var_containing_obj_id]`` can also be a hard-coded integer, like this::

        {% get_comment_list for lcom.eventtimes 23 as comment_list %}

    To get a list of comments in reverse order -- that is, most recent first --
    pass ``reversed`` as the last param::

        {% get_comment_list for lcom.eventtimes event.id as comment_list reversed %}
    """
    def __init__(self):
        pass

    def __call__(self, parser, token):
        tokens = token.contents.split()
        # Now tokens is a list like this:
        # ['get_comment_list', 'for', 'lcom.eventtimes', 'event.id', 'as', 'comment_list']
        if not len(tokens) in (6, 7):
            raise template.TemplateSyntaxError, "%r tag requires 5 or 6 arguments" % tokens[0]
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[0]
        try:
            package, module = tokens[2].split('.')
        except ValueError: # unpack list of wrong size
            raise template.TemplateSyntaxError, "Third argument in %r tag must be in the format 'package.module'" % tokens[0]
        try:
            content_type = ContentType.objects.get(
                app_label__exact=package,
                model__exact=module,
                )
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError, "%r tag has invalid content-type '%s.%s'" % (tokens[0], package, module)
        var_name, obj_id = None, None
        if tokens[3].isdigit():
            obj_id = tokens[3]
            try: # ensure the object ID is valid
                content_type.get_object_for_this_type(pk=obj_id)
            except ObjectDoesNotExist:
                raise template.TemplateSyntaxError, "%r tag refers to %s object with ID %s, which doesn't exist" % (tokens[0], content_type.name, obj_id)
        else:
            var_name = tokens[3]
        if tokens[4] != 'as':
            raise template.TemplateSyntaxError, "Fourth argument in %r must be 'as'" % tokens[0]
        if len(tokens) == 7:
            if tokens[6] != 'reversed':
                raise template.TemplateSyntaxError, "Final argument in %r must be 'reversed' if given" % tokens[0]
            sort_order = "-"
        else:
            sort_order = ""
        return CommentListNode(package, module, var_name, obj_id, tokens[5], sort_order)

# registration comments
register.tag('get_comment_list', DoGetCommentList())
register.tag('get_comment_latest', DoGetCommentLatest())
register.tag('comment_form', DoCommentForm())
register.tag('get_comment_count', DoCommentCount())
