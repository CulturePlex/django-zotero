# -*- coding: utf-8 -*-
from django import forms
from django.forms import models
from zotero.models import Field, TaggedItem


class FieldValueInlineFormset(models.BaseInlineFormSet):
    def clean(self):
        single_fields = []
        for form in self.forms:
            try:
                field = form.cleaned_data.get('field')
                tagged_item = form.cleaned_data.get('tagged_item')
                delete = form.cleaned_data.get('DELETE')
                if not delete:
                    if not tagged_item.is_applicable_field(field):
                        raise forms.ValidationError('The field %s is not\
                            applicable to the item type %s.' %
                            (field, tagged_item.item_type))
                    if not field.multiple:
                        if field in single_fields:
                            raise forms.ValidationError('The field %s has\
                                multiple values.' % field)
                        else:
                            single_fields.append(field)
            except AttributeError:
                pass


class GenericTaggedItemInlineModelForm(forms.ModelForm):
    field = forms.ModelChoiceField(queryset=Field.objects.all(), label='field', required=False)
    value = forms.CharField(max_length=256, label='value', required=False)
    
    def save(self, *args, **kwargs):
        super(GenericTaggedItemInlineModelForm, self).save(*args, **kwargs)
        try:
            field = self.cleaned_data['field']
            value = self.cleaned_data['value']
            tagged_item = self.instance
            tagged_item.fields_values.create(field=field, value=value)
        except AttributeError:
            pass
        import ipdb; ipdb.set_trace()
    
    class Meta:
        model = TaggedItem
