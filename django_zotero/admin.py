# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.contenttypes import generic
from django_zotero.forms import TagInlineFormsetAdmin, TagInlineFormAdmin
from django_zotero.models import Field, ItemType, Tag, Document
from django_zotero.views import itemtype_fields_view


# schema
class FieldInlineAdmin(admin.TabularInline):
    model = ItemType.fields.through
    extra = 0


class FieldAdmin(admin.ModelAdmin):
    inlines = (
        FieldInlineAdmin,
    )
    list_display = (
        '__unicode__',
        'multiple',
    )


class ItemTypeAdmin(admin.ModelAdmin):
    inlines = (
        FieldInlineAdmin,
    )
    exclude = (
        'fields',
    )
    
    def get_urls(self):
        urls = super(ItemTypeAdmin, self).get_urls()
        field_urls = patterns('',
            url(
                r'^fields/$',
                self.admin_site.admin_view(
                    itemtype_fields_view,
                    cacheable=True,
            ),
            name='zotero_itemtype_fields'),
        )
        return field_urls + urls

admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Tag)


# data
class TagInlineAdmin(generic.GenericTabularInline):
    model = Tag
    extra = 0
    form = TagInlineFormAdmin
    formset = TagInlineFormsetAdmin
    template = 'admin/edit_inline/extended_tabular.html'


# test
class DocumentAdmin(admin.ModelAdmin):
    inlines = (
        TagInlineAdmin,
    )
admin.site.register(Document, DocumentAdmin)
