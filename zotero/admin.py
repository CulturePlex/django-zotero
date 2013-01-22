from django.contrib import admin
from zotero.models import ItemType, Field, CreatorType
from zotero.models import TaggedItem, FieldValue, CreatorValue

#Metadata
#class FieldInline(admin.TabularInline):
#    model = Field
#    extra = 0

#class CreatorTypeInline(admin.TabularInline):
#    model = CreatorType
#    extra = 0

#class ItemTypeAdmin(admin.ModelAdmin):
#    inlines = [FieldInline,CreatorTypeInline]

#admin.site.register(ItemType,ItemTypeAdmin)
admin.site.register(ItemType)
admin.site.register(Field)
admin.site.register(CreatorType)

#Data
class FieldValueInline(admin.TabularInline):
    model = FieldValue
    extra = 0

class CreatorValueInline(admin.TabularInline):
    model = CreatorValue
    extra = 0

class TaggedItemAdmin(admin.ModelAdmin):
    inlines = [FieldValueInline,CreatorValueInline]

admin.site.register(TaggedItem,TaggedItemAdmin)
