from django.template import Library, Node, TemplateSyntaxError
from zotero.models import Tag

register = Library()


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
    
#    tags = Tag
    tagged_item = []
    field_value_list = tagged_item.fields_values.all()
    for field_value in field_value_list:
        field = field_value.field
        name = field.namespaces.get(vocabulary, field.name)
        value = field_value.value
        
        tag = u'<meta property="%s" content="%s"/>' % (name, value)
        result = u'%s\n%s' % (result, tag)
    
    return result
