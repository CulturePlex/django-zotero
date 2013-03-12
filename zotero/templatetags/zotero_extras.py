from django.template import Library, Node, TemplateSyntaxError, Variable
from zotero.models import TaggedItem, Field

register = Library()


@register.tag
def create_select(parser, token):
    """
    Returns a select for a form.
    Usage:
        {% create_select object %}
    """
    args = token.split_contents()
    if not len(args) > 1:
        raise TemplateSyntaxError('%s requires one argument.' % args[0])
    
    field_name = args[1]
    
    return SelectNode(field_name)


class SelectNode(Node):
    def __init__(self, field_name):
        self.field_name = Variable(field_name)
    
    def render(self, context):
        result = u'<select name="zotero-taggeditem-content_type-object_id-0-field" id="zotero-taggeditem-content_type-object_id-0-field">\n'
        result = u'%s<option value="">---------</option>\n' % result
        
        fields = Field.objects.all()
        index = 1
        field_name = self.field_name.resolve(context)
        for field in fields:
            if field.field_name == field_name:
                result = u'%s<option value="%d" selected="selected">%s \
                         </option>\n' % (result, index, field)
            else:
                result = u'%s<option value="%d">%s</option>\n' % \
                         (result, index, field)
            index += 1
            
        return result


@register.tag
def zotero_tags(parser, token):
    """
    Returns the code to be translated by Zotero.
    Usage:
        {% zotero_tags tagged_item vocabulary output_method %}
    Example:
        {% zotero_tags 1 "dc" "meta" %}
    """
    args = token.split_contents()
    if len(args) < 1 and len(args) > 3:
        raise TemplateSyntaxError('%s requires one argument.' % args[0])
    
    tagged_item = args[1]
    if args[2]:
        vocabulary = args[2]
    else:
        vocabulary = u'dc'
    if args[3]:
        output_method = args[3]
    else:
        output_method = u'meta'
    
    return ZoteroTagsNode(tagged_item, vocabulary, output_method)


class ZoteroTagsNode(Node):
    def __init__(self, tagged_item, vocabulary, output_method):
        self.tagged_item = tagged_item
        self.vocabulary = vocabulary
        self.output_method = output_method
    
    def render(self, context):
        if self.output_method == 'meta':
            result = render_meta(self.tagged_item, self.vocabulary)
        else:
            pass
        
        return result


def render_meta(tagged_item, vocabulary):
    result = u'<link rel="schema.dc" href="http://purl.org/dc/elements/1.1/">'
    
    tagged_item = TaggedItem.objects.get(pk=tagged_item)
    field_value_list = tagged_item.fields_values.all()
    for field_value in field_value_list:
        field = field_value.field
        name = field.namespaces.get(vocabulary, field.name)
        value = field_value.value
        
        tag = u'<meta property="%s" content="%s"/>' % (name, value)
        result = u'%s\n%s' % (result, tag)
    
    return result
