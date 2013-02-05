from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from jsonfield import JSONField


# METADATA
class Field(models.Model):
    """
    Field in a document: title, publisher, author, etc.
    """
    field_name = models.CharField(max_length=100)
    multiple = models.BooleanField('Creator type?')
    namespaces = JSONField()
    
    def __unicode__(self):
        return self.field_name


class ItemType(models.Model):
    """
    Type of document: book, journal article, etc.
    """
    type_name = models.CharField(max_length=100)
    fields = models.ManyToManyField(Field)
    
    def __unicode__(self):
        return self.type_name


#DATA
class TaggedItem(models.Model):
    """
    An instance of a tagged item: a book titled "A", an article written by "B",
    etc.
    """
    item_type = models.ForeignKey(ItemType)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        field_values = self.fieldvalue_set.all()
        return u'item_type: %s, content_type: %s, object_id: %s, \
            content_object: %s, fields: %s' % \
            (self.item_type, self.content_type, self.object_id,
            self.content_object, field_values)


class FieldValue(models.Model):
    """
    A value for a field of a tagged item: <title='Yerma'>
    """
    field = models.ForeignKey(Field)
    value = models.CharField(max_length=256)
    tagged_item = models.ForeignKey(TaggedItem)
    
    def __unicode__(self):
        return u'%s=%s' % (self.field, self.value)
