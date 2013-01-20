from django.db import models

# Create your models here.

#Type of document: book, journal article, etc.
class Item(models.Model):
    type_name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.type_name

#Field in a document: title, author, etc.
class Field(models.Model):
    field_name = models.CharField(max_length=100)
    item = models.ManyToManyField(Item)
    
    def __unicode__(self):
        return self.field_name
