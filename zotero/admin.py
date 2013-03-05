# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.forms import models
from zotero.models import ItemType, Field, TaggedItem, FieldValue, Document
#from zotero.widgets import MultiSelect


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
class FieldValueInlineFormset(models.BaseInlineFormSet):
    def clean(self):
        single_fields = []
        for form in self.forms:
            try:
                field = form.cleaned_data.get('field')
                tagged_item = form.cleaned_data.get('tagged_item')
                if not tagged_item.is_applicable_field(field):
                    raise forms.ValidationError('The field %s is not\
                        applicable to the item type %s.' %
                        (field, tagged_item.item_type))
                if not field.multiple:
                    if field in single_fields:
                        raise forms.ValidationError('The field %s has multiple\
                            values.' % field)
                    else:
                        single_fields.append(field)
            except AttributeError:
                pass


class FieldValueInline(admin.TabularInline):
    model = FieldValue
    extra = 0
    formset = FieldValueInlineFormset


class GenericFieldValueInline(generic.GenericTabularInline):
    model = FieldValue
    extra = 0
    formset = FieldValueInlineFormset


class TaggedItemAdminModelForm(forms.ModelForm):
    class Meta:
        model = TaggedItem


class TaggedItemAdmin(admin.ModelAdmin):
    inlines = [
        FieldValueInline,
    ]
    form = TaggedItemAdminModelForm

admin.site.register(TaggedItem, TaggedItemAdmin)


class TaggedItemInline(generic.GenericTabularInline):
    model = TaggedItem
    extra = 0


#test
class DocumentAdmin(admin.ModelAdmin):
    inlines = [
        TaggedItemInline,
    ]

admin.site.register(Document, DocumentAdmin)
