from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


# METADATA
#Field in a document: title, publisher, publicationTitle, etc.
class Field(models.Model):
    field_name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.field_name

#Type of creator: author, editor, etc.
class CreatorType(models.Model):
    type_name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.type_name

#Type of document: book, journal article, etc.
class ItemType(models.Model):
    type_name = models.CharField(max_length=100)
    fields = models.ManyToManyField(Field)
    creators_types = models.ManyToManyField(CreatorType)
    
    def __unicode__(self):
        return self.type_name


#DATA
#An instance of a tagged item: a book titled A, an article written by B, etc.
class TaggedItem(models.Model):
    item_type = models.ForeignKey(ItemType)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type','object_id')
    
    def __unicode__(self):
        fields_values = self.fieldvalue_set.all()
        creators_values = self.creatorvalue_set.all()
        return u'%s # %s # %s: (%s), (%s)' % (self.content_object,self.item_type,self.content_type,fields_values,creators_values)

#A value for a field of a tagged item: "title='Yerma'"
class FieldValue(models.Model):
    field = models.ForeignKey(Field)
    value = models.CharField(max_length=256)
    tagged_item = models.ForeignKey(TaggedItem)
    
    def __unicode__(self):
        return u'%s=%s' % (self.field,self.value)

#A name for a creator of a tagged item: "author='Lorca'"
class CreatorValue(models.Model):
    creator_type = models.ForeignKey(CreatorType)
    value = models.CharField(max_length=256)
    tagged_item = models.ForeignKey(TaggedItem)
    
    def __unicode__(self):
        return u'%s=%s' % (self.creator_type,self.value)
