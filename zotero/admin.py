from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse
from zotero.models import ItemType, Field, TaggedItem, FieldValue, Document


#metadata
class FieldInline(admin.TabularInline):
    model = ItemType.fields.through
    extra = 1


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
    extra = 1


class TaggedItemAdmin(admin.ModelAdmin):
    inlines = [
        FieldValueInline,
    ]
    
    def change_view2(self, request):
        return HttpResponse("Hola!")
    
    def get_urls(self):
        urls = super(TaggedItemAdmin, self).get_urls()
        taggeditem_urls = patterns('',
            url(r'^admin/zotero/taggeditem/$', self.change_view2)
        )
        return taggeditem_urls + urls

admin.site.register(TaggedItem, TaggedItemAdmin)


#test
admin.site.register(Document)
