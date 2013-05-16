# -*- coding: utf-8 -*-
from django.template import Library, Node, TemplateSyntaxError, Template, \
                            Variable, Context

register = Library()


@register.tag
def render_formset(parser, token):
    """
    Render an inline formset of tags.
    Usage:
        {% render_formset formset %}
    """
    
    args = token.split_contents()
    length = len(args)
    if length != 2:
        raise TemplateSyntaxError('%s requires 2 arguments.' % args[0])
    
    return RenderedFormsetNode(args[1])


class RenderedFormsetNode(Node):
    def __init__(self, formset):
        self.fs_name = formset
        self.fs_value = Variable(formset)
    
    def render(self, context):
        fs_name = self.fs_name
        fs_value = self.fs_value.resolve(context)
        code = u'{{ %s.management_form }}' % fs_name
        code = u'%s{& for form in %s &}' % (code, fs_name)
        code = u'%s<span>{{ form }}</span>' % code
        code = u'%s{& endfor &}' % code
        code = code.replace('&', '%')
        template = Template(code)
        context = Context({fs_name: fs_value})
        return template.render(context)
