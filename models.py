from django.db import models

# Create your models here.

#Type of document: book, journal article, etc.
class ItemType(models.Model):
    type_name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.type_name

#Field in a document: title, publisher, publicationTitle, etc.
class Field(models.Model):
    field_name = models.CharField(max_length=100)
    item = models.ManyToManyField(ItemType)
    
    def __unicode__(self):
        return self.field_name

#Type of creator: author, editor, etc.
class CreatorType(models.Model):
    type_name = models.CharField(max_length=100)
    item = models.ManyToManyField(ItemType)
    
    def __unicode__(self):
        return self.type_name
