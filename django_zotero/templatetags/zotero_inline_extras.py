# -*- coding: utf-8 -*-
from django import template as t
from django.template import loader


register = t.Library()


@register.tag
def zotero_inline_tags(parser, token):
    """
    Render an inline formset of tags.
    
    Usage:
        {% zotero_inline_tags formset[ option] %}
        option = "all" | "media" | "formset"
    """
    
    args = token.split_contents()
    length = len(args)
    if length == 2:
        rendered_node = RenderedAllNode(args[1])
    elif length == 3 and args[2].lower() == u'all':
        rendered_node = RenderedAllNode(args[1])
    elif length == 3 and args[2].lower() == u'media':
        rendered_node = RenderedMediaNode(args[1])
    elif length == 3 and args[2].lower() == u'formset':
        rendered_node = RenderedFormsetNode(args[1])
    else:
        raise t.TemplateSyntaxError('Incorrect arguments in %s.' % args[0])
    
    return rendered_node


class RenderedNode(t.Node):
    def __init__(self, formset):
        self.formset = t.Variable(formset)


class RenderedAllNode(RenderedNode):
    def render(self, context):
        formset = self.formset.resolve(context)
        template = loader.get_template('zotero/inline_tags.html')
        c = t.Context({'formset': formset, 'media': True})
        return template.render(c)


class RenderedMediaNode(RenderedNode):
    def render(self, context):
        formset = self.formset.resolve(context)
        return formset.media.render()


class RenderedFormsetNode(RenderedNode):
    def render(self, context):
        formset = self.formset.resolve(context)
        template = loader.get_template('zotero/inline_tags.html')
        c = t.Context({'formset': formset, 'media': False})
        return template.render(c)
