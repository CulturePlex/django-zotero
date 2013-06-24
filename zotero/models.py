# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from utils import humanize


#schema
class Field(models.Model):
    """
    Field in a document: title, publisher, author, etc.
    """
    field_name = models.CharField(_(u'name'), max_length=100)
    multiple = models.BooleanField(_(u'allows multiple?'))
    namespaces = JSONField(_(u'namespaces'), blank=True)
    
    def __unicode__(self):
        return humanize(self.field_name)
    
    def get_item_types(self):
        return self.item_types.all()
    
    class Meta:
        ordering = ('field_name',)


class ItemType(models.Model):
    """
    Type of document: book, journal article, etc.
    """
    type_name = models.CharField(_(u'name'), max_length=100)
    fields = models.ManyToManyField(Field, related_name='item_types',
        verbose_name=_(u'fields'))
    
    def __unicode__(self):
        return humanize(self.type_name)
    
    def get_fields(self):
        return self.fields.all()


#data
class Tag(models.Model):
    """
    A description (item_type, field, value) for an object.
    """
    #Generic foreign key to item
    content_type = models.ForeignKey(ContentType,
        verbose_name=_(u'content type'))
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    #Tag's fields
    item_type = models.ForeignKey(ItemType, related_name='tags',
        verbose_name=_(u'item type'))
    field = models.ForeignKey(Field, related_name='tags',
        verbose_name=_(u'field'))
    value = models.CharField(_(u'value'), max_length=256)
    
    def __unicode__(self):
        return u'%s: %s=%s' % (self.item_type, self.field, self.value)
    
    @staticmethod
    def get_tags(obj):
        ct = ContentType.objects.get_for_model(obj)
        tags = Tag.objects.filter(content_type__pk=ct.id, object_id=obj.id)
        return tags
    
    @staticmethod
    def get_object(tag):
        return tag.content_object


#test
class Document(models.Model):
    name = models.CharField(_('name'), max_length=256)
    
    def __unicode__(self):
        return self.name
