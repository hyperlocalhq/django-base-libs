from django import template
from django.template import loader
from django.conf import settings

register = template.Library()

def if_has_perm(parser, token):
    """
    TODO: Update document

    Checks permission on the given user. Checks row-level permissions if an
    object is given.

    Perm name should be in the format [app_label].[perm codename].
    """
    bits = token.contents.split()
    tag = bits[0]
    del bits[0]
    if not bits:
        raise template.TemplateSyntaxError, "'if_has_perm' statement requires at least one argument"
    # bits now looks something like this: ['a', 'or', 'not', 'b', 'or', 'c.d']
    bitstr = ' '.join(bits)
    boolpairs = bitstr.split(' and ')
    permtuples = []
    if len(boolpairs) == 1:
        link_type = 1
        boolpairs = bitstr.split(' or ')
    else:
        link_type = 0
        if ' or ' in bitstr:
            raise template.TemplateSyntaxError, "'if_has_perm' tags can't mix 'and' and 'or'"
    for boolpair in boolpairs:
        tokens = boolpair.split()
        object_var = None
        not_flag = False
        if tokens[0] == "not":
            not_flag = True
            permission = tokens[1]
            if len(tokens) > 2:
                object_var = parser.compile_filter(tokens[2])
        else:
            permission = tokens[0]
            if len(tokens) > 1:
                object_var = parser.compile_filter(tokens[1])
    
        #if not (permission[0] == permission[-1] and permission[0] in ('"', "'")):
        #    raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tokens[0]

        #permtuples.append((not_flag, permission[1:-1], object_var))
        permtuples.append((not_flag, permission, object_var))
        '''
        try:
            not_, permission, object_var = boolpair.split()
            if not_ != 'not':
                raise template.TemplateSyntaxError, "Expected 'not' in if_has_perm statement"
            
            if not (permission[0] == permission[-1] and permission[0] in ('"', "'")):
                raise template.template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tokens[0]
            
            permtuples.append((True, permission[1:-1], parser.compile_filter(object_var)))

        except ValueError:
            try:
                permission, object_var = boolpair.split()
            except ValueError:
                raise template.TemplateSyntaxError, "'if_has_perm' statement improperly formatted"

            if not (permission[0] == permission[-1] and permission[0] in ('"', "'")):
                raise template.template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tokens[0]

            permtuples.append((False, permission[1:-1], parser.compile_filter(object_var)))
        '''
    nodelist_true = parser.parse(('else', 'end_'+tag,))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end_'+tag,))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    result = None
    for item in permtuples:
        has_perm = HasPermNode(item[1], item[0], item[2], nodelist_true, nodelist_false)
        
        if result is None:
            result = has_perm
        else:
            if link_type == 1:
                result = result and has_perm
            else:
                result = result or has_perm
    return result

class HasPermNode(template.Node):
    def __init__(self, permission, not_flag, object_var, nodelist_true, nodelist_false):
        self.permission = permission
        self.not_flag = not_flag
        self.object_var = object_var
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<HasPerm node>"

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def get_nodes_by_type(self, nodetype):
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        nodes.extend(self.nodelist_true.get_nodes_by_type(nodetype))
        nodes.extend(self.nodelist_false.get_nodes_by_type(nodetype))
        return nodes

    def render(self, context):
        if self.object_var:
            try:
                obj = self.object_var.resolve(context)
            except template.VariableDoesNotExist:
                obj = None
        else:
            obj=None
        permission = template.resolve_variable(self.permission, context)
        try:
            user = template.resolve_variable("user", context)
        except template.VariableDoesNotExist:
            return settings.TEMPLATE_STRING_IF_INVALID

        bool_perm = user.has_perm(permission, obj=obj)
        if (self.not_flag and not bool_perm) or (not self.not_flag and bool_perm):
            return self.nodelist_true.render(context)
        if (self.not_flag and bool_perm) or (not self.not_flag and not bool_perm):
            return self.nodelist_false.render(context)
        return ''

register.tag('if_has_perm', if_has_perm)
