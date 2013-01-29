from django.contrib import admin
from zotero.models import ItemType, Field, CreatorType
from zotero.models import TaggedItem, FieldValue, CreatorValue

#Hidden models
#class HiddenModelAdmin(admin.ModelAdmin):
#    def get_model_perms(self, *args, **kwargs):
#        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
#        perms['list_hide'] = True
#        return perms


#Metadata
class FieldInline(admin.TabularInline):
    model = ItemType.fields.through
    extra = 0


class CreatorTypeInline(admin.TabularInline):
    model = ItemType.creator_types.through
    extra = 0

#class FieldAdmin(HiddenModelAdmin):
#    inlines = [
#        FieldInline,
#    ]

#class CreatorTypeAdmin(HiddenModelAdmin):
#    inlines = [
#        CreatorTypeInline,
#    ]


class FieldAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
    ]


class CreatorTypeAdmin(admin.ModelAdmin):
    inlines = [
        CreatorTypeInline,
    ]


class ItemTypeAdmin(admin.ModelAdmin):
    inlines = [
        FieldInline,
        CreatorTypeInline,
    ]
    exclude = (
        'fields',
        'creator_types',
    )

admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(CreatorType, CreatorTypeAdmin)


#Data
class FieldValueInline(admin.TabularInline):
    model = FieldValue
    extra = 0


class CreatorValueInline(admin.TabularInline):
    model = CreatorValue
    extra = 0


class TaggedItemAdmin(admin.ModelAdmin):
    raw_id_fields = ("item_type",)
    inlines = [
        FieldValueInline,
        CreatorValueInline,
    ]

admin.site.register(TaggedItem, TaggedItemAdmin)
