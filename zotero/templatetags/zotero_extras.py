from django.contrib.contenttypes.models import ContentType
from django.template import Library, Node, TemplateSyntaxError
from zotero.models import Tag

register = Library()


@register.tag
def zotero_tags(parser, token):
    """
    Returns the code to be translated by Zotero.
    Usage:
        {% zotero_tags
            mod=object_model
            oid=object_id
            voc=vocabulary
            out=output_method %}
    Example:
        {% zotero_tags mod=Document oid=1 voc=dc out=meta %}
    """
    letters = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven']
    default = {
        'mod': u'',
        'oid': u'',
        'voc': u'dc',
        'out': u'meta'
    }
    min_args = 2
    max_args = len(default)
    if min_args == 1:
        min_pl = ''
    else:
        min_pl = 's'
    if max_args == 1:
        max_pl = ''
    else:
        max_pl = 's'
    
    args = token.split_contents()
    length = len(args)
    if length < min_args + 1:
        raise TemplateSyntaxError('%s requires at least %s argument%s.' %
                                  (args[0], letters[min_args], min_pl))
    elif length > max_args + 1:
        raise TemplateSyntaxError('%s requires %s or less argument%s.' %
                                  (args[0], letters[max_args], max_pl))
    
    for arg in args[1:length]:
        f = arg.find('=')
        if f == -1:
            raise TemplateSyntaxError('%s syntax error: %s.' % (args[0], arg))
        else:
            key = arg[:f]
            val = arg[f + 1:]
            if not key in default.keys():
                raise TemplateSyntaxError('%s invalid argument: %s.' %
                                          (args[0], key))
            else:
                default[key] = val
    
    ct = ContentType.objects.get(app_label='zotero',
                                 model=default['mod'].lower())
    obj = ct.get_object_for_this_type(pk=default['oid'])
    
    return ZoteroTagsNode(ct, obj, default['voc'], default['out'])


class ZoteroTagsNode(Node):
    def __init__(self, model, obj, vocabulary, output_method):
        self.mod = model
        self.obj = obj
        self.voc = vocabulary
        self.out = output_method
    
    def render(self, context):
        if self.out == 'meta':
            result = render_meta(self.mod, self.obj, self.voc)
        else:
            pass
        
        return result


def render_meta(model, obj, vocabulary):
    result = u'<link rel="schema.dc" href="http://purl.org/dc/elements/1.1/">'
    
    tags = Tag.objects.filter(content_type__pk=model.id, object_id=obj.id)
    for tag in tags:
        field = tag.field
        name = field.namespaces.get(vocabulary, field.field_name)
        value = tag.value
        
        tag = u'<meta property="DC.%s" content="%s"/>' % (name, value)
        result = u'%s\n%s' % (result, tag)
    return result
