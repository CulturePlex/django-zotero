# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes import generic
from django.db import transaction
from django.forms import formsets
from models import Tag

#test
from models import Document


class GenericTagInlineFormset(generic.BaseGenericInlineFormSet):
    def clean(self):
        single_fields = []
        first_loop = True
        for form in self.forms:
            try:
                item_type = form.cleaned_data['item_type']
                field = form.cleaned_data['field']
                delete = form.cleaned_data.get('DELETE')
            except AttributeError:
                pass
            except KeyError:
                pass
            else:
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
    
    @transaction.autocommit
    def save(self):
        try:
            super(GenericTagInlineFormset, self).save()
        except TypeError, e:
            if e.message[0].startswith('Uniqueness'):
                tag = self.forms[0].instance
                new_item_type = tag.item_type
                obj = Tag.get_object(tag)
                tags = Tag.get_tags(obj)
                tags.update(item_type=new_item_type)
                self.save()


class GenericTagInlineForm(generic.ModelForm):
    class Media:
        js = ("js/tags.js",)


def get_tag_formset(obj, data=None):
    Formset = generic.generic_inlineformset_factory(
        Tag,
        form=GenericTagInlineForm,
        formset=GenericTagInlineFormset,
        extra=0
    )
    formset = Formset(instance=obj, data=data)
    return formset


#test
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
