from django.contrib import admin
from zotero.models import ItemType, Field, CreatorType

admin.site.register(ItemType)
admin.site.register(Field)
admin.site.register(CreatorType)
