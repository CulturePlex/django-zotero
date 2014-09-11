def humanize(s):
    result = ''
    if s.islower() or s.isupper():
        result = s
    else:
        for c in s:
            if c.isupper():
                result = '%s %s' % (result.rstrip(), c.lower())
            else:
                result = '%s%s' % (result, c)
    result = result.strip()
    return result

def render_fields():
    from django_zotero.models import ItemType, Field
    result = ''
    for item_type in ItemType.objects.all():
        result += '\n*** ' + item_type.type_name + ' ***\n'
        result += '\n-------------------------------------------------------\n'
        result += u'<link rel="schema.dc" href="http://purl.org/dc/elements/1.1/">'
        value = item_type.type_name
        meta_tag = u'<meta property="DC.type" content="%s"/>' % value
        result = u'%s\n%s' % (result, meta_tag)
        for field in item_type.get_fields():
            name = field.namespaces.get('dc', field.field_name)
            value = field.field_name
            if name == 'identifier':
                value = '%s %s' % (field.field_name.lower(), value)
            meta_tag = u'<meta property="DC.%s" content="%s"/>' % (name, value)
            result = u'%s\n%s' % (result, meta_tag)
        result += '\n=======================================================\n'
    print result
    f = open('item_types_and_fields.txt', 'w')
    f.write(result)
    f.close
