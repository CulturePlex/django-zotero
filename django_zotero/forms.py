# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes import generic
from django.db import transaction
from models import Tag


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


class TagInlineFormsetAdmin(GenericTagInlineFormset):
    pass


class TagInlineFormAdmin(generic.ModelForm):
    class Media:
        js = (
            'js/tags_admin.js',
        )


class TagInlineFormset(GenericTagInlineFormset):
    pass


class TagInlineFormNoJQuery(generic.ModelForm):
    class Media:
        js = (
#            'js/jquery.js',
            'js/jquery.formset.js',
            'js/tags.js',
        )
        css = {
            'all': ('css/tags.css',)
        }


class TagInlineForm(generic.ModelForm):
    class Media:
        js = (
            'js/jquery.js',
            'js/jquery.formset.js',
            'js/tags.js',
        )
        css = {
            'all': ('css/tags.css',)
        }


def get_tag_formset(obj=None, data=None, show_labels=False, labels=None, jquery=True):
    if obj and Tag.get_tags(obj):
        extra = 0
    else:
        extra = 1
    if jquery:
        tagInlineForm = TagInlineForm
    else:
        tagInlineForm = TagInlineFormNoJQuery
    Formset = generic.generic_inlineformset_factory(
        Tag,
        form=tagInlineForm,
        formset=TagInlineFormset,
        extra=extra,
    )
    formset = Formset(instance=obj, data=data)
    formset.show_labels = show_labels
    formset.item_type_label = 'Item type'
    formset.field_label = 'Field'
    formset.value_label = 'Value'
    if labels:
        formset.item_type_label = labels.get('item_type', 'Item type')
        formset.field_label = labels.get('field', 'Field')
        formset.value_label = labels.get('value', 'Value')
        for label in labels:
            field = formset.form.base_fields.get(label)
            if field:
                field.label = labels[label]
    return formset


#test
from models import Document
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
