from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


# METADATA
class Field(models.Model):
    '''Field in a document: title, publisher, publicationTitle, etc.'''
    field_name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.field_name


class CreatorType(models.Model):
    '''Type of creator: author, editor, etc.'''
    type_name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.type_name


class ItemType(models.Model):
    '''Type of document: book, journal article, etc.'''
    type_name = models.CharField(max_length=100)
    fields = models.ManyToManyField(Field)
    creator_types = models.ManyToManyField(CreatorType)
    
    def __unicode__(self):
        return self.type_name


#DATA
class TaggedItem(models.Model):
    '''An instance of a tagged item: a book titled "A", an article written by \
    "B", etc.'''
    item_type = models.ForeignKey(ItemType)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        field_values = self.fieldvalue_set.all()
        creator_values = self.creatorvalue_set.all()
        return u'item_type: %s, content_type: %s, object_id: %s, \
        content_object: %s, fields: %s, creators: %s' % \
        (self.item_type, self.content_type, self.object_id,
        self.content_object, field_values, creator_values)


class FieldValue(models.Model):
    '''A value for a field of a tagged item: "title='Yerma'"'''
    field = models.ForeignKey(Field)
    value = models.CharField(max_length=256)
    tagged_item = models.ForeignKey(TaggedItem)
    
    def __unicode__(self):
        return u'%s=%s' % (self.field, self.value)


class CreatorValue(models.Model):
    '''A name for a creator of a tagged item: "author='Lorca'"'''
    creator_type = models.ForeignKey(CreatorType)
    value = models.CharField(max_length=256)
    tagged_item = models.ForeignKey(TaggedItem)
    
    def __unicode__(self):
        return u'%s=%s' % (self.creator_type, self.value)
