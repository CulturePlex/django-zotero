# -*- coding: utf-8 -*-
from django import template as t
from django.template import loader


register = t.Library()


@register.tag
def zotero_inline_tags(parser, token):
    """
    Render an inline formset of tags.
    
    Usage:
        {% zotero_inline_tags formset %}
    """
    
    args = token.split_contents()
    length = len(args)
    if length != 2:
        raise t.TemplateSyntaxError('%s requires 2 arguments.' % args[0])
    
    return RenderedFormsetNode(args[1])


class RenderedFormsetNode(t.Node):
    def __init__(self, formset):
        self.fs_name = formset
        self.fs_value = t.Variable(formset)
    
    def render(self, context):
        fs = self.fs_name
        fs_val = self.fs_value.resolve(context)
        template = loader.get_template('zotero/inline_tags.html')
        context = t.Context({fs: fs_val})
        return template.render(context)
