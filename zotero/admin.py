from django.contrib import admin
from zotero.models import ItemType, Field, TaggedItem, FieldValue


#Metadata
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
    #list_display = ('field_name', 'multiple')

admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Field, FieldAdmin)


#Data
class FieldValueInline(admin.TabularInline):
    model = FieldValue
    extra = 1


class TaggedItemAdmin(admin.ModelAdmin):
    inlines = [
        FieldValueInline,
    ]

admin.site.register(TaggedItem, TaggedItemAdmin)
