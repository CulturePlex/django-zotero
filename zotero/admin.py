# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.contenttypes import generic
from zotero.forms import TagInlineFormsetAdmin, TagInlineFormAdmin
from zotero.models import Field, ItemType, Tag, Document
from zotero.views import itemtype_fields_view


# schema
class FieldInlineAdmin(admin.TabularInline):
    model = ItemType.fields.through
    extra = 0


class FieldAdmin(admin.ModelAdmin):
    inlines = (
        FieldInlineAdmin,
    )
    list_display = (
        'field_name',
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
                r'^(?P<itemtype_id>.+)/fields/$',
                self.admin_site.admin_view(
                    itemtype_fields_view,
                    cacheable=True,
            ),
            name="itemtype_fields"),
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


# test
class DocumentAdmin(admin.ModelAdmin):
    inlines = (
        TagInlineAdmin,
    )
admin.site.register(Document, DocumentAdmin)
