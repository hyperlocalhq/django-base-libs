from django import template

from jetson.apps.faqs.models import FaqCategory

register = template.Library()

class FaqCategoryListNode(template.Node):
    def __init__(
         self, 
         container_id_lookup_var,
         container_id,
         category_id_lookup_var, 
         category_id,
         template_path
     ):
        self.container_id_lookup_var = container_id_lookup_var
        self.container_id = container_id
        self.category_id_lookup_var = category_id_lookup_var
        self.category_id = category_id 
        self.template_path = template_path

    def render(self, context):
        # try to resolve container var name
        if self.container_id_lookup_var is not None:
            try:
                self.container_id = template.resolve_variable(
                     self.container_id_lookup_var, 
                     context
                )
            except template.VariableDoesNotExist:
                return ''
        # try to resolve category var name
        if self.category_id_lookup_var is not None:
            try:
                self.category_id = template.resolve_variable(
                     self.category_id_lookup_var, 
                     context
                )
            except template.VariableDoesNotExist:
                return ''

        # if category id is given, we do not need the container
        if self.category_id:
            try:
                category = FaqCategory.objects.get(id=self.category_id)
            except:
                return ''
            category_list = category.get_children()
        # no category id given, so get the roots of the container
        else:
            try:
                category_list = FaqCategory.objects.get_roots(self.container_id)
            except:
                return ''

        #if self.category_id == 14:
        #    ccc=nnnn
        try:
            template_path = template.resolve_variable(
              self.template_path, 
              context
            )
        except:
            template_path = ""
        
        context_vars = context
        context_vars.push()
        context_vars['categories'] = category_list
        output = template.loader.render_to_string(
            template_path or "faqs/category_children.html",
            context_vars
            )
        context_vars.pop()
        return output

class FaqListNode(template.Node):
    def __init__(
         self, 
         category_id_lookup_var, 
         category_id, var_name
     ):
        self.category_id_lookup_var = category_id_lookup_var
        self.category_id = category_id 
        self.var_name = var_name

    def render(self, context):
        # try to resolve object var name
        if self.category_id_lookup_var is not None:
            try:
                self.category_id = template.resolve_variable(
                     self.category_id_lookup_var, 
                     context
                )
            except template.VariableDoesNotExist:
                return ''

        try:
            category = FaqCategory.objects.get(id=self.category_id)
        except:
            return ''
        
        faq_list = getattr(category, 'get_faqs')()
        context[self.var_name] = faq_list
        return ''

class DoGetFaqCategoryList:
    """
    Gets Children or Descendants of a FaqCategory
    If the id is not specified, the top-level categories will be displayed.
    By default it uses the template faqs/categories.html, 
    but optionally you can set some custom template.

    Syntax::
        {% get_faq_category_children 
            in <context_var_containing_container_id> 
            [for <context_var_containing_category_id>] 
            [using <template_path>] %}

    Example usage::

        {% get_faq_category_children in container.id %}

    Note: ``[context_var_containing_<<whatever>>_id]`` can also be a 
            hard-coded integer, like this::

        {% get_faq_category_children in 1 for 12 %}
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        if not len(tokens) in (3, 5, 7,):
            raise template.TemplateSyntaxError,\
                "%r tag requires 2, 4 or 6 arguments" % tokens[0]
        
        if tokens[1] != 'in':
            raise template.TemplateSyntaxError,\
                 "first argument in %r tag must be 'in'" % tokens[0]
        
        container_var_name, container_id = None, None
        category_var_name, category_id = None, None
        template_path = None            
            
        if tokens[2].isdigit():
            container_id = tokens[2]
        else:
            container_var_name = tokens[2]

        if len(tokens) > 3:
            if tokens[3] == 'for':
                if tokens[4].isdigit():
                    category_id = tokens[4]
                else:
                    category_var_name = tokens[4]
                
                if len(tokens) > 5:
                    if tokens[5] == 'using':
                        template_path = tokens[6]
                    else:
                        raise template.TemplateSyntaxError,\
                            "fifth argument in %r tag must be 'for or 'using'" % tokens[0]
                
            elif tokens[3] == 'using':
                template_path = tokens[4]
            else:
                raise template.TemplateSyntaxError,\
                     "third argument in %r tag must be 'for or 'using'" % tokens[0]

        return FaqCategoryListNode(
           container_var_name,
           container_id,
           category_var_name, 
           category_id,
           template_path)

class DoGetFaqList:
    """
    Gets Faqs under a Faq category

    Syntax::
        {% get_faqs for [context_var_containing_category_id] as [varname] %}

    Example usage::

        {% get_faqs for category.id as faqs %}

    Note: ``[context_var_containing_category_id]`` can also be a 
            hard-coded integer, like this::

        {% get_faqs for 12 as faqs %}
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        if not len(tokens) in (5,):
            raise template.TemplateSyntaxError, "%r tag requires 4 arguments" % tokens[0]
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError, "Second argument in %r tag must be 'for'" % tokens[0]
        
        if tokens[1] == 'for':
            category_var_name, category_id = None, None
            
            if tokens[2].isdigit():
                category_id = tokens[2]
            else:
                category_var_name = tokens[2]
                    
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError, "Third argument in %r must be 'as'" % tokens[0]
                
            return FaqListNode(
                     category_var_name, 
                     category_id, 
                     tokens[4]
             )
            
            
register.tag('get_faq_category_children', DoGetFaqCategoryList())
register.tag('get_faqs', DoGetFaqList())
