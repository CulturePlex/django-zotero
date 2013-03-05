# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from zotero.models import TaggedItem, FieldValue


@receiver(pre_save, sender=TaggedItem)
def check_save(sender, **kwargs):
    pass
#    """
#    Checks field applicability and multiplicity.
#    """
#    tagged_item = kwargs['instance']
#    if not tagged_item.id:
#        print 'Objeto nuevo'
#    else:
#        print 'Objeto modificado'
#    appl_err_list = check_fields_applicable(tagged_item)
#    mult_err_list = check_fields_multiple(tagged_item)
#    if appl_err_list or mult_err_list:
#        raise TypeError((appl_err_list, mult_err_list))


def check_fields_applicable(tagged_item):
    """
    Returns a list of non-applicable fields to this item type.
    """
    error_fields = []
    assigned_fields_list = tagged_item.get_assigned_fields()
    for field in assigned_fields_list:
        if not tagged_item.is_applicable_field(field):
            #if it is not already contained
            if not field in error_fields:
                error_fields.append(field)
        
    return error_fields


def check_fields_multiple(tagged_item):
    """
    Returns a list of non-multiple fields with multiple values.
    """
    error_fields = []
    assigned_fields_list = tagged_item.get_assigned_fields()
    for field in assigned_fields_list:
        if not field.multiple and assigned_fields_list.count(field) > 1:
            #if it is not already contained
            if not field in error_fields:
                error_fields.append(field)
    return error_fields
