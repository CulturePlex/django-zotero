# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import widgets
#from zotero.models import TaggedItem


class ContentTypeSelect(forms.Select):
    def __init__(self, attrs=None):
        models = ContentType.objects.all()
        choices = [(0, None)]
        choices.extend([(i+1, models[i]) for i in range(models.count())])
        super(ContentTypeSelect, self).__init__(choices=choices)


class ObjectContentSelect(widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.Select, forms.Select]
        super(MultiSelect, self).__init__(widgets, attrs)


class MultiSelect(widgets.MultiWidget):
    class Media:
        css = {
            'all': ('zotero/css/jquery.combobox.css', ),
        }
        js = []
        js.append('zotero/js/jquery.combobox.js')
        js.append('zotero/js/combobox.js')
    
    def __init__(self, attrs=None):
        widgets = [ContentTypeSelect, forms.Select]
        super(MultiSelect, self).__init__(widgets, attrs)

    def decompress(self, value):
        return [None, None, None]
