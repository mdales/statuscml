# found in http://code.djangoproject.com/wiki/ExprTag
# 
# version: 0.2
# author: limodou@gmail.com

from django import template
from django.utils.translation import gettext_lazy as _
import re

register = template.Library()

class ExprNode(template.Node):
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name
    
    def render(self, context):
        clist = list(context)
        clist.reverse()
        d = {}
        d['_'] = _
        for c in clist:
            d.update(c)
        if self.var_name:
            context[self.var_name] = eval(self.expr_string, d)
            return ''
        else:
            return str(eval(self.expr_string, d))

def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    expr_string, var_name = m.groups()
    return ExprNode(expr_string, var_name)
do_expr = register.tag('expr', do_expr)
