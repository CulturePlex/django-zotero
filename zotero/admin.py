# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from zotero.forms import FieldValueInlineFormset,\
                         GenericTaggedItemInlineModelForm
from zotero.models import Field, ItemType, TaggedItem, FieldValue, Document


#schema
class FieldInline(admin.TabularInline):
    model = ItemType.fields.through
    extra = 0


class FieldAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]
    list_display = ('field_name', 'multiple')


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
class FieldValueInline(admin.TabularInline):
    model = FieldValue
    extra = 0
    formset = FieldValueInlineFormset


class TaggedItemAdmin(admin.ModelAdmin):
    inlines = [
        FieldValueInline,
    ]

admin.site.register(TaggedItem, TaggedItemAdmin)


class GenericTaggedItemInline(generic.GenericTabularInline):
    model = TaggedItem
    extra = 0
    form = GenericTaggedItemInlineModelForm
    template = "admin/edit_inline/tagged_item_inline.html"


#test
class DocumentAdmin(admin.ModelAdmin):
    inlines = [
        GenericTaggedItemInline,
    ]

admin.site.register(Document, DocumentAdmin)
