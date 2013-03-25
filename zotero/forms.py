# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes import generic


class GenericTagInlineFormset(generic.BaseGenericInlineFormSet):
    def clean(self):
        single_fields = []
        first_loop = True
        for form in self.forms:
            try:
                item_type = form.cleaned_data['item_type']
                field = form.cleaned_data['field']
                delete = form.cleaned_data.get('DELETE')
                
                if first_loop:
                    first_item_type = item_type
                    first_loop = False
                if not delete:
                    if first_item_type != item_type:
                        raise forms.ValidationError('The item type %s is\
                            different from the original item type %s.' %
                            (item_type, first_item_type))
                    if not field in item_type.fields.all():
                        raise forms.ValidationError('The field %s is not\
                            applicable to the item type %s.' %
                            (field, item_type))
                    if not field.multiple:
                        if field in single_fields:
                            raise forms.ValidationError('The field %s has\
                                multiple values.' % field)
                        else:
                            single_fields.append(field)
            except AttributeError:
                pass


class GenericTagInlineForm(forms.ModelForm):
    class Media:
        js = ("js/tag.js",)
