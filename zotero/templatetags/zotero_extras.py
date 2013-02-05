from django.template import Library, Node, TemplateSyntaxError
from zotero.models import TaggedItem

register = Library()


def zotero_tags(parser, token):
    """
    Returns the code to be translated by Zotero.
    Usage: {% zotero_tags tagged_item output_method vocabulary %}
    """
    args = token.split_contents()
    if len(args) < 1 and len(args) > 3:
        raise TemplateSyntaxError('%s requires one argument.' % args[0])
    
    tagged_item = args[1]
    if args[2]:
        output_method = args[2]
    else:
        output_method = u'meta'
    if args[3]:
        vocabulary = args[3]
    else:
        vocabulary = u'dc'
    
    return ZoteroTagsNode(tagged_item, output_method, vocabulary)


class ZoteroTagsNode(Node):
    def __init__(self, tagged_item, output_method, vocabulary):
        self.tagged_item = tagged_item
        self.output_method = output_method
        self.vocabulary = vocabulary
    
    def render(self, context):
        if self.output_method == 'meta':
            result = render_meta(self.tagged_item, self.vocabulary)
        else:
            pass
        
        return result


def render_meta(tagged_item, vocabulary):
    result = u''
    
    tagged_item = TaggedItem.objects.get(pk=tagged_item)
    field_value_list = tagged_item.fieldvalue_set.all()
    for field_value in field_value_list:
        field = field_value.field
        if field.namespaces[vocabulary]:
            name = field.namespaces[vocabulary]
        else:
            name = field.name
        value = field_value.value
        
        tag = u'<meta property="%s" content="%s"/>' % (name, value)
        result += u'%s%s\n' % (result, tag)
    
    return result
