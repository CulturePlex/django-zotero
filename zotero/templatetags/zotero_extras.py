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
            obj=app_label.model_name.object_id
            voc=vocabulary
            out=output_method %}
    Example:
        {% zotero_tags obj=zotero.document.1 voc=dc out=meta %}
    """
    letters = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven']
    default = {
        'obj': u'',
        'voc': u'dc',
        'out': u'meta'
    }
    min_args = 1
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
    
    object_identifier = default['obj'].split(".")
    if len(object_identifier) != 3:
        raise TemplateSyntaxError('%s syntax error: object identifier.' % \
                                  args[0])
    app = object_identifier[0]
    mod = object_identifier[1]
    oid = object_identifier[2]
    
    ct = ContentType.objects.get(app_label=app,
                                 model=mod)
    obj = ct.get_object_for_this_type(pk=oid)
    
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
    if tags:
        value = tags[0].item_type.type_name
        meta_tag = u'<meta property="DC.type" content="%s"/>' % value
        result = u'%s\n%s' % (result, meta_tag)
        for tag in tags:
            field = tag.field
            name = field.namespaces.get(vocabulary, field.field_name)
            value = tag.value
            meta_tag = u'<meta property="DC.%s" content="%s"/>' % (name, value)
            result = u'%s\n%s' % (result, meta_tag)
    return result
