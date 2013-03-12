# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField


#schema
class Field(models.Model):
    """
    Field in a document: title, publisher, author, etc.
    """
    field_name = models.CharField(_(u'name'), max_length=100)
    multiple = models.BooleanField(_(u'creator type?'))
    namespaces = JSONField(_(u'namespaces'), blank=True)
    
    def __unicode__(self):
        return self.field_name


class ItemType(models.Model):
    """
    Type of document: book, journal article, etc.
    """
    type_name = models.CharField(_(u'name'), max_length=100)
    fields = models.ManyToManyField(Field, related_name='fields',
        verbose_name=_(u'fields'))
    
    def __unicode__(self):
        return self.type_name


#data
class TaggedItem(models.Model):
    """
    An instance of a tagged item: a book titled "A", an article written by "B",
    etc.
    """
    item_type = models.ForeignKey(ItemType, related_name='tagged_items',
        verbose_name=_(u'item type'))
    content_type = models.ForeignKey(ContentType,
        verbose_name=_(u'content type'))
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

#    class Meta:
#        unique_together = ('content_type', 'object_id')
    
    def __unicode__(self):
        field_values = self.fields_values.all()
        return u'content_type: %s, item_type: %s, fields: %s' % \
            (self.content_type, self.item_type, field_values)
    
    def get_applicable_fields(self):
        """
        Returns a list of all applicable fields to this item type.
        """
        return self.item_type.fields.all()
    
    def is_applicable_field(self, field):
        """
        Returns True if a field is applicable to this item.
        """
        return field in self.get_applicable_fields()
    
    def get_assigned_fields(self):
        """
        Returns a list of assigned fields for this item.
        """
        field_value_list = self.fields_values.all()
        return [field_value.field for field_value in field_value_list]
    
    def get_field_values(self, field):
        """
        Returns the value(s) for a field.
        """
        field_value_list = self.fields_values.all()
        return [field_value.value 
            for field_value in field_value_list and field_value.field == field]


class FieldValue(models.Model):
    """
    A value for a field of a tagged item: <title='Yerma'>
    """
    field = models.ForeignKey(Field, related_name='values',
        verbose_name=_(u'field'))
    value = models.CharField(_(u'value'), max_length=256)
    tagged_item = models.ForeignKey(TaggedItem, related_name='fields_values',
                                    verbose_name=_(u'tagged item'))
    
    def __unicode__(self):
        return u'%s=%s' % (self.field, self.value)


#test
class Document(models.Model):
    name = models.CharField(_('name'), max_length=256)
    
    def __unicode__(self):
        return self.name
