# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from zotero.forms import GenericTagInlineFormset, GenericTagInlineForm
from zotero.models import Field, ItemType, Tag, Document


#schema
class FieldInline(admin.TabularInline):
    model = ItemType.fields.through
    extra = 0


class FieldAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]


class ItemTypeAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]
    exclude = (
        'fields',
    )

admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Field, FieldAdmin)


#data
class GenericTagInline(generic.GenericTabularInline):
    model = Tag
    extra = 0
    form = GenericTagInlineForm
    formset = GenericTagInlineFormset


#test
class DocumentAdmin(admin.ModelAdmin):
    inlines = [
        GenericTagInline,
    ]

admin.site.register(Document, DocumentAdmin)
