from django.db.models.signals import pre_save
from django.dispatch import receiver
from zotero.models import TaggedItem


@receiver(pre_save, sender=TaggedItem)
def check_save(sender, **kwargs):
    """
    Checks field applicability and multiplicity.
    """
    tagged_item = kwargs['instance']
    appl_err_list = check_fields_applicable(tagged_item)
    mult_err_list = check_fields_multiple(tagged_item)
    if not appl_err_list or not mult_err_list:
        raise TypeError((appl_err_list, mult_err_list))


def check_fields_applicable(tagged_item):
    """
    Returns a list of non-applicable fields to this item type.
    """
    error_fields = []
    set_fields_list = tagged_item.get_set_fields.all()
    for field in set_fields_list:
        if not tagged_item.is_applicable_field(field):
            error_fields.append(field)


def check_fields_multiple(tagged_item):
    """
    Returns a list of non-multiple fields with multiple values.
    """
    error_fields = []
    set_fields_list = tagged_item.get_set_fields.all()
    for field in set_fields_list:
        if not field.multiple and set_fields_list.counter(field) > 1:
            error_fields.append(field)
