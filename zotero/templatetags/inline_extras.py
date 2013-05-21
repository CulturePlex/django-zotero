# -*- coding: utf-8 -*-
from django.template import Library, Node, TemplateSyntaxError, Template, \
                            Variable, Context

register = Library()


@register.tag
def render_inline_tags(parser, token):
    """
    Render an inline formset of tags.
    Usage:
        {% render_inline_tags formset %}
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
        fs = self.fs_name
        fs_val = self.fs_value.resolve(context)
        
        c = '<link rel="stylesheet" type="text/css" href="/static/admin/css/base.css" />'
        c = '%s<link rel="stylesheet" type="text/css" href="/static/admin/css/forms.css" />' % c
        c = '%s<div class="{{ %s.prefix }} inline-group tabular inline-related">' % (c, fs)
        c = '%s{{ %s.media }}' % (c, fs)
        c = '%s{{ %s.management_form }}' % (c, fs)
        c = '%s<fieldset class="module">' % c
        c = '%s<h2>Tags</h2>' % c
        c = '%s{{ %s.non_form_errors }}' % (c, fs)
        c = '%s<table>' % c
        c = '%s  <thead>' % c
        c = '%s    <tr>' % c
        c = '%s      {& for field in %s.form.base_fields &}' % (c, fs)
        c = '%s        <th>{{ field|capfirst }}</th>' % c
        c = '%s      {& endfor &}' % c
        c = '%s      <th>Delete?</th>' % c
        c = '%s    </tr>' % c
        c = '%s  </thead>' % c
        c = '%s  <tbody>' % c
        c = '%s    {& for form in %s &}' % (c, fs)
        c = '%s      {& if form.non_field_errors &}' % c
        c = '%s        <tr>' % c
        c = '%s          <td>{{ form.non_field_errors }}</td>' % c
        c = '%s        </tr>' % c
        c = '%s      {& endif &}' % c
        c = '%s      <tr class="form-row {& cycle \'row1\' \'row2\' &}">' % c
        c = '%s        {& for field in form &}' % c
        c = '%s          <td class="field-{{ field.name }}">' % c
        c = '%s            {{ field.errors.as_ul }}' % c
        c = '%s            {{ field }}' % c
        c = '%s          </td>' % c
        c = '%s        {& endfor &}' % c
        c = '%s      </tr>' % c
        c = '%s    {& endfor &}' % c
        c = '%s  </tbody>' % c
        c = '%s</table>' % c
        c = '%s</fieldset>' % c
        c = '%s</div>' % c
        c = c.replace('&', '%')
        template = Template(c)
        context = Context({fs: fs_val})
        return template.render(context)
    
#    def render(self, context):
#        fs_name = self.fs_name
#        fs_value = self.fs_value.resolve(context)
#        code = u'{{ %s.management_form }}' % fs_name
#        code = u'%s{& for form in %s &}' % (code, fs_name)
#        code = u'%s<span class="%s">{{ form }}</span>' % (
#            code,
#            fs_value.prefix
#        )
#        code = u'%s{& endfor &}' % code
#        code = code.replace('&', '%')
#        template = Template(code)
#        context = Context({fs_name: fs_value})
#        return template.render(context)
